from api.procesador_datos import filtrar_y_calcular

from ui.interfaz_usuario import solicitar_datos_usuario, mostrar_resultados


# 2. Definir la función principal que orquesta el programa
def main():
    """
    Función principal que ejecuta el flujo del programa:
    1. Pide los datos al usuario.
    2. Procesa los datos.
    3. Muestra los resultados.
    """
    # Llama a la función para obtener los filtros del usuario
    departamento, municipio, cultivo, limite = solicitar_datos_usuario()
    
    # --- CAMBIO: Capturar los dos resultados que devuelve la función ---
    registros, mediana = filtrar_y_calcular(departamento, municipio, cultivo, limite)
    
    # --- CAMBIO: Pasar los dos resultados a la función que muestra ---
    mostrar_resultados(registros, mediana)

# 3. Punto de entrada del programa
# Este bloque asegura que el código dentro de él solo se ejecute
# cuando el archivo main.py es corrido directamente.
if __name__ == "__main__":
    main()