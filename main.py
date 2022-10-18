from training import training
from generation import generation

def main() :

    inp = input('t = entraînement / g = génération / q = quitter :\n')

    if inp == 't' :
        listText = [
            'textesPhilo2'
        ]
        training(listText, int(input('dimension de l\'entraînement :\n')))
    elif inp == 'g' :
        generation(int(input('nb de phrases à générer : \n'))) # , int(input('dimension de la génération :\n')))

if __name__ == '__main__' :
    main()