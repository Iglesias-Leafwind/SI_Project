import spacy
from spacy.tokens import Doc, DocBin
import random

def createSentences(sentence, questionEntityList,tagEntity):
    flag = "{ENTITY}"
    returningValues = []
    for entity in questionEntityList:
        words = []
        spaces = []
        ents = []

        for word in sentence.split(" "):
            if(flag in word):
                words.append(entity)
                ents.append("B-" + tagEntity)
                if("'s" == word[-2:]):
                    spaces.append(False)
                    words.append("'s")
                    ents.append("B-" + tagEntity)
                    spaces.append(True)
                else:
                    spaces.append(True)
                    if(word[-1] != "}"):
                        words.append(word[-1])
                        spaces.append(True)
                        ents.append("O")
            else:
                words.append(word)
                ents.append("O")
                spaces.append(True)
        spaces[-1] = False
        if(len(words) != len(spaces)):
                print(words)
                return
            
        returningValues.append((words,spaces,ents))
    return returningValues

def createSentencesMultiple(sentence, questionEntityList1,tagEntity1, questionEntityList2,tagEntity2):
    randomDescriptions = ["""White, wavy hair almost fully covers a lean, friendly face. Glistening pink eyes, set wickedly within their sockets, watch hungrily over the woods they've kept safe for so long. Scars stretching from the top of the right cheek , first running towards his fairly big lips and ending above his left eye leaves a tormenting burden of his former lover. This is the face of Almon Dawnthorn, a true protector among blood elves. He stands high among others, despite his heavy frame. There's something appealing about him, perhaps it's his painful past or perhaps it's simply his persistence. But nonetheless, people tend to brag about knowing him, while trying to subtly look more like him.""",
                          """Pink, well groomed hair awkwardly hangs over a round, menacing face. Wide pink eyes, set sunken within their sockets, watch hungrily over the town they've stood guard for for so long. Several moles are spread peculiarly across his whole face and leaves a lasting burden of his fortunate upbringing. This is the face of Alluin Moonwalker, a true victor among high elves. He stands easily among others, despite his tough frame. There's something enticing about him, perhaps it's his gentleness or perhaps it's simply his tenderness. But nonetheless, people tend to keep their distance, while hoping their sons will grow up to be like him.""",
                          """Red, straight hair awkwardly hangs over a chiseled, lively face. Shuttered gray eyes, set gracefully within their sockets, watch energetically over the deserts they've looked after for so long. Freckles are spread handsomely around her cheeks and and leaves a fascinating memory of her luck in love. The is the face of Goredo Burningfury, a true mercenary among orcs. She stands small among others, despite her athletic frame. There's something wonderful about her, perhaps it's her goodwill or perhaps it's simply her odd friends. But nonetheless, people tend to worship her, while trying to subtlely stare.""",
                          """Gray, shoulder-length hair awkwardly hangs over a craggy, friendly face. Clear black eyes, set concealed within their sockets, watch honorably over the armies they've fought for for so long. A gunshot left a mark reaching from just under the right eyebrow , running towards her right nostril and ending under her left eye and leaves a pleasurable memory of unexpected friendship. The is the face of Daphne Eustice, a true dreamer among halflings. She stands oddly among others, despite her light frame. There's something ambiguous about her, perhaps it's a feeling of sadness or perhaps it's simply a feeling of hospitality. But nonetheless, people tend to subtly ignore her, while making up bigger stories about her."""]
    flag1 = "{ENTITY1}"
    flag2 = "{ENTITY2}"
    flag1Mult = "{ENTITY1MULTIPLE}"
    flagRandom = "{RANDOMDESCRIPTION}"
    returningValues = []
    for entity1 in questionEntityList1:
        for entity2 in questionEntityList2:
            words = []
            spaces = []
            ents = []
            for word in sentence.split(" "):
                if(flag2 in word):
                    words.append(entity2)
                    ents.append("B-" + tagEntity2)
                    if("'s" == word[-2:]):
                        spaces.append(False)
                        words.append("'s")
                        ents.append("B-" + tagEntity2)
                        spaces.append(True)
                    else:
                        spaces.append(True)
                        if(word[-1] != "}"):
                            words.append(word[-1])
                            spaces.append(True)
                            ents.append("O")
                elif(flag1 in word):
                    spaces.append(True)
                    words.append(entity1)
                    ents.append("B-" + tagEntity1)
                    if(word[-1] != "}"):
                        words.append(word[-1])
                        spaces.append(True)
                        ents.append("O")
                elif(flag1Mult in word):
                    multipleEntity1Qty = random.randint(1, len(questionEntityList1))
                    for i in range(0,multipleEntity1Qty-1):
                        entity1Idx = random.randint(0, len(questionEntityList1)-1)
                        words.append(questionEntityList1[entity1Idx])
                        spaces.append(False)
                        ents.append("B-" + tagEntity1)
                        if(i != (multipleEntity1Qty-1)):
                            words.append(",")
                            spaces.append(True)
                            ents.append("O")
                    if(multipleEntity1Qty > 1):
                        words.append("and")
                        spaces.append(True)
                        ents.append("O")
                        entity1Idx = random.randint(0, len(questionEntityList1)-1)
                        words.append(questionEntityList1[entity1Idx])
                        spaces.append(True)
                        ents.append("B-" + tagEntity1)
                        
                elif(flagRandom in word):
                    selectedIdx = random.randint(0, len(randomDescriptions)-1)
                    for descWord in randomDescriptions[selectedIdx].split(" "):
                        spaces.append(True)
                        words.append(descWord)
                        if(descWord in questionEntityList2):
                            ents.append("B-" + tagEntity2)
                        elif(descWord in questionEntityList1):
                            ents.append("B-" + tagEntity1)
                        else:
                            ents.append("O")
                else:
                    spaces.append(True)
                    words.append(word)
                    ents.append("O")

            spaces[-1] = False
            returningValues.append((words,spaces,ents))
    return returningValues
foods = []
with open("fod.txt","r") as foodFile:
    for foodType in foodFile:
        foods.append(foodType.rstrip())

characters = ["Iron Man","Hulk","Thor","Captain America","Ant Man","Doctor Strange","Spider Man","Black Panther","Wasp","Captain Marvel","Black Widow","Shang Chi","Blade","Tony Stark","Bruce Banner","Loki","Steve Rogers","Hawkeye","Nick Fury","Falcon","Peter Quill","Ronan","Rocket","Groot","Gamora","Drax","Drax the Destroyer","Maria Hill","Scott Lang","Hank Pym","Vasily Karpov","Dr Stephen Strange","Stephen Strange","Peter Parker","May","Hela","TChalla","T Challa","Thanos","Hope van Dyne","Carol Danvers","Ned","MJ","Wong","Scarlet Witch","Wanda Maximoff","Wanda","Gorr the God Butcher","God Butcher","Valkyrie","Korg","Jane Foster","Monica Rambeau","Carol Danvers","Kamala Khan","Phil Coulson","Melinda May","Daisy Johnson","Jemma Simmons","Skye","Quake"]
movies = ["Iron Man","Iron Man 2", "The Incredible Hulk","Thor","Captain America The First Avenger","The Avengers","Iron Man 3","Thor The Dark World","The First Avenger","The Dark World","Captain America The Winter Soldier","The Winter Soldier","Guardians of the Galaxy","Avengers Age of Ultron","Age of Ultron","Ant Man","Captain America Civil War","Civil War","Doctor Strange","Guardians of the Galaxy Vol 2","Guardians of the Galaxy 2","Spider Man Homecoming","Homecoming","Thor Ragnarok","Ragnarok","Black Panther","Avengers Infinity War","Infinity War","Ant Man and the Wasp", "Captain Marvel","Avengers Endgame","Endgame","Spider Man Far From Home","Far From Home","Black Widow","Shang Chi and the Legend of the Ten Rings","Eternals","Spider Man No Way Home", "No Way Home","Doctor Strange in the Multiverse of Madness","Multiverse of Madness","Thor Love and Thunder","Love and Thunder","Black Panther Wakanda Forever","Wakanda Forever","Ant Man and the Wasp Quantumania","Quantumania","Guardians of the Galaxy vol 3","Guardians of the Galaxy 3","The Marvels", "Blade", "Fantastic Four"]
templatesChars = ["Do you know {ENTITY}?","I love {ENTITY}","{ENTITY} is the best character","{ENTITY} is the worst character","I hate {ENTITY}","What is {ENTITY}'s origin story?","Who is {ENTITY}?","What happened to {ENTITY}?","Who is the actor that represents {ENTITY}?","Which movies {ENTITY} appeared?","Do you know who {ENTITY} is?","Tell me about {ENTITY}","Can you tell me more about {ENTITY}?","In what movies has {ENTITY} appeared in?","Do you like the character {ENTITY}","Do you like character {ENTITY}"]
templatesMovies = ["I want to watch {ENTITY}","Never watched {ENTITY}","I love watching {ENTITY}","I love [ENTITY}, it's my favourite film, what about you do you like {ENTITY}?","Have you seen {ENTITY}?","Have you watched {ENTITY}?","Do you like {ENTITY}?","Do you like watching {ENTITY}?","Did you like {ENTITY}?","Tell me about {ENTITY}","Can you tell me more about {ENTITY}?","Do you like the movie {ENTITY}","Do you like movie {ENTITY}"]
templatesMultipleEntities = ["Did {ENTITY2} appear in {ENTITY1}?","Didn't see {ENTITY2} in {ENTITY1}","Who appears in {ENTITY1}? Did {ENTITY2} appear?","{ENTITY2} appears in {ENTITY1}","{ENTITY2} is a character {RANDOMDESCRIPTION} that appears in movies {ENTITY1MULTIPLE}"]
templatesFoods = ["Do you like the food {ENTITY}","Do you like food {ENTITY}","I like eating {ENTITY}","I love eating {ENTITY}","I want to eat {ENTITY}","Do you want to eat {ENTITY}","I would love to go get some {ENTITY}"]

sentences = []
for template in templatesChars:
    sentences += createSentences(template,characters,"MARVELCHARACTER")
for template in templatesMovies:
    sentences += createSentences(template,movies,"MARVELMOVIE")
for template in templatesMultipleEntities:
    sentences += createSentencesMultiple(template,movies,"MARVELMOVIE",characters,"MARVELCHARACTER")
for template in templatesFoods:
    sentences += createSentences(template,foods,"FOOD")

#generate the spaccy rules
nlp = spacy.blank("en")
nlp.add_pipe("ner")

ner = nlp.get_pipe("ner")
ner.add_label("MARVELCHARACTER")
ner.add_label("MARVELMOVIE")

db = DocBin()
for sentenceInfo in sentences:
    db.add(Doc(nlp.vocab,words=sentenceInfo[0],spaces=sentenceInfo[1],ents=sentenceInfo[2]))

db.to_disk("./marvelNER_train.spacy")
db.to_disk("./marvelNER_valid.spacy")
