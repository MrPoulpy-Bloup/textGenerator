from training import training
from generation import generation

def main() :

    inp = input('t = entraînement / g = génération / q = quitter :\n')

    if inp == 't' :
        listText = [
            'textsPhilo'
        ]
        training(listText, int(input('dimension de l\'entraînement :\n')))
    elif inp == 'g' :
        generation(int(input('nb de phrases à générer : \n')), 5) # , int(input('dimension de la génération :\n')))

if __name__ == '__main__' :
    main()