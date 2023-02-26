from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


#  hera we are creating custome model (login with email password )

# custome user manager 

class UserManager(BaseUserManager):
    def create_user(self, email,name, password=None,password2=None):
        """
        Creates and saves a User with the given email,password1 and password2.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name = name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# custome user model

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin



# Create your models here.


Gender = [
    ('M','M'),
    ('F','F')
]
Bloodgroup =[
    ("A+","A+"), ("A-","A-"),
    ("B+","B+"),("B-","B-"), 
    ("O+","O+"),('O-','O-'), ('AB+','AB+'),('AB-','AB-')
]

# all the details that are required to get blood 
class Reciver(models.Model):
    firstname           =models.CharField(max_length=100)
    middlename          =models.CharField(max_length=100,blank=True)
    lastname            =models.CharField(max_length=100)
    age                 =models.IntegerField()
    contactnumber       =models.IntegerField()
    email               =models.EmailField(max_length=20)
    incident            =models.CharField(max_length=100)
    bloodgroup          =models.CharField(max_length=10,choices=Bloodgroup)
    Gender              =models.CharField(max_length=1,choices=Gender)
    image               =models.FileField(max_length=100,upload_to='patient/')
    Hospital            =models.CharField(max_length=100)
    unit                =models.PositiveIntegerField()
    emergency           =models.BooleanField()
    requiredate         =models.DateTimeField(max_length=100)



'''this is for donor section '''
class Donor(models.Model):
    firstname               =models.CharField(max_length=100)
    middlename              =models.CharField(max_length=100,blank=True)
    lastname                =models.CharField(max_length=100)
    Gender                  =models.CharField(max_length=1,choices=Gender)
    age                     =models.IntegerField()
    contactnumber           =models.IntegerField()
    email                   =models.EmailField(max_length=20)
    # dateofbirth             =models.DateField(blank=True)
    image                   =models.FileField(max_length=100,upload_to='images/')
    bloodgroup              =models.CharField(max_length=10,choices=Bloodgroup)
    timesofdonate           =models.CharField(max_length=200)
    diseases                =models.CharField(max_length=100)
    donatedate              =models.DateTimeField()
    location                =models.CharField(max_length=100)


class Post(models.Model):
    topic = models.CharField(max_length=50)
    image  =models.FileField(max_length=100,upload_to='event/')
    describe = models.TextField()
    date = models.DateField(auto_now_add=True)



