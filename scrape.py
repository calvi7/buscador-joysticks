from lxml import html
import requests
import time

page = requests.get('https://videojuegos.mercadolibre.com.ar/para-playstation-ps4-4-gamepads-joysticks/dualshock-4_PriceRange_8000-0_NoIndex_True')
tree = html.fromstring(page.content)

links = tree.xpath('//a[@class="ui-search-result__content ui-search-link"]/@href')
title = tree.xpath('//a[@class="ui-search-result__content ui-search-link"]/@title')
price = tree.xpath('//span[@class="price-tag-fraction"]/text()')

time_data = time.asctime()

amount = 10

links = links[:amount]
title = title[:amount]
price = price[:amount]

data = dict()

for i, el in enumerate(title):
    data[el] = {
                'link':links[i], 
                'precio':price[i],
                }

data = dict(filter(lambda x: 'sony' in x[0].lower(), data.items()))

def int_(s):
    return int(s.replace('.', ''))

orden = dict(sorted(data.items(), key=lambda x: int_(x[1]["precio"])))

with open('data.html', 'w') as f:
    f.write('<head>'
            '<title>Mejores Joysticks</title>'
            '<link rel=stylesheet href="styles.css">'
            '<link rel="icon" type="image/x-icon" href="js.ico">'
            '</head>'
            '<body>'
            '<div class="container">'
            '<h1 class="header">INFO </h1>'
            f'<h3> Ult Actualizacion: {time_data} </h3>')
    
    for key, value in orden.items():
        f.write('')
        f.write(f'<p>{key} - VALOR: ${value["precio"]}<a href="{value["link"]}"> IR </a> <p>')
        
    f.write('</div>')
    
    f.write('<script>'
            'alert("Opciones de Joysticks!")'
            '</script>')
    
    f.write('</body>')
    