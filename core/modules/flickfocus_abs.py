from bs4 import BeautifulSoup
import requests, json


# def movie_info(link="https://flickfocus.com/movies/poor-things"):
#     result = {}
#     rspn = requests.get(link)
#     sup = BeautifulSoup(rspn.text, "html.parser")
#     info = sup.find('div', {'class':'lg:ml-4 2xl:ml-6 flex flex-col flex-grow justify-center'})
#     info1 = info.find('div', {'class':'w-full flex justify-between mt-4 lg:mt-0'})
#     result['title'] = info1.find('div', {'class':'text-xl lg:text-3xl text-gray-800 dark:text-gray-200'}).getText()
#     info2 = info1.find('div',{'class':'mt-1 flex flex-col lg:flex-row flex-wrap text-sm text-gray-500 dark:text-gray-400 gap-x-0 lg:gap-x-6'})
#     info3 = info2.find('div', {'class':'flex'})
#     info4 = info3.find_all('div')
#     result['year'] = info4[0].getText()
#     result['time'] = info4[1].getText()
#     genres_tags = info2.find_all('a')
#     genres = []
#     for gn in genres_tags:
#         genres.append(gn.getText())
#     result['genres'] = genres
#     # result['imdb'] = info1.find('a', {'title':'Go to IMDb'}).get('href')
#     result['image'] = info.find('img', {'title':'View Poster Image'}).get('src')
#     result['overview'] = info.find('div', {'class':'flex text-gray-900 dark:text-gray-200'}).getText()
#     result['release'] = info.find('div', {'class':'ml-2'}).getText()
#     subdirector = info.find('div', {'class':'mt-6 flex flex-col space-y-8 text-gray-900 dark:text-gray-200'})
#     result['director'] = subdirector.find('div', {'class':'ml-2'}).getText()
#     subcast = info.find('div', {'class':'mt-6 text-gray-900 dark:text-gray-200'})
#     subcast2 = subcast.find_all('a', {'title':'View Profile', 'class':'block font-medium text-gray-900 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-500'})
#     cast = []
#     for i in subcast2:
#         cast.append(i.getText())
#     result['cast'] = cast

#     return result


def movie_info(link="https://flickfocus.com/movies/poor-things"):
    result = {}
    rspn = requests.get(link)
    sup = BeautifulSoup(rspn.text, "html.parser")
    info = sup.find('div', {'class':'lg:ml-4 2xl:ml-6 flex flex-col flex-grow justify-center'})
    try:
        info1 = info.find('div', {'class':'w-full flex justify-between mt-4 lg:mt-0'})
        result['title'] = info1.find('div', {'class':'text-xl lg:text-3xl text-gray-800 dark:text-gray-200'}).getText()
    except:
        result['title'] = "unknown"
    
    try:
        info2 = info1.find('div',{'class':'mt-1 flex flex-col lg:flex-row flex-wrap text-sm text-gray-500 dark:text-gray-400 gap-x-0 lg:gap-x-6'})
        info3 = info2.find('div', {'class':'flex'})
        info4 = info3.find_all('div')
    except:
        try:
            info3 = info2.find('div', {'class':'flex'})
            info4 = info3.find_all('div')
        except:
            try:
                info4 = info3.find_all('div')
            except:
                pass


    try:
        result['year'] = info4[0].getText()
    except:
        try:
            result['year'] = info.find('div', {'class':'lg:hidden'})
        except:
            result['year'] = "unknown"

    try:
        result['time'] = info4[1].getText()
    except:
        result['time'] = "unknown"

    try:
        genres_tags = info2.find_all('a')
        genres = []
        for gn in genres_tags:
            genres.append(gn.getText())
        result['genres'] = genres
    except:
        result['genres'] = ["not added yet."]

    # result['imdb'] = info1.find('a', {'title':'Go to IMDb'}).get('href')

    try:
        result['image'] = info.find('img', {'title':'View Poster Image'}).get('src')
    except:
        result['image'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
    
    try:
        result['overview'] = info.find('div', {'class':'flex text-gray-900 dark:text-gray-200'}).getText()
    except:
        result['overview'] = "not added yet."
    
    try:
        result['release'] = info.find('div', {'class':'ml-2'}).getText()
    except:
        result['release'] = "not added yet."
    
    try:
        subdirector = info.find('div', {'class':'mt-6 flex flex-col space-y-8 text-gray-900 dark:text-gray-200'})
        result['director'] = subdirector.find('div', {'class':'ml-2'}).getText()
    except:
        result['director'] = "unknown"
    
    try:
        subcast = info.find('div', {'class':'mt-6 text-gray-900 dark:text-gray-200'})
        subcast2 = subcast.find_all('a', {'title':'View Profile', 'class':'block font-medium text-gray-900 dark:text-gray-200 hover:text-blue-500 dark:hover:text-blue-500'})
        cast = []
        for i in subcast2:
            cast.append(i.getText())
        result['cast'] = cast
    except:
        result['cast'] = ["not added yet."]

    return result

def Latest_Trailers(link="https://flickfocus.com/movies/explore/trailers"):
    result = []
    rspn = requests.get(link)
    sup = BeautifulSoup(rspn.text, "html.parser")
    tags = sup.find('div', {"class":"flex flex-wrap -m-2"})
    movies = tags.find_all('div', {'class':"w-1/2 lg:w-1/4 2xl:w-1/6 flex flex-col p-2"})


    for i in movies:
        moviejson = {}
        moviejson['url'] = i.find('a', {'class':'mt-2 font-medium text-sm text-gray-900 dark:text-gray-200 hover:text-blue-600 hover:underline'}).get('href')
        moviejson['title'] = i.find('a', {'class':'mt-2 font-medium text-sm text-gray-900 dark:text-gray-200 hover:text-blue-600 hover:underline'}).getText()
        moviejson['image'] = i.find('img').get('src')
        result.append(moviejson)
    
    return result

def New_Movies(link="https://flickfocus.com/movies/explore/new"):
    result = []
    rspn = requests.get(url=link)
    sup = BeautifulSoup(rspn.text, "html.parser")
    divs = sup.find('div', {'class': "flex flex-col flex-grow p-4 md:p-6"})
    movies = divs.find_all('div', {'class':'flex flex-col w-1/4 lg:w-1/8 2xl:w-1/12 p-2 relative'})

    for i in movies:
        moviejson = {}
        movie = i.find('a', {'class':'block hover:opacity-75'})
        moviejson['title'] = movie.get('title')
        moviejson['url'] = movie.get('href')
        try:
            moviejson['image'] = i.find('img').get('src')
        except:
            moviejson['image'] = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/330px-No-Image-Placeholder.svg.png"
        result.append(moviejson)
    
    return result
