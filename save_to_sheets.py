import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Función para extraer datos desde dolarhoy.com
def obtener_precio_dolar():
    url = "https://dolarhoy.com/cotizaciondolaroficial"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Encontrar la sección del dólar oficial
    oficial_div = soup.find_all('div', class_='tile is-child')[1]
    compra = oficial_div.find_all('div', class_='value')[0].text.replace('$', '').strip().replace(",", ".")
    venta = oficial_div.find_all('div', class_='value')[1].text.replace('$', '').strip().replace(",", ".")
    
    return float(compra), float(venta)

# Función para guardar en Google Sheets
def guardar_en_sheets():
    # Autenticación con Google
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credenciales.json', scope)
    client = gspread.authorize(creds)

    # Abrir la hoja (nombre exacto de tu archivo de Google Sheets)
    sheet = client.open("precios_dolar").sheet1

    # Obtener datos y agregarlos
    compra, venta = obtener_precio_dolar()
    ahora = datetime.now()
    sheet.append_row([str(ahora.date()), ahora.strftime('%H:%M'), compra, venta])

if __name__ == "__main__":
    guardar_en_sheets()
