# 🕸️ Scraper de Cursos de Coursera

Este repositorio contiene un script en Python que extrae información detallada de cursos ofrecidos en [Coursera.org](https://www.coursera.org/), utilizando **Selenium** y **BeautifulSoup**, y guarda los resultados en un archivo Excel.

---

## 📌 Características del Script

El script `main.py` recorre las 84 páginas de resultados de búsqueda de Coursera y extrae para cada curso:

- ✅ Título del curso  
- ✅ Organización que lo ofrece  
- ✅ Calificación del curso  
- ✅ Lista de habilidades obtenidas  
- ✅ Nivel del curso (Principiante, Intermedio, etc.)  
- ✅ Tipo de certificado  
- ✅ Número de estudiantes inscritos

El resultado final se guarda como `cursos_coursera.xlsx`.

---

## ✅ Requisitos

- Python 3.7 o superior  
- Google Chrome instalado en el sistema

---

## 🔧 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/uniicbog/CourseraWebScraping.git
cd tu-repo
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## ▶️ Ejecución

Ejecuta el script con:

```bash
python main.py
```

Al finalizar, se generará un archivo llamado cursos_coursera.xlsx en la raíz del proyecto, que contiene toda la información recolectada.

## 🧠 Consideraciones técnicas

- El script se ejecuta en modo headless (sin abrir el navegador).
- Utiliza webdriver-manager para descargar automáticamente el driver de Chrome.
- Hace scraping de cada curso individual para extraer el número de inscritos.
- Incluye una función para limpiar y validar números de inscritos.

## ⚠️ Advertencias

- Coursera puede modificar su estructura HTML en cualquier momento, lo que podría hacer que el script deje de funcionar.
- Evita hacer scraping masivo en cortos periodos de tiempo para no ser bloqueado.
