import os
import sqlite3
from flask import Flask, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import random
import json
from flask import request, redirect



app = Flask(__name__)


app.secret_key = b"random bytes representing flask secret key"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] =     # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = ""                # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = ""                 # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = ""                    # Required to access BOT resources.

discord = DiscordOAuth2Session(app)





@app.route("/login/")
def login():
    return discord.create_session()
	

@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()


    nwpss = []
    lst = ['a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z','!','@',
    '#','$','%','^','&','*','(',')','-','_','+','=','{',",",'}',']',
    '[',';',':','<','>','?','/','1','2','3','4','5','6','7','8','9','0'
    ,'`','~','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'
    ,'Q','R','S','T','U','V','W','X','Y','Z']
    for x in range(15):
        newpass = random.choice(lst)
        nwpss.append(newpass)
    fnpss = ''.join(nwpss)

    return redirect(url_for(".dashboard"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))
	
@app.route("/dashboard/")
@requires_authorization
def dashboard():
    user = discord.fetch_user()
    return f"""
    <html>
        <head>
            <title>{user.name}</title>
        </head>
        <body>
            <img src="{user.avatar_url}" alt="Avatar" style="border-radius: 50%" width="40" height="40">
        </body>
    </html>"""

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']

        print(first_name)
        print(last_name)

    return render_template('sign-up.html')

if __name__ == "__main__":
    app.run(host='localhost', port=80)
