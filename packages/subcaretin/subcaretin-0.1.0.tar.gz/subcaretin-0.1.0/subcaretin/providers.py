import requests
import json
import sys
from bs4 import BeautifulSoup as bso

api_search = "http://argenteam.net/api/v1/search"
api_episode = "http://argenteam.net/api/v1/episode"
api_movie = "http://argenteam.net/api/v1/movie"

titulos = []
descripciones = []
links = []
total = []


def subdivx(movie):
    core = 'http://www.subdivx.com/index.php?q='
    subdivx = '%s%s&accion=5&masdesc=&subtitulos=1&realiza_b=1' % (core, movie)
    page = requests.get(subdivx)
    soup = bso(page.content, 'html.parser')

    for titulo in soup.find_all(id='menu_titulo_buscador'):
        titulos.append(titulo.text)

    for descripcion in soup.find_all(id='buscador_detalle_sub'):
        descripciones.append(descripcion.text)

    for a in soup.find_all('a', class_='titulo_menu_izq'):
        links.append(a.get('href'))


def argenteam(movie):
    argenteam_search = '%s?q=%s' % (api_search, movie)
    page = requests.get(argenteam_search)
    soup = bso(page.content, 'html.parser')
    arg_json = json.loads(soup.text)

    def get_arg_links(moviePag):
        moviePag = requests.get('%s?id=%s' % (api_movie, arg_id))
        movieSop = bso(moviePag.content, 'html.parser')
        movieJson = json.loads(movieSop.text)
        movieTitle = movieJson['title']
        try:
            for rele in movieJson['releases']:
                if rele['subtitles']:
                    for uri in rele['subtitles']:
                        titulos.append('[Argenteam] %s' % (movieTitle))
                        links.append(uri['uri'])
                        descripciones.append(uri['uri'].rsplit('/', 1)[-1])
        except:
            print("Sin resultados en Argenteam")

    for tipo in arg_json['results']:
        mov_o_tv = tipo['type']
        arg_id = tipo['id']
        if mov_o_tv == 'movie':
            moviePag = requests.get('%s?id=%s' % (api_movie, arg_id))
            get_arg_links(moviePag)
        else:
            moviePag = requests.get('%s?id=%s' % (api_episode, arg_id))
            get_arg_links(moviePag)


def arg_subd(movie):
    argenteam(movie)
    subdivx(movie)
    limite = len(titulos)
    for number in range(limite):
        total.append('%s: %s - %s' %
                     (number, titulos[number], descripciones[number]))
    if not total:
        print('Sin resultados\n')
        sys.exit()
    else:
        return total, titulos, descripciones, links
