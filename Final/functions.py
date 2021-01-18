from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
from textblob import TextBlob
import numpy as np

def extract_text(url):
#     Parameters
#     url : string : contains url for website
#     Return
#     text : string: contains text from url
    request = requests.get(url).text
    soup = BeautifulSoup(request, "html.parser")
    p_tags = soup.find_all('p')
    p_tags_text = [tag.get_text().strip() for tag in p_tags]
    text = ' '.join(p_tags_text)
    return text

start_string='https://news.google.com/search?q='
end_string='&hl=en-US&gl=US&ceid=US%3Aen'
def search_url(query):
#     Parameters
#     query_url : string : query
#     Return
#     query : string: contains url for search
    query=query.split()
    query='%20'.join(query)
    query_url=start_string+query+end_string
    return query_url

def full_results(query_url):
#     Parameters
#     url : string : url of query
#     Return
#     results : list: contains list of dictionaries
#     each dictionary has the keys 'url', 'title', 'image', 'time', 'publisher' with the corresponding values for that ith search result
#     (i being the index in the list)
#     this function is meant to find all of the necessary info for cards from queries
    num=10
    request = requests.get(query_url).text
    soup = BeautifulSoup(request, "html.parser")
    result_tags = soup.find_all('div', {'jslog': '93789'})
    results=[]
    special_result_tags = soup.find_all('div', {'jscontroller': 'd0DtYd'})
    for i in range(len(special_result_tags)):
        results.append({})
        for element in special_result_tags[i].contents[0].contents[0].contents[0].contents[0].contents:
                if element['class']==['tvs3Id', 'QwxBBf']:
                    results[i]['image']=element['src']
        results[i]['url']='https://news.google.com/'+special_result_tags[i].contents[0].contents[0].contents[1].contents[0]['href'].strip('./')
        results[i]['title']=special_result_tags[i].contents[0].contents[0].contents[1].contents[1].contents[0].contents[0]
        results[i]['time']=special_result_tags[i].contents[0].contents[0].contents[1].contents[3].contents[0].contents[3].contents[0]
        results[i]['publisher']=special_result_tags[i].contents[0].contents[0].contents[1].contents[3].contents[0].contents[2].contents[0]
    if len(special_result_tags)>num-1:
        return results[:num]
    for i in range(min(len(result_tags),num-len(special_result_tags))):
        j=i+len(special_result_tags)
        results.append({})
        if len(result_tags[i]['class'])==6:
            for element in result_tags[i].contents[0].contents[0].contents:
                if element['class']==['tvs3Id', 'QwxBBf']:
                    results[j]['image']=element['src']
            results[j]['url']='https://news.google.com/'+result_tags[i].contents[1].contents[0].contents[0]['href'].strip('./')
            results[j]['title']=result_tags[i].contents[1].contents[0].contents[1].contents[0].contents[0]
            results[j]['time']=result_tags[i].contents[1].contents[0].contents[3].contents[0].contents[3].contents[0]
            results[j]['publisher']=result_tags[i].contents[1].contents[0].contents[3].contents[0].contents[2].contents[0]
        if len(result_tags[i]['class'])==5:
            results[j]['image']=False
            results[j]['url']='https://news.google.com/'+result_tags[i].contents[0].contents[0].contents[0]['href'].strip('./')
            results[j]['title']=result_tags[i].contents[0].contents[0].contents[1].contents[0].contents[0]
            results[j]['time']=result_tags[i].contents[0].contents[0].contents[3].contents[0].contents[3].contents[0]
            results[j]['publisher']=result_tags[i].contents[0].contents[0].contents[3].contents[0].contents[2].contents[0]
    return results

def only_urls(query_url,num):
#     Parameters
#     url : string : url of query
#     num : int : number of article urls to harvest
#     Return
#     results : list: contains list of dictionaries
#     each dictionary has the key 'url' with the corresponding value for that ith search result (i being the index in the list)
#     this function is meant to find only the url of the article
    request = requests.get(query_url).text
    soup = BeautifulSoup(request, "html.parser")
    result_tags = soup.find_all('div', {'jslog': '93789'})
    results=[]
    special_result_tags = soup.find_all('div', {'jscontroller': 'd0DtYd'})
    for i in range(len(special_result_tags)):
        results.append({})
        results[i]['url']='https://news.google.com/'+special_result_tags[i].contents[0].contents[0].contents[1].contents[0]['href'].strip('./')
    if len(special_result_tags)>num-1:
        return results[:num]
    for i in range(min(len(result_tags),num-len(special_result_tags))):
        j=i+len(special_result_tags)
        results.append({})
        if len(result_tags[i]['class'])==6:
            results[j]['url']='https://news.google.com/'+result_tags[i].contents[1].contents[0].contents[0]['href'].strip('./')
        if len(result_tags[i]['class'])==5:
            results[j]['url']='https://news.google.com/'+result_tags[i].contents[0].contents[0].contents[0]['href'].strip('./')
    return results

def add_sentiments(results, sort):
#     Parameters
#     results : list: contains list of dictionaries
#     sort : bool: whether or not to sort by polarity
#     each dictionary has the keys 'url', 'title', 'image' with the corresponding values for that ith search result
#     (i being the index in the list)
#     Return
#     results : list: contains list of dictionaries
#     each dictionary has the keys 'url', 'title', 'image', 'polarity', 'subjectivity' with the corresponding values for that
#     ith search result (i being the index in the list)
    for i in range(len(results)):
        if 'url' in results[i].keys():
            tb=TextBlob(extract_text(results[i]['url']))
            results[i]['polarity']=np.round(((tb.polarity)+1)/2,4)
            results[i]['subjectivity']=np.round(tb.subjectivity,4)
    if sort:
        results=sorted(results, key=lambda result: result['polarity'])
    return results

countries=[
    'United States',
    'India',
    'South Africa',
    'United Kingdom',
    'Singapore',
    'Canada',
    'Australia',
    'Nigeria'

]
country_urls=[
    'https://news.google.com/topstories?hl=en-US&gl=US&ceid=US%3Aen',
    'https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en',
    'https://news.google.com/topstories?hl=en-ZA&gl=ZA&ceid=ZA:en',
    'https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en',
    'https://news.google.com/topstories?hl=en-SG&gl=SG&ceid=SG:en',
    'https://news.google.com/topstories?hl=en-CA&gl=CA&ceid=CA:en',
    'https://news.google.com/topstories?hl=en-AU&gl=AU&ceid=AU:en',
    'https://news.google.com/topstories?hl=en-NG&gl=NG&ceid=NG:en'
]