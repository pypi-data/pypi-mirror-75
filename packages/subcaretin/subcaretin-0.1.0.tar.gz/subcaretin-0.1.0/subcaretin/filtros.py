import sys

# SubFiltro devuelve cinco listas. Todas son filtradas para evitar que
# subcaretin descargue archivos no deseados o perjudiciales en el modo
# automático. Al pasar por el primer filtro procede a calcular el puntaje.

# Aunque todaviía hayan varias palabras clave por agregar a ambos filtros,
# los resultados son efectivos.

filtroSubdivx = ("dvds|pack|Pack|PACK|DVDS|DVDs|partes|PARTES|Partes|cds|"
"archivos|ARCHIVOS|Archivos|tres partes|3 partes|2 partes|dos partes|CD|3 dvd|"
"2 dvd|discos|se pueden mejorar|faltan mejora|incomplet|mula |falta mejora"
"|dvd1|dvd2|cd1|cd2|CD2|CD3|CD1|DVD1|DVD2|Spa2|spa2|spa1|Spa1|SPA1|SPA2|Esp2|"
"Esp1|esp2|temporada completa|TEMPORADA COMPLETA|esp1|2 Cds|2cds|2CDs|"
"2CDS| Cds |Temporada completa|part1|part2|CDS|Parte 4|Parte 3|Parte 2")

filtroList = filtroSubdivx.split("|")

coincidencias = []
titulosFilt = []
descripcionesFilt = []
linksFilt = []
porFiltrar = []
filtrado = []


def SubFiltro(titulos, descripciones, links, sourceList, codecList, \
              audioList, resolutionList):
    # Las descripciones de Subdivx vienen en minúsuclas por defecto, pero
    # las de Argenteam no
    desLower = [objeto.lower() for objeto in descripciones]
    
    for each in range(len(titulos)):
        porFiltrar.append('%s|%s|%s'
                          % (titulos[each], desLower[each], links[each]))

    for cada in porFiltrar:
        if any(x in cada for x in filtroList):
            porFiltrar.remove(cada)

    for cada1 in range(len(porFiltrar)):
        scoreSource = 0
        scoreCodec = 0
        scoreAudio = 0
        scoreResolution = 0
        scoreTotal = 0

        if any(y in porFiltrar[cada1] for y in sourceList):
            scoreSource = 7
        if any(y in porFiltrar[cada1] for y in codecList):
            scoreCodec = 3
        if any(y in porFiltrar[cada1] for y in audioList):
            scoreAudio = 3
        if any(y in porFiltrar[cada1] for y in resolutionList):
            scoreResolution = 2

        scoreTotal = scoreSource + scoreCodec + scoreAudio + scoreResolution

        porFiltrar[cada1] = '%s|%s' % (scoreTotal, porFiltrar[cada1])

    porFiltrarSorted = sorted(porFiltrar, reverse = True)

    for cada1 in porFiltrarSorted:
        listaTemp = cada1.split("|")
        coincidencias.append(listaTemp[0])
        titulosFilt.append(listaTemp[1])
        descripcionesFilt.append(listaTemp[2])
        linksFilt.append(listaTemp[3])

    for number in range(len(titulosFilt)):
        filtrado.append('%s - %s'
                        % (titulosFilt[number], descripcionesFilt[number]))
    if not filtrado:
        print('Sin resultados\n')
        sys.exit()
    else:
        return filtrado, coincidencias, titulosFilt, descripcionesFilt, \
            linksFilt
