import requests
import json

class Gasto:
    def __init__(self, fecha, valor, metodo_pago, tipo_gasto, moneda):
        self.fecha = fecha
        self.valor = valor
        self.metodo_pago = metodo_pago
        self.tipo_gasto = tipo_gasto
        self.moneda = moneda
        self.tasa_cambio = self.obtener_tasa_cambio()

    def convertir_a_pesos(self):
        return self.valor * self.tasa_cambio

    def obtener_tasa_cambio(self):
        response = requests.get("https://csrng.net/csrng/csrng.php?min=3500&max=4500")
        tasa_base = response.json()[0]['random']
        if self.moneda == 'USD':
            return tasa_base
        elif self.moneda == 'EUR':
            return tasa_base + 200
        return 1

class Viaje:
    def __init__(self, destino, fecha_inicio, fecha_fin, presupuesto_diario):
        self.destino = destino
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.presupuesto_diario = presupuesto_diario
        self.gastos = []

    def agregar_gasto(self, gasto):
        self.gastos.append(gasto)

    def obtener_gastos_diarios(self):
        gastos_por_dia = {}
        for gasto in self.gastos:
            if gasto.fecha not in gastos_por_dia:
                gastos_por_dia[gasto.fecha] = {'efectivo': 0, 'tarjeta': 0}
            if gasto.metodo_pago == 'efectivo':
                gastos_por_dia[gasto.fecha]['efectivo'] += gasto.convertir_a_pesos()
            elif gasto.metodo_pago == 'tarjeta':
                gastos_por_dia[gasto.fecha]['tarjeta'] += gasto.convertir_a_pesos()
        return gastos_por_dia

    def obtener_gastos_por_tipo(self):
        gastos_por_tipo = {}
        for gasto in self.gastos:
            if gasto.tipo_gasto not in gastos_por_tipo:
                gastos_por_tipo[gasto.tipo_gasto] = {'efectivo': 0, 'tarjeta': 0}
            if gasto.metodo_pago == 'efectivo':
                gastos_por_tipo[gasto.tipo_gasto]['efectivo'] += gasto.convertir_a_pesos()
            elif gasto.metodo_pago == 'tarjeta':
                gastos_por_tipo[gasto.tipo_gasto]['tarjeta'] += gasto.convertir_a_pesos()
        return gastos_por_tipo

    def guardar_gastos(self, archivo):
        with open(archivo + '.json', 'w') as file:
            json.dump([gasto.__dict__ for gasto in self.gastos], file)

    def cargar_gastos(self, archivo):
        with open(archivo + '.json', 'r') as file:
            gastos = json.load(file)
            for gasto in gastos:
                gasto = {k: v for k, v in gasto.items() if k != "tasa_cambio"}
                self.agregar_gasto(Gasto(**gasto))
