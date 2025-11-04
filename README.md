![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.15-green?style=flat)
![Status](https://img.shields.io/badge/Status-Active-success?style=flat)
![Location](https://img.shields.io/badge/Location-Medell%C3%ADn-orange?style=flat)

# Scraper de Restaurantes - Medellín

Herramienta que desarrollé para extraer datos de restaurantes desde Google Maps. La idea surgió porque necesitaba automatizar la recolección de información para proyectos de análisis de mercado en Medellín.

## ¿Qué hace?

Básicamente va a Google Maps, busca restaurantes en Medellín (o cualquier ciudad que le pongas), y extrae toda la información relevante:

- Nombre y categoría
- Rating y número de reseñas
- Teléfono y dirección
- Sitio web
- Horarios
- Coordenadas GPS
- Link directo de Google Maps

Todo lo guarda en un Excel bien organizado.

## Requisitos

```bash
pip install -r requirements.txt
```

## Cómo usar

Super simple:

```bash
python scraper_restaurantes.py
```

El script se ejecuta solo y al final genera un archivo Excel con todos los datos.

Si quieres cambiar la ciudad, edita esta línea en el código:

```python
scraper.buscar("Tu Ciudad, Departamento, Colombia")
```

## Por qué lo hice

Me di cuenta que muchos proveedores y agencias en Medellín necesitan bases de datos actualizadas de restaurantes para sus negocios. Extraer esto manualmente es tedioso, así que automaticé el proceso.

## Estructura del Excel generado

El archivo resultante tiene estas columnas:
- nombre
- categoria
- rating
- num_reviews
- telefono
- direccion
- website
- horarios
- rango_precios
- latitud
- longitud
- link_maps

## Notas importantes

- El scraper toma tiempo porque hace scroll y entra en cada restaurante
- Usa delays para no sobrecargar Google Maps
- Si Google detecta actividad sospechosa, puede aparecer un captcha (raro pero pasa)

## Casos de uso

Esto lo puedes usar para:
- Generar leads para proveedores
- Análisis de mercado gastronómico
- Estudios de competencia
- Prospección de ventas B2B
- Análisis de zonas comerciales

## Disclaimer

Este código es para uso educativo y personal. Úsalo responsablemente y respeta los términos de servicio de Google.

## Contacto

Si necesitas algo personalizado o tienes dudas, escríbeme.
