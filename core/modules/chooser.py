from .applesmusic_abs import playlist_extractor
from .flickfocus_abs import New_Movies
from .digi_abs import get_new_offers

def choose(tag):
    if tag == "movie":
        result = New_Movies()
        result_json = []
        for i in result:
            content = {
                'title':i['title'],
                'image_url':i['image'],
                'desc':"",
                'url':i['url']
            }
            result_json.append(content)
        return result_json
    
    elif tag == "music":
        result = playlist_extractor()
        result_json = []
        for i in result:
            content = {
                'title':i['title'],
                'image_url':i['thumb'],
                'desc':i['artist'],
                'url':i['url']
            }
            result_json.append(content)
        return result_json

    elif tag == "digikala":
        result = get_new_offers()
        result_json = []
        for i in result:
            content = {
                'title':i['title_fa'],
                'image_url':i['images']['main']['url'][0],
                'desc': str(str(i['default_variant']['price']['selling_price'])[:-1]+"t"),
                'url':str("https://www.digikala.com/"+i['url']['uri'])
            }
            result_json.append(content)
        return result_json
