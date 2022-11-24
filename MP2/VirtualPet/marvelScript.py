import requests
from bs4 import BeautifulSoup

url = 'https://marvelcinematicuniverse.fandom.com/wiki/'


def getSynopsisAndPlotAboutMovie(entity: str):
    entity = '_'.join([e.capitalize() for e in entity.split()])
    res = requests.get(url + entity + '_(film)')

    if res.status_code != 200:
        return None, None

    soup = BeautifulSoup(str(res.content, 'utf-8'), 'html.parser')
    synopsisH = soup.find(id='Synopsis')
    synopsisBody = synopsisH.parent.findNext('p')
    for s in synopsisBody.find_all('sup'):
        s.extract()

    plotParagraphs = []
    plotH = soup.find(id='Plot')
    paragraph = plotH.parent.findNext('p')
    while True:
        try:
            if paragraph.name == 'h2':
                break

            if paragraph.name == 'figure' or paragraph.name != 'p':
                pass
            else:
                for s in paragraph.find_all('sup'):
                    s.extract()
                plotParagraphs.append(paragraph.text.strip())
        except:
            pass

        paragraph = paragraph.next_sibling

    return synopsisBody.text, plotParagraphs


def getInfoAboutCharacter(entity: str):
    entity = '_'.join([e.capitalize() for e in entity.split()])
    res = requests.get(url + entity)

    if res.status_code != 200:
        return None

    soup = BeautifulSoup(str(res.content, 'utf-8'), 'html.parser')
    characterDiv = soup.find(class_='mw-parser-output')
    p = characterDiv.find_all('p')[1]
    if len(p.text) > 0:
        for s in p.find_all('sup'):
            s.extract()
    return p.text
