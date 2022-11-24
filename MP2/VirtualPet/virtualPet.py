import os
from collections import defaultdict

from pyswip import Prolog, Variable, Atom
import string
import random
import spacy
from owlready2 import get_ontology, onto_path, Thing
from random import choice
from marvelScript import *

import random
from pyswip import Prolog
from threading import Thread
from time import sleep
import string
import random
from owlready2 import *
import time
import os
from Checkers import checkers
import traceback
from senticnet.senticnet import SenticNet

sn = SenticNet()

CHARACTER_KEY_WORDS = ['character', 'movie character']
MOVIE_KEY_WORDS = ['movie', 'film']
QUESTION_WORDS = {'do', 'who', 'what', 'which', 'whom'}
caches = {'movies': set(), 'characters': set()}

#initializing checkers
lastMoves = 100
cwd = os.getcwd()
cwd += "/checkersWins.owl"
game = checkers(cwd,lastMoves,False)

games = ["checkers"]
questions_bot_asks =  ["likes_which_food","dislikes_which_food","want_to_play"]

lastQ = -1  # 0: do, 1: who, 2: what, 3: whom, 4: which, -1 initial state
contexts = {'next': 0,
            'plot': False,
            'tell': False,
            'lastOperation': False,
            'movie': False,
            'character': False,
            'whichMovie': False,
            'waitingTell': False,
            'questionType': False
            }

# initializing variables
print("Loading Marvel NER model...")
nlp = spacy.load("marvelNERModel/model-last")
nlp2 = spacy.load('en_core_web_lg')
print("Marvel NER model loaded")
tell = [nlp("can you tell i more"), nlp("i want to know more"), nlp('tell i more about'), nlp('tell i more')]
whichMovies = [nlp2("in what movie have appear in"),
               nlp2("in which movie have appear in"),
               nlp2('in what film have appear in'),
               nlp2('in which film have appear in'),
               nlp2('which movie have'),
               nlp2('which film have')]


# converts a list of strings into a single string replacing spaceChar by _Char
def convertListOfStringsToSingleDividedByUnderscore(stringList):
    returning = ""
    for indx, stringElement in enumerate(stringList):
        if (indx == 0):
            returning += stringElement
        else:
            returning += "_" + stringElement
    return returning


# tries to decode a byte string into a normal string
def decodeStringIfPossible(element):
    try:
        return element.decode("utf-8")
    except:
        try:
            return str(element)
        except:
            return element


# my own array to string contructor
def toStr(answerList):
    ret = "["
    size = len(answerList)
    for indx, word in enumerate(answerList):
        ret += word
        if indx != size - 1:
            ret += ","
    ret += "]"
    return ret


def loadBotMemoryOnto():
    cwd = os.getcwd()
    cwd += "/botMemory.owl"
    onto_path.append("/")
    ontology_path = "file://" + cwd
    onto = get_ontology(ontology_path)
    onto.load()
    ontology_path += "#"
    try:
        if onto.base_iri != ontology_path:
            onto.base_iri = ontology_path
    except:
        pass

    with onto:
        class entity(Thing):
            pass

        class entityName(entity >> str):
            pass

        class likes(Thing):
            pass

        class dislikes(Thing):
            pass

        class has_likes(entity >> likes):
            pass

        class has_dislikes(entity >> dislikes):
            pass

        class movies(Thing):
            pass

        class characters(Thing):
            pass

        class has_movies(likes >> movies):
            pass

        class has_characters(likes >> characters):
            pass

        class has_movies(dislikes >> movies):
            pass

        class has_characters(dislikes >> characters):
            pass

        class description(movies >> str):
            pass

        class description(characters >> str):
            pass

        class has_characters(movies >> characters):
            pass

        class star_in(characters >> movies):
            pass
    

    return onto


def setup(entity, onto, prolog):
    if entity == "bot":
        print("?: Whats my name?")
        queryStart = "who(you,"
        answer = "I am"
    else:
        print(onto.bot.entityName[0] + ": Whats your name?")
        queryStart = "who(me,"
        answer = "You are"
    queryEnd = ",L)"
    stop = False
    while (not stop):
        whoAmI = input("- ")
        whoAmI = whoAmI.translate(str.maketrans('', '', string.punctuation))
        whomList = whoAmI.lower()
        whomList = whomList.split(" ")
        for i in range(0, 3):
            queryString = queryStart + str(whomList[0:(i + 1)]) + queryEnd
            try:
                lista = list(prolog.query(queryString))[0]
                stop = True
                phraseStart = 0
                for wordIdx in range(0, (i + 1)):
                    phraseStart += len(whomList[wordIdx]) + 1
                if (entity == "bot"):
                    onto.bot.entityName[0] = whoAmI[phraseStart:]
                else:
                    onto.user.entityName[0] = whoAmI[phraseStart:]
                print(onto.bot.entityName[0] + ":", answer, whoAmI[phraseStart:])
                break
            except:
                pass
        if (not stop and (2 >= len(whomList) or len(whomList) >= 6)):
            stop = True
            if (entity == "bot"):
                onto.bot.entityName[0] = whoAmI
            else:
                onto.user.entityName[0] = whoAmI
            print(onto.bot.entityName[0] + ":", answer, whoAmI)
        elif (not stop):
            print(onto.bot.entityName[0] + ":", "I am sorry I didn't catch that can you repeat?")
    onto.save()


def updateProlog(topic, newEntity):
    fileName = ''
    keyWords = ''
    if topic == 'MARVELCHARACTER':
        fileName = 'characterNoun.pl'
        keyWords = 'marvelContextCharacter'
    elif topic == 'MARVELMOVIE':
        fileName = 'movieNoun.pl'
        keyWords = 'marvelContextMovie'

    with open(fileName, 'a') as f:
        withoutSpace = newEntity.lower().replace(' ', '')
        withoutSpace = withoutSpace.replace("\"", '')
        f.write(f"\n{keyWords}(sing,{withoutSpace}) --> [\"{newEntity}\"].")


def getMovieEntity(bot, movieName):
    movie = 'movie' + movieName.lower().replace(' ', '')
    for m in bot.likes.movies:
        if m.name == movie:
            return m, True

    for m in bot.dislikes.movies:
        if m.name == movie:
            return m, False
    entity = onto.movies(movie, realName=movieName, hateLevel=0, likeLevel=0, namespace=onto, description=[],
                         characters=[])

    if random.randint(0, 1) == 1:
        entity.likeLevel = random.randint(1, 5)
        bot.likes.movies.append(entity)
        return entity, True
    else:
        entity.hateLevel = random.randint(1, 5)
        bot.dislikes.movies.append(entity)
        return entity, False


def getCharacterEntity(bot, character):
    cc = 'character' + character.lower().replace(' ', '')
    for m in bot.likes.characters:
        if m.name == cc:
            return m, True

    for m in bot.dislikes.characters:
        if m.name == cc:
            return m, False
    
    entity = onto.characters(cc, realName=character.lower(), hateLevel=0, likeLevel=0, namespace=onto, description=[], movies=[])
    
    if random.randint(0, 1) == 1:
        entity.likeLevel = random.randint(1, 5)
        bot.likes.characters.append(entity)
        return entity, True
    else:
        entity.hateLevel = random.randint(1, 5)
        bot.dislikes.characters.append(entity)
        return entity, False


def addIfDoesNotKnow(bot, entity, isMovie):
    if entity not in caches['movies'] and entity not in caches['characters']:
        # bot does not know the entity
        # so create a new onto instance for it
        if isMovie:
            caches['movies'].add(entity)  # add entity name (str) to cache
            entity = entity.lower()
            entity = onto.movies("movie" + entity.replace(' ', ''), realName=entity, hateLevel=0, likeLevel=0,
                                 namespace=onto, description=[],
                                 characters=[])
        else:
            caches['characters'].add(entity)  # add entity name (str) to cache
            entity = entity.lower()
            entity = onto.characters("character" + entity.replace(' ', ''), realName=entity, hateLevel=0, likeLevel=0,
                                     namespace=onto, description=[],
                                     movies=[])

        if random.randint(0, 1) == 1:
            entity.likeLevel = random.randint(1, 5)
            if isMovie:
                bot.likes.movies.append(entity)
            else:
                bot.likes.characters.append(entity)
        else:
            entity.hateLevel = random.randint(1, 5)
            if isMovie:
                bot.dislikes.movies.append(entity)
            else:
                bot.dislikes.characters.append(entity)
    else:
        # bot has already known the entity
        # return the stored entity
        if isMovie:
            entity, _ = getMovieEntity(bot, entity)
        else:
            entity, _ = getCharacterEntity(bot, entity)

    return entity


def parsePrologResult(l):
    def flatten_(l):
        res = []
        for v in l:
            if isinstance(v, list):
                res.extend(v)
            else:
                res.append(v)
        return res

    l = flatten_(l)
    result = set()
    for i, v in enumerate(l):
        if isinstance(v, Atom):
            try:
                result.add(str(v.chars, 'utf-8'))
            except:
                result.add(str(v.chars))
        elif isinstance(v, Variable):
            if i < len(l):
                continue
            break
        else:
            try:
                result.add(str(v, 'utf-8'))
            except:
                result.add(str(v))
    return result


def getResponsePhrase(like: bool, level: int, movie: bool):
    key = 'like' if like else 'dislike'
    res = [k['L'] for k in list(prolog.query(f"phrase({key}({level}), L)"))]
    phrases = []
    for p in res:
        p = ' '.join([str(t.chars, 'utf-8') for t in p])
        phrases.append(p)

    if not movie:
        phrases = [p.replace('it', 'this character') for p in phrases]
    return phrases

from datetime import datetime
def getMoAfEv():
    hour = datetime.now().hour
    if(12 > hour >= 5):
        return "morning"
    elif(17 > hour >= 12):
        return "afternoon"
    elif(21 > hour >= 17):
        return "evening"
    else:
        return "night"

def getDontUnderstand(prolog,howManyTimesGotWrong):
    #howManyTimesGotWrong is a int that will increase giving other answers to the user
    if(howManyTimesGotWrong > 5):
        howManyTimesGotWrong = 5
    elif(howManyTimesGotWrong < 0):
        howManyTimesGotWrong = 0
    wrongMsg = list(prolog.query("phrase(wrong(" + str(howManyTimesGotWrong) + "),L3)"))
    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in wrongMsg]
    answerId = random.randint(0,len(answers)-1)
    response = answers[answerId]
    response = response[0].upper() + response[1:]
    return response


def getSynonymosOf(key):
    return [k['X'] for k in list(prolog.query(f"synonym({key.lower()},X)"))]


def containsSynonymsOf(key, data):
    syns = set(getSynonymosOf(key))
    for n in syns:
        n = set(n.split(' '))
        if len(n.intersection(data)) == len(n):
            return True
    return False


def connectCharacteroMovie(bot, character, movie):
    movieEntity = addIfDoesNotKnow(bot, movie, True)
    movie = movieEntity.name
    exits = False
    for m in character.movies:
        if m.name == movie:
            exits = True
            break

    if not exits:
        character.movies.append(movieEntity)

    exits = False
    for c in movieEntity.characters:
        if c.name == character.name:
            exits = True
            break

    if not exits:
        movieEntity.characters.append(character)


def respond(bot, entity=None, isMovie=None, res=None):
    # global lastQ
    # lastQ = 0  # last question is do
    global initialBotSentence
    if contexts['plot']:  # user want to know more plot
        contexts['lastOperation'] = 'plot'  # last operation
        contexts['plot'] = False
        movie = True if contexts['movie'] else False

        if movie:
            entity, like = getMovieEntity(bot, contexts['movie'])
        else:
            entity, like = getCharacterEntity(bot, contexts['character'])

        next = contexts['next']  # index of the next plot
        if next == False or next >= len(entity.description):
            # all plot were printed
            print(initialBotSentence,"I don't have more descriptions :(")
        else:
            # there are more plots to be printed
            print(initialBotSentence,f"{entity.description[contexts['next']]}.")
            if next == 1 and next + 1 < len(entity.description):
                print(initialBotSentence,f"You can insert space to get more plots of the {'movie' if movie else 'character'}")
            contexts['next'] += 1

        return

    if contexts['tell']:  # user talks to bot about a movie/character
        if isMovie:
            movie = addIfDoesNotKnow(bot, contexts['movie'], True)
            movie.description.extend(contexts['tell']['description'].split('.'))

        else:
            character = addIfDoesNotKnow(bot, contexts['character'], False)
            for m in contexts['tell']['movie']:
                connectCharacteroMovie(bot, character, m[0].text)

            character.description.extend(contexts['tell']['description'].split('.'))
        contexts['tell'] = False
        contexts['waitingTell'] = False
        contexts['lastOperation'] = 'tell'  # last operation
        print(initialBotSentence,"Thank you~")
        return

    if contexts['whichMovie']:  # In what movies has [character] appeared in
        contexts['whichMovie'] = False
        contexts['movie'] = False

        entity = contexts['character']
        if entity in caches['characters']:
            character, _ = getCharacterEntity(bot, entity)
            movies = character.movies
            if len(movies) == 0:
                print(initialBotSentence,'I dont know in which movies this character has appeared in')
                print(initialBotSentence,'Can you tell me? :)')
                contexts['waitingTell'] = True
            else:
                print(initialBotSentence,f"Character {character.realName} has appeared in {','.join([m.realName for m in movies])}.")
        else:
            print(initialBotSentence,"Sorry~, i dont know who is this character~")
            contexts['waitingTell'] = True
        return

    if "know" in res:
        contexts['lastOperation'] = 'know'  # last operation
        if isMovie:
            # movie
            contexts['movie'] = entity
            contexts['character'] = False
            if entity in caches['movies']:  # if bot knows the given entity
                movie, like = getMovieEntity(bot, entity)
                if like:
                    print(
                        initialBotSentence,f"Yes! {choice(getResponsePhrase(True, movie.likeLevel, True))} It is {movie.description[0]}.")
                    if len(movie.description) > 1:
                        print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['next'] = 1
                else:
                    print(
                        initialBotSentence,f"Hmm! I know this movie, but {choice(getResponsePhrase(False, movie.hateLevel, True))}")

            else:
                # bot does not know
                print(initialBotSentence,"No~ but i am trying to find it on the internet~")
                synopsis, plot = getSynopsisAndPlotAboutMovie(entity)
                if synopsis is None:
                    contexts['waitingTell'] = True
                    print(initialBotSentence,"I cant find it, can you tell what it is?")
                else:
                    movie = addIfDoesNotKnow(bot, entity, True)
                    movie.description.append(synopsis)
                    movie.description.extend(plot)
                    print(initialBotSentence,f"I found it!\nHere is a its synopsis: {synopsis.strip()}")
                    print()
                    print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['lastOperation'] = 'plot'
                    contexts['next'] = 0
        else:
            # character
            contexts['character'] = entity
            contexts['movie'] = False

            if entity in caches['characters']:  # if bot knows the given entity
                character, like = getCharacterEntity(bot, entity)

                if like:
                    print(
                        initialBotSentence,f"Yes! {choice(getResponsePhrase(True, character.likeLevel, False))} This character is {character.description[0]}.")
                    if len(character.description) > 1:
                        print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['next'] = 1
                else:
                    print(
                        initialBotSentence,f"Hmm... I know this character, but {choice(getResponsePhrase(False, character.hateLevel, False))}")
            else:
                # bot does not know
                print(initialBotSentence,"No~ but i am trying to find this character on the internet~")
                desc = getInfoAboutCharacter(entity)
                if desc is None:
                    contexts['waitingTell'] = True
                    print(initialBotSentence,"I cant find it, can you tell what this character is?")
                else:
                    character = addIfDoesNotKnow(bot, entity, False)
                    character.description.extend(desc.split('.'))
                    print(initialBotSentence,f"I found it!\n Here is the character's description: {character.description[0]}")
                    print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['lastOperation'] = 'plot'
                    contexts['next'] = 1
        return

    # check if user is asking for what the bot likes
    hasLike = containsSynonymsOf("like", res)
    if hasLike and 'not' not in res:
        contexts['lastOperation'] = 'like'  # last operation

        if contexts['questionType'] in ('what', 'which'):
            isMovie = True if containsSynonymsOf('movie', res) else False
            if isMovie:
                likes = bot.likes.movies
            else:
                likes = bot.likes.characters
            likes = sorted(likes, key=lambda x: x.likeLevel, reverse=True)

            mostLikes = []
            if len(likes) > 0:
                mostLikes.append(likes[0])
                for i in range(1, len(likes)):
                    if mostLikes[i - 1].likeLevel == likes[i].likeLevel:
                        mostLikes.append(likes[i])
                    else:
                        break

            if len(mostLikes) > 1:  # if there are more than 1 movies/characters with the same like level
                print(
                    initialBotSentence,f"My favorite {'movies' if isMovie else 'characters'} are: {' '.join([m.realName for m in mostLikes])}")
            elif len(mostLikes) == 1:  # if bot knows only one movie/character
                print(initialBotSentence,f"My favorite {'movie' if isMovie else 'character'} is: {mostLikes[0].realName}")
            else:
                if len(caches['movies' if isMovie else 'characters']) > 0:
                    print(initialBotSentence,f"I dont have favorite {'movies' if isMovie else 'characters'}.")
                else:
                    print(initialBotSentence,f"I dont know any {'movies' if isMovie else 'characters'}...")

            return

        # may be asking if the bot like something
        if entity in caches['movies'] or entity in caches['characters']:
            if isMovie and not contexts['movie'] and contexts['character']:
                # do you know who iron man is?   iron man -> character
                # do you like iron man?          iron man -> movie
                # but we know that user is asking for iron man character,
                # so in this situation we need to flip the flag
                isMovie = False
            elif not isMovie and contexts['character'] and contexts['movie']:
                isMovie = True

            # if bot knows this thing
            if isMovie:
                # if it is a movie
                contexts['movie'] = entity
                contexts['character'] = False
                movie_like = getMovieEntity(bot, entity)
                if movie_like is None:
                    # do you like iron man? we dont know if user if talking about the movie or character
                    # but iron man exists in the cache, if it is not a movie, then it is a character
                    respond(bot, entity, False, res)
                    return

                movie, like = movie_like
                if like:
                    # if bot likes it
                    print(
                        initialBotSentence,f"Yes! {choice(getResponsePhrase(True, movie.likeLevel, True))} Here is its description: {movie.description[0]}.")
                    if len(movie.description) > 1:
                        print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['next'] = 1
                else:
                    # if bot hates it
                    print(initialBotSentence,f"Sorry, {choice(getResponsePhrase(False, movie.hateLevel, True))}")
            else:
                # if it is a movie
                contexts['character'] = entity
                contexts['movie'] = False
                character_like = getCharacterEntity(bot, entity)
                if character_like is None:
                    # do you like iron man? we dont know if user if talking about the movie or character
                    # but iron man exists in the cache, so if it is not a character, then is a movie
                    respond(bot, entity, True, res)
                    return

                character, like = character_like
                if like:
                    # if bot likes it
                    print(
                        initialBotSentence,f"Yes! {choice(getResponsePhrase(True, character.likeLevel, False))} This character is: {character.description[0]}.")
                    if len(character.description) > 1:
                        print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['next'] = 1
                else:
                    # if bot hates it
                    print(
                        initialBotSentence,f"Hmm! I know this character, but {choice(getResponsePhrase(False, character.hateLevel, False))}")
        else:
            # bot does not know what is it
            if isMovie:
                print(initialBotSentence,"Sorry, i don't know what is this movie. Can you tell what it is?")
                contexts['movie'] = entity
                contexts['character'] = False
            else:
                print(initialBotSentence,"Sorry, i don't know who is this character, can you tell me something about it?")
                contexts['movie'] = False
                contexts['character'] = entity
            contexts['waitingTell'] = True
        return

    hasHate = containsSynonymsOf("hate", res)
    if hasHate:
        contexts['lastOperation'] = 'hate'  # last operation

        if contexts['questionType'] in ('what', 'which'):
            isMovie = True if containsSynonymsOf('movie', res) else False
            if isMovie:
                dislikes = bot.dislikes.movies
            else:
                dislikes = bot.dislikes.characters
            dislikes = sorted(dislikes, key=lambda x: x.hateLevel, reverse=True)

            mostHates = []
            if len(dislikes) > 0:
                mostHates.append(dislikes[0])
                for i in range(1, len(dislikes)):
                    if mostHates[i - 1].hateLevel == dislikes[i].hateLevel:
                        mostHates.append(dislikes[i])
                    else:
                        break

            if len(mostHates) > 1:  # if there are more than 1 movies/characters with the same like level
                print(
                    initialBotSentence,f"I dont like {'movies' if isMovie else 'characters'} like {' '.join([m.realName for m in mostHates])}")
            elif len(mostHates) == 1:  # if bot knows only one movie/character
                print(initialBotSentence,f"I dont like {'movie' if isMovie else 'character'} {mostHates[0].realName}")
            else:
                if len(caches['movies' if isMovie else 'characters']) > 0:
                    print(initialBotSentence,f"There are no {'movies' if isMovie else 'characters'} that i dont like.")
                else:
                    print(initialBotSentence,f"I dont know any {'movies' if isMovie else 'characters'}...")

            return

        # may be asking if the bot hates something
        if entity in caches['movies'] or entity in caches['characters']:
            # if bot knows this thing
            if isMovie:
                # if it is a movie
                contexts['movie'] = entity
                contexts['character'] = False
                movie, like = getMovieEntity(bot, entity)
                if like:
                    # if bot likes it
                    print(
                        initialBotSentence,f"No! {choice(getResponsePhrase(True, movie.likeLevel, True))} Here is its plot: {movie.description[0]}.")
                    if len(movie.description) > 1:
                        print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['next'] = 1
                else:
                    # if bot hates it
                    print(initialBotSentence,f"Yes, {choice(getResponsePhrase(False, movie.hateLevel, True))}")
            else:
                # if it is a movie
                contexts['character'] = entity
                character, like = getCharacterEntity(bot, entity)
                if like:
                    # if bot likes it
                    print(
                        initialBotSentence,f"No! {choice(getResponsePhrase(True, character.hateLevel, False))} This character is: {character.description[0]}.")
                    if len(character.description) > 1:
                        print(initialBotSentence,"Let me know if you want know more about it!")
                    contexts['next'] = 1
                else:
                    # if bot hates it
                    print(
                        initialBotSentence,f"Yes! I am with you! {choice(getResponsePhrase(False, character.hateLevel, False))}")
        else:
            # bot does not know what is it
            if isMovie:
                print(initialBotSentence,"Sorry, i don't know what is this movie. Can you tell what it is?")
                contexts['movie'] = entity
                contexts['character'] = False
            else:
                print(initialBotSentence,"Sorry, i don't know who is this character, can you tell me something about it?")
                contexts['movie'] = False
                contexts['character'] = entity
            contexts['waitingTell'] = True
        return

    print(initialBotSentence,"Umn?")

    
def resetOtherContext(current):
    for k in contexts:
        if k != current:
            context = contexts[k]
            for i in context:
                context[i] = None




random = random.Random()

onto = loadBotMemoryOnto()
user = onto.user
bot = onto.bot
try:
    caches['movies'] = set(bot.likes.movies)
except:
    bot.likes = onto.likes("loves", namespace=onto, movies=[], characters=[])

try:
    caches['characters'] = set(bot.dislikes.characters)
except:
    bot.dislikes = onto.dislikes("hates", namespace=onto, movies=[], characters=[])

caches['movies'].update(set(bot.dislikes.movies))
caches['characters'].update(set(bot.likes.characters))

print("Loading prolog files...")
prolog = Prolog()
prolog.consult("./who.pl")
prolog.consult("./gramatica.pl")
prolog.consult("./characterNoun.pl")
prolog.consult("./movieNoun.pl")
prolog.consult("./synonyms.pl")

prolog.consult("./hello.pl")
prolog.consult("./bye.pl")
prolog.consult("./wrong.pl")

prolog.consult("./answers grammar.pl")
prolog.consult("./answers grammar ext.pl")
prolog.consult("./question grammar.pl")

print("Prolog files loaded\n")

pipe = list(prolog.query("make."))

if bot.entityName[0] == "":
    setup("bot", onto, prolog)
    setup("user", onto, prolog)
    print(bot.entityName[0] + ": ", "Hello,", user.entityName[0])
else:
    timeTag = getMoAfEv()
    helloMsg = list(prolog.query("phrase(hello(" + timeTag + "),L3)"))
    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in helloMsg]
    answerId = random.randint(0,len(answers)-1)
    response = answers[answerId]
    response = response[0].upper() + response[1:]
    response = response.replace("username",user.entityName[0])
    response = bot.entityName[0] + ": " + response
    print(response)
    
pipe = list(prolog.query("make."))

# start talk loop until bye message

initialBotSentence = bot.entityName[0] + ":"


def extractEntities(question, countLabels, entLists):
    doc = nlp(question)
    ent = None
    for ent in doc.ents:
        countLabels[ent.label_] += 1
        if ent.start_char > 4 and question[ent.start_char - 4: ent.start_char] == 'who':
            # do you know iron man? -> movie
            # do you know who iron is? -> character
            entLists['MARVELCHARACTER'].append((ent, ent.start_char))
        elif (ent.start_char > 6 and ('movie' in question[ent.start_char - 6: ent.start_char]
                                      or 'film' in question[ent.start_char - 6: ent.start_char])):
            # spider man is a super hiro that appears in movie spider man
            # the first spider man is a character, the second is a movie
            entLists['MARVELMOVIE'].append((ent, ent.start_char))
        elif ent.start_char > 10 and 'character' in question[ent.start_char - 10: ent.start_char]:
            entLists['MARVELCHARACTER'].append((ent, ent.start_char))
        else:
            entLists[ent.label_].append((ent, ent.start_char))

    return doc, entLists, ent


def analisEntities(question, countLabels, entLists, ent):
    maxKey = ""
    maxQty = 0
    entList = []
    for key, qty in countLabels.items():
        if maxQty < qty:
            maxQty = qty
            maxKey = key
            entList = entLists[maxKey]
    for key in countLabels:
        countLabels[key] = 0
        entLists[key] = []

    if question.startswith('do') and (question.endswith('it')
                                      or question.endswith('he')
                                      or question.endswith('she')
                                      or question.endswith('this character')
                                      or question.endswith('this movie')):
        movie = True if contexts['movie'] else False
        entList = []
    else:
        movie = False if maxKey == 'MARVELCHARACTER' else True

    return maxKey, maxQty, entList, movie

def checkBye(prolog,question,bot,user,random):
    timeTag = getMoAfEv()
    try:
        checkBye = question.replace(bot.entityName[0],"entity")
        checkBye = checkBye.translate(str.maketrans('', '', string.punctuation))
        checkBye = checkBye.lower().split(" ")
        byeString = f"bye(T,B," + toStr(checkBye) + ",L)"
        lista = list(prolog.query(byeString))[0]
        byeMsg = list(prolog.query("phrase(bye(" + timeTag + ",yes),L3)"))
        answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in byeMsg]
        answerId = random.randint(0,len(answers)-1)
        response = answers[answerId]
        response = response[0].upper() + response[1:]
        response = response.replace("entity",user.entityName[0])
        response = bot.entityName[0] + ": " + response
        print(response)
        return True
    except Exception as e:
        return False

def changeEmotionBasedOnAction(action):
    global emotion
    if(emotion == "happy"):
        if(action == "dislikedFood"):
            emotion = "sad"
    elif(emotion == "satisfied"):
        if(action == "likedFood"):
            emotion = "happy"
        elif(action == "playAGame"):
            emotion = "happy"
        elif(action == "dislikedFood"):
            emotion = "sad"
    elif(emotion == "calm"):
        if(action == "likedFood"):
            emotion = "satisfied"
        elif(action == "playAGame"):
            emotion = "happy"
        elif(action == "dislikedFood"):
            emotion = "sad"
    elif(emotion == "bored"):
        if(action == "likedFood"):
            emotion = "satisfied"
        elif(action == "playAGame"):
            emotion = "satisfied"
        elif(action == "dislikedFood"):
            emotion = "angry"
    elif(emotion == "angry"):
        if(action == "likedFood"):
            emotion = "calm"
        elif(action == "playAGame"):
            emotion = "calm"
    elif emotion == "sad":
        if(action == "likedFood"):
            emotion = "happy"
        elif(action == "playAGame"):
            emotion = "happy"
        elif(action == "dislikedFood"):
            emotion = "angry"

def analysePhraseAndChangeEmotion(phrase):
    global emotion
    global sn
    happy = 0
    satisfied = 0
    calm = 0
    bored = 0
    angry = 0
    sad = 0

    for word in phrase.split(" "):
        try:
            for emotionType,value in sn.sentics(word).items():
                value = float(value)
                if emotionType == "introspection":
                    happy += value
                    satisfied += value
                    bored += value
                    sad += value
                elif emotionType == "temper":
                    calm += value
                    bored += value
                    angry += value
                elif emotionType == "attitude":
                    happy += value
                    satisfied += value
                    bored += value
                    angry += value
                elif emotionType == "sensitivity":
                    happy += value
                    calm += value
                    bored += value
                    sad += value
        except:
            continue
    biggestEmotion = "happy"
    highest = abs(happy)
    if highest < abs(satisfied):
        biggestEmotion = "satisfied"
        highest = abs(satisfied)
    if highest < abs(calm):
        biggestEmotion = "calm"
        highest = abs(calm)
    if highest < abs(bored):
        biggestEmotion = "bored"
        highest = abs(bored)
    if highest < abs(angry):
        biggestEmotion = "angry"
        highest = abs(angry)
    if highest < abs(sad):
        biggestEmotion = "sad"
        highest = abs(sad)
    if highest != 0:
        emotion = biggestEmotion
        print("{You see him",biggestEmotion,"}")


import threading
 
import time

def timer():
    global timePerIteration
    global initialBotSentence
    while(True):
        time.sleep(timePerIteration)
        global stop_threads
        if stop_threads:
            break
        global error
        global counting
        global hungry
        global emotion
        global gaming
        if(gaming):
            counting = 0
        counting += 1
        if counting == 5 and emotion != "sleeping":
            counting = 0
            error = 0
            if emotion == "bored":
                emotion = "sleeping"
                print("\n",initialBotSentence,"I am bored... going to sleep.","\n-", end="")
            else:    
                if emotion == "happy":
                    emotion = "satisfied"
                elif emotion == "satisfied":
                    emotion = "calm"
                elif emotion == "calm":
                    emotion = "bored"
                elif emotion == "angry":
                    emotion = "calm"
                elif emotion == "sad":
                    emotion = "calm"
                hungryFlag = random.randint(0,1)
                if(hungryFlag == 1):
                    hungry = True
                    print("\n",initialBotSentence,"I am hungry","\n-", end="")
                else:
                    hungry = False
        elif counting == 5 and emotion == "sleeping":
            counting = 0
            error = 0
            hungry = True
            emotion = "calm"
            print("\n",initialBotSentence,"Had a great sleep. Let's have breakfast!","\n-", end="")

gaming = False
timePerIteration = 5
emotion = "calm"
counting = 0
error = 0
hungry = False

stop_threads = False
sleep = threading.Thread(target = timer)
sleep.start()

while True:
    question = input("- ")
    counting = 0
    questionList = []
    countLabels = defaultdict(int)
    entLists = defaultdict(list)
    #Check if it is a food or game related frase
    if emotion == "sleeping":
        print(initialBotSentence,"I was sleeping... I hate when you wake me up early.")
        emotion = "angry"
    analysePhraseAndChangeEmotion(question)
    #preparing string for query in prolog
    try:
        questionF = question.translate(str.maketrans('','',string.punctuation))
        questionF = questionF.lower()
        questionList = questionF.split() + ['?']
        queryString = "foodquestion(Command,Food,"+str(questionList)+",L3)"
        #we try to get a valid result
        lista = list(prolog.query(queryString))[0]
        #if we get a valid result we check what command it is
        if(lista["Command"] == 'hungry'):
            if(hungry):
                acceptLista = list(prolog.query("phrase(accepting(yes),L3)"))
                answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in acceptLista]
                answerId = random.randint(0,len(answers)-1)
                print(initialBotSentence,answers[answerId])
                try:
                    if(isinstance(lista['Food'], str)):
                        lista = list(prolog.query("phrase(foodanswer(yes,_," + lista["Food"] + "),L3)"))
                        changeEmotionBasedOnAction("dislikedFood")
                    else:
                        lista = list(prolog.query("phrase(foodanswer(yes,like,_),L3)"))
                        changeEmotionBasedOnAction("likedFood")
                    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                    answerId = random.randint(0,len(answers)-1)
                    print(initialBotSentence,answers[answerId])
                except Exception as err:
                    pass
                hungry = False
            else:
                print(initialBotSentence,"No I am full.")
            continue
        elif(lista["Command"] == 'like_certain_food'):
            try:
                lista = list(prolog.query("phrase(foodanswer(no,Feeling," + lista["Food"] + "),L3)"))
                answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                answerId = random.randint(0,len(answers)-1)
                print(initialBotSentence,answers[answerId])
                continue
            except Exception as err:
                pass
        elif(lista["Command"] == 'likes_which_food'):
            try:
                lista = list(prolog.query("phrase(foodanswer(no,like,Food),L3)"))
                answers = {}
                for result in lista:
                    try:
                        answers[result["Food"]] += [" ".join([decodeStringIfPossible(word) for word in result["L3"]])]
                    except:
                        answers[result["Food"]] = [" ".join([decodeStringIfPossible(word) for word in result["L3"]])]
                for food in answers:
                    answerId = random.randint(0,len(answers[food])-1)
                    print(initialBotSentence,answers[food][answerId])
                continue
            except Exception as err:
                pass
        elif(lista["Command"] == 'dislikes_which_food'):
            try:
                lista = list(prolog.query("phrase(foodanswer(no,dislike,Food),L3)"))
                answers = {}
                for result in lista:
                    try:
                        answers[result["Food"]] += [" ".join([decodeStringIfPossible(word) for word in result["L3"]])]
                    except:
                        answers[result["Food"]] = [" ".join([decodeStringIfPossible(word) for word in result["L3"]])]
                for food in answers:
                    answerId = random.randint(0,len(answers[food])-1)
                    print(initialBotSentence,answers[food][answerId])
                continue
            except Exception as err:
                pass
        elif([lista["Command"] == 'want_to_play']):
            lista = list(prolog.query("phrase(accepting(yes),L3)"))
            answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
            answerId = random.randint(0,len(answers)-1)
            print(initialBotSentence,answers[answerId])
            gaming = True
            game.start()
            gaming = False
            changeEmotionBasedOnAction("playAGame")
            continue
    except Exception as e:
        try:
            questionQuery = "question(positive_directed,"+str(questionList[0:2])+",L3)"
            lista = list(prolog.query(questionQuery))[0]
            if(questionList[2] == "like"):
                food = questionList[3:len(questionList)-1]
                foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
            else:
                if(questionList[4] == "eat"):
                    food = questionList[5:len(questionList)-1]
                    foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
                else:
                    food = questionList[3:len(questionList)-1]
                    foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
            doc, entLists, ent = extractEntities(questionF, countLabels, entLists)
            if(food not in games and len(entLists.keys()) == 0):
                lista = list(prolog.query("phrase(nevertried(" + "_".join(food) + "),L3)"))
                answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                answerId = random.randint(0,len(answers)-1)
                print(initialBotSentence,answers[answerId].replace("_"," "))
                if(random.randint(0,1) == 0):
                    like = "dislike"
                    changeEmotionBasedOnAction("dislikedFood")
                    with open("./answers grammar ext.pl","a") as grammar:
                        grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                    pipe = list(prolog.query("make."))
                
                    lista = list(prolog.query("phrase(foodanswer(yes,Feeling," + foodTag + "),L3)"))
                    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                    answerId = random.randint(0,len(answers)-1)
                    print(initialBotSentence,answers[answerId])
                    hungry = False
                    continue
                
                else:
                    like = "like"
                    changeEmotionBasedOnAction("likedFood")
                    with open("./answers grammar ext.pl","a") as grammar:
                        grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                    pipe = list(prolog.query("make."))
                
                    lista = list(prolog.query("phrase(foodanswer(yes,Feeling," + foodTag + "),L3)"))
                    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                    answerId = random.randint(0,len(answers)-1)
                    print(initialBotSentence,answers[answerId])
                    hungry = False
                    continue
        except Exception as e:
            pass
        
    # preparing string for query in prolog
    try:
        if len(question) > 0 and question[-1] == "?":
            question = question.translate(str.maketrans('', '', string.punctuation))
            question = question.lower()
            question = ' '.join([i.lemma_ for i in nlp2(question)])  # convert verbs to infinitive
            # question
            doc, entLists, ent = extractEntities(question, countLabels, entLists)

            maxKey, maxQty, entList, movie = analisEntities(question, countLabels, entLists, ent)
            for idx, ent in enumerate(entList):
                question = question[0:ent[1]] + "<ENTITY" + str(idx) + ">" + question[(ent[1] + len(ent[0].text)):]
            try:
                if entList:
                    entity = entList[0][0].text
            
                    if 'which' in question or 'what' in question:
                        question2 = question[:entList[0][1]] + question[entList[0][1] + len(entity) + 1:]
                        doc2 = nlp2(question2)
                        for t in whichMovies:
                            if t.similarity(doc2) >= 0.9:
                                contexts['whichMovie'] = True
                                break
            
                if not contexts['whichMovie']:
                    questionList = question.split()
                    for idx, token in enumerate(questionList):
                        if token.startswith("<ENTITY"):
                            questionList[idx] = "\"" + entList[int(token[7:8])][0].text + "\""

                    queryString = f"sentenceQuestion(Q,S,V," + toStr(questionList) + ",L)"

                    # we try to get a valid result
                    lista = list(prolog.query(queryString))
                else:
                    lista = [{'Q': question.split()[0], 'V': [], "S": [], "L": []}]
                
                if len(lista) > 0:
                    lista = lista[0]
                    # if we get a valid result we check what question it is
                    res = parsePrologResult(lista['V'])
                    res.update(parsePrologResult(lista['S']))
                    res.update(parsePrologResult(lista['L']))
                    if not contexts['whichMovie']:
                        for t in tell:
                            if t.similarity(
                                    doc) >= 0.88 and 'more' in question:  # user want to know more about the movie/character
                                contexts['plot'] = True
                                break
                    if question.startswith('do'):
                        contexts['questionType'] = 'do'
                    elif lista["Q"] == "what":
                        contexts['questionType'] = 'what'
                    elif lista["Q"] == "which":
                        contexts['questionType'] = 'which'
                    elif lista['Q'] == 'have':
                        contexts['questionType'] = 'have'
                        if 'see' in res:
                            contexts['character'] = False
                            if entList:
                                contexts['movie'] = entList[0][0].text
                            res.remove('see')
                            res.add('know')
                    else:
                        pass

                    if not entList:
                        respond(bot, contexts['movie'] if movie else contexts['character'], movie, res)
                    else:
                        respond(bot, entList[0][0].text, movie, res)
                    onto.save()
                else:
                    print(initialBotSentence,getDontUnderstand(prolog,error))
                    error += 1
            except Exception as e:
                
                pipe = list(prolog.query("make."))
                # onto.save()
                print("here?",e)
                traceback.print_exc() 

        else:

            question = question.translate(str.maketrans('', '', string.punctuation))
            question = question.lower()
            question = ' '.join([i.lemma_ for i in nlp2(question)])  # convert verbs to infinitive

            if len(question) == 0 and contexts['lastOperation'] == 'plot':
                # user can get more plots inserting black msg
                contexts['plot'] = True
                respond(bot)
            elif contexts['waitingTell']:
                # bot is waiting for the user to tell it what the character/movie  is
                # question
                doc, entLists, ent = extractEntities(question, countLabels, entLists)

                index = question.find(' be ')
                start = question[:index]  # initial part of the sentence

                if contexts['character']:
                    # if the last question was about character, but bot didn't know who he is

                    # try to find where the description ends using the following possible sentences
                    delimiters = ['that appear in movie', 'that appear in movie',
                                  'who appear in movie', 'who appear in movie', 'appear in']

                    # verify if the sentence is describing the character
                    if contexts['character'] in start or 'he' in start or 'she' in start or 'it' in start:
                        minDelimiterIndex = len(question)
                        if 'MARVELMOVIE' in entLists:
                            minMovieIndex = min([i[1] for i in entLists['MARVELMOVIE']])
                            minDelimiterIndex = 1 << 31
                            for d in delimiters:
                                i = question.find(d)
                                if i != -1:
                                    minDelimiterIndex = min(minDelimiterIndex, i)
                            if minDelimiterIndex == 1 << 31:
                                minDelimiterIndex = len(question)

                        contexts['tell'] = {'movie': entLists['MARVELMOVIE'],
                                            'character': entLists['MARVELCHARACTER'],
                                            'description': question[index + 4: minDelimiterIndex]}
                        respond(bot, isMovie=False)
                    else:
                        if(checkBye(prolog,question,bot,user,random)):
                            break
                        print('Uhm?')

                else:
                    if contexts['movie'] in start or 'it' in start:
                        contexts['tell'] = {'movie': [],
                                            'character': [],
                                            'description': question[index + 4:]}
                        respond(bot, isMovie=True)
                    else:
                        if(checkBye(prolog,question,bot,user,random)):
                            break
                        print('Uhm?')

            else:
                #checking if it is a bye message
                if(checkBye(prolog,question,bot,user,random)):
                    break
                
                # tell me about xxx
                # tell me more about xxx
                doc, entLists, ent = extractEntities(question, countLabels, entLists)
                maxKey, maxQty, entList, movie = analisEntities(question, countLabels, entLists, ent)

                if len(question) > 0:
                    for t in tell:
                        if t.similarity(
                                doc) >= 0.88 and 'more' in question:  # user want to know more about the movie/character
                            contexts['plot'] = True
                            respond(bot, movie)
                            break
                print(initialBotSentence,getDontUnderstand(prolog,error))
                error += 1
            onto.save()
            # print(initialBotSentence, "OOF", question)
    except Exception as e:
        print(e)

stop_threads = True
sleep.join()
