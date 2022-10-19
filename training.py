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
        with open(f'texts/{text}.txt','r',encoding='utf-8') as f :
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

        # Création du dictionnaire de majuscules à partir du fichier json (s'il existe)
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
            pointInMot = True
            motsSuivantIsPoint = True

            if not('!' in mot or '?' in mot or '.' in mot) :
                pointInMot = False

            if it < len(text)-1 :
                if not(text[it+1] == '!' or text[it+1] == '?' or text[it+1] == '.') :
                    motsSuivantIsPoint = False

            if mot.istitle() and not pointInMot and not motsSuivantIsPoint :
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

        # Entraînement de 1 à dimension
        trainingBoucle(mots,dicMots,nbMots,nbText,dimension)

        # Sauvegarde du dictionnaire dans le fichier json
        with open('json/mots.json','w',encoding='utf-8') as f :
            json.dump(dicMots,f,indent=2)

    os.system('cls')
    print('\nDone !')


def training_dimension_1(mots: list, dicMots: dict, nbMots: int, nbText: int, dimension: int) :
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
            print(f'nombre de mots dans le texte {nbText+1} : {nbMots//dimension}\n')
            print(f'Progression : {pct}%')
        lastPct = pct


def trainingBoucle(mots: list,dicMots: dict, nbMots: int, nbText: int, dimension: int) :
    # Entraînement de la 1ère dimension
    training_dimension_1(mots,dicMots,nbMots,nbText,dimension)

    lastPct = None

    # Entraînement des dimensions de 2 à dimension
    for dim in range(2,dimension+1) :
        for k in range(len(mots)-dim) :
            clef = ''
            kIsNotNone = True
            noPointinK = True
            pointInLastK = False

            for i in range(dim) :
                if mots[k+i] is None or mots[k+dim] is None :
                    # Vérifie que la clef et la future valeur sont différentes de None
                    kIsNotNone = False
                    break
                if kIsNotNone :
                    if '.' in mots[k+i] or '!' in mots[k+i] or '?' in mots[k+i] :
                        # Vérifie que la clef ne contient pas de ponctuation de fin de phrase
                        noPointinK = False
                        break
                    if '.' in mots[k+dim] or '!' in mots[k+dim] or '?' in mots[k+dim] :
                        # Vérifie si la valeur contient une ponctuation de fin de phrase
                        pointInLastK = True

                # Création de la clef : mots[k] + mots[k+1] + ... + mots[k+dim-1]
                clef += mots[k + i]
                if i != dim-1 :
                    clef += ' '

            if kIsNotNone and noPointinK :
                # La clef et la future valeur sont différentes de None et la clef ne contient pas de ponctuation de fin de phrase
                if dicMots.get(clef) is not None :
                    dicMots[clef].append(mots[k+dim].replace('.','').replace('?','').replace('!',''))
                else :
                    dicMots[clef] = [mots[k+dim].replace('.','').replace('?','').replace('!','')]

            elif kIsNotNone and pointInLastK :
                # La clef et la valeur sont différentes de None et la future valeur contient une ponctuation de fin de phrase
                if dicMots.get(clef.replace('.','').replace('!','').replace('?','')) is not None :
                    dicMots[clef.replace('.','').replace('!','').replace('?','')].append(None)
                else :
                    dicMots[clef.replace('.','').replace('!','').replace('?','')] = [None]

            # Progression de l'entraînement
            pct = k*100//nbMots + (dim-1)*100//dimension
            if pct % 10 == 0 and pct != lastPct :
                os.system('cls')
                print(f'nombre de mots dans le texte {nbText+1} : {nbMots//dimension}\n')
                print(f'Progression : {pct}%')
            lastPct = pct