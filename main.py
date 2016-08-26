#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import re
import cgi

def valid_name(name):
    p = re.compile("^[a-zA-Z0-9_-]{3,20}$")
    m = p.match(name)
    if m:
        error = ""
        return (True,error)
    else:
        error = "invalid username"
        return (False, error)


def valid_pass(password):
    p = re.compile("^.{3,20}$")
    m = p.match(password)
    if m:
        error = ""
        return(True,error)
    else:
        error = "invalid password"
        return(False,error)


def valid_vpass(password,vpassword):
    if password == vpassword:
        error = ""
        return(True,error)
    else:
        error ="passwords dont match"
        return(False,error)


def valid_email(email):
    p = re.compile("^[\S]+@[\S]+.[\S]+$")
    m = p.match(email)
    if m:
        error = ""
        return(True,error)
    elif email=="":
        error = ""
        return(True,error)
    else:
        error = "invalid email"
        return(False,error)

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
</head>
<body>
    <h1>Signup</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""



form="""
<form action="/" method= "post">
    <label>
        ..........username
        <input type="text" name="username" value="%(username)s"/>
        <span style= "color:red">%(uerror)s</span>
    </label>
    <br>
    <br>
    <label>
        ..........password
        <input type="password" name="password" value="%(password)s"/>
        <span style= "color:red">%(perror)s</span>
    </label>
    <br>
    <br>
    <label>
        verify password
        <input type="password" name="vpassword" value="%(vpassword)s"/>
        <span style= "color:red">%(verror)s</span>
    </label>
    <br>
    <br>
    <label>
        ................email
        <input type="text" name="email" value="%(email)s"/>
        <span style= "color:red">%(berror)s</span>
    </label>
    <br>
    <br>
    <input type ="submit">
</form>
"""

class MainPage(webapp2.RequestHandler):
    def write_form(self,username="",uerror="",password="",
                        perror="",vpassword="",verror="",
                        email="",berror=""):
        form1 = page_header + form + page_footer
        self.response.out.write(form1 % {"username": cgi.escape(username,quote = True),
                                        "uerror": uerror,
                                        "password":"",
                                        "perror": perror,
                                        "vpassword":"",
                                        "verror": verror,
                                        "email": cgi.escape(email,quote = True),
                                        "berror": berror})

    def get(self):
        self.write_form()


    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        vpassword = self.request.get("vpassword")
        email = self.request.get("email")

        (vusername,uerror) = valid_name(username)
        (vppassword,perror) = valid_pass(password)
        (vvpassword,verror) = valid_vpass(password,vpassword)
        (vemail,berror) = valid_email(email)

        if not (vusername and vppassword and vvpassword and vemail):
            self.write_form(username,uerror,password,perror,vpassword,verror,email,berror)
        else:
            self.redirect("/thanks?username="+username)
class nextt(webapp2.RequestHandler):
    def get(self):
        username = self.request.get("username")
        thanks ="Thanks   "
        response =thanks + username
        self.response.out.write(response )

app = webapp2.WSGIApplication([
                             ('/', MainPage),
                             ('/thanks',nextt)
], debug=True)
