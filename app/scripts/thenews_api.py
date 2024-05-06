import http.client, urllib.parse

conn = http.client.HTTPSConnection('api.thenewsapi.com')

params = urllib.parse.urlencode({
    'api_token': 'BINUOyGwmAusSoekyoPsaP6vvvJwDidu6eFwh8TC',
    'categories': 'sports',
    'limit': 3,
    })

conn.request('GET', '/v1/news/all?{}'.format(params))

res = conn.getresponse()
data = res.read()

print(data.decode('utf-8'))