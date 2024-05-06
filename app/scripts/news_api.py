import requests
import json

url = "https://newsnow.p.rapidapi.com/newsv2"

headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "90a9e29896mshc06e1816b7d9b53p143ee5jsn04550eb886b8",
	"X-RapidAPI-Host": "newsnow.p.rapidapi.com"
}

transformed_news = []
with open('data4.json', 'w') as file:
    for i in range(1, 100):
        payload = {
        "query": "sports",    
        "time_bounded": True,
        "from_date": "01/02/2022",
        "to_date": "05/06/2022",
        "location": "us",
        "language": "en",
        "page": i
        }
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        news = data['news']
        for article in news:
            news_object = {
                'title': article['title'],
                'description': article['short_description'],
                'url': article['url'],
                'source': article['publisher']['title'],
                'published_at': article['date'],
                'scraped_at': article['date']
            }

            transformed_news.append(news_object)
        
    json.dump(transformed_news, file, indent=4)


# import json


# with open('data2.json', 'r') as file:
#     data = json.load(file)
#     news = data['news']
#     transformed_news = []
#     for article in news:
#         news_object = {
#             'title': article['title'],
#             'description': article['short_description'],
#             'url': article['url'],
#             'source': article['publisher']['title'],
#             'published_at': article['date'],
#             'scraped_at': article['date']
#         }

#         transformed_news.append(news_object)

# with open('data3.json', 'w') as new_file:
#     json.dump(transformed_news, new_file, indent=4)


