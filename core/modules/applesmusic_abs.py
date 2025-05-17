from bs4 import BeautifulSoup
import requests, json

ex = "https://music.apple.com/us/room/1532310781"

def room_extractor(link=ex):
    result = []
    rspn = requests.get(link)
    sup = BeautifulSoup(rspn.text, "html.parser")
    items = sup.find('script',{"id":"serialized-server-data"})
    our_json = json.loads(items.text)[0]

    items = (our_json['data']['sections'][0]['items'])

    for i in items:
        song = i['title']
        artist = i['artistName']
        artwork = i['artwork']['dictionary']['url']
        # artist_url = i['subtitleLinks'][0]['segue']['destination']['contentDescriptor']['url']
        thumb = artwork.replace("{w}x{h}{c}.{f}", f"630x630bb.jpg")
        midd = artwork.replace("{w}x{h}{c}.{f}", f"120x120bb.jpg")
        artwork = artwork.replace("{w}x{h}{c}.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
        song_url = i['tertiaryLinks'][0]['segue']['destination']['contentDescriptor']['url']
        result.append({'title':song, 'artist':artist, 'thumb':thumb, 'url':song_url, 'artwork':artwork, 'midd':midd})
    
    return result



exx = "https://music.apple.com/us/playlist/new-music-daily/pl.2b0e6e332fdf4b7a91164da3162127b5"
def playlist_extractor(link=exx):
    result = []
    rspn = requests.get(link)
    sup = BeautifulSoup(rspn.text, "html.parser")
    items = sup.find('script',{"id":"serialized-server-data"})

    our_json = json.loads(items.text)

    items = (our_json[0]['data']['sections'][1]['items'])

    for i in items:
        song = i['title']
        artist = i['artistName']
        artwork = i['artwork']['dictionary']['url']
        # artist_url = i['subtitleLinks'][0]['segue']['destination']['contentDescriptor']['url']
        thumb = artwork.replace("{w}x{h}bb.{f}", f"630x630bb.jpg")
        midd = artwork.replace("{w}x{h}bb.{f}", f"120x120bb.jpg")
        artwork = artwork.replace("{w}x{h}bb.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
        song_url = i['tertiaryLinks'][0]['segue']['destination']['contentDescriptor']['url']
        result.append({'title':song, 'artist':artist, 'thumb':thumb, 'url':song_url, 'artwork':artwork, 'midd':midd})
    
    return result

def search(keyword):
    result = {}
    link = "https://music.apple.com/us/search?term="+keyword
    # print(link)
    rspn = requests.get(link)
    soup = BeautifulSoup(rspn.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})

    our_json = json.loads(items.text)

    index=0
    for i in our_json[0]['data']['sections']:
        if "artist" in i['id']:
            artistindex = index
        elif "album" in i['id']:
            albumindex = index
        elif "song" in i['id']:
            songindex = index
        elif "playlist" in i['id']:
            playlistindex = index
        elif "music_video" in i['id']:
            music_videoindex = index
        index+=1
    # print(artistindex, albumindex, songindex, playlistindex, music_videoindex)

    try:
        artists = (our_json[0]['data']['sections'][artistindex]['items'])
        lst0 = []
        for i in artists:
            artist = i['title']
            try:
                artwork = i['artwork']['dictionary']['url']
                thumb = artwork.replace("{w}x{h}bb.{f}", f"630x630bb.jpg")
                midd = artwork.replace("{w}x{h}bb.{f}", f"120x120bb.jpg")
                artwork = artwork.replace("{w}x{h}bb.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
            except:
                artwork="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
                thumb,midd = artwork,artwork
            url = i['contentDescriptor']['url']
            lst0.append({'title':artist, 'thumb':thumb, 'url':url, 'artwork':artwork, 'midd':midd})
        result['artists'] = lst0
    except Exception as e:
        print("musics/search/artists/error:\n"+str(e))
        result['artists'] = [{'title':"not found", 'thumb':"", 'url':"not found", 'artwork':"", 'midd':""}]



    try:
        albums = (our_json[0]['data']['sections'][albumindex]['items'])
        lst1 = []
        for i in albums:
            song = i['titleLinks'][0]['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                artwork = i['artwork']['dictionary']['url']
                thumb = artwork.replace("{w}x{h}bb.{f}", f"630x630bb.jpg")
                midd = artwork.replace("{w}x{h}bb.{f}", f"120x120bb.jpg")
                artwork = artwork.replace("{w}x{h}bb.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
            except:
                artwork="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
                thumb,midd = artwork,artwork
            url = i['contentDescriptor']['url']
            lst1.append({'title':song, 'artist':artist, 'thumb':thumb, 'url':url, 'artwork':artwork, 'midd':midd})
        result['albums'] = lst1
    except Exception as e:
        print("musics/search/albums/error:\n"+str(e))
        result['albums'] = [{'title':"not found", 'artist':'not found', 'thumb':"", 'url':"not found", 'artwork':"", 'midd':""}]


    try:
        songs = (our_json[0]['data']['sections'][songindex]['items'])
        lst2 = []
        for i in songs:
            song = i['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                artwork = i['artwork']['dictionary']['url']
                thumb = artwork.replace("{w}x{h}bb.{f}", f"630x630bb.jpg")
                midd = artwork.replace("{w}x{h}bb.{f}", f"120x120bb.jpg")
                artwork = artwork.replace("{w}x{h}bb.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
            except:
                artwork="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
                thumb,midd = artwork,artwork
            url = i['contentDescriptor']['url']
            lst2.append({'title':song, 'artist':artist, 'thumb':thumb, 'url':url, 'artwork':artwork, 'midd':midd})
        result['songs'] = lst2
    except Exception as e:
        print("musics/search/songs/error:\n"+str(e))
        result['songs'] = [{'title':"not found", 'artist':'not found', 'thumb':"", 'url':"not found", 'artwork':"", 'midd':""}]



    try:
        playlists = (our_json[0]['data']['sections'][playlistindex]['items'])
        lst3 = []
        for i in playlists:
            song = i['titleLinks'][0]['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                artwork = i['artwork']['dictionary']['url']
                thumb = artwork.replace("{w}x{h}bb.{f}", f"630x630bb.jpg")
                midd = artwork.replace("{w}x{h}bb.{f}", f"120x120bb.jpg")
                artwork = artwork.replace("{w}x{h}bb.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
            except:
                artwork="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
                thumb,midd = artwork,artwork
            url = i['contentDescriptor']['url']
            lst3.append({'title':song, 'artist':artist, 'thumb':thumb, 'url':url, 'artwork':artwork, 'midd':midd})
        result['playlists'] = lst3
    except Exception as e:
        print("musics/search/playlists/error:\n"+str(e))
        result['playlists'] = [{'title':"not found", 'artist':'not found', 'thumb':"", 'url':"not found", 'artwork':"", 'midd':""}]


    try:
        musicvideos = (our_json[0]['data']['sections'][music_videoindex]['items'])
        lst4 = []
        for i in musicvideos:
            song = i['titleLinks'][0]['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                artwork = i['artwork']['dictionary']['url']
                thumb = artwork.replace("{w}x{h}bb.{f}", f"630x630bb.jpg")
                midd = artwork.replace("{w}x{h}bb.{f}", f"120x120bb.jpg")
                artwork = artwork.replace("{w}x{h}bb.{f}", f"{i['artwork']['dictionary']['width']}x{i['artwork']['dictionary']['height']}bb.jpg")
            except:
                artwork="https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
                thumb,midd = artwork,artwork
            url = i['contentDescriptor']['url']
            lst4.append({'title':song, 'artist':artist, 'thumb':thumb, 'url':url, 'artwork':artwork, 'midd':midd})
        result['musicvideos'] = lst4
    except Exception as e:
        print("musics/search/musicvideos/error:\n"+str(e))
        result['musicvideos'] = [{'title':"not found", 'artist':'not found', 'thumb':"", 'url':"not found", 'artwork':"", 'midd':""}]
    
    return result


