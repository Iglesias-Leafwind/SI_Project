import os
from owlready2 import *
cwd = os.getcwd()
f = open(cwd+"/checkersWins.owl", "w")
f.close()
onto_path.append("/")
onto = get_ontology("file://" + cwd + "/checkersWins.owl")
onto.load()

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
    
    
onto.save()

bw = wins("black", namespace = onto, has_win = [])
ww = wins("white", namespace = onto, has_win = [])
onto.save()
