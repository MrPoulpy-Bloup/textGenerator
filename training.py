import json
import os


def training(listText: list,dimension: int) :
    '''
    Entraîne le programme à partir d'une liste de fichiers textes.
    :param listText: Liste des textes à ajouter.
    :param dimension: Dimension de l'entraînement.
    :return: Ajout des textes dans le fichier json (+ création du fichier si inexistant).
    '''

    for nbText, text in enumerate(listText) :

        # Ouverture du texte
        with open(f'textes/{text}.txt','r',encoding='utf-8') as f :
            mots = f.read()

        # Suppression de certains caractères
        mots = mots.replace('- ', '')
        lSuppr = ['"', '<', '>', '«', '»', '[', ']', ':', ';', '=', '(', ')', '-', '—', ',', '\n', '\u200b', '\x0c']
        for charact in lSuppr :
            mots = mots.replace(charact,' ')

        text = mots.split(' ')
        mots = mots.lower()
        # String -> List (+ suppression des espaces en trop)
        mots = mots.split()

        nbMots = len(mots)*dimension

        # Crétion du dictionnaire de majuscules à partir du fichier json (s'il existe)
        try :
            with open('json/majuscules.json','r',encoding='utf-8') as f :
                file = f.read()
                if file != '' or file != '{}' :
                    majuscules = json.loads(file)
                else :
                    majuscules = {'majuscules' : []}
        except FileNotFoundError :
            majuscules={'majuscules' : []}

        # Ajout des mots commençant par une majuscule dans le dictionnaire
        # + mise en minuscule des mots
        for it, mot in enumerate(text) :
            if mot.istitle() and not('!' in mot or '?' in mot or '.' in mot) and not(text[it+1] == '!' or text[it+1] == '?' or text[it+1] == '.') :
                mot = mot.lower()
                majuscules['majuscules'].append(mot.replace('.','').replace('!','').replace('?',''))

        # suppression des doublons
        majuscules['majuscules']=list(set(majuscules['majuscules']))

        # Sauvegarde du dictionnaire de majuscules
        with open('json/majuscules.json','w',encoding='utf-8') as f :
            json.dump(majuscules,f,indent=2)

        # Création du dictionnaire de mots à partir du fichier json (s'il existe)
        try :
            with open('json/mots.json','r',encoding='utf-8') as f :
                file = f.read()
                if file != '' or file != '{}' :
                    dicMots=json.loads(file)
                else :
                    dicMots = {}
        except FileNotFoundError :
            dicMots = {}

    for k in range(1,dimension + 1) :
        # appel de la fonction d'entraînement en fonction de la dimension
        eval(f'training_dimension_{k}(mots, dicMots, nbMots, nbText)')
        # TODO: Ajouter une boucle pour réunir toutes les fonctions en une et gérer plus que 3 dimensions

        # Sauvegarde du dictionnaire dans le fichier json
        with open('json/mots.json','w',encoding='utf-8') as f :
            json.dump(dicMots,f,indent=2)

    os.system('cls')
    print('\nDone !')


def training_dimension_1(mots: list, dicMots: dict, nbMots: int, nbText: int) :
    lastPct = None

    # Ajout des mots dans le dictionnaire
    for k in range(len(mots)) :
        if mots[k] is not None :
            if k == len(mots)-1 :
                # Dernier mot du texte
                if dicMots.get(mots[k]) is not None :
                    dicMots[mots[k].replace('.','').replace('?','').replace('!','')].append(None)
                else :
                    dicMots[mots[k].replace('.','').replace('?','').replace('!','')] = [None]
            elif '.' in mots[k] or '!' in mots[k] or '?' in mots[k] :
                # Mot suivi d'une ponctuation de fin de phrase
                if dicMots.get(mots[k]) is not None :
                    dicMots[mots[k].replace('.','').replace('?','').replace('!','')].append(None)
                else :
                    dicMots[mots[k].replace('.','').replace('?','').replace('!','')] = [None]
            elif mots[k + 1] == '!' or mots[k + 1] == '?' or mots[k + 1] == '.' :
                # Prochain mot est une ponctuation de fin de phrase
                mots[k + 1] = None
                if dicMots.get(mots[k]) is not None :
                    dicMots[mots[k]].append(None)
                else :
                    dicMots[mots[k]] = [None]
            else :
                # Reste des mots
                if dicMots.get(mots[k]) is not None :
                    dicMots[mots[k]].append(mots[k + 1].replace('.','').replace('?','').replace('!',''))
                else :
                    dicMots[mots[k]] = mots[k + 1].replace('.','').replace('?','').replace('!','').split()

        # Progression de l'entraînement
        pct = k*100//nbMots
        if pct % 10 == 0 and pct != lastPct :
            os.system('cls')
            print(f'nombre de mots dans le texte {nbText+1} : {nbMots//3}\n')
            print(f'Progression : {k*100//nbMots}%')
        lastPct = pct


def training_dimension_2(mots: list,dicMots: dict, nbMots: int, nbText: int) :
    lastPct = None

    # Ajout des mots dans le dictionnaire
    for k in range(len(mots)-2) :
        if mots[k] is not None and mots[k+1] is not None and mots[k+2] is not None :

            if not('.' in mots[k] or '!' in mots[k] or '?' in mots[k]) and not('.' in mots[k+1] or '!' in mots[k+1] or '?' in mots[k+1]):
                # mot et mot suivant ne contiennent pas des ponctuations de fin de phrase
                if dicMots.get(f'{mots[k]} {mots[k+1]}') is not None :
                    dicMots[f'{mots[k]} {mots[k+1]}'].append(mots[k+2].replace('.','').replace('?','').replace('!',''))
                else :
                    dicMots[f'{mots[k]} {mots[k+1]}'] = mots[k+2].replace('.','').replace('?','').replace('!','').split()

            elif '.' in mots[k+1] or '!' in mots[k+1] or '?' in mots[k+1] and not('.' in mots[k] or '!' in mots[k] or '?' in mots[k]) :
                # mot suivant contient une ponctuation de fin de phrase mais pas le mot actuel
                if dicMots.get(f'{mots[k]} {mots[k+1]}'.replace('.','').replace('!','').replace('?','')) is not None :
                    dicMots[f'{mots[k]} {mots[k+1]}'.replace('.','').replace('!','').replace('?','')].append(None)
                else :
                    dicMots[f'{mots[k]} {mots[k+1]}'.replace('.','').replace('!','').replace('?','')] = [None]

        # Progression de l'entraînement
        pct = k*100//nbMots
        if pct%10 == 0 and pct != lastPct and pct != 0 :
            os.system('cls')
            print(f'nombre de mots dans le texte {nbText+1} : {nbMots//3}\n')
            print(f'Progression : {k*100//nbMots+30}%')
        lastPct = pct

def training_dimension_3(mots: list,dicMots: dict, nbMots: int, nbText: int) :
    lastPct = None

    # Ajout des mots dans le dictionnaire
    for k in range(len(mots)-3) :
        if mots[k] is not None and mots[k+1] is not None and mots[k+2] is not None and mots[k+3] is not None :

            if not('.' in mots[k] or '!' in mots[k] or '?' in mots[k]) and not('.' in mots[k+1] or '!' in mots[k+1] or '?' in mots[k+1]) and not('.' in mots[k+2] or '!' in mots[k+2] or '?' in mots[k+2]) :
                # mot actuel, mot suivant et 2ème mot suivant ne contiennent pas des ponctuations de fin de phrase
                if dicMots.get(f'{mots[k]} {mots[k+1]} {mots[k+2]}') is not None :
                    dicMots[f'{mots[k]} {mots[k+1]} {mots[k+2]}'].append(mots[k+3].replace('.','').replace('?','').replace('!',''))
                else :
                    dicMots[f'{mots[k]} {mots[k+1]} {mots[k+2]}'] = mots[k+3].replace('.','').replace('?','').replace('!','').split()

            elif '.' in mots[k+2] or '!' in mots[k+2] or '?' in mots[k+2] and not('.' in mots[k] or '!' in mots[k] or '?' in mots[k]) and not('.' in mots[k+1] or '!' in mots[k+1] or '?' in mots[k+1]) :
                # 2ème mot suivant contient une ponctuation de fin de phrase mais pas le mot actuel ni le mot suivant
                if dicMots.get(f'{mots[k]} {mots[k+1]} {mots[k+2]}'.replace('.','').replace('!','').replace('?','')) is not None :
                    dicMots[f'{mots[k]} {mots[k+1]} {mots[k+2]}'.replace('.','').replace('!','').replace('?','')].append(None)
                else :
                    dicMots[f'{mots[k]} {mots[k+1]} {mots[k+2]}'.replace('.','').replace('!','').replace('?','')] = [None]

        # Progression de l'entraînement
        pct = k*100//nbMots
        if pct%10 == 0 and pct != lastPct and pct != 0 :
            os.system('cls')
            print(f'nombre de mots dans le texte {nbText+1} : {nbMots//3}\n')
            print(f'Progression : {k*100//nbMots+60}%')
        lastPct = pct
