from registro.gastos_viaje import Gasto, Viaje

def main():
    print("Bienvenido a la aplicación de gestión de gastos de viaje")
    destino = input("Ingrese el destino del viaje: ")
    fecha_inicio = input("Ingrese la fecha de inicio del viaje (AAAA-MM-DD): ")
    fecha_fin = input("Ingrese la fecha de fin del viaje (AAAA-MM-DD): ")
    presupuesto_diario = float(input("Ingrese el presupuesto diario en pesos colombianos: "))

    viaje = Viaje(destino, fecha_inicio, fecha_fin, presupuesto_diario)

    while True:
        print("\nMenú:")
        print("1. Registrar gasto")
        print("2. Ver reporte de gastos por día")
        print("3. Ver reporte de gastos por tipo")
        print("4. Guardar gastos")
        print("5. Cargar gastos")
        print("6. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            fecha = input("Ingrese la fecha del gasto (AAAA-MM-DD): ")
            valor = float(input("Ingrese el valor del gasto: "))
            metodo_pago = input("Ingrese el método de pago (efectivo/tarjeta): ")
            tipo_gasto = input("Ingrese el tipo de gasto (transporte/alojamiento/alimentación/entretenimiento/compras): ")
            moneda = input("Ingrese la moneda del gasto (COP/USD/EUR): ")
            gasto = Gasto(fecha, valor, metodo_pago, tipo_gasto, moneda)
            viaje.agregar_gasto(gasto)
            print("Gasto registrado exitosamente.")

        elif opcion == '2':
            gastos_diarios = viaje.obtener_gastos_diarios()
            for fecha, gastos in gastos_diarios.items():
                total = gastos['efectivo'] + gastos['tarjeta']
                presupuesto_diario_restante = viaje.presupuesto_diario - total
                print(f"Fecha: {fecha}, Efectivo: {gastos['efectivo']}, Tarjeta: {gastos['tarjeta']}, Total: {total}, Presupuesto diario restante: {presupuesto_diario_restante}")

        elif opcion == '3':
            gastos_por_tipo = viaje.obtener_gastos_por_tipo()
            for tipo, gastos in gastos_por_tipo.items():
                total = gastos['efectivo'] + gastos['tarjeta']
                print(f"Tipo: {tipo}, Efectivo: {gastos['efectivo']}, Tarjeta: {gastos['tarjeta']}, Total: {total}")

        elif opcion == '4':
            archivo = input("Ingrese el nombre del archivo para guardar los gastos: ")
            viaje.guardar_gastos(archivo)
            print("Gastos guardados exitosamente.")

        elif opcion == '5':
            archivo = input("Ingrese el nombre del archivo para cargar los gastos: ")
            viaje.cargar_gastos(archivo)
            print("Gastos cargados exitosamente.")

        elif opcion == '6':
            break

        else:
            print("Opción no válida. Por favor intente de nuevo.")

if __name__ == '__main__':
    main()
