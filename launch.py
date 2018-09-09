from InstagramAPI import InstagramAPI
import getpass, http, json, urllib, base64, time

def getImageDesc(image_url):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '##### Token #####',
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
    try:
        return output['description']['captions'][0]['text']
    except:
        pass

def login():
    username = input('Username: ')
    password = getpass.getpass(prompt='Password: ')
    print("Logging in...")

    global API
    API = InstagramAPI(username,password)
    API.login()

    API.getProfileData()
    result = API.LastJson
    username = result['user']['username']

    print("Successfully logged in as: {}".format(username))

def getPosts():

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
    return posts

def printPosts(posts):
    for post in posts:
        print("\n \n ~ ~ ~ ~ ~ \n Loading Post... \n ~ ~ ~ ~ ~ \n \n")
        description = getImageDesc(post['image_url'])
        
        time.sleep(2)
        print("{0} posted a picture of {1}, it has {2} likes. \n".format(post['username'], description, post['number_likes']))
        print("Caption: \n \n{0}".format(post['caption']))
        time.sleep(0.5)

login()

printPosts(getPosts())

