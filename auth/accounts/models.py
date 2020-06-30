import password as password
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, is_staff=False, is_active=True, is_admin=False):
        if not phone:
            raise ValueError('Users must have a  phone number')
        if not password:
            raise ValueError('User must have a password')

        user_obj = self.model(phone=phone)
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,

        )

    def create_superuser(self, phone, password=None):
        user = self.create_user(
            phone,
            password=password,
            is_staff=True,
            is_admin=True,


        )
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex = r'^\+?1?\d{9,14}$',
                                 message='Phone number must in the format: "+380XXXXXXXXX')
    phone = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    first_login = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    object = UserManager()

    def __str__(self):
        return  self.phone

    def get_full_name(self):
        if self.name:
            return self.name
        else:
            return self.phone

    def get_short_name(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


# Create your models here.
