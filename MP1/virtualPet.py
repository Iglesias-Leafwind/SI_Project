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

#initializing checkers
lastMoves = 100
cwd = os.getcwd()
cwd += "/checkersWins.owl"
game = checkers(cwd,lastMoves,False)      

#converts a list of strings into a single string replacing spaceChar by _Char
def convertListOfStringsToSingleDividedByUnderscore(stringList):
    returning = ""
    for indx,stringElement in enumerate(stringList):
        if(indx == 0):
            returning += stringElement
        else:
            returning += "_" + stringElement
    return returning

#tries to decode a byte string into a normal string
def decodeStringIfPossible(element):
    try:
        return element.decode("utf-8")
    except:
        return element
#my own array to string contructor
def toStr(answerList):
    ret = "["
    size = len(answerList)
    for indx,word in enumerate(answerList):
        ret += word
        if indx != size-1:
            ret += ","
    ret += "]"
    return ret

#checks if person food answer is correct
def correctFoodAnswer(prolog,answerList):

    try:
        lista = list(prolog.query("foodanswercheck(Feeling," + toStr(answerList[0:2]) + ",L3)"))[0]
        return 2
    except:
        try:
            lista = list(prolog.query("foodanswercheck(Feeling," + toStr(answerList[0:3]) + ",L3)"))[0]
            return 3
        except:
            try:
                lista = list(prolog.query("foodanswercheck(Feeling," + toStr(answerList[0:4]) + ",L3)"))[0]
                return 4
            except:
                return None
                             
#initializing variables
random = random.Random()
prolog = Prolog()
prolog.consult("./answers grammar.pl")
prolog.consult("./answers grammar ext.pl")
prolog.consult("./question grammar.pl")
pipe = list(prolog.query("make."))

#creating temp wrong answers (TODO create a grammar for saying wrong answers)
wrong = ["I'm sorry I didn't quite catch what you said could you please repeat?","Please repeat.","What?","I guess I am deaf..."]
#tells us if the virtual pet is hungry or not
hungry = False
#tells us the passage of time for the pet currently as 1 time frame is 1 action
#TODO we can just create a separate thread that will count time after a while the bot changes state
counting = 0
#TODO add bot moods
#TODO create more hello messages and create a 1st time hello message if person name isn't recorded
print("Hello, I am Chatbot! Pleased to meat you.")
print("Currently you can only talk to me about food I like or dislike and if I want to eat or play checkers")
#start talk loop until bye message
#TODO add bye grammar message
games = ["checkers"]
questions_bot_asks =  ["likes_which_food","dislikes_which_food","want_to_play"]

while(True):
    question = input("- ")
    #preparing string for query in prolog
    question = question.translate(str.maketrans('','',string.punctuation))
    question = question.lower()
    questionList = question.split() + ['?']
    queryString = "foodquestion(Command,Food,"+str(questionList)+",L3)"
    try:
        #we try to get a valid result
        lista = list(prolog.query(queryString))[0]
        #if we get a valid result we check what command it is
        if(lista["Command"] == 'hungry'):
            if(hungry):
                acceptLista = list(prolog.query("phrase(accepting(yes),L3)"))
                answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in acceptLista]
                answerId = random.randint(0,len(answers)-1)
                print(answers[answerId])
                try:
                    if(isinstance(lista['Food'], str)):
                        lista = list(prolog.query("phrase(foodanswer(yes,_," + lista["Food"] + "),L3)"))
                    else:
                        lista = list(prolog.query("phrase(foodanswer(yes,like,_),L3)"))
                    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                    answerId = random.randint(0,len(answers)-1)
                    print(answers[answerId])
                except Exception as err:
                    print(err)
                hungry = False
            else:
                print("No I am full.")
        elif(lista["Command"] == 'like_certain_food'):
            try:
                lista = list(prolog.query("phrase(foodanswer(no,Feeling," + lista["Food"] + "),L3)"))
                answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                answerId = random.randint(0,len(answers)-1)
                print(answers[answerId])
            except Exception as err:
                print(err)
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
                    print(answers[food][answerId])
            except Exception as err:
                print(err)
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
                    print(answers[food][answerId])
            except Exception as err:
                print(err)
        elif([lista["Command"] == 'want_to_play']):
            lista = list(prolog.query("phrase(accepting(yes),L3)"))
            answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
            answerId = random.randint(0,len(answers)-1)
            print(answers[answerId])
            game.start()
    except Exception as e:
        # print(e)
        # printing stack trace
        # traceback.print_exc()                        
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
            if(food not in games):
                lista = list(prolog.query("phrase(nevertried(" + "_".join(food) + "),L3)"))
                answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                answerId = random.randint(0,len(answers)-1)
                print(answers[answerId].replace("_"," "))
                if(random.randint(0,1) == 0):
                    like = "dislike"
                    with open("./answers grammar ext.pl","a") as grammar:
                        grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                    pipe = list(prolog.query("make."))
                
                    lista = list(prolog.query("phrase(foodanswer(yes,Feeling," + foodTag + "),L3)"))
                    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                    answerId = random.randint(0,len(answers)-1)
                    print(answers[answerId])
                    hungry = False
                
                else:
                    like = "like"
                    with open("./answers grammar ext.pl","a") as grammar:
                        grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                    pipe = list(prolog.query("make."))
                
                    lista = list(prolog.query("phrase(foodanswer(yes,Feeling," + foodTag + "),L3)"))
                    answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                    answerId = random.randint(0,len(answers)-1)
                    print(answers[answerId])
                    hungry = False
        except Exception as e:
            wrongId = random.randint(0,len(wrong)-1)
            print(wrong[wrongId])
            
    if counting == 2:
        counting = 0
        if(random.randint(0,1) == 1):
            if(not hungry):
                hungry = True
                print("I am hungry can we eat something?")
            else:
                print("Let's eaaaaat I want BUUUUUUUUURGEEEEEEEERS")
        else:
            question = questions_bot_asks[random.randint(0,len(questions_bot_asks)-1)]
            lista = list(prolog.query("phrase(askquestion("+question+",Game),L3)"))
            sentence = lista[random.randint(0,len(lista)-1)]
            answer = " ".join([decodeStringIfPossible(word) for word in sentence["L3"]])
            print(answer)
            if(question == "likes_which_food"):
                while(True):
                    answer = input("- ")
                    #preparing string for query in prolog
                    answer = answer.translate(str.maketrans('','',string.punctuation))
                    answer = answer.lower()
                    answer = answer.replace(" i "," \"I\" ")
                    answer = answer.replace("i ","\"I\" ")
                    answerList = answer.split()
                    try:
                        food = correctFoodAnswer(prolog,answerList)
                        food = answerList[food:]
                        foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
                        answerString = "name(Food,Feeling,"+ toStr(food) +",L3)"
                        #we try to get a valid result
                        lista = list(prolog.query(answerString))[0]
                        print("I",lista["Feeling"],lista["Food"])
                        #TODO save food user likes
                        break
                    except Exception as e:
                        # print(e)
                        # printing stack trace
                        # traceback.print_exc()
                        food = correctFoodAnswer(prolog,answerList)
                        if(food != None):
                            food = answerList[food:]
                            foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
                            lista = list(prolog.query("phrase(nevertried(" + "_".join(food) + "),L3)"))
                            answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                            answerId = random.randint(0,len(answers)-1)
                            print(answers[answerId].replace("_"," "))
                            if(random.randint(0,1) == 0):
                                like = "dislike"
                                with open("./answers grammar ext.pl","a") as grammar:
                                    grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                                pipe = list(prolog.query("make."))
                                
                            else:
                                like = "like"
                                with open("./answers grammar ext.pl","a") as grammar:
                                    grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                                pipe = list(prolog.query("make."))
                            #TODO save food user likes
                            break
                        else:
                            wrongId = random.randint(0,len(wrong)-1)
                            print(wrong[wrongId])
            elif(question == "dislikes_which_food"):
                while(True):
                    answer = input("- ")
                    #preparing string for query in prolog
                    answer = answer.translate(str.maketrans('','',string.punctuation))
                    answer = answer.lower()
                    answer = answer.replace(" i "," \"I\" ")
                    answer = answer.replace("i ","\"I\" ")
                    answer = answer.replace(" dont "," don't ")
                    answerList = answer.split()
                    try:
                        food = correctFoodAnswer(prolog,answerList)
                        food = answerList[food:]
                        foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
                        answerString = "name(Food,Feeling,"+ toStr(food)+",L3)"
                        #we try to get a valid result
                        lista = list(prolog.query(answerString))[0]
                        print("I",lista["Feeling"],lista["Food"])
                        #TODO save food user dislikes
                        break
                    except Exception as e:
                        # print(e)
                        # printing stack trace
                        # traceback.print_exc()
                        food = correctFoodAnswer(prolog,answerList)
                        if(food != None):
                            food = answerList[food:]
                            foodTag = convertListOfStringsToSingleDividedByUnderscore(food)
                            lista = list(prolog.query("phrase(nevertried(" + "_".join(food) + "),L3)"))
                            answers = [" ".join([decodeStringIfPossible(word) for word in sentence["L3"]]) for sentence in lista]
                            answerId = random.randint(0,len(answers)-1)
                            print(answers[answerId].replace("_"," "))
                            if(random.randint(0,1) == 0):
                                like = "dislike"
                                with open("./answers grammar ext.pl","a") as grammar:
                                    grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                                pipe = list(prolog.query("make."))
                                
                            else:
                                like = "like"
                                with open("./answers grammar ext.pl","a") as grammar:
                                    grammar.write("\nfoodextension("+foodTag+","+like+") --> "+str(food)+".")
                                pipe = list(prolog.query("make."))
                            #TODO save food user dislikes
                            break
                        else:
                            wrongId = random.randint(0,len(wrong)-1)
                            print(wrong[wrongId])
            elif(question == "want_to_play"):
                while(True):
                    try:
                        answer = input("- ")
                        #preparing string for query in prolog
                        answer = answer.translate(str.maketrans('','',string.punctuation))
                        answer = answer.lower()
                        answer.replace(" i "," \"I\" ")
                        answerList = answer.split()
                        answerString = "accepting(Acceptance,"+str(answerList)+",L3)"
                        #we try to get a valid result
                        lista = list(prolog.query(answerString))[0]
                        if(lista["Acceptance"] == "yes"):
                            game.start()
                        else:
                            print("ok :c")
                        break
                    except:
                        wrongId = random.randint(0,len(wrong)-1)
                        print(wrong[wrongId])
        
    else:
        counting += 1
