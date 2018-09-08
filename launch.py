#This function connects to the instagram API, then uses the Azure OCR API to give the user a pure reading instagram feed
#https://medium.com/@dvoiak.stepan/https-medium-com-dvoiak-stepan-instagram-analitics-with-unofficial-api-ipython-and-matplotlib-a9f3f8b2b16a
#https://github.com/billcccheng/instagram-terminal-news-feed/blob/master/start.py
#https://www.kdnuggets.com/2017/08/instagram-python-data-analysis.html


from InstagramAPI import InstagramAPI
import getpass, http, json, urllib, base64

def getImageDesc(image_url):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': 'f78d91e88f874eb5b43fffcf43070467',
    }

    params = urllib.parse.urlencode({
    # Request parameters
    'visualFeatures': 'Description, Adult',
    'language': 'en',
    })   
   
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')

    conn.request("POST", "/vision/v1.0/analyze?{}".format(params), "{{'url':'{0}'}}".format(image_url), headers)
    response = conn.getresponse()
    data = response.read()
    output = json.loads(data)
    conn.close()
    return output



username = input('Username: ')
password = getpass.getpass(prompt='Password: ')
print("Logging in...")

API = InstagramAPI(username,password)
API.login()

API.getProfileData()
result = API.LastJson

username = result['user']['username']

print("Successfully logged in as: {}".format(username))

API.timelineFeed()
timeline = API.LastJson
print("Variable timeline is of type {}".format(type(timeline)))
timelinePosts = timeline['items']

print("Variable timelinePosts is type: {}".format(type(timelinePosts)))
print(timelinePosts)
posting_users=[]

for post in timelinePosts:
    posting_users.append(post['taken_at'])

print(posting_users)
print(len(posting_users))


