from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd

# Configurar Selenium
options = Options()
options.add_argument("--headless")  # Ejecutar en segundo plano (sin abrir ventana)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def limpiar_numero(texto):
    if not texto:
        return "No es texto"
    limpio = texto.replace("\xa0", "").replace(".", "").strip()
    return limpio if limpio.isdigit() else "No se limpió bien"

base_url = "https://www.coursera.org/courses?sortBy=BEST_MATCH&page="
prefix_url = "https://www.coursera.org"

#Lista para almacenar los datos
datos = []

for page in range(1, 3):
    driver.get(base_url + str(page))
    time.sleep(3)  # Esperar a que se cargue la página

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    cards = soup.find_all('div', class_='cds-ProductCard-gridCard')

    for card in cards:
        titulo_tag = card.find('h3')
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título no encontrado"

        partner_tag = card.find('p', class_='cds-ProductCard-partnerNames')
        partner = partner_tag.get_text(strip=True) if partner_tag else "Socio no encontrado"

        rating_tag = card.find('div', attrs={'aria-label': 'calificación'})
        rating = rating_tag['aria-valuenow'] if rating_tag and rating_tag.has_attr('aria-valuenow') else "Sin rating"

        body_content = card.find('div', class_='cds-CommonCard-bodyContent')
        skills = "No encontrados"

        if body_content:
            skills_tag = body_content.find('p', class_='css-vac8rf')
            if skills_tag:
                skills = skills_tag.get_text(strip=True)
                if skills.lower().startswith("habilidades que obtendrás:"):
                    skills = skills.replace("Habilidades que obtendrás:", "").strip()

        metadata_div = card.find('div', class_='cds-CommonCard-metadata')
        description_tag = metadata_div.find('p', class_='css-vac8rf') if metadata_div else None
        descripcion = description_tag.get_text(strip=True) if description_tag else ""
        partes = [p.strip() for p in descripcion.replace('\xa0', ' ').split('·')]
        nivel = partes[0] if len(partes) > 0 else "No disponible"
        tipo = partes[1] if len(partes) > 1 else "No disponible"

        link_tag = card.find('a', href=True)
        estudiantes = "No disponible"

        if link_tag:
            full_link = prefix_url + link_tag['href']
            try:
                driver.get(full_link)
                time.sleep(3)

                detail_soup = BeautifulSoup(driver.page_source, 'html.parser')
                div_inscritos = detail_soup.find('div', class_='css-1qi3xup')

                if div_inscritos:
                    spans = div_inscritos.find_all('span')
                    if len(spans) >= 2:
                        raw_text = spans[1].get_text(strip=True)
                        estudiantes = limpiar_numero(raw_text)
                    else:
                        estudiantes = "No lo encontró"
                else:
                    estudiantes = "No encontró div de inscritos"
            except Exception as e:
                estudiantes = f"Error: {str(e)}"

        # Crear una fila por cada skill (separadas por comas)
        lista_skills = [s.strip() for s in skills.split(',')] if skills != "No encontrados" else ["No encontrados"]
        for skill in lista_skills:
            datos.append({
                "Título": titulo,
                "Organización": partner,
                "Calificación": rating,
                "Skill": skill,
                "Dificultad": nivel,
                "Tipo de certificado": tipo,
                "Inscritos": estudiantes
            })

# Guardar en Excel
df = pd.DataFrame(datos)
df.to_excel("cursos_coursera.xlsx", index=False)
print("\n Archivo 'cursos_coursera.xlsx' creado con éxito.")

driver.quit()