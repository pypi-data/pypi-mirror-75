# subcaretin

`subcaretin` ofrece la forma más efectiva de descargar automáticamente subtítulos en español. Busca, descarga, extrae y renombra subtítulos de Subdivx y Argenteam.

## Características

Ambos modos obtienen subtítulos de Subdivx y Argenteam. Cada modo opera así:

### Automático

* Incorpora el excelente reconocimiento de metadatos de vídeo por parte de [guessit](https://github.com/guessit-io/guessit)
* Utiliza un algoritmo simple para ordenar de mejor a peor los resultados de acuerdo a los datos obtenidos por guessit
* Descarga el mejor subtítulo disponible
* Renombra el subtítulo descargado de acuerdo al nombre del archivo de vídeo introducido

El cálculo de puntajes está inspirado en subliminal. En orden de importancia, cuenta los puntos de esta forma:

* Source (Bluray, DVD, WEB, etc): 7 puntos
* Codec de vídeo (x264, x265, etc): 3 puntos
* Codec de audio (aac, flac, etc): 3 puntos
* Resolución (480p, 720p, etc): 2 puntos

### Manual

* El modo manual espera la interacción del usuario/usuaria en la búsqueda, la elección del subtítulo a descargar y la elección del archivo a extraer
 
## Alistar uso
Primero, instala las dependencias con pip:
```
pip3 install requests guessit beautifulsoup4 unrar python-magic --user
```
Luego, instala `subcaretin` a través de pip:
```
pip3 install subcaretin --user
```
O, para instalarlo manualmente:
```
git clone https://github.com/vitiko98/subcaretin.git
cd subcaretin
pip3 install -r requirements.txt
python3 setup.py install --user
```
Ahora, `subcaretin` está listo
## Uso
```
Uso: subcaretin [-h] [-m] [-l int] [-p int] [-f] VIDEO

descarga subtítulos de forma automática o manual desde Subdivx y Argenteam

Ejemplos:
subcaretin Taxi.Driver.1976.Bluray.x264.mkv
subcaretin -m -l 5 Taxi.Driver.1976.Bluray.x264.mkv

Argumento posicional obligatorio:
  VIDEO       el archivo de video de referencia

Argumentos opcionales:
  -h, --help  mostrar este mensaje cerrar
  -m          activar el modo manual (desactivado por defecto)
  -l int      el límite de resultados (ilimitado por defecto)
  -p int      puntaje mínimo para descargar subtítulos automáticamente (3 por defecto)
  -f          de existir, sobreescribir subtítulo descargado
```
## Ejemplo del modo automático
```console
[victor@arch]$ subcaretin True.Detective.S01E01.WEB.x264.720p.AAC.mkv
Buscando mejor subtítulo...
Bajando:
Subtitulos de True Detective S01E01 [(...) s01e01 the long bright dark 1080p amzn web-dl dd 5 1 h 265-sigma]
Puntaje: 9
Subtítulo descargado correctamente: True.Detective.S01E01.WEB.x264.720p.AAC.es.srt
```
## Ejemplo del modo manual
```console
[victor@arch]$ subcaretin -m -l 9 Taxi.Driver.1976.Bluray.x264.mkv

Introduce el nombre de la película y su año:
- Taxi Driver 1976

Buscando subtítulos...
0: [Argenteam] Taxi Driver (1976) - Taxi.Driver.%281976%29.DVDRip.DivX-NoGRP
1: [Argenteam] Taxi Driver (1976) - Taxi.Driver.%281976%29.DVDRip.XviD.AC3-Taitongtan
2: [Argenteam] Taxi Driver (1976) - Taxi.Driver.%281976%29.BDRip.x264.720p.DTS-AMIABLE
3: [Argenteam] Taxi Driver (1976) - Taxi.Driver.%281976%29.BDRip.x264.1080p.DTS-AMIABLE
4: Subtitulos de Taxi Driver (1976) - son para la nueva versión taxi driver 1976 1080p  x264-amiable  tome los que subió jfca283 (leanlestat) "taxi driver 1976 720p  dts x264 ebp" y los resincronicé  espero les sirva
5: Subtitulos de Taxi Driver (1976) - sirve para taxi driver [bdrip-1080p-multilang-multisub-chapters][rip by max]
6: Subtitulos de Taxi Driver (1976) - para la version de "zeus diaz" que ocupa 700 mb
7: Subtitulos de Taxi Driver (1976) - a este lo bake del donkey, esta coordinado con la version que tewngo de 706 3 mb que comienza directamente con los titulos de la columbia, aparte estan corregidas las letras z que aparecian el algunas partes remplazando a la a, a diferencia de las demas e
8: Subtitulos de Taxi Driver (1976) - son los de leanlestat  ajustados para "taxi driver 1976 720p  dts x264 ebp"
(...)

Elige el número a descargar:
- 3

Bajando: [Argenteam] Taxi Driver (1976) Taxi.Driver.%281976%29.BDRip.x264.1080p.DTS-AMIABLE

Archivos a extraer:
0: ['Taxi.Driver.1976.1080p.BluRay.X264-AMIABLE.srt']

Elige el número del archivo a extraer:
- 0

Subtítulo descargado correctamente: Taxi.Driver.1976.Bluray.x264.es.srt
```
## Eficacia
`subcaretin` tiene una serie de filtros específicamente optimizados para las búsquedas en Argenteam y Subdivx, por lo que apunta a ser más eficaz que aplicaciones similares de subtítulos.
## TODO
* Mejorar los filtros
* Descargar por carpetas
* Corregir el estilo del código
* Mejorar el manejo de errores
## Miscelánea
* Para mejorar la compatibilidad, este script fue reescrito en Python a partir del 25 de Julio de 2020. Anteriormente fue un bash script. Puedes encontrar la versión obsoleta en las branches
* Mi subdivx: https://www.subdivx.com/X9X2117299
