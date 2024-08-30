import requests
import bot_config
import json
from bs4 import BeautifulSoup


def get_response(user_input,user,logger):
    lowered = user_input.lower()
    if lowered == "test":
        return f"Hey im a bot made for suffering {user}"
    elif lowered == "test noe":
        return "te amo mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho mucho"
    elif lowered == "test rodri":
        return f"El bosque te espera {user}"
    elif lowered == "test roo":
        return f"No me olvide de vos tampoco {user}"
    elif lowered == "soy un puto genio":
        return f"No te la creas tanto {user}"
    elif lowered == "tuki":
        return f"deja de hacerte el boludo {user}"
    elif "help" in lowered:
        return f"Para Buscar una carta: \n!encontrame tucarta \n Para que la respuesta sea privada:\n?encontrame tucarta"
    elif "encontrame" in lowered:
        lowered = lowered.replace("encontrame", "")
        lowered = lowered.strip()
        return f"\nBuscaste:{lowered}\n----Pirulo: \n{get_cards_pirulo(lowered,logger)}\n ----Lair:\n{get_cards_lair(lowered,logger)}\n ----Dealers:\n{get_cards_dealers(lowered,logger)}\n ----Batikueva:\n{get_cards_batikueva(lowered,logger)}"
        
def get_cards_batikueva(input,logger):
    
    url = f"https://www.labatikuevastore.com/search/?q={input}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        logger.info(soup)
        for item in soup.find_all('div', class_="js-product-container js-quickshop-container position-relative js-quickshop-has-variants"): 
            #aria-label
            data_variants = item.get('data-variants')
            variants_list = json.loads(data_variants)
            img_tag = item.find('img', class_='js-item-image')
            titulo = img_tag.get('alt')
            logger.info(titulo)
            if str(titulo).lower() != input:
                continue
            for variant in variants_list:
                if int(variant.get('stock')) != 0:
                    card_list.append({
                        'titulo': titulo,
                        "variante":variant.get('option2'),
                        'precio': variant.get('price_short')
                    })
        logger.info(card_list)

        formatted_list = []
        for i, card in enumerate(card_list):
            if i >= 6:  
                break
            titulo = card.get('titulo', '')
            variante = card.get('variante', '')
            precio = card.get('precio', '')
            formatted_list.append(f"{titulo}// {variante} // {precio} pesitos crocantes")

        if len(card_list) < 6:
            extra= "\n----------------Disfrute-----------------"
        else:    
            extra = "\n---------Hay mas pero hay limite de caracteres-----------"

        # Join the formatted items into a single string (optional)
        formatted_string = "\n".join(formatted_list)    
        return formatted_string +f"{extra}" if formatted_string else "No hay resultados con stock En Batikueva"
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    
def get_cards_dealers(input,logger):
    
    url = f"https://www.magicdealersstore.com/products/search?q={input}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_="variant-row in-stock"): 
            if item.find("div",class_="product-price"):
                continue
            form = item.find('form', class_='add-to-cart-form')

            
            data_name = form.get('data-name')
            logger.info(input)
            logger.info(str(data_name).lower())
            if str(data_name).lower() != input:
                continue
            data_category = form.get('data-category')
            data_price = form.get('data-price')
            data_variant = form.get('data-variant')
    
            card_list.append({
                'titulo': data_name,
                "variante":data_category + "-" + data_variant,
                'precio': data_price
            })
        logger.info(card_list)

        formatted_list = []
        for i, card in enumerate(card_list):
            if i >= 6:  
                break
            titulo = card.get('titulo', '')
            variante = card.get('variante', '')
            precio = card.get('precio', '')
            formatted_list.append(f"{titulo}// {variante} // {precio} Patacones")

        if len(card_list) < 6:
            extra= "\n----------------Disfrute-----------------"
        else:    
            extra = "\n---------Hay mas pero hay limite de caracteres-----------"

        # Join the formatted items into a single string (optional)
        formatted_string = "\n".join(formatted_list)    
        # return formatted_string if formatted_string else "No hay resultados con stock En pirulo"
        return formatted_string +f"{extra}" if formatted_string else "No hay resultados con stock En Dealers"
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None

def get_cards_pirulo(input,logger):
    
    url = f"https://www.mtgpirulo.com/products/search?q={input}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_="variant-row in-stock"): 
            form = item.find('form', class_='add-to-cart-form')

            
            data_name = form.get('data-name')
            logger.info(input)
            logger.info(str(data_name).lower())
            if str(data_name).lower() != input:
                continue
            data_category = form.get('data-category')
            data_price = form.get('data-price')
            data_variant = form.get('data-variant')
    
            card_list.append({
                'titulo': data_name,
                "variante":data_category + "-" + data_variant,
                'precio': data_price
            })
        logger.info(card_list)

        formatted_list = []
        for i, card in enumerate(card_list):
            if i >= 6:  
                break
            titulo = card.get('titulo', '')
            variante = card.get('variante', '')
            precio = card.get('precio', '')
            formatted_list.append(f"{titulo}// {variante} // {precio} dolarucos")

        if len(card_list) < 6:
            extra= "\n----------------Disfrute-----------------"
        else:    
            extra = "\n---------Hay mas pero hay limite de caracteres-----------"    

        # Join the formatted items into a single string (optional)
        formatted_string = "\n".join(formatted_list)    
        # return formatted_string if formatted_string else "No hay resultados con stock En pirulo"
        return formatted_string +f"{extra}" if formatted_string else "No hay resultados con stock En pirulo"
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    

def get_cards_lair(input,logger):
    
    url = f"https://www.magiclair.com.ar/search?q={input}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        #logger.info(soup)
        for item in soup.find_all('div', class_='productCard__card'):
            
            no_stock = item.find("div", class_="productCard__button productCard__button--outOfStock" )
            product_type = item.get("data-producttype")
            logger.error(product_type)
            if no_stock or product_type != "MTG Single":
                continue

            titulo = item.find('p', class_='productCard__setName').text.strip()
            precio = item.find('p', class_='productCard__price').text.strip()
   
            logger.error(titulo)
            logger.error(precio)
            card_list.append({
                'titulo': input + "-" +titulo,
                'precio': precio,
            })
        logger.info(card_list)

        formatted_list = []
        for i, card in enumerate(card_list):
            if i >= 6:  
                break
            titulo = card.get('titulo', '')
            precio = card.get('precio', '')
            formatted_list.append(f"{titulo} // {precio}")

        if len(card_list) < 6:
            extra= "\n----------------Disfrute-----------------"
        else:    
            extra = "\n---------Hay mas pero hay limite de caracteres-----------"    

        # Join the formatted items into a single string (optional)
        formatted_string = "\n".join(formatted_list)    
        return formatted_string +f"{extra}" if formatted_string else "No hay resultados con stock En lair"
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None        