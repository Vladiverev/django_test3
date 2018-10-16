from django.db import models


# Create your models here.
class Client(models.Model):
    user_name = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    pass_user =  models.CharField(max_length=20)
    

    def __str__(self):
        return str(self.user_name)