#This function connects to the instagram API, then uses the Azure OCR API to give the user a pure reading instagram feed 

from InstagramAPI import InstagramAPI
import getpass, http, json, urllib, base64

def getImageDesc(image_url):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '***Key For Azure***',
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
timeline_posts = timeline['items']

posts=[]

for post in timeline_posts:
    try:
        posts.append({
        'username': post['user']['username'],
        'number_likes': str(post['like_count']),
        'caption': post['caption']['text'],
        'image_url': post['image_versions2']['candidates'][0]['url']
        })
    except KeyError:
        pass