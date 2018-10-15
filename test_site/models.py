from django.db import models


# Create your models here.
class Client(models.Model):
    user_name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    passwords = models.CharField(max_length=200)
    

    def __str__(self):
        return self.user_name