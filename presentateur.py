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

#----- IMPORT -----
from modele import *
from vue import *

#================================
#===== PACKAGE PRESENTATEUR =====
#================================

#----- PRESENTATEUR -----
class Presentateur(object):
    """Classe permettant de lancer une partie avec une intelligence et une interface graphique"""
    def __init__(self, dimension):
        self.dimension = dimension
        self.modele = Modele(dimension)
        self.modele.newIA(Color.RED)
        self.vue = Vue(dimension, self.modele.board, self)

    def mark(self, id, color):
        return self.modele.mark(id, color)

    def choiceIA(self):
        return self.modele.choiceIA()

    def endGame(self, id):
        return self.modele.board.solve(id)

    def initiate(self):
        self.modele = Modele(self.dimension)
        self.modele.newIA(Color.RED)
            

