#Mon projet test

#1 Le plateau de jeu
#1.1

cases_MT = [[0,0],[0,7],[0,14],[7,0],[7,14],[14,0],[14,7],[14,14]]
cases_MD = [[1,1],[1,13],[2,2],[2,12],[3,3],[3,11],[4,4],[4,10],[7,7],[10,4],[10,10],[11,3],[11,11],[12,2],[12,12],[13,1],[13,13]]
cases_LT = [[1,5],[1,9],[5,1],[5,5],[5,9],[5,13],[9,1],[9,5],[9,9],[9,13],[13,5],[13,9]]
cases_LD = [[0,3],[0,11],[2,6],[2,8],[3,0],[3,7],[3,14],[6,2],[6,6],[6,8],[6,12],[7,3],[7,11],[8,2],[8,6],[8,8],[8,12],[11,0],[11,7],[11,14],[12,6],[12,8],[14,3],[14,11]]
cases_n = ""

def init_bonus():
    """ Initialise et renvoie une liste de listes de caractères contenant les bonus """
    bonus = [cases_MT, cases_MD, cases_LT, cases_LD, cases_n]
    return bonus

init_bonus()

#1.2

def init_jetons():
    """ Initialise et renvoie une liste de listes contenant uniquement des cases vides """
    jetons = []

