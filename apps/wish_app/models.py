from __future__ import unicode_literals
from django.db import models
from urllib import request
import re, bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        reuser=User.objects.filter(email=postData['email'])
        if reuser:
            errors['email']="There is already a user with this email address."
            return errors
        if len(postData['first_name'])<2:
            errors["first_name"] = "Your first name should be at least 2 characters long."
        if (postData['first_name']).isalpha() !=True:
            errors["first_name2"] = "Your first name should be comprised only of letters."
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Your last name should be at least 2 characters long."
        if (postData['last_name']).isalpha() !=True:
            errors["last_name2"] = "Your last name should be comprised only of letters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email2'] = ("Your email address is not a valid format.")
        if len(postData['password']) < 8:
            errors["password"] = "Your password should be at least 8 characters long."
        if postData['password'] !=postData['confirm_password']:
            errors["confirm_password"] = "Your password confirmation does not match your password."
        return errors
    def login_validator(self, postData):
        errors ={}
        logged_user=User.objects.filter(email=postData['email'])
        if logged_user:
            user=logged_user[0]
        else:
            errors['email']='There is no user that matches this email. Please register.'
            return errors
        if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
            return errors
        else:
            errors['password']='This password does not match this email. Please try again.'
            return errors
    def wish_validator(self, postData):
        errors = {}
        if len(postData['item'])<3:
            errors['title']="Your wish must be at least three characters long. Come on. Dream big."
        if len(postData['description'])<3:
            errors['description']="Your description needs to be a little longer."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 45)
    password = models.CharField(max_length = 70)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()

class Wish(models.Model):
    item=models.CharField(max_length=255)
    description=models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    wished_by = models.ForeignKey(User, related_name="wishes_made")
    objects = UserManager()

class Granted(models.Model):
    item=models.CharField(max_length=255)
    description=models.TextField()
    # wish_created=models.DateTimeField()
    wished_by = models.ForeignKey(User, related_name="wishes_granted")
    # wishers_who_like = models.ManyToManyField(User, related_name="liked_wishes")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UserManager()  