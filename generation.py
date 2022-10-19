import json
from random import randint, choice

def generation(nb: int, dimension: int = 3) :
    '''
    Genère un nombre de phrases aléatoires à partir d'un texte.

    :param nb : Nombre de phrases à générer.
    :param dimension : Dimension de la génération (par défaut : 3).
    Maximum recommandé : 5.
    :return: Affiche les phrases générées.
    '''

    # Ouverture du fichier json contenant les mots
    with open('json/mots.json','r',encoding='utf-8') as f :
        dicMots = json.load(f)

    # Ouverture du fichier json contenant les mots avec majuscule (début de phrase)
    with open('json/majuscules.json','r',encoding='utf-8') as f :
        majuscules = json.load(f)

    for n in range(nb) :

        # Choix aléatoire d'un mot de début de phrase
        lastWord = choice(majuscules['majuscules'])
        lastestWords = []
        phrase = ''
        clef = ''
        phraseLimite = False

        while lastWord is not None :

            # Ajout du mot à la phrase
            phrase += f' {lastWord}'

            if len(phrase.split(' ')) > 14 and None in dicMots[lastWord] :
                # Limite la phrase à 15 mots
                phraseLimite = True
                break

            if dicMots[lastWord] == [None] :
                break

            if len(lastestWords) < dimension :
                lastestWords.append(lastWord)

            else :
                lastestWords.pop(0)
                lastestWords.append(lastWord)

            for dim in range(dimension) :
                clef = ' '.join(lastestWords[dim:])
                if dicMots.get(clef) is not None :
                    break

            lastWord = choice(list(dicMots[clef]))

        phrase = f'{phrase.lstrip().capitalize()}.'

        if phraseLimite :
            phrase += ' (phrase limitée)'

        print(f'phrase {n+1} : {phrase}')

        with open('résultats/résultats.txt','a',encoding='utf-8') as f :
            f.write(f'phrase {n+1} : {phrase}\n')
