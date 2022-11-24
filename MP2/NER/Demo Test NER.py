import spacy

testPhrase1 = "Phil Colson, Leopold Fitz, Melinda May, Daisy Johnson, Jemma Simmons, Doctor Strange and Black Panther are my favorite characters."
testPhrase2 = "I love watching Iron man and The Avengers, sad Phil Colson isn't here."
testPhrase3 = "Thor: Love and Thunder is going to release soon! I want to see it!"
testPhrase4 = "Do you like Thor? He is my favorite character."
testPhrase5 = "Which movies do you like?"
testPhrase6 = "I just finished watching The Avengers end game"
#testing the model

nlp = spacy.load("marvelNERModel/model-last")

print("Phrase 1 -->",testPhrase1)
doc = nlp(testPhrase1)
for ent in doc.ents:
    print(ent.label_, "-->",ent.text)

print("Phrase 2 -->",testPhrase2)
doc = nlp(testPhrase2)
for ent in doc.ents:
    print(ent.label_, "-->",ent.text)

print("Phrase 3 -->",testPhrase3)
doc = nlp(testPhrase3)
for ent in doc.ents:
    print(ent.label_, "-->",ent.text)

print("Phrase 4 -->",testPhrase4)
doc = nlp(testPhrase4)
for ent in doc.ents:
    print(ent.label_, "-->",ent.text)

print("Phrase 5 -->",testPhrase5)
doc = nlp(testPhrase5)
for ent in doc.ents:
    print(ent.label_, "-->",ent.text)

print("Phrase 6 -->",testPhrase6)
doc = nlp(testPhrase6)
for ent in doc.ents:
    print(ent.label_, "-->",ent.text)
