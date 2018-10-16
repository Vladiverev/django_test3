from django.db import models


# Create your models here.
class Client(models.Model):
    user_name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user_name