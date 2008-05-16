#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
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
#############################################################################
#
#    Sistema de soporte de decisiones para Ricardo Bieler S.A.
#    Copyright (C) 2007-2008 Nicolas D. Cesar, Mariano N. Galan
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
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
