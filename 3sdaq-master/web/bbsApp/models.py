from django.db import models

# Create your models here.
class BbsUser(models.Model) :
    user_id   = models.CharField(max_length=50, primary_key=True)
    user_pwd  = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id +"\t"+ self.user_pwd +"\t"+ self.user_name


