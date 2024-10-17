import requests
import bot_config
import json
import re
from bs4 import BeautifulSoup


def get_response(user_input,user,command,logger):
    lowered = user_input.lower()
    responses= []
    if lowered in bot_config.CUSTOM_RESPONSES:
        responses.append(bot_config.CUSTOM_RESPONSES[lowered].format(user))
        return responses
    elif "help" in command:
        responses.append(f"Para Buscar una carta:\n!find tucarta\nPara que la respuesta sea privada:\n?find tucarta\nPara buscar por lista de cartas:\nSeparar nombre de cartas con ;")
        return responses
    elif "find" in command:
        lowered = lowered.replace("find", "").strip()
        responses.append(f"Pediste: {lowered}\n")
        responses = get_cards_pirulo(lowered,responses,logger)
        logger.info(responses)
        responses = get_cards_lair(lowered,responses,logger)
        logger.info(responses)
        responses = get_cards_dealers(lowered,responses,logger)
        logger.info(responses)
        responses = get_cards_batikueva(lowered,responses,logger)
        logger.info(responses)
        return responses
    else:
        responses.append("Pegale a las teclas capoeira")
        return responses     
        
def get_cards_batikueva(input,responses,logger):
    logger.info(type(responses))
    url = bot_config.STORE_URL["batikueva"].format(input)
    headers = bot_config.HEADERS
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_="js-product-container js-quickshop-container position-relative js-quickshop-has-variants"): 
            
            data_variants = item.get('data-variants')
            variants_list = json.loads(data_variants)
            img_tag = item.find('img', class_='js-item-image')
            titulo = img_tag.get('alt')
            a_tag = soup.find('a', {'aria-label': titulo})
            link = a_tag['href']

            if not input in str(titulo).lower():
                continue
            for variant in variants_list:
                if int(variant.get('stock')) != 0:
                    card_list.append({
                        'titulo': titulo,
                        "variante":variant.get('option2'),
                        'precio': variant.get('price_short'),
                        "link":f"[link](<{link}>)"
                    })
        logger.info(card_list)

        formatted_string = format_list(card_list,"Batikueva")
        
        responses.append(formatted_string) 
        
        return responses
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    
def get_cards_dealers(input,responses,logger):
    logger.info(type(responses))
    url = bot_config.STORE_URL["dealers"].format(input)
    headers = bot_config.HEADERS
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_="meta"):
            if item.find('div', class_="variant-row in-stock"):
                form = item.find('form', class_='add-to-cart-form')

                data_name = form.get('data-name')
    
                if not input in str(data_name).lower():
                    continue
                data_category = form.get('data-category')
                data_price = form.get('data-price')
                data_variant = form.get('data-variant')
                link = item.find('a')['href']
                card_list.append({
                    'titulo': data_name,
                    "variante":data_category + "-" + data_variant,
                    'precio': data_price,
                    "link": f"[link](<https://www.magicdealersstore.com{link}>)"
                })
        logger.info(card_list)

        formatted_string = format_list(card_list,"Dealers")
        
        responses.append(formatted_string) 
        
        return responses
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None

def get_cards_pirulo(input,responses,logger):
    logger.info(type(responses))
    logger.info(responses)
    url = bot_config.STORE_URL["pirulo"].format(input)
    headers = bot_config.HEADERS
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_="meta"):
            if item.find('div', class_="variant-row in-stock"): 
                form = item.find('form', class_='add-to-cart-form')

                
                data_name = form.get('data-name')

                if not input in str(data_name).lower():
                    continue
                data_category = form.get('data-category')
                data_price = form.get('data-price')
                data_variant = form.get('data-variant')
                link = item.find('a')['href']
                card_list.append({
                    'titulo': data_name,
                    "variante":data_category + "-" + data_variant,
                    'precio': data_price,
                    "link": f"[link](<https://www.mtgpirulo.com{link}>)"
                })
        logger.info(card_list)

        formatted_string = format_list(card_list,"Pirulo")

        responses.append(formatted_string) 
        
        return responses 
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    

def get_cards_lair(input,responses,logger):
    logger.info(type(responses))
    url = bot_config.STORE_URL["lair"].format(input)
    headers = bot_config.HEADERS
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_='productCard__card'):
            
            no_stock = item.find("div", class_="productCard__button productCard__button--outOfStock" )
            product_type = item.get("data-producttype")
            #logger.error(product_type)
            if no_stock or product_type != "MTG Single":
                continue
            img_tag = item.find('img', class_='productCard__img')
            alt_text = img_tag['alt'] if img_tag else None
            # cleaned_text = re.sub(r'\s*\[.*?\]', '', alt_text)
            # if cleaned_text.lower() != input:
            #     continue
            if not input in str(alt_text).lower():
                continue
            #titulo = item.find('p', class_='productCard__setName').text.strip()
            precio = item.find('p', class_='productCard__price').text.strip()
            link_item = item.find("a", class_="productCard__a")
            link = link_item["href"]
            card_list.append({
                'titulo': alt_text,
                'precio': precio,
                "link" : f"[link](<https://www.magiclair.com.ar{link}>)" 
            })
        logger.info(card_list)

        formatted_string = format_list(card_list,store="Lair")
        
        responses.append(formatted_string) 
        
        return responses
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None

def format_list(card_list,store=None):
    formatted_list = []
    if not card_list:
        return f"{store}:\nNo hay resultados con stock"
    for i, card in enumerate(card_list[:10]):
        titulo = card.get('titulo', '')
        precio = card.get('precio', '')
        link = card.get('link', '')
        if store == "Lair":
            formatted_list.append(f"{titulo} // {precio}// {link}")
        else:
            variante = card.get('variante', '')
            formatted_list.append(f"{titulo}// {variante} // {precio} // {link}")    


    extra= "\n----------------Disfrute-----------------" if len(card_list) < 10 else "\n---------Hay mas pero hay limite de caracteres-----------"   

    formatted_string = "\n".join(formatted_list)+f"{extra}"
    formatted_string =f"{store}:\n" + formatted_string  
    return formatted_string        