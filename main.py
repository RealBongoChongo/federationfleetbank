from flask import Flask, render_template, request, redirect, abort, send_file
from flask_discord import DiscordOAuth2Session
from utility import handler
import os
import requests
import asyncio
import dotenv
import socketio
import random
import threading
import json

dotenv.load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("client_secret")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 1102706108134588467
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("client_secret")
app.config["DISCORD_BOT_TOKEN"] = os.getenv("token")
app.config["DISCORD_REDIRECT_URI"] = "https://bank.federationfleet.xyz/callback"

sio = socketio.Server(async_mode="threading", namespaces=["/"], logger=True, cors_allowed_origins='*')
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

discord = DiscordOAuth2Session(app)
APIPREFIX = "https://discord.com/api/v10{}"

@app.route("/")
def home():
    if discord.authorized:
        user = discord.fetch_user()
        url="/accounts"
        login_status="Dashboard"
    else:
        url="/login"
        login_status="Login"

    counts = handler.getCounts()
    accounts = counts[0]
    credits = counts[1]
    transactions = counts[2]
    reserve = counts[3]
    
    return render_template("index.html", discord_url=url, login_status=login_status, accounts=accounts, credits=credits, transactions=transactions, reserve=reserve)

@app.route("/minecraft")
def minecraft():
    return render_template("minecraft.html")

@app.route("/shipakinator/home")
def akinatorhome():
    return render_template("home.html")

@app.route("/shipakinator/game")
def akinatorgame():
    return render_template("shipakinator.html")

@app.route("/shipakinator/ships")
def akinatorships():
    return render_template("shipakinator-ships.html")

@app.route("/login")
def login():
    return discord.create_session(scope=["identify", "guilds"], prompt=None)

@app.route("/image")
def imagething():
    return send_file("images/Screenshot 2023-09-16 182743.png")

@app.route("/logout")
def logout():
    discord.revoke()
    return redirect("/")

@app.route("/accounts")
def accounts():
    if not discord.authorized:
        return redirect("/login")

    user = discord.fetch_user()
    accounts = handler.getAccounts(user)
    
    return render_template("accounts.html", accounts=accounts)

@app.route("/dashboard/<accountid>/<setting>")
def dashboard(accountid, setting):
    accountid = int(accountid)
    if not discord.authorized:
        return redirect("/login")

    if setting.lower() not in ["main", "holders", "transactions", "transfers"]:
        return redirect("/accounts")

    account = handler.getAccount(int(accountid))
    user = discord.fetch_user()

    if not account:
        return redirect("/")
    elif user.id not in account["holders"].values():
        return redirect("/")

    return render_template("dashboard.html", account=account, setting=setting.lower(), user=user, avatar=user.avatar_url)

@app.route("/callback")
def callback():
    data = discord.callback()
    if "redirect" in data:
        r = data["redirect"]
    else:
        r = "/accounts"
    
    return redirect(r)

@app.route("/change/holders/<eventtype>/<accountid>", methods=["POST"])
def changeHolders(eventtype, accountid: int):
    accountid = int(accountid)
    if not discord.authorized:
        return abort(401)

    user = discord.fetch_user()
    account = handler.getAccount(accountid)

    if not account:
        return abort(404)
    
    if user.id != account["owner"]:
        return abort(401)

    data = request.get_json()
    if "holder" not in data or not data["holder"]:
        return abort(400)

    if eventtype == "add":
        if data["holder"] in account["holders"].keys():
            return abort(400)

        res = requests.get(
            APIPREFIX.format("/users/{}".format(data["holder"])), 
            headers={"Authorization": "Bot {}".format(os.getenv("token"))}
        )
        resData = res.json()
        if res.status_code == 404:
            return abort(404)
        
        handler.addHolder(accountid, resData["username"], data["holder"])
        return {"username": resData["username"]}
    else:
        if "holder" not in data or not data["holder"]:
            return abort(400)
        
        if not data["holder"] in account["holders"].keys():
            return abort(400)

        handler.removeHolder(accountid, data["holder"])
        return "Yes"

@app.route("/admin/transaction/<accountid>/<adder>", methods=["POST"])
def adminTransaction(accountid: int, adder):
    accountid = int(accountid)
    data = request.get_json()
    if not data["auth"] == os.getenv("token"):
        return abort(401)
        
    account = handler.getAccount(accountid)

    if not account:
        return abort(404)

    if (not "reason" in data) or (not "amount" in data):
        return abort(400)
    
    if not data["reason"]:
        return abort(400)

    if data["amount"] > 0:

        handler.createBalance(accountid, adder, data["amount"], data["reason"])
    
        handler.logBalance(accountid, adder, data["amount"], data["reason"])
    else:
        handler.createBalance(accountid, adder, data["amount"], data["reason"])
    
        handler.logRemoval(accountid, adder, data["amount"] * -1, data["reason"])

    return "Yes"

@app.route("/transaction/external/<accountid>/<directid>", methods=["POST"])
def externaltransaction(accountid: int, directid):
    accountid = int(accountid)
    data = request.get_json()
    
    if not (discord.authorized or data["auth"] == os.getenv("token")):
        return abort(401)

    user = discord.fetch_user()
    account = handler.getAccount(accountid)

    if not account:
        return abort(404)
    
    if user.id not in account["holders"].values():
        return abort(401)

    if (not "reason" in data) or (not "amount" in data):
        return abort(400)
    
    if data["amount"] <= 50 if accountid != 1 else 0 or not data["reason"]:
        return abort(400)

    if data["amount"] > account["balance"]:
        return abort(403)

    handler.createBalance(accountid, directid, data["amount"] * -1, data["reason"])
    handler.logRemoval(accountid, directid, data["amount"], data["reason"])

    return "Yes"

@app.route("/transaction/<accountid>/<directid>", methods=["POST"])
def transaction(accountid: int, directid: int):
    accountid = int(accountid)
    directid = int(directid)
    data = request.get_json()
    
    if not (discord.authorized or data["auth"] == os.getenv("token")):
        return abort(401)

    user = discord.fetch_user()
    account = handler.getAccount(accountid)
    directAccount = handler.getAccount(directid)

    if not account or not directAccount:
        return abort(404)
    
    if user.id not in account["holders"].values():
        return abort(401)

    if (not "reason" in data) or (not "amount" in data):
        return abort(400)
    
    if data["amount"] <= 50 if accountid != 1 else 0 or not data["reason"]:
        return abort(400)

    if data["amount"] > account["balance"]:
        return abort(403)

    handler.createTransaction(accountid, data["amount"] * -1, directid, data["reason"], user.username)
    asyncio.run(asyncio.sleep(0.5))
    handler.createTransaction(directid, data["amount"], accountid, data["reason"])

    handler.logTransaction(accountid, data["amount"], directid, data["reason"], user.username)

    return "Yes"

@app.route("/loans/<accountid>", methods=["POST"])
def payAccountLoans(accountid: int):
    accountid = int(accountid)
    if not discord.authorized:
        return abort(401)

    user = discord.fetch_user()
    account = handler.getAccount(accountid)

    if not account:
        return abort(404)
    
    if user.id not in account["holders"].values():
        return abort(401)
    
    if account["owed"] > account["balance"]:
        return abort(403)
    
    handler.createTransaction(accountid, account["owed"] * -1, 1, "Paying Loans", user.username)
    handler.createTransaction(1, account["owed"], accountid, "Paying Loans")

    handler.logTransaction(accountid, account["owed"], 1, "Paying Loans", user.username)

    handler.emptyLoans(accountid)
    
    return "yes"

@app.route("/upgrade/<accountid>", methods=["POST"])
def upgradeAccount(accountid: int):
    accountid = int(accountid)
    if not discord.authorized:
        return abort(401)

    user = discord.fetch_user()
    account = handler.getAccount(accountid)

    if not account:
        return abort(404)
    
    if user.id not in account["holders"].values():
        return abort(401)

    amount = 0
    if account["tier"] == 1:
        amount = 150
    elif account["tier"] == 2:
        amount = 350
    
    if amount > account["balance"]:
        return abort(403)

    handler.createTransaction(accountid, amount * -1, 1, "Account Tier Upgrade", user.username)
    handler.createTransaction(1, amount, accountid, "Account Tier Upgrade")

    handler.logTransaction(accountid, amount, 1, "Account Tier Upgrade", user.username)

    handler.upgradeAccount(accountid, amount)
    
    return "yes"

@app.route("/create", methods=["POST"])
def accountCreate():
    if not discord.authorized:
        return abort(401)

    user = discord.fetch_user()
    guilds = discord.fetch_guilds()

    if not 1132706354415534162 in [guild.id for guild in guilds]:
        return abort(401)

    if len(handler.getAccountsOwned(user)) >= 2 or handler.isInDebt(user):
        return abort(403)

    data = request.get_json()

    if not "accountName" in data or not data["accountName"]:
        return abort(400)

    accountId = handler.createAccount(user, data["accountName"])
    asyncio.run(asyncio.sleep(0.5))

    if handler.getAccountsOwned(user) == 1:
        handler.createTransaction(1, -200, accountId, "Account Starting Bonus", "bungochungo")
        asyncio.run(asyncio.sleep(0.5))
        handler.createTransaction(accountId, 200, 1, "Account Starting Bonus")
        asyncio.run(asyncio.sleep(0.5))
        handler.logTransaction(1, 200, accountId, "Account Starting Bonus", "bungochungo")
    
    return {"url": "https://bank.federationfleet.xyz/dashboard/{}/main".format(accountId)}

@app.route("/data")
def getDataFromJson():
    return handler.getAll()

callbacks = {}

def createCallback(callback):
    stringProcessID = str(random.randrange(100000000,999999999))

    callbacks[stringProcessID] = callback

    return stringProcessID

@app.route("/ufp/library")
def getLibrary():
    if not discord.authorized:
        return discord.create_session(scope=["identify", "guilds"], prompt=None, data=dict(redirect="/ufp/library"))
    else:
        user = discord.fetch_user()
        ev = threading.Event()
        result = None
        with open("test.json", "r") as f:
            result = json.load(f)

        def ack(data):
            nonlocal ev
            nonlocal result
            result = data["data"]
            ev.set()

        sio.emit("returnData", {"processID": createCallback(ack)})

        ev.wait(timeout=2)
        if not result:
            return "Shipyard Library seems to be offline"
        else:
            if str(user.id) in result:
                return render_template("library.html", data=json.dumps(result))
            else:
                return redirect("/access-denied")

@app.route("/access-denied")
def accessDenied():
    return render_template("accessdenied.html")

######################
# WEBSOCKET HANDLERS #
######################
@sio.on("connect", namespace="/")
def connect(sid, environ):
    print("Websocket connected")

@sio.on("my event", namespace="/")
def myevent(sid, data):
    print(data)
    sio.emit("respondaigshdfk", {"data": "piss 2"})

@sio.on("ping_packet", namespace="/")
def heartbeat(sid, data):
    sio.emit("heartbeat", "Heartbeat")

@sio.on("message", namespace="/")
def on_message(sid, data):
    if data["processID"] in callbacks:
        callbacks[data["processID"]](data)
        callbacks.pop(data["processID"])

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)
