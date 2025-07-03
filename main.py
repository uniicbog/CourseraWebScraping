from bs4 import BeautifulSoup
import requests
import time

def limpiar_numero(texto):
    if not texto:
        return "No es texto"
    limpio = texto.replace("\xa0", "").replace(",", "").strip()
    return limpio if limpio.isdigit() else "No se limpio bien"

base_url = "https://www.coursera.org/courses?sortBy=BEST_MATCH&page="
prefix_url = "https://www.coursera.org"

for page in range(1, 3):
    url = base_url + str(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(f"\n--- Página {page} ---")

    cards = soup.find_all('div', class_='cds-ProductCard-gridCard')

    for card in cards:
        # Título
        titulo_tag = card.find('h3')
        titulo = titulo_tag.get_text(strip=True) if titulo_tag else "Título no encontrado"

        # Socio
        partner_tag = card.find('p', class_='cds-ProductCard-partnerNames')
        partner = partner_tag.get_text(strip=True) if partner_tag else "Socio no encontrado"

        # Rating
        rating_tag = card.find('div', attrs={'aria-label': 'Rating'})
        rating = rating_tag['aria-valuenow'] if rating_tag and rating_tag.has_attr('aria-valuenow') else "Sin rating"

        # Nivel y tipo
        metadata_div = card.find('div', class_='cds-CommonCard-metadata')
        description_tag = metadata_div.find('p', class_='css-vac8rf') if metadata_div else None
        descripcion = description_tag.get_text(strip=True) if description_tag else ""
        partes = [p.strip() for p in descripcion.replace('\xa0', ' ').split('·')]
        nivel = partes[0] if len(partes) > 0 else "No disponible"
        tipo = partes[1] if len(partes) > 1 else "No disponible"

        # Enlace a la tarjeta
        link_tag = card.find('a', href=True)
        estudiantes = "No disponible"

        if link_tag:
            full_link = prefix_url + link_tag['href']
            if "/specializations/" in full_link:
                try:
                    detalle_resp = requests.get(full_link)
                    print(detalle_resp)
                    detalle_soup = BeautifulSoup(detalle_resp.text, 'html.parser')

                    # Buscar segundo <span> dentro de <div class="css-1qi3xup">
                    div_inscritos = detalle_soup.find('div', class_='css-1qi3xup')
                    if div_inscritos:
                        spans = div_inscritos.find_all('span')
                        if len(spans) >= 2:
                            raw_text = spans[1].get_text(strip=True)
                            print(raw_text)
                            estudiantes = limpiar_numero(raw_text)
                        else:
                            estudiantes = "No lo encontro"
                except Exception as e:
                    estudiantes = f"Error: {str(e)}"

        print(f"Título: {titulo}")
        print(f"Socio: {partner}")
        print(f"Rating: {rating}")
        print(f"Nivel: {nivel}")
        print(f"Tipo: {tipo}")
        print(f"Inscritos: {estudiantes}")
        print("---")