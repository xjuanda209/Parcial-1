def solicitar_datos_usuario():
    print("--- Consulta de Datos Edáficos ---")
    departamento = input("Ingrese el Departamento: ")
    municipio = input("Ingrese el Municipio: ")
    cultivo = input("Ingrese el Cultivo: ")
    limite = int(input("¿Cuántos registros desea ver? ")) # Convertimos a entero
    return departamento, municipio, cultivo, limite

# --- CAMBIO: La función ahora recibe 'registros' y 'mediana' por separado ---
def mostrar_resultados(registros, mediana):
    if registros is not None and not registros.empty:
        print("\n--- Registros Encontrados ---")
        print(registros.to_string(index=False))
        
        print("\n--- Mediana Total de los Registros Filtrados ---")
        print(mediana.to_string(index=False))
    elif registros is not None:
        print("\nNo se encontraron registros que coincidan con los criterios de búsqueda.")
