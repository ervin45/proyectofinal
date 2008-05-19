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

