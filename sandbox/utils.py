from django.apps import apps
from django.apps.config import MODELS_MODULE_NAME
from django.core.exceptions import AppRegistryNotReady
from importlib import import_module


def get_model(app_label, model_name):
    """
    Fetches a Django model using the app registry.

    This doesn't require that an app with the given app label exists,
    which makes it safe to call when the registry is being populated.
    All other methods to access models might raise an exception about the
    registry not being ready yet.
    Raises LookupError if model isn't found.
    USAGE:
        admin.site.register(get_model('address', 'useraddress'), UserAddressAdmin)
    """
    try:
        return apps.get_model(app_label, model_name)
    except AppRegistryNotReady:
        if apps.apps_ready and not apps.models_ready:
            # If this function is called while `apps.populate()` is
            # loading models, ensure that the module that defines the
            # target model has been imported and try looking the model up
            # in the app registry. This effectively emulates
            # `from path.to.app.models import Model` where we use
            # `Model = get_model('app', 'Model')` instead.
            app_config = apps.get_app_config(app_label)
            # `app_config.import_models()` cannot be used here because it
            # would interfere with `apps.populate()`.
            import_module('%s.%s' % (app_config.name, MODELS_MODULE_NAME))
            # In order to account for case-insensitivity of model_name,
            # look up the model through a private API of the app registry.
            return apps.get_registered_model(app_label, model_name)
        else:
            # This must be a different case (e.g. the model really doesn't
            # exist). We just re-raise the exception.
            raise


def is_model_registered(app_label, model_name):
    """
    Checks whether a given model is registered. This is used to only
    register models if they aren't overridden by a forked app.
    USAGE:
        if not is_model_registered('address', 'UserAddress')
    """
    try:
        apps.get_registered_model(app_label, model_name)
    except LookupError:
        return False
    else:
        return True

# ADDING SEARCH IN ADMIN DYNAMIC
# def user_search_fields():
#     User = get_user_model()
#     fields = [
#         "user__{0}".format(User.USERNAME_FIELD)
#     ]
#     if "email" in [f.name for f in User._meta.fields]:  # pragma: no branch
#         fields += ["user__email"]
#     return fields
# USAGE:
# def customer_search_fields():
#     return [
#         "customer__{0}".format(field)
#         for field in user_search_fields()
#     ]
#  search_fields = [
#         "FIELD_NAME",
#     ] + user_search_fields()

# DJANGO ADMIN FILTER
# class CustomerHasCardListFilter(admin.SimpleListFilter):
#     title = "card presence"
#     parameter_name = "has_card"
#
#     def lookups(self, request, model_admin):
#         return [
#             ["yes", "Has Card"],
#             ["no", "Does Not Have a Card"]
#         ]
#
#     def queryset(self, request, queryset):
#         if self.value() == "yes":
#             return queryset.filter(card__isnull=True)
#         elif self.value() == "no":
#             return queryset.filter(card__isnull=False)
#         return queryset.all()
# USAGE:
#  list_filter = [CustomerHasCardListFilter]


# Prefetching Change List
# class PrefetchingChangeList(ChangeList):
#     """A custom changelist to prefetch related fields."""
#     def get_queryset(self, request):
#         qs = super(PrefetchingChangeList, self).get_queryset(request)
#
#         if subscription_status in self.list_display:
#             qs = qs.prefetch_related("subscription_set")
#         if "customer" in self.list_display:
#             qs = qs.prefetch_related("customer")
#         if "user" in self.list_display:
#             qs = qs.prefetch_related("user")
#         return qs
# USAGE:
# class ModelAdmin(admin.ModelAdmin):
#     def has_add_permission(self, request, obj=None):
#         return False
#
#     def change_view(self, request, object_id, form_url="", extra_context=None):
#         """Adjust change_view title ("View" instead of "Change")."""
#         opts = self.model._meta
#
#         extra_context = extra_context or {}
#         extra_context["title"] = _("View %s" % force_text(opts.verbose_name))
#         return super(ModelAdmin, self).change_view(
#             request, object_id, form_url, extra_context=extra_context,
#         )
#
#     def has_change_permission(self, request, obj=None):
#         if request.method == "POST":
#             return False
#         return True
#
#     def get_changelist(self, request, **kwargs):
#         return PrefetchingChangeList
