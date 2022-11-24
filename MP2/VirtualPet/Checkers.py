import random
from checkers.game import Game
from owlready2 import *

from pyswip import Prolog, Functor, Query, Variable, call, Atom
import time
import os
import string

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
def toStr(answerList,v1=False):
    ret = "["
    size = len(answerList)
    for indx, word in enumerate(answerList):
        if(v1):
            ret += word
        else:
            ret += "'"+ word + "'"
        if indx != size - 1:
            ret += ","
    ret += "]"
    return ret

class checkers:
    #numLastMoves = 0 then it will ignore last moves
    #numLastMoves > 0 then it will check last moves
    def __init__(self,file_path,numLastMoves,debug=False):
        onto_path.append("/")
        ontology_path = "file://" + file_path
        onto = get_ontology(ontology_path)
        onto.load()
        ontology_path += "#"
        self.prolog = Prolog()
        self.prolog.consult("./checkers.pl")
        self.prolog.consult("./bye.pl")

        pipe = list(self.prolog.query("make."))

        try:
            if(onto.base_iri != ontology_path):
                onto.base_iri = ontology_path
        except:
            pass
        
        with onto:
            class wins(Thing):
                pass

            class winPath(Thing):
                pass

            class has_win(wins >> winPath):
                pass
            
            class path(Thing):
                pass
            
            class has_path(winPath >> path):
                pass
            
            class move(Thing):
                pass
            
            class has_loser_moves(path >> move):
                pass
            
            class has_moves(path >> move):
                pass
        
        self.debug = debug
        self.numLastMoves = numLastMoves
        self.ontology = onto
        self.numberToLetter = ["","8B","8D","8F","8H","7A","7C","7E","7G","6B","6D","6F","6H","5A","5C","5E","5G","4B","4D","4F","4H","3A","3C","3E","3G","2B","2D","2F","2H","1A","1C","1E","1G"]
    def checkBye(self,question):
        try:
            checkBye = question.translate(str.maketrans('', '', string.punctuation))
            checkBye = checkBye.lower().split(" ")
            byeString = f"bye(T,B," + toStr(checkBye) + ",L)"
            lista = list(self.prolog.query(byeString))[0]
            return True
        except Exception as e:
            return False
            
    def start(self):
        letterToNumber = {"8B":1,"8D":2,"8F":3,"8H":4,"7A":5,"7C":6,"7E":7,"7G":8,"6B":9,"6D":10,"6F":11,"6H":12,"5A":13,"5C":14,"5E":15,"5G":16,"4B":17,"4D":18,"4F":19,"4H":20,"3A":21,"3C":22,"3E":23,"3G":24,"2B":25,"2D":26,"2F":27,"2H":28,"1A":29,"1C":30,"1E":31,"1G":32}
        #0 - black 1 - white
        side = random.randint(0,1)
        self.valid_paths = []
        self.move = 0
        self.moves = {1:[],2:[]}
        game = Game()
        self.game = game
        onto = self.ontology
        if side:
            print("You start with the whites!")
            side = 1
            self.side = 1
            for winPath in onto.black.has_win:
                self.valid_paths.append((winPath.has_moves,winPath.has_loser_moves))
        else:
            print("You start with the blacks!")
            side = 2
            self.side = 2
            for winPath in onto.white.has_win:
                self.valid_paths.append((winPath.has_moves,winPath.has_loser_moves))
            self.aiMove(letterToNumber)
            
        while(not game.is_over()):
            while(side == game.whose_turn()):
                board = self.updateBoard(game)
                self.printBoard(board)
                print("What do you want to move?")
                possible_moves = game.get_possible_moves()
                while(True):
                    move = input("# ")
                    if(self.checkBye(move)):
                        return
                    try:
                        move = move.translate(str.maketrans('', '', string.punctuation)).lower().split(" ")
                        moveString = f"checkersmoveC(From,To," + toStr(move) + ",L)"
                        lista = list(self.prolog.query(moveString))[0]
                        moves = [decodeStringIfPossible(lista["From"]).upper()]
                        moves.append(decodeStringIfPossible(lista["To"]).upper())
                    except Exception as e:
                        print("Invallid response for example say: 'Move " + self.numberToLetter[possible_moves[0][0]] + " to " + self.numberToLetter[possible_moves[0][1]] + "'")
                        while(True):
                            #not a valid move
                            move = input("# ")
                            if(self.checkBye(move)):
                                return
                            try:
                                move = move.translate(str.maketrans('', '', string.punctuation)).lower().split(" ")
                                moveString = f"checkersmoveC(From,To," + toStr(move) + ",L)"
                                lista = list(self.prolog.query(moveString))[0]
                                moves = [decodeStringIfPossible(lista["From"]).upper()]
                                moves.append(decodeStringIfPossible(lista["To"]).upper())
                                break
                            except:
                                print("No no no no for example say: 'Move " + self.numberToLetter[possible_moves[0][0]] + " to " + self.numberToLetter[possible_moves[0][1]] + "'")
                        
                    if(moves[0] in letterToNumber and moves[1] in letterToNumber):
                        moving = [letterToNumber[moves[0]],letterToNumber[moves[1]]]
                        if(moving in possible_moves):
                            break
                    print("That isn't a valid move the houses you can move to are the ones marked with x.")
                    print("And only the pieces diagonly and directly near the x can move to it.")
                self.registerMove(game.whose_turn(),moving)
                game.move(moving)
            if(game.is_over()):
                break
            self.aiMove(letterToNumber)
            while(side != game.whose_turn()):
                self.aiMove(letterToNumber)

        winner = game.get_winner()
        if(winner == side):
            print("Congratulations you won!")
        elif(winner == None):
            print("Its a tie lmao...")
        else:
            print("Ha Ha I win!")
            
        if(winner == 1):
            ontoWinner = onto.white
            loser = 2
        elif(winner == 2):
            ontoWinner = onto.black
            loser = 1
        else:
            return
        history = self.moves[winner]
        
        ontoWinner.has_win.append(onto.winPath(namespace = onto, has_moves = []))
        ontoWinPath = ontoWinner.has_win[len(ontoWinner.has_win)-1]
        for indx in range(0,len(history)):
            ontoWinPath.has_moves.append(onto.move(history[indx], namespace = onto))
        history = self.moves[loser]
        for indx in range(0,len(history)):
            ontoWinPath.has_loser_moves.append(onto.move(history[indx], namespace = onto))
        try:
            onto.save()
        except:
            pass
        return
    
    def aiMove(self,letterToNumber):
        game = self.game
        validPaths = self.valid_paths
        newValidPaths = []
        validMoves = {}
        move = self.move
        total_paths = 0
        gamePossibleMoves = game.get_possible_moves()
        possibleMovesKeys = self.convertMoves(gamePossibleMoves)
        for path in validPaths:
            try:
                if(path[0][move].name in possibleMovesKeys):
                    if(self.numLastMoves == 0 or self.moves[self.side] == []):
                        try:
                            validMoves[path[0][move].name] += 1
                        except:
                            validMoves[path[0][move].name] = 1
                    else:
                        lastHistoryMoves = self.moves[self.side][-self.numLastMoves:]
                        numHistoryMoves = len(self.moves[self.side])
                        rememberLastMoves = [onto_path.name for onto_path in path[1][max(0,numHistoryMoves-3):numHistoryMoves]]
                        flag = True
                        for indxLastMove in range(0,min(self.numLastMoves,numHistoryMoves)):
                            if(rememberLastMoves[indxLastMove] != lastHistoryMoves[indxLastMove]):
                                flag = False
                                break
                        if(flag):
                            try:
                                validMoves[path[0][move].name] += 1
                            except:
                                validMoves[path[0][move].name] = 1
                    total_paths += 1
                newValidPaths.append(path)
            except:
                continue
        if(self.debug):
            print(validMoves)
        self.valid_paths = newValidPaths
        moving = []
        if(validMoves != {}):
            probabilityAccumulator = 0
            newValidMoves = {}
            moveProb = random.randint(1,total_paths)/total_paths
            for moveKey in possibleMovesKeys:
                if(moveKey not in validMoves):
                    continue
                probabilityAccumulator += validMoves[moveKey]
                if(moveProb <= (probabilityAccumulator/total_paths)):
                    moving.append(letterToNumber[moveKey[0]+moveKey[1]])
                    moving.append(letterToNumber[moveKey[3]+moveKey[4]])
                    break
        
        if moving == []:
            moving = gamePossibleMoves[random.randint(0,len(gamePossibleMoves)-1)]
        self.registerMove(game.whose_turn(),moving)
        game.move(moving)
        self.move += 1

    def convertMoves(self,possibleMoves):
        convertedMoves = []
        for move in possibleMoves:
            convertedMoves.append(self.convertSingleMove(move))
        return convertedMoves
    
    def registerMove(self,side,move):
        self.moves[side].append(self.convertSingleMove(move))
        
    def convertSingleMove(self,move):
        return self.numberToLetter[move[0]] + "-" + self.numberToLetter[move[1]]
        
    def updateBoard(self,game):
        board = {}
        numbToLetter = self.numberToLetter
        for piece in game.board.pieces:
            if(not piece.captured):
                if(piece.player == 1):
                    if(piece.king):
                        board[numbToLetter[piece.position]] = " W "
                    else:
                        board[numbToLetter[piece.position]] = " w "
                else:
                    if(piece.king):
                        board[numbToLetter[piece.position]] = " B "
                    else:
                        board[numbToLetter[piece.position]] = " b "
        for move in game.get_possible_moves():
            board[numbToLetter[move[1]]] = " x "
            board[numbToLetter[move[0]]] = "~" + board[numbToLetter[move[0]]][1] + "~"
        for house in numbToLetter[1:]:
            if (house not in board):
                board[house] = "   "
        return board
    
    def checkPiece(self,piece):
        return len(piece) == 2 and piece[0] in ["1","2","3","4","5","6","7","8"] and piece[1] in ["A","B","C","D","E","F","G","H"]
    
    def printBoard(self,board):
        print("---A---B---C---D---E---F---G---H---")
        print(f'8|   |{board["8B"]}|   |{board["8D"]}|   |{board["8F"]}|   |{board["8H"]}|8')
        print(f'7|{board["7A"]}|   |{board["7C"]}|   |{board["7E"]}|   |{board["7G"]}|   |7')
        print(f'6|   |{board["6B"]}|   |{board["6D"]}|   |{board["6F"]}|   |{board["6H"]}|6')
        print(f'5|{board["5A"]}|   |{board["5C"]}|   |{board["5E"]}|   |{board["5G"]}|   |5')
        print(f'4|   |{board["4B"]}|   |{board["4D"]}|   |{board["4F"]}|   |{board["4H"]}|4')
        print(f'3|{board["3A"]}|   |{board["3C"]}|   |{board["3E"]}|   |{board["3G"]}|   |3')
        print(f'2|   |{board["2B"]}|   |{board["2D"]}|   |{board["2F"]}|   |{board["2H"]}|2')
        print(f'1|{board["1A"]}|   |{board["1C"]}|   |{board["1E"]}|   |{board["1G"]}|   |1')
        print("---A---B---C---D---E---F---G---H---")

    def trainAI(self,randomMovesFlag):
        letterToNumber = {"8B":1,"8D":2,"8F":3,"8H":4,"7A":5,"7C":6,"7E":7,"7G":8,"6B":9,"6D":10,"6F":11,"6H":12,"5A":13,"5C":14,"5E":15,"5G":16,"4B":17,"4D":18,"4F":19,"4H":20,"3A":21,"3C":22,"3E":23,"3G":24,"2B":25,"2D":26,"2F":27,"2H":28,"1A":29,"1C":30,"1E":31,"1G":32}
        #0 - black 1 - white
        side = random.randint(0,1)
        self.valid_paths = []
        self.enemy_paths = []
        self.move = 0
        self.moves = {1:[],2:[]}
        game = Game()
        self.game = game
        onto = self.ontology
        if side:
            side = 1
            self.side = 1
            for winPath in onto.black.has_win:
                self.valid_paths.append((winPath.has_moves,winPath.has_loser_moves))
            for winPath in onto.white.has_win:
                self.enemy_paths.append((winPath.has_moves,winPath.has_loser_moves))
        else:
            side = 2
            self.side = 2
            for winPath in onto.white.has_win:
                self.valid_paths.append((winPath.has_moves,winPath.has_loser_moves))
            for winPath in onto.black.has_win:
                self.enemy_paths.append((winPath.has_moves,winPath.has_loser_moves))
            self.aiMove(letterToNumber)
            
        while(not game.is_over()):
            while(side == game.whose_turn()):
                possible_moves = game.get_possible_moves()
                if(randomMovesFlag):
                    moving = possible_moves[random.randint(0,len(possible_moves)-1)]
                    self.registerMove(game.whose_turn(),moving)
                    game.move(moving)
                else:
                    self.trainEnemyAi(letterToNumber)
            if(game.is_over()):
                break
            self.aiMove(letterToNumber)
            while(side != game.whose_turn()):
                self.aiMove(letterToNumber)

        winner = game.get_winner()

        if(winner == 1):
            ontoWinner = onto.white
            loser = 2
        elif(winner == 2):
            ontoWinner = onto.black
            loser = 1
        else:
            return

        history = self.moves[winner]
            
        ontoWinner.has_win.append(onto.winPath(namespace = onto, has_moves = []))
        ontoWinPath = ontoWinner.has_win[len(ontoWinner.has_win)-1]
        for indx in range(0,len(history)):
            ontoWinPath.has_moves.append(onto.move(history[indx], namespace = onto))
        history = self.moves[loser]
        for indx in range(0,len(history)):
            ontoWinPath.has_loser_moves.append(onto.move(history[indx], namespace = onto))
        
        return

    def trainEnemyAi(self,letterToNumber):
        game = self.game
        validPaths = self.enemy_paths
        newValidPaths = []
        validMoves = {}
        move = self.move
        total_paths = 0
        if(self.side == 1):
            side = 2
        else:
            side = 1
        gamePossibleMoves = game.get_possible_moves()
        possibleMovesKeys = self.convertMoves(gamePossibleMoves)
        for path in validPaths:
            try:
                if(path[0][move].name in possibleMovesKeys):
                    if(self.numLastMoves == 0 or self.moves[side] == []):
                        try:
                            validMoves[path[0][move].name] += 1
                        except:
                            validMoves[path[0][move].name] = 1
                    else:
                        lastHistoryMoves = self.moves[side][-self.numLastMoves:]
                        numHistoryMoves = len(self.moves[side])
                        rememberLastMoves = [onto_path.name for onto_path in path[1][max(0,numHistoryMoves-3):numHistoryMoves]]
                        flag = True
                        for indxLastMove in range(0,min(self.numLastMoves,numHistoryMoves)):
                            if(rememberLastMoves[indxLastMove] != lastHistoryMoves[indxLastMove]):
                                flag = False
                                break
                        if(flag):
                            try:
                                validMoves[path[0][move].name] += 1
                            except:
                                validMoves[path[0][move].name] = 1
                    total_paths += 1
                newValidPaths.append(path)
            except:
                continue
        if(self.debug):
            print(validMoves)
        self.valid_paths = newValidPaths
        moving = []
        if(validMoves != {}):
            probabilityAccumulator = 0
            newValidMoves = {}
            moveProb = random.randint(1,total_paths)/total_paths
            for moveKey in possibleMovesKeys:
                if(moveKey not in validMoves):
                    continue
                probabilityAccumulator += validMoves[moveKey]
                if(moveProb <= (probabilityAccumulator/total_paths)):
                    moving.append(letterToNumber[moveKey[0]+moveKey[1]])
                    moving.append(letterToNumber[moveKey[3]+moveKey[4]])
                    break
        
        if moving == []:
            moving = gamePossibleMoves[random.randint(0,len(gamePossibleMoves)-1)]
        self.registerMove(game.whose_turn(),moving)
        game.move(moving)
        self.move += 1
        
    def changeLastMoves(self,numLastMoves):
        self.numLastMoves = numLastMoves
        
if(__name__ == "__main__"):
    cwd = os.getcwd()
    cwd += "/checkersWins.owl"
    train = False
    lastMoves = 3
    randomMovesFlag = True
    debug = False
    forever = False
    game = checkers(cwd,lastMoves,debug)
    if(train):
        #train AI
        total = 100
        while(True):
            counter = 0
            for i in range(0,total):
                start = time.time()
                for lastNumMoves in range(0,lastMoves):
                    game.trainAI(randomMovesFlag)
                counter += 1
                took = time.time()-start
                if((counter % (total/10)) == 0):
                    print((total - counter)*lastMoves,(total - counter)*took)
                    onto.save()
                start = time.time()
            if(forever):
                print("currently doing: ",total*lastMoves)
            else:
                total *= 10
                if(input("Next total will be -> "+str(total*lastMoves)+" Want to stop?") != ""):
                    break
    else:
        while(lastMoves <= 100):
            print(lastMoves)
            game.start()
            lastMoves += 1
            game.changeLastMoves(lastMoves)
            break
