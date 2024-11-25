# Análisis de Sentimientos en Publicaciones de Instagram

Este proyecto tiene como objetivo procesar publicaciones y comentarios extraídos de Instagram para realizar análisis de sentimientos y clasificar imágenes según su contexto, utilizando herramientas de ETL, AWS y modelos de Machine Learning.

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
  1. `instagram_comments_general_data`: Información general de los comentarios.
  2. `instagram_comments_detail`: Detalle de los comentarios.
  3. Clasificación inicial de imágenes.
  4. Almacenamiento de fotos en formato JPG.

### 3. **Almacenamiento Inicial**
- Los datos procesados se almacenan en **Amazon S3 - Raw** como fuente cruda para análisis posterior.

### 4. **Catalogación y Organización**
- **AWS Crawler**:
  - Escanea y cataloga los datos almacenados en S3 - Raw.
- **AWS Glue Tables**:
  - Crea tablas estructuradas para consultas y análisis.

### 5. **Clasificación de Imágenes**
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
- **Catalogación**:
  - AWS Glue (Crawler y Tablas).
- **Modelos de Machine Learning**:
  - Clasificación de imágenes y análisis de sentimientos.

---

## Estructura del Proyecto

```plaintext
/
├── data/
│   ├── instagram_comments_general_data/  # JSON con datos generales de comentarios.
│   ├── instagram_comments_detail/       # JSON con detalles específicos.
│   ├── photos/                          # Imágenes en formato JPG.
│   ├── processed/                       # Datos procesados y limpios.
│
├── scripts/
│   ├── etl_preprocessing.py             # ETL inicial para datos de comentarios.
│   ├── image_classification.py          # Clasificación de imágenes.
│   ├── sentiment_analysis.py            # Modelo de análisis de sentimientos.
│
├── aws/
│   ├── crawler_config/                  # Configuración para AWS Crawler.
│   ├── glue_schemas/                    # Esquemas para tablas en AWS Glue.
│
├── models/
│   ├── image_classification_model/      # Modelo entrenado para clasificación de imágenes.
│   ├── sentiment_analysis_model/        # Modelo de sentimientos.
│
└── README.md                            # Documentación del proyecto.
