import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import *


class MyUserManager(BaseUserManager):
    def create_user(self, id=None, password=None, user_type=None, etsid=None, school=None, nickname=None, name=None,
                    email=None):
        if not id:
            raise ValueError('Users must have an id')

        user = self.model(
            id=id,
            password=password,
            user_type='CO',
            etsid=etsid,
            school=school,
            nickname=nickname,
            name=name,
            email=email
        )

        user.set_password(password)
        user.is_active=True
        user.save(using=self._db)
        return user

    def create_superuser(self, id, password):
        u = self.create_user(id=id,
                             password=password,
                             user_type='SU',
                             )
        u.is_admin = True
        u.is_active = True
        u.save(using=self._db)
        return u


class AuthUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = "유저정보"

    type_choices = (
        ('SU', 'Super User'),
        ('CO', 'Common'),
    )
    user_type = models.CharField(max_length=2,
                                 choices=type_choices,
                                 default='CO')
    id = models.CharField(max_length=20, verbose_name="id", primary_key=True)

    name = models.CharField(max_length=20, verbose_name="이름",blank=True,null=True)
    nickname = models.CharField(max_length=20, verbose_name="닉네임",blank=True,null=True)
    school = models.CharField(max_length=20, verbose_name="학교",blank=True,null=True)
    etsid = models.TextField(verbose_name="쿠키 냠냠",blank=True,null=True)
    gender = models.BooleanField(default=False, verbose_name="성별",blank=True,null=True)
    phone_number = models.TextField(verbose_name="폰번호", blank=True, null=True)
    email = models.EmailField(verbose_name="이메일",blank=True,null=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    is_sms = models.BooleanField(verbose_name="sms수신여부", default=True)
    is_email = models.BooleanField(verbose_name="email수신여부", default=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'id'
    PASSWORD_FIELD = 'password'

    def get_user_type(self):
        return self.user_type

    def get_full_name(self):
        # The user is identified by their email address
        return self.id

    def get_short_name(self):
        # The user is identified by their email address
        if self.name == None:
            display_name = self.id
        else:
            display_name = self.name
        return display_name + "님"

    def __str__(self):
        return self.id

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def __str__(self):
        return self.user_type + " " + self.id
