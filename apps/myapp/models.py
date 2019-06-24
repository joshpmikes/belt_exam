from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length = 75)
    last_name = models.CharField(max_length = 75)
    email = models.EmailField(max_length = 75)
    password = models.CharField(max_length = 75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #quotes_uploaded = a list of quotes uploaded by the user
    #quotes_liked = a list of quotes liked by the user
    

class Quote(models.Model):
    author = models.CharField(max_length = 75)
    actual_quote = models.TextField()
    uploaded_by=models.ForeignKey(User,related_name="quotes_uploaded")
    users_who_liked= models.ManyToManyField(User, related_name="quotes_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #likes = a list of likes for a given quote

