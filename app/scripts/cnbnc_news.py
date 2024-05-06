import requests

url = "https://cnbc.p.rapidapi.com/news/v2/list"

querystring = {"franchiseId":"19794221","count":"2"}

headers = {
	"X-RapidAPI-Key": "8df5df34a3mshd2ba01ec055ecd0p1ab946jsn738f69d603f0",
	"X-RapidAPI-Host": "cnbc.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
