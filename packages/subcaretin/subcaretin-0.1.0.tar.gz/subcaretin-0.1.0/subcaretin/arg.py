import argparse

def Argumentos():
    parser = argparse.ArgumentParser(prog='subcaretin', description='descarga \
                                     subtítulos de forma manual o automática desde \
                                     Subdivx y Argenteam')
    parser.add_argument("VIDEO",
                        help="el archivo de video de referencia")
    parser.add_argument("-m", action="store_true",
                        help="activar el modo manual (desactivado por defecto)")
    parser.add_argument("-l", metavar="int", type=int,
                        help="el límite de resultados (ilimitado por defecto)")
    parser.add_argument("-p", metavar="int", type=int,
                        help="puntaje mínimo para descargar subtítulos \
                        automáticamente (3 por defecto)")
    return parser.parse_args()
