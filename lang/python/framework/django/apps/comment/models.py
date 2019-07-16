from django.db import models

from apps.blog.models import Post
from apps.core.models import TimeStampObject


class Comment(TimeStampObject, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


# complex problem:
# Assume A: Journal voucher, B: Transaction and C:TransactionEntry
# we need all the c's value on save to fill ledger
class A(models.Model):
    a_name = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        print('called from save method in model by jv')
        super(A, self).save(*args, **kwargs)

    def __str__(self):
        return self.a_name


class B(models.Model):
    b_name = models.CharField(max_length=200)
    a = models.ForeignKey(A, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        print('called from save method in model by transaction')
        super(B, self).save(*args, **kwargs)

    def __str__(self):
        return self.b_name


# class CManager(models.Manager):
#     use_for_related_fields = True
#
#     def get_all_entries(self):
#         # don't do this !!!
#         # unsuitable for related managers as could retrieve extraneous objects
#         # qs = super(EventManager, self).get_query_set()
#         # Use queryset proxy method as follows, instead:
#         qs = self.get_query_set()
#         # qs = qs.filter(visible_from__lte=today, visible_to__gte=today)
#         # return qs


class C(models.Model):
    c_name = models.CharField(max_length=200)
    b = models.ForeignKey(B, on_delete=models.CASCADE)
    # objects = CManager()

    def save(self, *args, **kwargs):
        print('called from save method in model by transaction entry')
        super(C, self).save(*args, **kwargs)

    def __str__(self):
        return self.c_name
