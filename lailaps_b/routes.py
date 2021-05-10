from tornado import web,escape
from bs4 import BeautifulSoup
import config
import requests
import instaloader
import agent
import json
import sys


class instagramHandler(web.RequestHandler):

    def post(self):

        self.args = escape.xhtml_escape(self.request.body).split("=")
        key = config.search_credential("instagram")

        user_ig  = key["key"]["user"]
        pass_ig = key["key"]["pass"]
        user = self.args[1]

        L = instaloader.Instaloader()


        if(user_ig and pass_ig):
            try:
                L.login(user_ig,pass_ig)
            except instaloader.exceptions.BadCredentialsException:
                self.write({"success":False,"status":"Bad Credentials"})
            except instaloader.exceptions.ConnectionException:
                self.write({"success":False,"status":"Try Later"})

        try:
            profile = instaloader.Profile.from_username(L.context,user)
        except instaloader.exceptions.ProfileNotExistsException:
            self.write({"success":False,"status":"Profile Not Found"})

        info = profile.__dict__

        userData = {
            "id": info["_node"]["id"],
            "fbId": info["_node"]["fbid"],
            "name":info["_node"]["full_name"],
            "username": info["_node"]["username"],
            "bio": info["_node"]["biography"],
            "pick": info["_node"]["profile_pic_url"],
            "external_url": info["_node"]["external_url"],
            "followed": info["_node"]["edge_followed_by"],
            "follow": info["_node"]["edge_follow"],
            "verified":info["_node"]["is_verified"],
            "isPrivate": info["_node"]["is_private"],
            "businessAcount":{
            "isBussiness":info["_node"]["is_business_account"],
            "category":info["_node"]["business_category_name"],
            "nameCategory":info["_node"]["category_name"]
            }
        }

        self.write({"success":True,"resp":userData})



class tiktokHandler(web.RequestHandler):

    def post(self):
        self.args = escape.xhtml_escape(self.request.body).split("=")


        url = "https://www.tiktok.com/@%s/" % self.args[1]
        req = requests.get(url, headers={'User-Agent': agent.user_agent()})
        if req.status_code == 200:
            print(req.status_code)
            soup = BeautifulSoup(req.text, "html.parser")



        try:
            content = soup.find_all("script",attrs={"type":"application/json","crossorigin":"anonymous"})
            content = json.loads(content[0].contents[0])

            user = content["props"]["pageProps"]["userInfo"]


            tiktokData = {
                "userId": user["user"]["id"],
                "username": user["user"]["uniqueId"],
                "nickname": user["user"]["nickname"],
                "avatar": user["user"]["avatarMedium"],
                "bio": user["user"]["signature"],
                "createTime": user["user"]["createTime"],
                "verified": user["user"]["verified"],
                "follower": user["stats"]["followerCount"],
                "following": user["stats"]["followingCount"],
                "heart": user["stats"]["heart"]
            }

            self.write({"success":True,"data":tiktokData})
        except:
            self.write({"success":False,"status":400})



class userSearchHandler(web.RequestHandler):


    def post(self):
        self.args = escape.xhtml_escape(self.request.body).split("=")
        payload = {"username": self.args[1]}
        req = requests.post("https://usersearch.org/results_normal.php", data=payload, verify=False)

        if req.status_code == 200:
            soup = BeautifulSoup(req.content, "lxml")
            asTag = soup.find_all('a',class_="pretty-button results-button")
            if len(asTag) > 0:
                links = []
                for atag in asTag:
                    if atag.text == "View Profile":
                        links.append(atag["href"])
                self.write({"success":True,"data":links})
            else:
                self.write({"success":False,"status":"Not Have Regist"})
        else:
            self.write({"success":False,"status":req.status_code})
