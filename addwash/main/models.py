# from django.conf import settings
# from django.db import models
# from django.utils import timezone
# from django.db.models.signals import post_save
# from django.contrib.auth.models import (AbstractUser, BaseUserManager)

# # class User(models.Model):


# class UserManager(BaseUserManager):
#     def create_superuser(self, *args, **kwargs):
#         return super().create_superuser(nickname="", phone="", *args, **kwargs)


# class User(AbstractUser):
#     nickname = models.CharField(max_length=50)
#     profile_img = models.ImageField(null=True)
#     owner_id = models.CharField(max_length=20, primary_key=True)
#     password = models.CharField(max_length=20, null=False)
#     name = models.CharField(max_length=20, null=False)
#     email = models.CharField(max_length=30, null=False)
#     phone = models.CharField(max_length=20)
#     store_name = models.CharField(max_length=30)

#     def __str__(self):
#         return self.username

#     class Meta:
#         swappable = settings.AUTH_USER_MODEL


# class service(models.Model):
#     SERVICE_CATEGORY_CHOICES = (
#         ('수선', '수선'),
#         ('세탁', '세탁'),
#     )

#     service = models.CharField(max_length=10, primary_key=True)
#     category = models.CharField(max_length=2, choices=SERVICE_CATEGORY_CHOICES)


# class clothe(models.Model):
#     CLOTHES_CATEGORY_CHOICES = (
#         ('아우터', '아우터'),
#         ('상의', '상의'),
#         ('하의', '하의'),
#         ('원피스', '원피스'),
#         ('신발', '신발'),
#     )

#     clothe = models.CharField(max_length=10, primary_key=True)
#     category = models.CharField(
#         max_length=10, choices=CLOTHES_CATEGORY_CHOICES)


# class customer(models.Model):
#     phone_num = models.CharField(max_length=20, primary_key=True, null=False)
#     name = models.CharField(max_length=20)
#     address = models.TextField()
#     get_message = models.CharField(max_length=1)
#     created_date = models.DateTimeField(default=timezone.now)


# class customer_order(models.Model):
#     phone_num = models.ForeignKey('customer', on_delete=models.CASCADE)
#     order_num = models.ForeignKey('order', on_delete=models.CASCADE)
#     owner_id = models.ForeignKey('User', on_delete=models.CASCADE)

#     class Meta:
#         unique_together = (('phone_num', 'order_num', 'owner_id'),)


# class order(models.Model):
#     order_num = models.CharField(max_length=5, primary_key=True)
#     requirements = models.TextField()


# class request(models.Model):
#     STATUS = (
#         ('처리전', '처리 전'),
#         ('처리중', '처리중'),
#         ('처리완료', '처리 완료'),
#         ('수거완료', '수거 완료'),
#     )

#     order_num = models.ForeignKey('order', on_delete=models.CASCADE)
#     request_num = models.CharField(max_length=2)
#     clothe = models.ForeignKey('clothe', on_delete=models.CASCADE)
#     service = models.ForeignKey('service', on_delete=models.CASCADE)
#     status = models.CharField(max_length=5, choices=STATUS)
#     rqst_date = models.DateTimeField(default=timezone.now)
#     est_date = models.DateTimeField()
#     fin_date = models.DateTimeField()
#     rtrn_date = models.DateTimeField()
#     requiremnets = models.TextField()
#     price = models.CharField(max_length=5)

#     class Meta:
#         unique_together = (('order_num', 'request_num'),)

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.auth.models import (AbstractUser, BaseUserManager)

# class User(models.Model):


class UserManager(BaseUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(nickname="", phone="", *args, **kwargs)


class User(AbstractUser):
    nickname = models.CharField(max_length=50)
    profile_img = models.ImageField(null=True)
    owner_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=False)
    email = models.CharField(max_length=30, null=False)
    phone = models.CharField(max_length=10)
    store_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username

    class Meta:
        swappable = settings.AUTH_USER_MODEL


class Service(models.Model):
    SERVICE_CATEGORY_CHOICES = (
        ('수선', '수선'),
        ('세탁', '세탁'),
    )

    service = models.CharField(max_length=10, primary_key=True)
    category = models.CharField(max_length=2, choices=SERVICE_CATEGORY_CHOICES)


class Clothe(models.Model):
    CLOTHES_CATEGORY_CHOICES = (
        ('아우터', '아우터'),
        ('상의', '상의'),
        ('하의', '하의'),
        ('원피스', '원피스'),
        ('신발', '신발'),
    )

    clothe = models.CharField(max_length=10, primary_key=True)
    category = models.CharField(
        max_length=10, choices=CLOTHES_CATEGORY_CHOICES)


class Customer(models.Model):
    phone_num = models.CharField(max_length=11, null=False, primary_key=True)
    name = models.CharField(max_length=20)
    address = models.TextField()
    get_message = models.SmallIntegerField()
    created_date = models.DateTimeField(default=timezone.now)


class Request(models.Model):
    STATUS = (
        ('처리전', '처리 전'),
        ('처리중', '처리중'),
        ('처리완료', '처리 완료'),
        ('수거완료', '수거 완료'),
    )
    request_num = models.CharField(max_length=20, primary_key=True)
    phone_num = models.ForeignKey('customer', on_delete=models.CASCADE)
    clothe = models.ForeignKey('clothe', on_delete=models.CASCADE)
    service = models.ForeignKey('service', on_delete=models.CASCADE)
    status = models.CharField(max_length=5, choices=STATUS)
    rqst_date = models.DateTimeField(default=timezone.now)
    est_date = models.DateTimeField(null=True)
    fin_date = models.DateTimeField(null=True)
    rtrn_date = models.DateTimeField(null=True)
    requiremnets = models.TextField(null=True)
    price = models.IntegerField()

    def __str__(self):
        return self.request_num

    def getList(self):
        row = []
        row.append(self.request_num)
        row.append(self.phone_num.phone_num)
        row.append(self.clothe.clothe)
        row.append(self.service.service)
        row.append(self.status)
        row.append(str(self.rqst_date))
        row.append(str(self.est_date))
        row.append(str(self.fin_date))
        row.append(str(self.rtrn_date))
        row.append(self.requiremnets)
        row.append(str(self.price))
        return row
