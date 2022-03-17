
from django.db import models

# Create your models here.
class WebNotice(models.Model) :
    id      = models.BigAutoField(primary_key = True)
    title   = models.CharField(max_length=500)
    writer  = models.CharField(max_length=100)
    content = models.TextField()
    regdate = models.DateTimeField(auto_now=True)
    viewcnt = models.IntegerField(default=0)

class WebNoticeComment(models.Model) :
    id     = models.BigAutoField(primary_key=True)
    txt    = models.CharField(max_length=500)
    writer = models.CharField(max_length=100)
    notice_id = models.ForeignKey(WebNotice , on_delete=models.CASCADE , db_column='notice_id')
