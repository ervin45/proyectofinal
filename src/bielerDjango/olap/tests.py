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
import unittest
from django.test.client import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def __test_rotacion_mes(self):
        # Issue a GET request.
        url = """/report/compras/pieza/tipo_pieza/grupo_constructivo/tipo_pieza/xr={}/yr={}/ore=[]/same/params=[['ft_compras', 'costo_dolar', 'sum']]/order_and_slice_the_cube/params=[]/"""

        response=self.client.get(url)

        # Check that the respose is 200 OK.
        self.failUnlessEqual(response.status_code, 200)

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
import unittest
from django.test.client import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def __test_rotacion_mes(self):
        # Issue a GET request.
        url = """/report/compras/pieza/tipo_pieza/grupo_constructivo/tipo_pieza/xr={}/yr={}/ore=[]/same/params=[['ft_compras', 'costo_dolar', 'sum']]/order_and_slice_the_cube/params=[]/"""

        response=self.client.get(url)

        # Check that the respose is 200 OK.
        self.failUnlessEqual(response.status_code, 200)

