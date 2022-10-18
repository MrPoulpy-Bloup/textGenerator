import json
from random import randint, choice

def generation(nb: int, dimension: int = 3) :
    '''
    Genère un nombre de phrases aléatoires à partir d'un texte.

    :param nb : Nombre de phrases à générer.
    :param dimension : Dimension de la génération.
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
        nextWord = ''
        lastestWords = []
        phrase = ''

        while lastWord is not None :

            # Ajout du mot à la phrase
            phrase += f' {lastWord}'

            if dicMots[lastWord] == [None] :
                break

            if dimension == 3 :

                if len(lastestWords) < dimension :
                    lastestWords.append(lastWord)
                else :
                    lastestWords.pop()
                    lastestWords.append(lastWord)

                if len(lastestWords) < dimension :
                    nextWord = choice(list(dicMots[lastWord]))
                    lastestWords.append(nextWord)

                else :

                    if dicMots.get(f'{lastestWords[0]} {lastestWords[1]} {lastestWords[2]}') is not None :
                        nextWord = choice(list(dicMots[f'{lastestWords[0]} {lastestWords[1]} {lastestWords[2]}']))

                    elif dicMots.get(f'{lastestWords[1]} {lastestWords[2]}') is not None :
                        nextWord = choice(list(dicMots[f'{lastestWords[1]} {lastestWords[2]}']))

                    else :
                        nextWord = choice(list(dicMots[lastWord]))

                    lastestWords.pop(0)
                    lastestWords.append(nextWord)

            elif dimension == 1 :
                # Choix aléatoire d'un mot suivant
                nextWord=choice(list(dicMots[lastWord]))

            elif dimension == 2 :

                if len(lastestWords) < dimension :
                    lastestWords.append(lastWord)
                else :
                    lastestWords.pop()
                    lastestWords.append(lastWord)

                if len(lastestWords) < dimension :
                    nextWord=choice(list(dicMots[lastWord]))
                    lastestWords.append(nextWord)
                else :

                    if dicMots.get(f'{lastestWords[0]} {lastestWords[1]}') is not None :
                        nextWord=choice(list(dicMots[f'{lastestWords[0]} {lastestWords[1]}']))

                    else :
                        nextWord=choice(list(dicMots[lastWord]))

                    lastestWords.pop(0)
                    lastestWords.append(nextWord)

            lastWord = nextWord

        print(f'phrase {n + 1} : {phrase.lstrip().capitalize()}.')
