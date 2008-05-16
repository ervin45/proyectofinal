from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(maxlength=70)
    user_id = models.IntegerField()
    class Meta:
        db_table = 'categorias'

    class Admin:
        pass

class Reporte(models.Model):
    nombre = models.CharField(maxlength=60)
    dwp = models.CharField(maxlength=600)
    user_id = models.IntegerField()
    categoria = models.ForeignKey(Categoria)
    class Meta:
        db_table = 'reportes'

    class Admin:
        pass

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
