# Importamos las librerías necesarias
import pandas as pd
import os

# Definimos la función principal que se encargará de todo el proceso.
# Recibe como parámetros los filtros que después ingresará el usuario.
def filtrar_y_calcular(departamento, municipio, cultivo, limite):
    """
    Esta función lee los datos, los filtra según los criterios
    y calcula la mediana de las variables edáficas.
    """
    try:
        # --- SOLUCIÓN: Construir una ruta absoluta al archivo ---
        # Obtiene la ruta del directorio actual (donde está este script, es decir, 'api')
        script_dir = os.path.dirname(__file__) 
        # Construye la ruta completa al archivo subiendo un nivel ('..') y luego buscando el archivo
        file_path = os.path.join(script_dir, '..', 'resultado_laboratorio_suelo.xlsx')
        
        # Paso 1: Cargar los datos desde la ruta absoluta
        df = pd.read_excel(file_path)

        # --- MEJORA: Normalizar los datos a mayúsculas para evitar errores de coincidencia ---
        df.columns = df.columns.str.upper()
        # 2. Renombrar las columnas largas a cortas (usando los nombres ya en mayúsculas)
        df = df.rename(columns={
            'PH AGUA:SUELO 2,5:1,0': 'PH',
            'FÓSFORO (P) BRAY II MG/KG': 'FOSFORO (P)',
            'POTASIO (K) INTERCAMBIABLE CMOL(+)/KG': 'POTASIO (K)'
        })
        # --- SOLUCIÓN: Convertir columnas a tipo numérico ---
        # Las columnas de mediciones deben ser numéricas para poder calcular la mediana.
        # errors='coerce' convierte los valores no numéricos en NaN (Not a Number), que son ignorados en el cálculo.
        numeric_cols = ['PH', 'FOSFORO (P)', 'POTASIO (K)']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Convertir los valores de las columnas relevantes a mayúsculas
        df['DEPARTAMENTO'] = df['DEPARTAMENTO'].str.upper()
        df['MUNICIPIO'] = df['MUNICIPIO'].str.upper()
        df['CULTIVO'] = df['CULTIVO'].str.upper()

        # Paso 2: Filtrar el DataFrame basado en los inputs del usuario (también en mayúsculas)
        df_filtrado = df[
            (df['DEPARTAMENTO'] == departamento.upper()) &
            (df['MUNICIPIO'] == municipio.upper()) &
            (df['CULTIVO'] == cultivo.upper())
        ]

        # Si después de filtrar no hay datos, no se puede continuar.
        if df_filtrado.empty:
            return pd.DataFrame() # Devuelve un DataFrame vacío para que el UI lo maneje

         # --- CAMBIO: Devolver registros individuales Y la mediana total ---

        # 1. Seleccionar las columnas para mostrar los registros individuales
        columnas_a_mostrar = ['DEPARTAMENTO', 'MUNICIPIO', 'CULTIVO', 'TOPOGRAFIA', 'PH', 'FOSFORO (P)', 'POTASIO (K)']
        registros_individuales = df_filtrado[columnas_a_mostrar].head(limite)

        # 2. Calcular la mediana del conjunto de datos filtrado completo
        mediana_total = df_filtrado[['PH', 'FOSFORO (P)', 'POTASIO (K)']].median().to_frame().T
        mediana_total.rename(columns={'PH': 'Mediana_pH', 'FOSFORO (P)': 'Mediana_Fosforo', 'POTASIO (K)': 'Mediana_Potasio'}, inplace=True)

        # 3. Devolver ambos resultados
        return registros_individuales, mediana_total

    except FileNotFoundError:
        print("Error: No se encontró el archivo 'resultado_laboratorio_suelo.xlsx'.")
        print("Asegúrate de que el archivo esté en la carpeta principal del proyecto.")
        return None
    except KeyError as e:
        print(f"Error: La columna {e} no se encontró en el archivo. Revisa el nombre de las columnas.")
        return None