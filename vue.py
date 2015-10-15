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
import pygame

#=======================
#===== PACKAGE VUE =====
#=======================

#----- COLOR -----
class Color(object):
    """Classe simulant un type enumere ou chaque instance correspont a un code couleur RVB"""
    WHITE = (255, 255, 255)
    BLUE = (40, 96, 255)
    BLUE_C = (74, 121, 255)
    RED = (255, 0, 0)
    RED_C = (255, 40, 40)
    BLACK = BLACK = (0 , 0, 0)

#----- FONT -----
class Font(object):
    """ Classe permettant l'affichage du texte avec une
    police bien precise, lors de l'initialisation, on donne
    comme argument le repertoire de la police."""
    def __init__(self,path_font):
        pygame.font.init()
        self.font = pygame.font.Font(path_font, 20)
        
    def render(self, text):
        return self.font.render(text, False, Color.BLACK)

#----- HEXAGON -----
class HexagonGraphic(object):
    """Classe permettant la creation et les differents
    traitements d'un hexagone"""
    
    def __init__(self, screen, x, y, id, size, color=Color.WHITE):
        self.screen = screen
        self.size = size
        self.color = color
        self.marked = False
        self.id = id
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.size/2 - 4, self.y - self.size, self.size + 8, self.size*2)


    def draw(self):
        """Methode qui dessine l'objet HexagonGraphic dans une fenetre"""
        p1 = [(self.x - self.size, self.y),
              (self.x - self.size/2, self.y - self.size),
              (self.x + self.size/2, self.y - self.size),
              (self.x + self.size, self.y),
              (self.x + self.size/2, self.y + self.size),
              (self.x - self.size/2, self.y + self.size)]
        pygame.draw.polygon(self.screen, self.color, p1)
        pygame.draw.polygon(self.screen, (100,100,100), p1, 3)

    def update(self, x, y, color):
        """Methode permettant de mettre a jour la couleur d'un objet HexagonGraphic"""
        if self.rect.collidepoint(x, y):
            self.mark(color)


    def mark(self, color):
        self.color = color
        self.marked = True

    def isMe(self, x, y):
        """Methode qui renvoie si les coordonnees mises en parametre
        correspondent aux coordonnees de l'objet HexagonGraphic"""
        if self.rect.collidepoint(x, y):
            return True
        return False
    

#----- BOARD -----
class BoardGraphic(object):
    """Classe correspondant a un plateau affichable a l'ecran"""
    def __init__(self, screen, size, dimension, plateau):
        self.screen = screen
        self.size = size
        self.dimension = dimension
        self.plateau = plateau
        self.hexas = {}
        

    def initiate(self):
        """Methode qui initialise le plateau"""
        dx = self.size
        dy = self.size*self.dimension
        id = 0
        for i in xrange(self.dimension):
            for j in xrange(self.dimension):
                x = dx + self.size*(j+i)*1.5
                y = dy + self.size*(i-j)
                id+=1
                self.hexas[id] = HexagonGraphic(self.screen, x, y, id,  self.size)

    def draw(self):
        """Methode qui dessine le plateau dans une fenetre"""
        pygame.draw.rect(self.screen, Color.RED, (0, 0, self.size*self.dimension*1.5, self.size*self.dimension))
        pygame.draw.rect(self.screen, Color.BLUE, (self.size*self.dimension*1.5, 0, self.size*self.dimension*1.5*2, self.size*self.dimension))
        pygame.draw.rect(self.screen, Color.BLUE, (0, self.size*self.dimension, self.size*self.dimension*1.5, self.size*self.dimension))
        pygame.draw.rect(self.screen, Color.RED, (self.size*self.dimension*1.5, self.size*self.dimension, self.size*self.dimension*1.5, self.size*self.dimension))

        for i in self.hexas.keys():
            hexa = self.hexas[i]
            hexa.draw()


    def getCoords(self, id):
        """Methode permettant de recuperer les coordonnees d'un hexagone"""
        h = self.hexas[id] #On retrouve l'hexagone correspondant a l'id
        return h.x, h.y

    def getID(self, x, y):
        for i in self.hexas.keys():
            if self.hexas[i].isMe(x,y):
                return self.hexas[i].id


#----- VUE -----
class Vue(object):
    """Classe representant la fenetre"""
    def __init__(self, dimension, plateau, presentateur, size=20):
        self.dimension = dimension
        self.plateau = plateau
        self.presentateur = presentateur
        self.size = size
        self.player = Color.BLUE
        
        self.win = True
        self.winner = None
        
        pygame.init()
        pygame.display.set_caption("JEU DE HEX")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((dimension*size*3, dimension*size*2))
        self.board = BoardGraphic(self.screen, self.size, self.dimension, self.plateau)
        self.main()


    def updateCase(self, id, color):
        """Methode qui met a jour la couleur d'une case."""
        self.board.hexas[id].mark(color)

    def reset(self):
            self.win = False
            self.winner = None
            self.board.initiate()
            self.presentateur.initiate()
            self.player = Color.BLUE

    def changePlayer(self):
        """Methode qui permet de changer de joueur"""
        if self.player == Color.BLUE:
            self.player = Color.RED
        else:
            self.player = Color.BLUE
        
    def main(self):
        """Methode constituant la boucle principale de jeu"""
        self.board.initiate()
        while True:
            
            if not self.win:
                
                self.board.draw()
                x, y = pygame.mouse.get_pos()
                #Boucle concernant le choix du joueur
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        id = self.board.getID(x, y)
                        if id!=None:#VERIFIE SI LE CLICK DE LA SOURIS ETAIT EN DEHORS DU PLATEAU
                            if self.presentateur.mark(id, self.player):#VERIFIE SI LA CASE A DEJA ETAIT MARQUE
                                self.updateCase(id, self.player)
                                if self.presentateur.endGame(id)!=None:#VERIFIE SI LE JEU EST FINI
                                    self.win = True
                                    self.winner = self.player
                                self.changePlayer()    
                            continue

                #PARTIE CONCERNANT L'IA       
                if self.player == Color.RED:
                    id = self.presentateur.choiceIA()
                    self.updateCase(id, self.player)
                    if self.presentateur.endGame(id)!=None:#VERIFIE SI LE JEU EST FINI
                        self.win = True
                        self.winner = self.player
                    self.changePlayer()
            else:
                self.menu()
                
            pygame.display.update()
            
            if not self.update():
                break
            self.clock.tick(40)
        pygame.quit()

        
    def update(self):
        """Methode recupere les differentes evenements"""
        k = pygame.key.get_pressed()
        
        if k[pygame.K_ESCAPE]: #Touche Echap -> Fermeture du jeu
            return False
        
        elif k[pygame.K_c]:#Touche C -> Nouvelle Partie
            self.reset()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        
        return True

    def menu(self):
        """Methode appele lors de la fin d'une partie"""
        
        if self.winner == Color.BLUE:
            color = "Bleu"
        elif self.winner == Color.RED:
            color = "Rouge"

            

        # Fill background
	background = pygame.Surface(self.screen.get_size())
	background = background.convert()
	background.fill(Color.WHITE)

	# Display some text
	font = pygame.font.Font("./Computerfont.ttf", 20)
	t1 = font.render("[C] Commencer", 2, Color.BLACK)
	t2 = font.render("[Echap] Quitter", 2, Color.BLACK)

	t1pos = t1.get_rect()
	t1pos.centerx = background.get_rect().centerx
	t1pos.centery = background.get_rect().centery-15
	
	t2pos = t2.get_rect()
	t2pos.centerx = background.get_rect().centerx
	t2pos.centery = background.get_rect().centery+15

	if self.winner != None:
            t3 = font.render("Le joueur "+color+" a gagne!", 2, self.winner)
            t3pos = t3.get_rect()
            t3pos.centerx = background.get_rect().centerx
            t3pos.centery = background.get_rect().centery-45
            background.blit(t3, t3pos)

	background.blit(t1, t1pos)
	background.blit(t2, t2pos)

	self.screen.blit(background, (0,0))
	pygame.display.flip()










































        
