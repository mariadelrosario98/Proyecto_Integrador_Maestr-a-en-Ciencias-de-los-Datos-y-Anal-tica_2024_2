# Análisis de Sentimientos en Publicaciones de Instagram

Este proyecto tiene como objetivo procesar publicaciones y comentarios extraídos de Instagram para realizar análisis de sentimientos y clasificar imágenes según su contexto, utilizando herramientas de ETL, AWS y modelos de Machine Learning.

![ARQUITECTURA_PI drawio (2)](https://github.com/user-attachments/assets/5d80dac8-0422-4ec7-9b21-9de9c16cf0ab)

---

## Descripción General del Flujo
### 1. **Extracción de Datos**
- **Fuente**: API Meta para Instagram.
- **Datos extraídos**:
  - Publicaciones.
  - Comentarios asociados.
- **Formato**: JSON.

### 2. **ETL - Conversión y Preprocesamiento**
- Conversión de imágenes a JSON para un análisis estructurado.
- Procesamiento inicial para dividir los datos en:

### 3. **Almacenamiento Inicial**
- Los datos procesados se almacenan en **Amazon S3 - Raw** como fuente cruda para análisis posterior.

### 4. **Clasificación de Imágenes**
- Uso de un modelo de Machine Learning para clasificar imágenes en dos categorías:
  - **Producto**: Relacionado con productos de la marca.
  - **Mensaje de Activismo**: Contenido de responsabilidad social u otras causas.
- Los datos clasificados son reubicados en **S3 - Trusted** para mayor fiabilidad.

### 6. **Análisis de Comentarios**
- **Procesamiento ETL con Python**:
  - Tokenización y lematización de comentarios.
- Los resultados del procesamiento se almacenan nuevamente en **S3 - Trusted**.

### 7. **Modelo de Análisis de Sentimientos**
- Un modelo de análisis de sentimientos procesa los comentarios, generando insights sobre las percepciones de los usuarios hacia los productos y mensajes de activismo.

---

## Herramientas Utilizadas

- **Extracción de Datos**:
  - API Meta para Instagram.
- **ETL**:
  - Scripts en Python para preprocesamiento.
- **Almacenamiento**:
  - Amazon S3 (Raw y Trusted).
- **Modelos de Machine Learning**:
  - Clasificación de imágenes y análisis de sentimientos.

---
