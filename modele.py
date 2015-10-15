##Program: JEU DE HEX
##Authors: Simon BITTON, Luiz CLaudio VISNADI
##Copyright (C) 2013
##
##This program is free software; you can redistribute it and/or
##modify it under the terms of the GNU General Public License
##as published by the Free Software Foundation; either version 2
##of the License, or (at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#----- IMPORTS -----
from random import randint

#==========================
#===== PACKAGE MODELE =====
#==========================

#----- COLOR -----
class Color(object):
    """Classe simulant un type enumere ou chaque instance correspont a un code couleur RVB"""
    WHITE = (255, 255, 255)
    BLUE = (40, 96, 255)
    RED = (255, 0, 0)

#----- TREE -----
class Tree(object):
    """Classe simulant un arbre avec plusieurs fils"""
    def __init__(self, root, val = 0, **kw):
        self.root = root
        self.val = val
        self.children = kw


#----- IA -----
class IA(object):
    """Classe representant l'intelligence artificielle du jeu"""
    def __init__(self, color):
        self.color = color

    def randomChoice(self, n):
        """Methode qui permet de choisir une case au hasard"""
        return randint(1,n)

    def successeurs(self, id, board):
        """Methode permettant de creer un arbre avec les differents etats suivants d'un
        plateau a partir d'une case id donnee"""
        self.tree = Tree(board) #creation de l'arbre, elle a pour racine l'etat actuel

        pos = board.around(id)#on repertorie toutes les cases voisines a la case ayant comme numero id
        
        for i in range(len(pos)):#on parcoure toutes les cases voisines
            
            if id+pos[i]>0:
                if id+pos[i]<((board.dimension**2)+1):
                    
                    if(board.plateau[id+pos[i]].color == Color.WHITE):#si la case et vide

                        
                        res = Board(board.dimension) #on cree un etat fils
                        res.plateau = board.plateau # on copie l'etat actuel
                        res.mark(id+pos[i], self.color) #on choisi la case libre, creant ainsi un etat suivant

                        if res.solve(id+pos[i]) == self.color:
                            self.tree.children[id+pos[i]] = Tree(res, 2)#on cree un fils qui a pour cle la position future choisie
                            print id+pos[i]
                        else :
                            self.tree.children[id+pos[i]] = Tree(res, 1)

#----- HEXAGON -----
class Hexagon(object):
    """Classe representant un hexagone"""
    def __init__(self, id, blue_d, blue_f, red_d, red_f):
        self.id = id
        self.color = Color.WHITE
        self.marked = False
        #chacune des variables d'objet
        #suivantes correspondent a
        #chaque bord du tableau
        self.blue_d = blue_d #correspond au bord haut gauche
        self.blue_f = blue_f #correspond au bord bas droit
        self.red_d =red_d #correspond au bord bas gauche
        self.red_f = red_f #correspond au bord haut droit

    def mark(self, color):
        """Methode permettant de changer la couleur de l'objet Hexagon"""
        if not self.marked:
            self.color = color
            self.marked = True


    def __repr__(self):
        return "HEXAGONE - "+str(self.id)

#----- BOARD -----
class Board(object):
    """Classe representant un plateau de jeu"""
    def __init__(self, dimension):
        self.plateau = {}
        self.dimension = dimension
        self.initiate(dimension)

    def initiate(self, dimension):
        """ Methode permettant d'initialiser un tableau. """
        liste = {}
        for i in xrange(1, (dimension*dimension)+1):
            
            blue_d, blue_f, red_d, red_f = self.edge(i)
            liste[i] = Hexagon(i, blue_d, blue_f, red_d, red_f)
            
        self.plateau.clear()
        self.plateau.update(liste)

    def edge(self, id):
        """Methode permettant de definir la position
        d'une case dans le plateau"""
        #Angle gauche
        if id == 1:
            return True, False, True, False
        #Angle du haut
        if id == self.dimension:
            return False, True, True, False
        #Angle du bas
        if id == ((self.dimension*(self.dimension-1))+1):
            return True, False, True, False
        #Angle droit
        if id == (self.dimension**2):
            return False, True, False, True
        #Bord bas gauche (blue_p)
        if id % self.dimension == 1:
            return True, False, False, False
        #Bord haut gauche (red_p)
        if id > 1 and id < self.dimension:
            return False, False, True, False
        #Bord haut droit (blue_f)
        if (id % self.dimension) == 0:
            return False, True, False, False
        #Bord bas droit (red_f)
        if (id - ((self.dimension*(self.dimension-1))+1)) > 1 and (id - ((self.dimension*(self.dimension-1))+1)) < 11:
            return False, False, False, True
        #Milieu
        else:
            return False, False, False, False

    def mark(self, id, color):
        """Methode permettant de changer de couleur d'une case"""
        if not self.plateau[id].marked:
            self.plateau[id].mark(color)
            return True
        else:
            return False


    #METHODES POUR LA RESOLUTION DU JEU
    def solve(self, id):
        """Methode verifiant si le jeu est fini.
        Elle renvoie la couleur du vainqueur."""
        views = []
        color = self.plateau[id].color
        chain = [hexa for hexa in self.sameColor(id, color, views)]
        if self.begin(chain, color) and self.end(chain, color):
            return color
        return None

    def around(self, id):
        """Methode qui renvoie les positions relatives des voisins d'une case"""
        if self.plateau[id].blue_d == True:
            return 0, -(self.dimension-1), -self.dimension, 1, self.dimension
        if self.plateau[id].blue_f == True:
            return 0, -self.dimension, -1, self.dimension, (self.dimension-1)
        else:
            return 0, -(self.dimension-1), -self.dimension, 1, -1, self.dimension, (self.dimension-1)

    def sameColor(self, id, color, views):
        """Methode qui renvoie un ensemble de cases de meme couleur formant une chaine"""
        pos = self.around(id)
        alr = [self.plateau[id+i].id for i in pos if (self.plateau.has_key(id+i) and (id+i not in views))]
        chain = [self.plateau[hexa].id for hexa in alr if (self.plateau[hexa].color == color)]
        views.extend(chain)
        for i in chain:
            self.sameColor(i, color, views)
        return views

    def begin(self, chain, color):
        """Methode verifiant s'il existe un ensemble de cases de meme couleur si
        l'une d'entres elles est adjacente a un des bords du cote gauche"""
        if color == Color.BLUE:
            for c in chain:
                if self.plateau[c].blue_d:
                    return True
        else:
            for c in chain:
                if self.plateau[c].red_d:
                    return True
        return False
        
    def end(self, chain, color):
        """Methode verifiant s'il existe un ensemble de cases de meme couleur si
        l'une d'entres elles est ajdacente a un des bords du cote droit"""
        if color == Color.BLUE:
            for c in chain:
                if self.plateau[c].blue_f:
                    return True
        else:
            for c in chain:
                if self.plateau[c].red_f:
                    return True
        return False

#----- GAME -----
class Modele(object):
    """Classe representant une partie"""
    def __init__(self, dimension):
        self.player = None
        self.board = Board(dimension)
        self.win = None


    #--
    def mark(self, id , color):
       """Methode permettant de changer de couleur d'une case dans le plateau"""
       return self.board.mark(id, color)

    def newIA(self, color):
        """Methode qui permet d'initialiser une intelligence artificielle"""
        self.player = IA(color)

    def loopChoice(self, player):
        """Methode qui boucle tant que le joueur n'a pas fait un
        choix valide"""
        case = player.randomChoice(self.board.dimension**2)
        while not self.board.mark(case, player.color):
            case = player.randomChoice(self.board.dimension**2)
        return case

    def choiceIA(self):
        """Methode qui renvoie le choix d'une intelligence artificielle"""
        return self.loopChoice(self.player)







