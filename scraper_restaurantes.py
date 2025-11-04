# -*- coding: utf-8 -*-
"""
Scraper de restaurantes para Montería usando Google Maps
Desarrollado para generar leads B2B de forma automatizada
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
from datetime import datetime


class ScraperRestaurantes:
    """
    Clase para extraer información de restaurantes desde Google Maps
    """
    
    def __init__(self):
        print("Iniciando scraper...")
        
        # Configurar Chrome para que no detecte que es un bot
        opciones = Options()
        opciones.add_argument('--no-sandbox')
        opciones.add_argument('--disable-dev-shm-usage')
        opciones.add_argument('--disable-blink-features=AutomationControlled')
        opciones.add_argument('--start-maximized')
        
        # Inicializar navegador
        servicio = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=servicio, options=opciones)
        self.espera = WebDriverWait(self.driver, 10)
        
        self.datos_restaurantes = []
        
    def buscar(self, ciudad="Montería, Córdoba, Colombia"):
        """
        Busca restaurantes en la ciudad especificada
        """
        print(f"\nBuscando restaurantes en {ciudad}...")
        
        # Construir URL de búsqueda
        busqueda = f"restaurantes en {ciudad}"
        url = f"https://www.google.com/maps/search/{busqueda.replace(' ', '+')}"
        
        self.driver.get(url)
        time.sleep(5)
        
        # Hacer scroll para cargar más resultados
        print("Cargando resultados...")
        self._hacer_scroll()
        
        # Extraer información
        print("Extrayendo datos...")
        self._extraer_todos()
        
    def _hacer_scroll(self, veces=10):
        """
        Hace scroll en el panel lateral para cargar más restaurantes
        """
        try:
            panel = self.driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
            
            for i in range(veces):
                self.driver.execute_script(
                    'arguments[0].scrollTop = arguments[0].scrollHeight', 
                    panel
                )
                time.sleep(2)
                print(f"  Scroll {i+1}/{veces}")
                
        except Exception as e:
            print(f"Error en scroll: {e}")
    
    def _extraer_todos(self):
        """
        Extrae la info de cada restaurante
        """
        try:
            # Encontrar todos los restaurantes en la lista
            items = self.driver.find_elements(
                By.CSS_SELECTOR,
                "div[role='feed'] > div > div > a"
            )
            
            print(f"Encontrados {len(items)} restaurantes\n")
            
            for i, item in enumerate(items, 1):
                try:
                    print(f"Procesando {i}/{len(items)}...")
                    
                    # Click para ver detalles
                    item.click()
                    time.sleep(2)
                    
                    # Extraer la info
                    info = self._obtener_info()
                    
                    if info:
                        self.datos_restaurantes.append(info)
                        print(f"  OK: {info['nombre']}")
                    
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error general: {e}")
    
    def _obtener_info(self):
        """
        Obtiene toda la información del restaurante actual
        """
        info = {}
        
        try:
            # Nombre
            try:
                nombre = self.driver.find_element(By.CSS_SELECTOR, "h1.DUwDvf").text
                info['nombre'] = nombre
            except:
                info['nombre'] = "N/A"
            
            # Rating
            try:
                rating = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "div.F7nice span[aria-hidden='true']"
                ).text
                info['rating'] = rating
            except:
                info['rating'] = "N/A"
            
            # Número de reseñas
            try:
                reviews = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "div.F7nice span[aria-label*='reseñas']"
                ).get_attribute('aria-label')
                num = re.search(r'(\d+)', reviews)
                info['num_reviews'] = num.group(1) if num else "N/A"
            except:
                info['num_reviews'] = "N/A"
            
            # Categoría
            try:
                cat = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[jsaction*='category']"
                ).text
                info['categoria'] = cat
            except:
                info['categoria'] = "N/A"
            
            # Dirección
            try:
                dir = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-item-id='address']"
                ).get_attribute('aria-label')
                info['direccion'] = dir.replace('Dirección: ', '')
            except:
                info['direccion'] = "N/A"
            
            # Teléfono
            try:
                tel = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-item-id*='phone']"
                ).get_attribute('aria-label')
                info['telefono'] = tel.replace('Teléfono: ', '')
            except:
                info['telefono'] = "N/A"
            
            # Sitio web
            try:
                web = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "a[data-item-id='authority']"
                ).get_attribute('href')
                info['website'] = web
            except:
                info['website'] = "N/A"
            
            # Horarios
            try:
                horario = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "button[data-item-id*='oh']"
                ).get_attribute('aria-label')
                info['horarios'] = horario
            except:
                info['horarios'] = "N/A"
            
            # Rango de precios
            try:
                precio = self.driver.find_element(
                    By.CSS_SELECTOR,
                    "span[aria-label*='Rango de precios']"
                ).get_attribute('aria-label')
                info['rango_precios'] = precio
            except:
                info['rango_precios'] = "N/A"
            
            # Coordenadas GPS desde la URL
            try:
                url_actual = self.driver.current_url
                coords = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url_actual)
                if coords:
                    info['latitud'] = coords.group(1)
                    info['longitud'] = coords.group(2)
                    info['link_maps'] = url_actual
                else:
                    info['latitud'] = "N/A"
                    info['longitud'] = "N/A"
                    info['link_maps'] = url_actual
            except:
                info['latitud'] = "N/A"
                info['longitud'] = "N/A"
                info['link_maps'] = "N/A"
            
            return info
            
        except Exception as e:
            print(f"  Error obteniendo datos: {e}")
            return None
    
    def guardar_excel(self, nombre=None):
        """
        Guarda todos los datos en un Excel
        """
        if not self.datos_restaurantes:
            print("No hay datos para guardar")
            return
        
        if nombre is None:
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre = f"restaurantes_monteria_{fecha}.xlsx"
        
        # Crear DataFrame
        df = pd.DataFrame(self.datos_restaurantes)
        
        # Ordenar columnas
        orden = [
            'nombre', 'categoria', 'rating', 'num_reviews',
            'telefono', 'direccion', 'website', 
            'horarios', 'rango_precios',
            'latitud', 'longitud', 'link_maps'
        ]
        
        # Filtrar solo columnas que existen
        orden = [col for col in orden if col in df.columns]
        df = df[orden]
        
        # Guardar con formato
        with pd.ExcelWriter(nombre, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Restaurantes')
            
            # Ajustar ancho de columnas
            hoja = writer.sheets['Restaurantes']
            for columna in hoja.columns:
                max_len = 0
                columna = [celda for celda in columna]
                for celda in columna:
                    try:
                        if len(str(celda.value)) > max_len:
                            max_len = len(celda.value)
                    except:
                        pass
                ancho = min(max_len + 2, 50)
                hoja.column_dimensions[columna[0].column_letter].width = ancho
        
        print(f"\nCompletado!")
        print(f"Archivo: {nombre}")
        print(f"Total: {len(self.datos_restaurantes)} restaurantes")
        
        return nombre
    
    def cerrar(self):
        """
        Cierra el navegador
        """
        self.driver.quit()
        print("\nNavegador cerrado")


def main():
    """
    Función principal
    """
    print("=" * 50)
    print("SCRAPER DE RESTAURANTES - MONTERÍA")
    print("=" * 50)
    
    scraper = ScraperRestaurantes()
    
    try:
        # Buscar y extraer
        scraper.buscar("Montería, Córdoba, Colombia")
        
        # Guardar
        archivo = scraper.guardar_excel()
        
        print("\n" + "=" * 50)
        print("PROCESO COMPLETADO")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError: {e}")
        
    finally:
        scraper.cerrar()


if __name__ == "__main__":
    main()
