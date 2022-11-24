import os
from owlready2 import *

cwd = os.getcwd()
f = open(cwd + "/checkersWins.owl", "w")
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

bw = wins("black", namespace=onto, has_win=[])
ww = wins("white", namespace=onto, has_win=[])
onto.save()

f = open(cwd + "/botMemory.owl", "w")
f.close()
onto_path.append("/")
onto = get_ontology("file://" + cwd + "/botMemory.owl")
onto.load()

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

onto.save()

bot = entity("bot", namespace=onto, likes=likes("loves", namespace=onto, movies=[], characters=[]),
             dislikes=dislikes("hates", namespace=onto, movies=[], characters=[]), entityName=[""])
user = entity("user", namespace=onto, likes=likes("loves", namespace=onto, movies=[], characters=[]),
              dislikes=dislikes("hates", namespace=onto, movies=[], characters=[]), entityName=[""])
# Tutorial on how to create a movie
irmn = movies("movieironman1", needMoreDescription=True, realName='', hateLevel=0, likeLevel=0, namespace=onto,
              description=[
                  "2008's Iron Man tells the story of Tony Stark, a billionaire industrialist and genius inventor who is kidnapped and forced to build a devastating weapon. Instead, using his intelligence and ingenuity, Tony builds a high-tech suit of armor and escapes captivity. When he uncovers a nefarious plot with global implications, he dons his powerful armor and vows to protect the world as Iron Man."],
              characters=[])
irmn.description.append(
    "Playboy and visionary industrial genius Tony Stark, CEO of leading military defense contractor, Stark Industries, is in war-torn Kunar, Afghanistan, to demonstrate his company's new Jericho missile. With him is his friend and military liaison, Lieutenant Colonel James Rhodes, a member of the U.S. Air Force.")
irmn.description.append(
    "While riding in a transport convoy, Stark is critically wounded in an ambush and held captive in a cave by the Ten Rings. An electromagnet built by fellow captive Ho Yinsen keeps the shrapnel that wounded Stark from reaching his heart and killing him. The Ten Rings leader, Raza, offers Stark freedom; in exchange, Stark must build a Jericho missile for the terrorists. Stark and Yinsen agree that Raza will not keep his word of letting Stark live.")
irmn.description.append(
    "While pretending to work on the missile, Stark and Yinsen secretly build a powerful electric generator called an Arc Reactor to power Stark's electromagnet. They then begin to build a powered suit of armor, designed by Stark, to help them escape. The Ten Rings ambush the workshop when they discover Stark's plan, but Yinsen sacrifices himself to distract them while Stark's suit powers up. Using the armored suit, Stark fights his way out of the cave to find a mortally wounded Yinsen, who reassures Stark and urges him to continue his escape and not waste his life. An enraged Stark leaves the cave, burns the terrorist's stockpile of Stark Industries-produced weapons, and flies away. Having escaped, Stark crashes in the desert, which destroys the suit.")
irmn.description.append(
    "After being rescued by a search party, including Rhodes, Stark returns home. He calls a press conference to announce that his company will no longer manufacture weapons, having seen first-hand the strife that they cause in the wrong hands. Obadiah Stane, his father's old partner and the company's manager, informs Stark that this may ruin Stark Industries and his father's legacy.")
irmn.description.append(
    "In his home workshop, Stark spends the next few months building an improved version of his suit, as well as a more powerful arc reactor for his chest. At Stark's first public appearance after his return, Christine Everhart informs him that Stark Industries weapons, including the Jericho missile, were recently delivered to the Ten Rings and are being used to attack Gulmira, Yinsen's home village. Stark confronts Stane about the supplied weapons and learns that Stane is trying to replace him as head of the company.")
irmn.description.append(
    "Enraged, Stark dons his new armor and flies to Afghanistan, where he saves the citizens of Gulmira from the Ten Rings' wrath. While flying home, Stark is engaged by two F-22 Raptors on behalf of the U.S. Air Force. He phones Rhodes and reveals his identity in an attempt to call off the attack. Meanwhile, the Ten Rings gather the pieces of Stark's prototype suit. Raza meets with Stane and offers to exchange the suit with him. However, Stane has Raza and his faction eliminated, taking the suit for himself. Returning to Stark Industries, Stane orders his scientists to have a new suit reverse-engineered from the wreckage.")
irmn.description.append(
    "Seeking to find any other weapons delivered to the Ten Rings, Stark sends his trusted personal assistant, Pepper Potts, to hack into the company computer system from Stane's office. Potts finds evidence of Stane supplying weapons to the terrorists, but also discovers that Stane had initially hired the Ten Rings to kill Stark in Afghanistan. After an uncomfortable encounter with a suspicious Stane, Potts meets with Phil Coulson of the Strategic Homeland Intervention, Enforcement and Logistics Division to inform him of Stane's activities.")
irmn.description.append(
    "Stane's scientists reveal that they cannot finish his suit, as no one can manage to duplicate Stark's Arc Reactor. Stane ambushes Stark at his home, using a Sonic Taser to paralyze him and take his current Arc Reactor. Left to die, Stark manages to crawl to his lab and saves himself by re-using his original arc reactor. Potts and several S.H.I.E.L.D. agents attempt to arrest Stane, but he dons his suit and attacks them. Stark fights Stane, but is outmatched without his upgraded reactor to run his suit at full capacity.")
irmn.description.append(
    "Stark lures Stane atop the Stark Industries building and instructs Potts to overload the large Arc Reactor there. Doing so unleashes a massive electrical surge that knocks Stane unconscious, causing him and his armor to fall into the exploding reactor, killing him. The next day, the press has dubbed the armored hero \"Iron Man.\" Agent Coulson gives Stark a cover story to explain the events of the night and Stane's death. At a press conference, Stark begins giving the cover story, but then instead announces that he is Iron Man, shocking the public as the crowd of interviewers suddenly begin roaring out questions, much to Rhodes' confusion.")
irmn.description.append(
    "Afterward, Nick Fury visits Stark at his home, stating that Iron Man is not \"the only superhero in the world,\" and wants to discuss the Avengers Initiative.")
irmnChar = characters("characterironman", needMoreDescription=True, realName='', hateLevel=0, likeLevel=0,
                      namespace=onto, description=[
        "Anthony Edward \"Tony\" Stark was a billionaire industrialist, a founding member of the Avengers, and the former CEO of Stark Industries. A brash but brilliant inventor, Stark was self-described as a genius, billionaire, playboy, and philanthropist. With his great wealth and exceptional technical knowledge, Stark was one of the world's most powerful men following the deaths of his parents and enjoyed the playboy lifestyle for many years until he was kidnapped by the Ten Rings in Afghanistan, while demonstrating a fleet of Jericho missiles. With his life on the line, Stark created an armored suit which he used to escape his captors. Upon returning home, he utilized several more armors to use against terrorists, as well as Obadiah Stane who turned against Stark. Following his fight against Stane, Stark publicly revealed himself as Iron Man."],
                      movies=[irmn])
irmn.characters.append(irmnChar)
print(bot.likes.movies)
print(bot.dislikes.movies)
print(irmn.description)
print(irmn.characters)
print(irmn.characters[0].description)
print(irmn.characters[0].movies)
onto.save()
