import unittest
from django.test.client import Client

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_details(self):
        # Issue a GET request.
        url = """/report2/ventas/pieza/tiempo/modelo/mes/xr={'grupo_constructivo':[184], 'modelo':[3]}/yr={}/ore={}/movimientos/pieza/tiempo/modelo/anio/xr={'grupo_constructivo':[184], 'modelo':[3]}/yr={}/ore={}/"""
        response=self.client.get(url)

        # Check that the respose is 200 OK.
        self.failUnlessEqual(response.status_code, 200)