from django.db import models

class ReportTemplate(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField()
    ft = models.CharField()
    default_dwp = models.CharField()
    user_id = models.IntegerField()
    
    class Admin:
        pass
    
    class Meta:
        db_table = 'report_template'

