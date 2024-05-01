# utils.py
from bs4 import BeautifulSoup
import requests
import re

def get_data_from_kabum(link):
    # Make a GET request to the link
    response = requests.get(link)

    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the component text
    component_element = soup.find('h1', class_='sc-58b2114e-6 brTtKt')
    component = component_element.text if component_element else None

    # Find the cash price
    cash_price_element = soup.find('h4', class_='sc-5492faee-2 ipHrwP finalPrice')
    cash_price = cash_price_element.text.replace('R$', '').replace('\u00a0', ' ') if cash_price_element else None

    # Find the installment price
    installment_price_element = soup.find('b', class_='regularPrice')
    installment_price = installment_price_element.text.replace('R$', '').replace('\u00a0', ' ') if installment_price_element else None

    return {
        'component': component,
        'cash_price': cash_price,
        'installment_price': installment_price
    }

def get_data_from_pichau(link):
    # Make a GET request to the link
    response = requests.get(link)

    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the component text
    component_element = soup.select_one('h1.MuiTypography-root.MuiTypography-h6')
    component = component_element.text.strip() if component_element else None

    # Find the cash price (à vista) element
    cash_price_element = soup.select_one('div.jss284')  # Adjusted selector for cash price
    cash_price = None
    if cash_price_element:
        cash_price_text = cash_price_element.text.strip()
        # Extract the numeric value after 'R$'
        match = re.search(r'R\$\s*([\d,\.]+)', cash_price_text)
        if match:
            cash_price = match.group(1).replace('.', '').replace(',', '.')

    # Find the installment price element
    installment_price_element = soup.select_one('div.jss311')  # Adjusted selector for installment price
    installment_price = None
    if installment_price_element:
        installment_price_text = installment_price_element.text.strip()
        # Extract the numeric value after 'R$'
        match = re.search(r'R\$\s*([\d,\.]+)', installment_price_text)
        if match:
            installment_price = match.group(1).replace('.', '').replace(',', '.')

    return {
        'component': component,
        'cash_price': cash_price,
        'installment_price': installment_price
    }

def get_data_from_amazon(link):
    # Make a GET request to the link
    response = requests.get(link)

    # Parse the HTML of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the component text
    component_element = soup.select_one('span#productTitle')
    component = component_element.text.strip() if component_element else None
    
    # Find the cash price element
    cash_price_element = soup.select_one('span.a-price span.a-offscreen')
    cash_price = None
    if cash_price_element:
        cash_price_text = cash_price_element.text.strip()
        # Extract the numeric value after 'R$'
        match = re.search(r'R\$\s*([\d,\.]+)', cash_price_text)
        if match:
            cash_price = match.group(1).replace('.', '').replace(',', '.')

    # Find the installment price element
    installment_price_element = soup.select_one('span.best-offer-name.a-text-bold')
    installment_price = None
    if installment_price_element:
        installment_price_text = installment_price_element.text.strip()
        # Extract the numeric value after 'R$'
        match = re.search(r'R\$\s*([\d,\.]+)', installment_price_text)
        if match:
            installment_price = match.group(1).replace('.', '').replace(',', '.')

    return {
        'component': component,
        'cash_price': cash_price,
        'installment_price': installment_price
    }