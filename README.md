# Natural Melodic Language Processing (NMLP)

<p align="center">
  <img src="https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge" alt="License: GPL v3">
  <img src="https://img.shields.io/github/stars/lopezrpablo/NMelodicLP?style=for-the-badge" alt="Stars">
  <img src="https://img.shields.io/github/issues/lopezrpablo/NMelodicLP?style=for-the-badge" alt="Issues">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python">
</p>

El proyecto Natural Melodic Language Processing (NMLP) es una plataforma integral de procesamiento orientado principalmente a analizar y comparar líneas melódicas de polifonía clásica mediante N-gramas y bags-of-words (BoW). NMLP utiliza fundamentalmente técnicas de procesamiento de lenguaje natural (como el paquete NLTK) y técnicas de aprendizaje automático (Scikit-learn) y visualización (Matplotlib o Pyplot) para, no solo extraer información melódica definitoria de los repertorios abordados, sino que también ver de primera mano las diferencias y semejanzas más importantes de cara a elaborar estudios empíricos de Music Information Retrieval (MIR) y Musicología Digital. Este paquete se ha desarrollado a raíz de una estancia de investigación que tuvo su autor, Pablo López-Rocamora (PhD, Universidad de Murcia) en el Departamento de Lenguajes y Sistemas Informáticos de la Universidad de Alicante en 2023.

El proyecto tiene como objetivo proporcionar un entorno robusto e interactivo para investigadores, analistas y entusiastas de la música para explorar y comprender las complejidades del lenguaje musical. Las características principales del proyecto incluyen la **carga de datos musicales**, la **extracción de características** y **análisis y modelado**, así como capacidades de **visualización**.

---

## 🚀 Características
- **Carga de Datos Musicales**: NMLP permite a los usuarios cargar y procesar archivos de música en varios formatos, incluyendo archivos MIDI, `**kern`, MEI y MusicXML.
- **Extracción de Características**: El proyecto utiliza caracteres ASCII para representar los cambios rítmicos e interválicos producidos entre dos notas. Estos elementos se llaman Inter-onset-Ratios (IORs) y mucho tiene que ver con las técnicas diseñadas por Doraisamy y Rüger (2001). En la carga de archivos se habilita la carga multicarpeta, pudiéndose encontrar la música de cada *corpus* a comparar en una de ellas.
- **Análisis y Modelado**: También implementa capacidades de manipulación de los N-gramas extraídos a través de diferentes escenarios: (a) seleccionar la longitud de los N-gramas; (b) seleccionar si se quiere analizar todas las voces juntas o una de ellas (definidas por orden numérico: S = 1, A = 2, T = 3 y B = 4); (c) elegir el tipo de codificación, ya sea base-40, base-12 o si se quiere indicar el sentido melódico (positivo = ascendente y negativo = descendente) o si se quiere procesar las voces mediante predicciones más cortas (metodología de *sliding window*); (d) se implementan modelos estadísticos como Laplace para medir si un modelo puede predecir mejor o peor una melodía desconocida mediante el cálculo de la "perplejidad" (que se puede traducir como semejanza); (e) la metodología de las BoW entronca directamente con el aprendizaje de máquina y se aplica al entrenar modelos capaces de clasificar obras anónimas basadas en un entrenamiento previo; y (f) incluye diferentes formas de visualización para comprender las complejidades del lenguaje musical.
- **Entorno Interactivo**: El proyecto proporciona un entorno interactivo --desplegado mediante JupyterLab-- para que investigadores, analistas y entusiastas de la música exploren y comprendan los datos musicales.

---

## 🛠️ Stack Tecnológico
- **Frontend**: Jupyter Notebook, Music21
- **Backend y análisis**: Python, pandas, numpy, nltk, sklearn
- **Base de datos**: Carpetas con codificaciones, siempre dentro del directorio "Music_Files".
- **Dependencias**: music21, pandas, numpy, nltk, sklearn, argparse, os, json

---

## 📦 Instalación
Para instalar el proyecto, sigue estos pasos:

1. **Configurar un entorno venv**: Cree un entorno virtual de Python en un directorio de su máquina.

```bash
python -m venv Nombre_del_entorno
```

2. **Clonar el Repositorio**: Dentro de la carpeta de su entorno virtual ejecute los siguientes comandos para iniciar el entorno virtual y clonar el repositorio NMelodicLP.

```bash
source bin/activate
git clone [https://github.com/lopezrpablo/NMelodicLP.git](https://github.com/lopezrpablo/NMelodicLP.git)
cd NMelodicLP
```
   
3. **Instalar Dependencias**: El paquete requiere de la instalación previa de Python, JupyterLab y otras librerías requeridas (music21, pandas, numpy, nltk, sklearn, argparse, os, json). Una vez desplegado el terminal del entorno virtual, se procede a instalar las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```

4. **Crear un kernel *ad hoc* para nuestros experimentos**:

```bash
python -m ipykernel install --user --name NMelodicLP --display-name "NMelodicLP"
```

> **Nota:** Al iniciar JupyterLab (si procede), se deberá cambiar el kernel por el llamado NMelodicLP.

5. **Configurar Variables de Entorno**: Configura las variables de entorno en el archivo .env. Básicamente se debe definir la variable MUSIC_FOLDER con el valor de la carpeta que contendrá todas las partituras codificadas para nuestros experimentos (predefinido como /Comp).

---

## 💻 Modos de uso
Existen dos modos de utilizar NMLP:

1. **Jupyter Lab**: desplegar este entorno a través del terminal de comandos hace mucho más sencillo el análisis. De hecho, se proporcionan tres cuadernos provistos de comentarios e instrucciones muy útiles: `1_main.ipynb` (análisis preliminar), `2_prediccion_sliding_window.ipynb` (aplicación del análisis anterior con la técnica *sliding window*) y `3_clasificadores.ipynb` (para el uso de modelos de aprendizaje automático sobre nuestra muestra musical).

2. **Extracción de características local**: Exportar conjuntos de N-gramas de los datos musicales localmente usando el script featureExtractor.py.

```bash
python3 featureExtractor.py [opciones]
```

| Parámetro | Tipo | Descripción |
| :--- | :--- | :--- |
| `--n` | *int* | Longitud de los N-gramas a extraer. |
| `--mode` | *str* | Información a codificar alfanuméricamente en cada elemento del N-grama (I incluye IORs (ritmo); i incluye intervalos melódicos; b codifica ratios calculados entre la fuerza métrica de ataque de dos eventos consecutivos; y d calcula los ratios del número de ataques que ocurren mientras suena cada una de las notas). |
| `--diatonic` | *bool* | Extracción de interválica según la codificación de base-7 (excluyente) |
| `--base40` | *bool* | Extracción de interválica según la codificación de base-40 (excluyente) |

> **Nota 1:** La selección de archivos se mostrará tras este primer comando.  
> **Nota 2:** Si el parámetro base-12 es igual a *True*, base-40 deberá ser *False* (y viceversa).

---

## 🚀 Funciones importantes y sus parámetros

### `select_files`

```python
select_files(multiple_folder_selection=False, split_by_voices=True)
```

| Parámetro | Tipo | Descripción | Por defecto |
| :--- | :--- | :--- | :--- |
| `multiple_folder_selection` | *Bool* | Si se quiere agrupar en un mismo conjunto las partituras de más de una carpeta | *False* |
| `split_by_voices` | *Bool* | Si se plantea filtrar las partituras seleccionadas por el número total de sus voces | *True* |

### `corpora_parser`

```python
def corpora_parser(n, data, data2, diatonic=False, base40=True, stack=True, mode='Iibd', voice_selec='All'):
```

| Parámetro | Tipo | Descripción | Por defecto |
| :--- | :--- | :--- | :--- |
| `n` | *Int* | Longitud de los N-gramas | None |
| `data` | *Array* | Objeto devuelto por la función select_files() para el primer compositor de referencia | *None* |
| `data2` | *Array* | Objeto devuelto por la función select_files() para el segundo compositor de referencia | *None* |
| `diatonic` | *Bool* | Extracción de interválica según la codificación de base-7 | *False* |
| `base40` | *Bool* | Opción de codificación en base-40 | *True* |
| `stack` | *Bool* | Si la selección de voces es "All", deberá ser *True* | *True* |
| `mode` | *str* | Mismos criterios que en featureExtractor.py | *None* |
| `voice_selec` | *str* | Voces a extraer (All, 1, 2, 3, etc.) | "All" |

> **Nota:** El uso óptimo de todos los comandos está detallado y articulado en los cuadernos de JupyterLab con ejemplos concretos.

---

## 📂 Estructura del Proyecto

```text
NMLP_Project/
├── NMLP_loaders.py
├── featureExtractor.py
├── plotters.py
├── 1_main.ipynb
├── 2_prediccion_sliding_window.ipynb
├── 3_clasificadores.ipynb
├── translator.json
├── requirements.txt
├── README.md
├── .env
├── Comp/
│   ├── Anon/
│   ├── Comp1/
│   └── ...
├── Exports/
│   ├── exportfile.csv.gz
│   ├── exportfile2.csv.gz
│   └── ...
└── ...
```

---

## 🤝 Contribuyendo y Citación

Para contribuir al proyecto, por favor sigue estos pasos:

1. **Hacer un Fork del Repositorio**: Haz un fork del repositorio del proyecto NMLP desde GitHub.
2. **Crear una Rama**: Crea una nueva rama para tu contribución.
3. **Hacer Cambios**: Realiza cambios en el código y haz un commit con ellos.
4. **Crear un Pull Request**: Crea un pull request para fusionar tus cambios en la rama principal.

### 📚 Cómo citar este trabajo
Si utilizas NMLP o parte de su código en tus investigaciones, publicaciones académicas o proyectos de Musicología Digital / MIR, por favor cita el repositorio y su registro en Zenodo:

```bibtex
@software{lopez_rocamora_nmlp,
  author       = {López-Rocamora, Pablo},
  title        = {{Natural Melodic Language Processing (NMLP)}},
  month        = oct,
  year         = {2026},
  publisher    = {Zenodo},
  version      = {v1.0.0},
  doi          = {10.5281/zenodo.23728128},
  url          = {https://doi.org/10.5281/zenodo.23728128}
}
```

> **Nota para investigadores:** Sustituye `10.5281/zenodo.XXXXXXX` por el identificador DOI definitivo una vez generado el release en Zenodo.

---

## 📝 Licencia
Este proyecto está bajo la Licencia **GNU General Public License v3.0** (GNU GPLv3). Consulta el archivo `LICENSE` para más detalles.

---

## 📬 Contacto
Para más información, por favor ponte en contacto conmigo a través de DM o abriendo un *issue* en este repositorio.

---

## 🙏 Agradecimientos
¡Gracias por usar el proyecto NMLP! Este proyecto está diseñado para proporcionar una plataforma integral de procesamiento y análisis musical para investigadores, analistas y entusiastas de la música. Esperamos que te sea útil.
