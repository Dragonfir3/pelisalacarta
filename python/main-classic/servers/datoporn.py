# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para datoporn
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# ------------------------------------------------------------

import re

from core import logger
from core import scrapertools
from lib import jsunpack


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    if 'FILE NOT FOUND' in data:
        return False, "[Datoporn] El archivo no existe o ha sido borrado"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    data = scrapertools.cache_page(page_url)

    media_urls = scrapertools.find_multiple_matches(data, 'file\:"([^"]+\.mp4)",label:"([^"]+)"')
    if not media_urls:
        match = scrapertools.find_single_match(data, "<script type='text/javascript'>(.*?)</script>")
        data = jsunpack.unpack(match)
        media_urls = scrapertools.find_multiple_matches(data, '\[\{file\:"([^"]+)"')

    # Extrae la URL
    video_urls = []
    for media_url in sorted(media_urls, key=lambda x: int(x[1])):
        video_urls.append(["." + media_url[0].rsplit('.', 1)[1] + " " + media_url[1] + "p [datoporn]", media_url[0]])

    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos = 'datoporn.com/(?:embed-|)([A-z0-9]+)'
    logger.info("#" + patronvideos + "#")
    matches = re.compile(patronvideos, re.DOTALL).findall(data)

    for match in matches:
        titulo = "[datoporn]"
        url = "http://datoporn.com/embed-%s.html" % match
        if url not in encontrados:
            logger.info("  url=" + url)
            devuelve.append([titulo, url, 'datoporn'])
            encontrados.add(url)
        else:
            logger.info("  url duplicada=" + url)

    return devuelve
