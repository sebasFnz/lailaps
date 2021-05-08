from tornado.web import RequestHandler
import instaloader
import json
import sys


class instagramHandler(RequestHandler):

    def get(self):

        user_ig  = ""
        pass_ig = ""
        user =
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
