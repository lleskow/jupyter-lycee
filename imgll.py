from PIL import Image
from os.path import splitext
from inspect import signature

################################################################################
#
# Module permettant "d'appliquer une fonction aux pixels d'une image"
# La relative complexité est du au fait qu'on demande aucune information
# sur la fonction appliquée, et qu'on accepte un nombre important de
# fonction
#
################################################################################

def determine_mode(f):
    nbr_para = len(signature(f).parameters)
    if nbr_para == 3:
        mode_depart = "RGB"
        if type(f(1,2,3)) != type(1.0) and type(f(1,2,3)) != type(1):
            mode_arrive = "RGB"
        else:
            mode_arrive = "L"
    elif nbr_para == 1:
    # On ne peut pas aller de "L" vers "RGB" uniquement "L" vers "L"
        mode_depart, mode_arrive = "L", "L"
    else:
        print("Votre fonction n'est pas valide car elle posséde trop de paramètres")
    return mode_depart, mode_arrive

def appliquer_fonction_vers_nb(f,image,mode_depart):
    im = Image.open(image)
    largeur, hauteur = im.size
    im2 = Image.new("L",im.size)
    for y in range(hauteur): #parcours des lignes
        for x in range(largeur): #parcours des colonnes d'une ligne
            pixel = im.getpixel((x,y))
            if mode_depart == "L":
                im2.putpixel((x,y),f(pixel))
            else:
                im2.putpixel((x,y),int(f(pixel[0],pixel[1],pixel[2])))
    # f peut retourner des floats, mais putpixel n'accepte que des entiers
    # une conversion via int est donc nécessaire
    im2.show()
    print("fait")

def appliquer_fonction_vers_couleur(f,image):
    im = Image.open(image)
    largeur, hauteur = im.size
    im2 = Image.new("RGB",im.size)
    for y in range(hauteur): #parcours des lignes
        for x in range(largeur): #parcours des colonnes d'une ligne
            pixel = im.getpixel((x,y))
            im2.putpixel((x,y),tuple(map(int,f(pixel[0],pixel[1],pixel[2]))))
# map permet d'appliquer la fonction int aux 3 coordonnées retournée par f dans
# ce cas, tuple permet de reconstituer un tuple à partir du retour de map
    im2.show()
    print("fait")


def appliquer_fonction(f,image):
    mode_depart, mode_arrive = determine_mode(f)
    if mode_arrive == "RGB":
        appliquer_fonction_vers_couleur(f,image)
    else:
        appliquer_fonction_vers_nb(f,image,mode_depart)
