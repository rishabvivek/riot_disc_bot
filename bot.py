import discord
import os
import json
from discord.ext.commands.core import check 
import requests

from dotenv import load_dotenv
from urllib.request import urlopen
from discord.ext import commands


client = commands.Bot(command_prefix = '!')

load_dotenv('token.env')

TOKEN = os.getenv('API_TOKEN')

riot_token = os.getenv('RIOT_TOKEN')

def getChamp(number):

    versionURL = "https://ddragon.leagueoflegends.com/api/versions.json"

    versionResponse = requests.get(versionURL)
    
    versionJSON = versionResponse.json()

    versionDict = json.dumps(versionJSON)

    versionLoad = json.loads(versionDict)

    currVersion = versionLoad[0]

    champURL = "http://ddragon.leagueoflegends.com/cdn/" + currVersion + "/data/en_US/champion.json"

    champResponse = requests.get(champURL)

    champJSON = champResponse.json()

    champDict = json.dumps(champJSON)

    champLoad = json.loads(champDict)

    champList = champLoad["data"]



    keyChecker = number

    for key in champList:
         currChamp = champList[key]
         if (currChamp['key'] == keyChecker):
             champReturn = currChamp['name']
    
    return(champReturn)

def getSummoner(name):

    #API for getting player name and encrypted ID
    nameURL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + riot_token

    #requesting from API
    summ = requests.get(nameURL)
    
    #converts request to JSON
    summJSON = summ.json()

    #converts JSON into string type
    summDict = json.dumps(summJSON)

    #converts JSON into dictionary
    summLoad = json.loads(summDict)

    #getting name from dictionary
    summName = summLoad['name']

    #changing spaces with + to use for NA.OP.GG web search
    opggName = summName.replace(" ", "+")

    #getting encryped ID from dictionary
    encryptedID = summLoad['id'] 



    #using encrypted ID to make another API call"
    rankURL = "https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/" + encryptedID + "?api_key=" + riot_token

    rank = requests.get(rankURL)

    rankJSON = rank.json()

    rankDict = json.dumps(rankJSON)

    rankLoad = json.loads(rankDict)

    #getting solo queue dictionary
    soloCheck = "SOLO"
        

    if (len(rankLoad) > 1):
        rankLoadListOne = rankLoad[0]
        if soloCheck in rankLoadListOne['queueType']:
            soloRankJSON = rankLoad[0]
            flexRankJSON = rankLoad[1]
             #solo rank tier and number
            soloRankTier = soloRankJSON['tier']

            soloRankNumber = soloRankJSON['rank']

            #solo queue wins and losses
            soloWins = str(soloRankJSON['wins'])

            soloLoss = str(soloRankJSON['losses'])

            #flex rank tier and number
            flexRankTier = flexRankJSON['tier']

            flexRankNumber = flexRankJSON['rank']

            #flex queue wins and losses
            flexLoss = str(flexRankJSON['wins'])

            flexWins = str(flexRankJSON['losses'])
        else:
            soloRankJSON = rankLoad[1]
            flexRankJSON = rankLoad[0]
             #solo rank tier and number
            soloRankTier = soloRankJSON['tier']

            soloRankNumber = soloRankJSON['rank']

            #solo queue wins and losses
            soloWins = str(soloRankJSON['wins'])

            soloLoss = str(soloRankJSON['losses'])

            #flex rank tier and number
            flexRankTier = flexRankJSON['tier']

            flexRankNumber = flexRankJSON['rank']

            #flex queue wins and losses
            flexLoss = str(flexRankJSON['wins'])

            flexWins = str(flexRankJSON['losses'])
    elif (len(rankLoad) == 1):
        rankLoadListOne = rankLoad[0]
        if soloCheck in rankLoadListOne['queueType']:
            soloRankJSON = rankLoad[0]
            #solo rank tier and number
            soloRankTier = soloRankJSON['tier']

            soloRankNumber = soloRankJSON['rank']

            #solo queue wins and losses
            soloWins = str(soloRankJSON['wins'])

            soloLoss = str(soloRankJSON['losses'])

             #flex rank tier and number
            flexRankTier = "N/A"

            flexRankNumber = "N/A"

            #flex queue wins and losses
            flexLoss = "N/A"

            flexWins = "N/A"
        else:
            flexRankJSON = rankLoad[0]
            soloRankTier = "N/A"

            soloRankNumber = "N/A"

            #solo queue wins and losses
            soloWins = "N/A"

            soloLoss = "N/A"

            #flex rank tier and number
            flexRankTier = flexRankJSON['tier']

            flexRankNumber = flexRankJSON['rank']

            #flex queue wins and losses
            flexLoss = str(flexRankJSON['wins'])

            flexWins = str(flexRankJSON['losses'])


    else:
        return (summName + '\n' + '\n' + "NO RANK")

    return ("**" + summName + "**" + '\n' + '\n' + "SOLO: " + soloRankTier + " " + soloRankNumber + " " 
    + "W: " + soloWins + " " + "L: " + soloLoss + '\n' + "FLEX: " + flexRankTier
    + " " + flexRankNumber + " " + "W: " + flexWins + " " + "L: " + flexLoss + '\n' 
    + '\n' + "__See full match history at:__ " + '\n' + "https://na.op.gg/summoner/userName=" + opggName)

def getMain(name):
    #API for getting player name and encrypted ID
    namesURL = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + name + "?api_key=" + riot_token
    #requesting from API
    summ = requests.get(namesURL)
    
    #converts request to JSON
    summJSON = summ.json()

    #converts JSON into string type
    summDict = json.dumps(summJSON)

    #converts JSON into dictionary
    summLoad = json.loads(summDict)
    #getting encryped ID from dictionary
    encryptedID = summLoad['id']

    #getting champion mastery data
    URL = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/" + encryptedID + "?api_key=" + riot_token

    mains = requests.get(URL)

    mainsJSON = mains.json()

    mainsDict = json.dumps(mainsJSON)

    mainsLoad = json.loads(mainsDict)

    #setting count to 0, this is to only show top 3 champs for every player
    count = 0

    #looping over the list of dictionaries, breaking at 3 so once 3 champs found exit
    for i in range(len(mainsLoad)):
        if(count == 3):
            break
        checker = mainsLoad[i]
        if (i == 0):
            mainOne = checker['championId']
            mainOneLevel = checker['championLevel']
            mainOnePoints = checker['championPoints']
            count = count + 1
        elif (i == 1):
            mainTwo = checker['championId']
            mainTwoLevel = checker['championLevel']
            mainTwoPoints = checker['championPoints']
            count = count + 1
        else:
            mainThree = checker['championId']
            mainThreeLevel = checker['championLevel']
            mainThreePoints = checker['championPoints']
            count = count + 1

    firstMain = str(mainOne)
    firstMainLevel = str(mainOneLevel)
    firstMainPoints = str(mainOnePoints)

    secondMain = str(mainTwo)
    secondMainLevel = str(mainTwoLevel)
    secondMainPoints = str(mainTwoPoints)

    thirdMain = str(mainThree)
    thirdMainLevel = str(mainThreeLevel)
    thirdMainPoints = str(mainThreePoints)

    secondMain = str(mainTwo)
    #returning champ IDs
    return (getChamp(firstMain) + " - " + "Mastery: " + firstMainLevel + " | " + firstMainPoints + " points" + '\n' +
            getChamp(secondMain) + " - " + "Mastery: " + secondMainLevel + " | " + secondMainPoints + " points" +'\n' + 
            getChamp(thirdMain) + " - " + "Mastery: " + thirdMainLevel + " | " + thirdMainPoints + " points")
    
    
        

@client.event
async def on_ready( ):
    print ("Bot ready")

@client.command(help = "Find a summoner, type this and the summoners IGN to search.")
async def summoner(ctx, *, arg):
    await ctx.send(getSummoner(arg))

@client.command(help = "Find a summoner's top 3 champs")
async def mains(ctx, *, arg2):
    await ctx.send(getMain(arg2))



client.run(TOKEN)