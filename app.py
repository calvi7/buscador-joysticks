from flask import Flask, render_template, request
from lxml import html
import requests
import time
import os

app = Flask(__name__)

app.static_folder = 'static'

port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port, debug=True)

@app.route('/')
def hello():
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

    page_data = [(f"{key} - {value['precio']}", value["link"]) for key, value in orden.items()]

    return render_template('index.html', time_data=time_data, page_data=page_data)
