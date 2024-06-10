import unittest
from unittest.mock import patch
import os
from gastos_viaje import Gasto, Viaje

class TestGastosViaje(unittest.TestCase):

    @patch('gastos_viaje.requests.get')
    def test_registro_gasto_reporte_diario(self, mock_get):
        # Simulamos la respuesta de la API para conversión de moneda
        mock_get.return_value.json.return_value = [{'random': 4000}]

        # Registrar un gasto de $100 USD en efectivo en transporte
        viaje = Viaje("USA", "2023-01-01", "2023-01-10", 100000)
        gasto = Gasto("2023-01-01", 100, "efectivo", "transporte", "USD")
        viaje.agregar_gasto(gasto)

        # Generar el reporte de gastos por día y verificar el valor convertido
        gastos_diarios = viaje.obtener_gastos_diarios()
        self.assertEqual(gastos_diarios["2023-01-01"]["efectivo"], 400000)
        self.assertEqual(gastos_diarios["2023-01-01"]["tarjeta"], 0)

    @patch('gastos_viaje.requests.get')
    def test_registro_gasto_reporte_por_tipo(self, mock_get):
        mock_get.return_value.json.return_value = [{'random': 4000}]

        # Registrar un gasto de €50 en tarjeta en alimentación
        viaje = Viaje("Europa", "2023-01-01", "2023-01-10", 100000)
        gasto = Gasto("2023-01-02", 50, "tarjeta", "alimentación", "EUR")
        viaje.agregar_gasto(gasto)

        # Generar el reporte de gastos por tipo y verificamos el valor convertido
        gastos_por_tipo = viaje.obtener_gastos_por_tipo()
        self.assertEqual(gastos_por_tipo["alimentación"]["tarjeta"], 210000)
        self.assertEqual(gastos_por_tipo["alimentación"]["efectivo"], 0)

    @patch('gastos_viaje.requests.get')
    def test_guardar_y_cargar_gastos(self, mock_get):
        mock_get.return_value.json.return_value = [{'random': 4000}]

        # Registramos varios gastos
        viaje = Viaje("París", "2023-01-01", "2023-01-10", 100000)
        gasto1 = Gasto("2023-01-01", 100, "efectivo", "transporte", "USD")
        gasto2 = Gasto("2023-01-02", 50, "tarjeta", "alimentación", "EUR")
        viaje.agregar_gasto(gasto1)
        viaje.agregar_gasto(gasto2)

        # Guardamos los gastos en un archivo
        archivo = 'gastos_test'
        viaje.guardar_gastos(archivo)

        # Cargamos los gastos desde el archivo
        nuevo_viaje = Viaje("París", "2023-01-01", "2023-01-10", 100000)
        nuevo_viaje.cargar_gastos(archivo)

        # Verificamos que los datos sean consistentes
        self.assertEqual(len(nuevo_viaje.gastos), 2)
        self.assertEqual(nuevo_viaje.gastos[0].fecha, "2023-01-01")
        self.assertEqual(nuevo_viaje.gastos[0].valor, 100)
        self.assertEqual(nuevo_viaje.gastos[1].fecha, "2023-01-02")
        self.assertEqual(nuevo_viaje.gastos[1].valor, 50)

        # Eliminamos el archivo de prueba
        os.remove(archivo + '.json')

if __name__ == '__main__':
    unittest.main()
