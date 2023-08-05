from guessit import guessit
import sys

def Adivinar(film):
    try:
        guess = guessit(film, '-s')
    except:
        print('Error reconociendo el archivo. Prueba el modo manual')

    if (guess['type']) == 'episode':
        title = str(guess['title']).replace(" ", "+")
        season = "{:02d}".format(int(guess['season']))
        episode = "{:02d}".format(int(guess['episode']))
        source = guess.get('source', '')
        codec = guess.get('video_codec', '')
        audio = guess.get('audio_codec', '')
        resolution = guess.get('screen_size', '')
        paraBuscar = '%s+S%sE%s' % (title, season, episode)
        return paraBuscar, source, codec, audio, resolution
    else:
        paraBuscar = str(guess['title']).replace(" ", "+")
        try:
            year = guess['year']
        except:
            print('Tu video no tiene información suficiente para una búsqueda'
                  ' automática')
            sys.exit()
        source = guess.get('source', '')
        codec = guess.get('video_codec', '')
        audio = guess.get('audio_codec', '')
        resolution = guess.get('screen_size', '')
        return paraBuscar, year, source, codec, audio, resolution

def palabrasClave(source, codec, audio, resolution):
    sourceList = []
    codecList = [] 
    audioList = []
    resolutionList = [] 

    if 'Blu-ray' == source:
        sourceList = ['bluray', 'blu-ray', 'bdrip', 'bd-rip', 'brrip',
                      'br-rip', 'blu ray', 'bdrip']
    elif 'DVD' == source:
        sourceList = ['dvdrip', '.dvd.', 'dvd-r', 'ntsc', ' dvd ', ' pal ']
    elif 'Web' == source:
        sourceList = ['web-dl', 'web-rip', 'webdl', ' web ', '.web.', '.web',
                      'web.', 'webrip']    
    elif 'HDTV' == source:
        sourceList = ['hdtv', 'screen-tv']

    if 'H.264' == codec:
        codecList = ['264', 'avc']
    elif 'H.265' == codec:
        codecList = ['265', 'hevc']
    elif 'Divx' == codec:
        codecList = [' divx ', '.divx.', '-divx']
    elif 'Xvid' == codec:
        codecList = ['xvid']
    
    if 'Dolby Digital' == audio or 'Dolby Digital Plus' == audio:
        audioList = ['dolby', '.dd', '-dd', 'dd-', 'd.d', ' dd ', 'ac3']
    elif 'FLAC' == audio:
        audioList = ['flac', 'lossless']
    elif 'AAC' == audio:
        audioList = [' aac ', '.aac', 'aac.', '-aac', 'aac-']
    elif 'DTS' == audio:
        audioList = ['dts']

    if '1080p' == resolution or '720p' == resolution or '576p' == resolution:
        resolutionList = ['1080', '720', '576', '4k', '2k', 'full hd']
    elif '480p' == resolution:
        resolutionList = ['480', '360']

    return sourceList, codecList, audioList, resolutionList
