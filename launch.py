from InstagramAPI import InstagramAPI
import getpass, http, json, urllib, base64, time, os

def getImageDesc(image_url):
    headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '### Subscription Key ###',
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
        return "some sort of image type thing"

def login():
    os.system('cls||clear')
    print("Please enter Instagram login credentials: \n")
    username = input('Username: ')
    password = getpass.getpass(prompt='Password: ')
    print("Logging in... \n")

    global API
    API = InstagramAPI(username,password)
    API.login()
    if API.isLoggedIn:
        pass
    else:
        print("Unable to log in, please try again: \n")
        login()

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
            'image_url': post['image_versions2']['candidates'][0]['url'],
            })
        except KeyError:
            pass
    return posts

def printPosts(posts):
    n = 0
    nextPostDesc = getImageDesc(posts[n]['image_url'])
    input("Press enter to load first post: ")
    os.system('cls||clear')

    for post in posts:   
        print("\n#########\n\n")
        
        print("{0} posted a picture of {1}, it has {2} likes. \n".format(post['username'], nextPostDesc, post['number_likes']))
        print("Caption: \n \n{0}".format(post['caption']))
        print("\n\n#########\n")
        n += 1
        try:
            nextPostDesc = getImageDesc(posts[n]['image_url'])
        except:
            pass
        input("Show next Post: ")
        os.system('cls||clear')
    restart = input("\nOut of posts. Reload? (y/n): ")
    if restart.lower() == "n":
        exit()
    else: 
        printPosts(getPosts())

def exit():
    print("\nThank you for using this extremely useful tool! \n\n ")

def main():
    login()
    printPosts(getPosts())

if __name__ == '__main__':
    main()