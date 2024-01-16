import json
import random
import requests
import os
import discord
import asyncio
import pymongo
import dotenv

dotenv.load_dotenv()

mongoCli = pymongo.MongoClient(os.getenv("mongodb"))
federationDB = mongoCli["federationfleet"]
bankDB = federationDB["banking"]

APIPREFIX = "https://discord.com/api/v10{}"

def getAll():
    return list(bankDB.find())

def getCounts():
    credits = 0
    transactions = 0

    for accountData in bankDB.find():
        credits += accountData["balance"]
        transactions += len(accountData["transactions"])

    return [len(list(bankDB.find())), credits, transactions, getAccount(1)["balance"]]

def getAccounts(user):
    accessable = []
    
    for accountData in bankDB.find():
        if user.id in accountData["holders"].values():
            accessable.append(accountData)

    return accessable

def getAccountsOwned(user):
    accessable = []
    
    for accountData in bankDB.find():
        if user.id == accountData["owner"]:
            accessable.append(accountData)

    return accessable

def isInDebt(user):
    data = getAccountsOwned(user)

    for accountData in data:
        if accountData["balance"] < 0 or accountData["owed"] > 0:
            return True

    return False

def getAccount(accountNumber):
    accountData = bankDB.find_one({"_id": accountNumber})
    
    if accountData:
        return accountData
    else:
        return None

def addHolder(accountNumber, holderName, holderId):
    accountData = bankDB.find_one({"_id": accountNumber})

    accountData["holders"][holderName] = holderId

    bankDB.update_one({"_id": accountNumber}, {"$set": {"holders": accountData["holders"]}})

def removeHolder(accountNumber, holderName):
    accountData = bankDB.find_one({"_id": accountNumber})

    accountData["holders"].pop(holderName)

    bankDB.update_one({"_id": accountNumber}, {"$set": {"holders": accountData["holders"]}})

def createTransaction(accountNumber, amount, directAccountNumber, description, authorizer=None):
    stringAmount = str(amount)
    if amount > 0:
        stringAmount = "+{}".format(amount)

    accountData = bankDB.find_one({"_id": accountNumber})

    accountData["balance"] += amount
    accountData["transactions"].append({
        "amount": stringAmount,
        "description": description,
        "recipient": "#{} (\"{}\" Owner: {})".format(directAccountNumber, getAccount(directAccountNumber)["name"], getAccount(directAccountNumber)["ownerName"]),
        "authorizedBy": authorizer if authorizer else ""
    })

    bankDB.update_one({"_id": accountNumber}, {"$set": {"balance": accountData["balance"], "transations": accountData["transactions"]}})

def createBalance(accountNumber, adder, amount, description):
    stringAmount = str(amount)
    if amount > 0:
        stringAmount = "+{}".format(amount)

    accountData = bankDB.find_one({"_id": accountNumber})

    accountData["balance"] += amount
    accountData["transactions"].append({
        "amount": stringAmount,
        "description": description,
        "recipient": "{}".format(adder),
        "authorizedBy": ""
    })

    bankDB.update_one({"_id": accountNumber}, {"$set": {"balance": accountData["balance"], "transations": accountData["transactions"]}})

def logBalance(accountNumber, adder, amount, description):
    totalBalance = 0
    for accountData in bankDB.find():
        totalBalance += accountData["balance"]

    res = requests.patch(
        APIPREFIX.format("/channels/1144438545025597491"), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))},
        json={"name": "[CREDITS]: {}".format(totalBalance)}
    )

    asyncio.run(asyncio.sleep(0.5))

    res = requests.patch(
        APIPREFIX.format("/channels/1132707139866075186"), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))},
        json={"name": "[RESERVE]: {}".format(getAccount(1)["balance"])}
    )
    
    embed = discord.Embed(
        title="New Transaction",
        color=0x00ff00 if amount > 0 else 0xff0000,
        description="`{}` **({} Credits)** > **{}'s Account** (`#{}` \"{}\")\n\nDescription: {}".format(adder, amount, getAccount(accountNumber)["ownerName"], getAccount(accountNumber)["_id"], getAccount(accountNumber)["name"], description)   
    )

    webhook = discord.SyncWebhook.from_url(os.getenv("webhook"))
    webhook.send(embed=embed)

def logRemoval(accountNumber, adder, amount, description):
    totalBalance = 0
    for accountData in bankDB.find():
        totalBalance += accountData["balance"]

    res = requests.patch(
        APIPREFIX.format("/channels/1144438545025597491"), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))},
        json={"name": "[CREDITS]: {}".format(totalBalance)}
    )

    asyncio.run(asyncio.sleep(0.5))

    res = requests.patch(
        APIPREFIX.format("/channels/1132707139866075186"), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))},
        json={"name": "[RESERVE]: {}".format(getAccount(1)["balance"])}
    )
    
    embed = discord.Embed(
        title="New Transaction",
        color=0x00ff00 if amount > 0 else 0xff0000,
        description="**{}'s Account** (`#{}` \"{}\") **({} Credits)** > `{}` \n\nDescription: {}".format(getAccount(accountNumber)["ownerName"], getAccount(accountNumber)["_id"], getAccount(accountNumber)["name"], amount, adder, description)   
    )

    webhook = discord.SyncWebhook.from_url(os.getenv("webhook"))
    webhook.send(embed=embed)

def logTransaction(accountNumber, amount, directAccountNumber, description, authorizer=None):
    totalBalance = 0
    for accountData in bankDB.find():
        totalBalance += accountData["balance"]

    res = requests.patch(
        APIPREFIX.format("/channels/1144438545025597491"), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))},
        json={"name": "[CREDITS]: {}".format(totalBalance)}
    )

    asyncio.run(asyncio.sleep(0.5))

    res = requests.patch(
        APIPREFIX.format("/channels/1132707139866075186"), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))},
        json={"name": "[RESERVE]: {}".format(getAccount(1)["balance"])}
    )
    
    embed = discord.Embed(
        title="New Transaction",
        color=0x00ff00 if amount > 0 else 0xff0000,
        description="{}**{}'s Account** (`#{}` \"{}\") **({} Credits)** > **{}'s Account** (`#{}` \"{}\")\n\nDescription: {}".format("" if not authorizer else "`" + authorizer + "`\n\n", getAccount(accountNumber)["ownerName"], getAccount(accountNumber)["_id"], getAccount(accountNumber)["name"], amount, getAccount(directAccountNumber)["ownerName"], getAccount(directAccountNumber)["_id"], getAccount(directAccountNumber)["name"], description)   
    )

    webhook = discord.SyncWebhook.from_url(os.getenv("webhook"))
    webhook.send(embed=embed)

def logAccount(owner, name, randid):
    embed = discord.Embed(
        title="New Account",
        color=0x00ff00,
        description="{} Created Account `#{}` \"{}\"".format(owner,randid,name)   
    )

    webhook = discord.SyncWebhook.from_url(os.getenv("webhook2"))
    webhook.send(embed=embed)

def createAccount(owner, name):
    randAccountId = random.randint(1000000000,9999999999)

    bankDB.insert_one({
        "name": name,
        "_id": randAccountId,
        "holders": {
            owner.username: owner.id
        },
        "owner": owner.id,
        "ownerName": owner.username,
        "balance": 0,
        "owed": 0,
        "tier": 1,
        "transactions": []
    })

    logAccount(owner,name,randAccountId)

    requests.put(
        APIPREFIX.format("/guilds/1132706354415534162/members/{}/roles/1132711495378153613".format(owner.id)), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))}
    )

    asyncio.run(asyncio.sleep(0.5))
    
    requests.put(
        APIPREFIX.format("/guilds/1132706354415534162/members/{}/roles/1132711797183492146".format(owner.id)), 
        headers={"Authorization": "Bot {}".format(os.getenv("token"))}
    )
    
    return randAccountId

def upgradeAccount(accountNumber, amount):
    tier = 3
    if amount == 150:
        tier = 2
    elif amount == 350:
        tier = 3

    bankDB.update_one({"_id": accountNumber}, {"$set": {"tier": tier}})

def emptyLoans(accountNumber):
    bankDB.update_one({"_id": accountNumber}, {"$set": {"owed": 0}})