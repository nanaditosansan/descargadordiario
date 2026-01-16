import requests
import os
from urllib.parse import urlparse

def descargar_zip_bajador(url, ruta_destino):
    print(f"Iniciando descarga de: {url}")
    print(f"Guardando en: {ruta_destino}")
    # Asegúrate de que la carpeta de destino exista antes de escribir
    carpeta_destino = os.path.dirname(ruta_destino)
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino) # Crea la carpeta si no existe    
    try:        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(ruta_destino, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("\n ¡Descarga completada exitosamente!")        
    except requests.exceptions.RequestException as e:
            print(f"\n Error durante la descarga: {e}")
    except IOError as e:
            print(f"\n Error al guardar el archivo: Asegúrate de tener permisos para escribir en {ruta_destino}. Error: {e}")

def validar_archivo_zip_bajador(url):
    """
    Valida si una URL es accesible y si el servidor indica que el contenido
    es un archivo ZIP.
    """
    
    print(f"Validando URL: {url}...")
    

    try:
        resultado_parseo = urlparse(url)
        if not all([resultado_parseo.scheme, resultado_parseo.netloc]):
            print(" URL no válida sintácticamente.")
            return False
    except Exception as e:
        print(f" Error al parsear la URL: {e}")
        return False
        
    
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        response.raise_for_status() # Verifica si el código de estado es 200 (OK)
        
        # 3. Comprobar el Tipo de Contenido (MIME Type)
        # El encabezado 'Content-Type' indica el tipo de archivo.
        content_type = response.headers.get('Content-Type', '').lower()
        
        # Los MIME Types comunes para ZIP son:
        # - application/zip
        # - application/x-zip-compressed
        mime_types_zip = ['application/zip', 'application/x-zip-compressed']
        
        if any(mime in content_type for mime in mime_types_zip):
            print(f" Validación Exitosa: Código {response.status_code} y Content-Type: {content_type} (Es un ZIP)")
            return True
        else:
            print(f" Fallo de Validación: La URL existe, pero el Content-Type es: {content_type} (No es un ZIP esperado)")
            return False

    except requests.exceptions.HTTPError as e:
        print(f" Fallo de Acceso (Código de Error): La URL devolvió un código de error (e.g., 404, 500). Error: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f" Fallo de Conexión: No se pudo conectar a la URL (e.g., timeout, DNS error). Error: {e}")
        return False
    
def generar_cadenas_zip_bajador(prefijo_archivo:str, sufijo_archivo: str, anio: int) -> list[str]:
    """
    Genera una lista de 12 cadenas URL, variando el mes (01 a 12) para un año dado,
    y utilizando un sufijo de archivo personalizado.

    Args:
        prefijo_archivo : El prefijo del archivo por ejemplo https://www.asfi.gob.bo/sites/default/files/estadisticaif/bancos_multiples
        sufijo_archivo (str): El sufijo que se adjuntará al nombre del archivo 
                              (Ej: "_BMU_EstadosFinancieros.zip").
        anio (int, opcional): El año para el cual generar las cadenas.
        un ejemplo de resultado seria https://www.asfi.gob.bo/sites/default/files/estadisticaif/bancos_multiples/2025/02/202502_BMU_EstadosFinancieros.zip

    Returns:
        list[str]: Una lista de strings con el formato 'MM/YYYYMM{sufijo_archivo}'.
    """
    cadenas_urls = []
    
    # Iteramos desde el mes 1 (enero) hasta el mes 12 (diciembre)
    for mes in range(1, 13):
        
        # 1. Formato de Mes (MM) con padding de cero
        mes_str = f"{mes:02d}"
        
        # 2. Construcción de la Parte Variable (YYYYMM)
        parte_variable = f"{anio}{mes_str}"
        
        # 3. Construcción de la Cadena Final usando el sufijo_archivo
        cadena_final = f"{prefijo_archivo}/{anio}/{mes_str}/{parte_variable}{sufijo_archivo}"
        
        # Añadir a la lista
        cadenas_urls.append(cadena_final)
        
    return cadenas_urls

def final_bajador(prefijo,sufijo, anio, ruta_destino):
    lista_bmu = generar_cadenas_zip_bajador(prefijo,sufijo, anio)
    for cadena in lista_bmu:
        print(cadena)
        nombre_local = cadena.split('/')[-1]
        #destino_final=f"C:\\{ruta_destino}"
        destino_final = f"/data/{ruta_destino}"
        ruta_destino1 = os.path.join(destino_final, nombre_local)
        if validar_archivo_zip_bajador(cadena):
            descargar_zip_bajador(cadena, ruta_destino1)

def bajaanios(an1, an2, prefijo,sufijo,ruta_destino):
    an11=int(an1)
    an22=int(an2)
    for anio in range(an11, an22):
        final_bajador(prefijo,sufijo, anio, ruta_destino)

if __name__ == "__main__":
    # Estos valores podrían pasarse por variables de entorno o argumentos
    ANIO1 = os.getenv("ANIO1")
    ANIO2 = os.getenv("ANIO2")
    PREFIJO=os.getenv("PREFIJO")
    SUFIJO=os.getenv("SUFIJO")
    RUTA = os.getenv("RUTA")
    bajaanios(ANIO1,ANIO2, PREFIJO, SUFIJO, RUTA)