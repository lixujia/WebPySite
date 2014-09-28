import web
import sys
import json

from web import form 

urls = ("/","login",
        "/(.*)/","redirect",
        "/login","login",)

render = web.template.render("templates/")

class redirect:
    def GET(self,path):
        return web.seeother("/" + path)

def check_passwd(user,passwd):
    passwd_map = {}
    
    with open("password.json","r") as fp:
        passwd_map = json.load(fp)

        if not passwd_map.has_key(user):
            return False
        elif passwd != passwd_map[user]:
            return False

        fp.close()
        
    return True

class login:
    logform = form.Form(form.Textbox("User Name"),
                        form.Password("Password"),
                        form.Button("Login"),
                        validators = [form.Validator("User name cannot be empty!",
                                                     lambda i: "" != i["User Name"]),
                                      form.Validator("Password cannot be empty!",
                                                     lambda i: "" != i["Password"]),
                                      form.Validator("User dosen't exist or Password and User Name dosen't match!",
                                                     lambda i: check_passwd(i["User Name"],i["Password"]))])

    def GET(self):
        f = self.logform()

        return render.login(f)

    def POST(self):
        f = self.logform()
            
        if not f.validates():
            return render.login(f)
        elif "" == f.d["User Name"] or "" == f.d["Password"]:
            return render.login(f)
        else:
            return "OK"

if __name__ == "__main__":
    web.config.debug = False
    app = web.application(urls,globals())
    app.run()
    
