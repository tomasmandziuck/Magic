import requests
import bot_config
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
    elif "encontrame:" in lowered:
        lowered = lowered.replace("encontrame:", "")
        return get_cards_pirulo(lowered,logger)



def get_cards_pirulo(input,logger):
    
    url = f"https://www.magiclair.com.ar/search?q={input}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        logger.info(soup)
        # for item in soup.find_all('div', class_='productCard__card'):
        #     no_stock = item.find("div", class_="productCard__button productCard__button--outOfStock" )
        #     if no_stock:
        #       continue   
        #     titulo = item.find('p', class_='productCard__setName').text.strip()
        #     precio = item.find('p', class_='productCard__price').text.strip()
    
        #     card_list.append({
        #         'titulo': input + "-" +titulo,
        #         'precio': precio,
        #     })
        # logger.info(card_list)

        # formatted_list = []
        # for i in range(0, len(card_list), 2):
        #     titulo = card_list[i+1].get('titulo', '')
        #     precio = card_list[i+1].get('precio', '')
        #     formatted_list.append(f"{titulo} // {precio}")

        # # Join the formatted items into a single string (optional)
        # formatted_string = "\n".join(formatted_list)    
        # return formatted_string if formatted_string else "No hay resultados con stock En pirulo"
        return "todavia no termine con esto"
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None
    

def get_cards_lair(input,logger,stock=False):
    
    url = f"https://www.magiclair.com.ar/search?q={input}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
         #Aquí deberás identificar la estructura de la página HTML y extraer los datos
        card_list=[]
        logger.info(soup)
        for item in soup.find_all('div', class_='productCard__card'):
            no_stock = item.find("div", class_="productCard__button productCard__button--outOfStock" )
            if no_stock:
              continue   
            titulo = item.find('p', class_='productCard__setName').text.strip()
            precio = item.find('p', class_='productCard__price').text.strip()
    
            card_list.append({
                'titulo': input + "-" +titulo,
                'precio': precio,
            })
        logger.info(card_list)

        formatted_list = []
        for i in range(0, len(card_list), 2):
            titulo = card_list[i+1].get('titulo', '')
            precio = card_list[i+1].get('precio', '')
            formatted_list.append(f"{titulo} // {precio}")

        # Join the formatted items into a single string (optional)
        formatted_string = "\n".join(formatted_list)    
        return formatted_string if formatted_string else "No hay resultados con stock En lair"
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None        