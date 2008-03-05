from django.db import models

class ReportTemplate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=60)
    ft = models.CharField(max_length=60)
    default_dwp = models.CharField(max_length=600)
    user_id = models.IntegerField()
    
    class Admin:
        pass
    
    class Meta:
        db_table = 'report_template'

