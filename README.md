# 🧠 Natural Melodic Language Processing (NMLP)

<p align="center">
  <img src="https://img.shields.io/github/license/lopezrpablo/NMelodicLP?style=for-the-badge&color=main" alt="License">
  <img src="https://img.shields.io/github/stars/lopezrpablo/NMelodicLP?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/issues/lopezrpablo/NMelodicLP?style=for-the-badge" alt="Issues">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
</p>

El proyecto Natural Melodic Language Processing (NMLP) es una plataforma integral de procesamiento y análisis musical que utiliza técnicas de aprendizaje automático y procesamiento de lenguaje natural para extraer características de datos musicales. El proyecto tiene como objetivo proporcionar un entorno robusto e interactivo para investigadores, analistas y entusiastas de la música para explorar y comprender las complejidades del lenguaje musical. Las características principales del proyecto incluyen la carga de datos musicales, la extracción de características y el análisis, así como capacidades de modelado y visualización interactiva.

---

## 🚀 Características
* **Carga de Datos Musicales**: El proyecto permite a los usuarios cargar y procesar archivos de música en varios formatos, incluyendo archivos MIDI y de audio.
* **Extracción de Características**: El proyecto utiliza técnicas de aprendizaje automático y procesamiento de lenguaje natural para extraer características de los datos musicales, incluyendo características melódicas, armónicas y rítmicas.
* **Análisis y Modelado**: El proyecto proporciona capacidades de modelado y visualización interactiva, lo que permite a los usuarios explorar y comprender las complejidades del lenguaje musical.
* **Entorno Interactivo**: El proyecto proporciona un entorno interactivo para que investigadores, analistas y entusiastas de la música exploren y comprendan los datos musicales.

---

## 🛠️ Stack Tecnológico
* **Frontend**: Jupyter Notebook, Music21
* **Backend**: Python, pandas, numpy, nltk, sklearn
* **Base de datos**: Ninguna
* **Herramientas de IA**: librería music21, librería nltk, librería sklearn
* **Herramientas de construcción**: Ninguna
* **Dependencias**: music21, pandas, numpy, nltk, sklearn, argparse, os, json

---

## 📦 Instalación
Para instalar el proyecto, sigue estos pasos:
1. **Prerrequisitos**: Instala Python, Jupyter Notebook y las librerías requeridas (music21, pandas, numpy, nltk, sklearn, argparse, os, json).
2. **Clonar el Repositorio**: Clona el repositorio del proyecto NMLP desde GitHub.
   ```
   git clone [https://github.com/lopezrpablo/NMelodicLP.git](https://github.com/lopezrpablo/NMelodicLP.git)
   cd NMelodicLP```
   
3. **Instalar Dependencias**: Instala las dependencias requeridas usando pip.

```pip install music21 pandas numpy nltk scikit-learn jupyter```

4. **Configurar Variables de Entorno**: Configura las variables de entorno en el archivo env_variables.env.

💻 **MODO DE USO**
Para usar el proyecto, sigue estos pasos:

1. **Cargar Datos Musicales**: Carga archivos de música usando la función select_files en el script NMLP_loaders.py.

2. **Extraer Características**: Extrae características de los datos musicales usando el script featureExtractor.py.

3. **Analizar y Modelar**: Analiza y modela los datos musicales usando el notebook 1_main.ipynb.

📂 Estructura del Proyecto

```
NMLP_Project/
├── NMLP_loaders.py
├── featureExtractor.py
├── 1_main.ipynb
├── env_variables.env
├── assets/
│   ├── loadMelodic.py
│   ├── select_files.py
│   ├── corpora_parser.py
│   └── ...
├── data/
│   ├── music_files/
│   └── ...
├── models/
│   ├── trained_models/
│   └── ...
├── notebooks/
│   ├── 1_main.ipynb
│   └── ...
├── scripts/
│   ├── NMLP_loaders.py
│   ├── featureExtractor.py
│   └── ...
└── ...```
📸 **Capturas de pantalla**
🤝 **Contribuyendo**
Para contribuir al proyecto, por favor sigue estos pasos:

1. **Hacer un Fork del Repositorio**: Haz un fork del repositorio del proyecto NMLP desde GitHub.

2. **Crear una Rama**: Crea una nueva rama para tu contribución.

3. **Hacer Cambios**: Realiza cambios en el código y haz un commit con ellos.

4. **Crear un Pull Request**: Crea un pull request para fusionar tus cambios en la rama principal.

📝 Licencia
El proyecto NMLP está bajo la Licencia MIT.

📬 Contacto
Para más información, por favor ponte en contacto con nosotros en [insertar correo electrónico de contacto].

AGRADECIMIENTO

¡Gracias por usar el proyecto NMLP! Este proyecto está diseñado para proporcionar una plataforma integral de procesamiento y análisis musical para investigadores, analistas y entusiastas de la música. Esperamos que te sea útil.
