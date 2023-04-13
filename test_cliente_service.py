import unittest
from unittest.mock import patch, MagicMock
from dto.cliente_dto import ClienteDTO
import services.cliente_service


class TestDatabase(unittest.TestCase):

    @patch('database.session.query')
    def test_obtener_clientes(self, mock_query):
        # Crear una lista de clientes falsos para simular la respuesta de la base de datos
        clientes_falsos = [
            MagicMock(id=1, tipo_identificacion="CC", num_identificacion="123456789", nombres="Juan", apellidos="Pérez",
                      correo="juanperez@example.com", direccion="Calle 123", telefono="555-1234"),
            MagicMock(id=2, tipo_identificacion="NIT", num_identificacion="987654321", nombres="María",
                      apellidos="Gómez",
                      correo="mariagomez@example.com", direccion="Carrera 456", telefono="555-4321")
        ]
        mock_query.return_value.all.return_value = clientes_falsos

        # Llamar a la función que se va a probar
        resultado = services.cliente_service.obtener_clientes()

        # Verificar que la función retornó lo que se esperaba
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), len(clientes_falsos))
        self.assertIsInstance(resultado[0], ClienteDTO)
        self.assertEqual(resultado[0].tipo_identificacion, clientes_falsos[0].tipo_identificacion)
        self.assertEqual(resultado[0].num_identificacion, clientes_falsos[0].num_identificacion)
        self.assertEqual(resultado[0].nombres, clientes_falsos[0].nombres)
        self.assertEqual(resultado[0].apellidos, clientes_falsos[0].apellidos)
        self.assertEqual(resultado[0].correo, clientes_falsos[0].correo)
        self.assertEqual(resultado[0].direccion, clientes_falsos[0].direccion)
        self.assertEqual(resultado[0].telefono, clientes_falsos[0].telefono)

    @patch('database.session.query')
    def test_buscar_cliente_por_correo(self, mock_query):
        # Crear un cliente falso para simular la respuesta de la base de datos
        cliente_falso = MagicMock(id=1, tipo_identificacion="CC", num_identificacion="123456789", nombres="Juan",
                                  apellidos="Pérez",
                                  correo="juanperez@example.com", direccion="Calle 123", telefono="555-1234")
        mock_query.return_value.filter.return_value.first.return_value = cliente_falso

        # Llamar a la función que se va a probar
        resultado = services.cliente_service.buscar_cliente_por_tipo_y_num_identificacion(
            cliente_falso.tipo_identificacion, cliente_falso.num_identificacion)

        # Verificar que la función retornó lo que se esperaba
        self.assertIsInstance(resultado, ClienteDTO)
        self.assertEqual(resultado.tipo_identificacion, cliente_falso.tipo_identificacion)
        self.assertEqual(resultado.num_identificacion, cliente_falso.num_identificacion)
