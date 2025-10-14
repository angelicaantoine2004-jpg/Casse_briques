#qui : Angelica/ Radu/ Sebastian 
#quand : 07/10/2025
#quoi : Fichier principal du jeu, contenant les bouttons, et appelant les différents objets

''''Importation des bibliothèques'''

from tkinter import * 
import random
from bricks import Brick #les briques à casser
from racket import Racket #la raquette pour casser les briques 
#from menu import Menu # le menu qui permet de choisir sa difficulté. 
#from ball import Ball # la balle


#Variables utiles

largeur = 400

hauteur = 500

#Paramètres du jeu 

difficulté= 3 #à faire sélectionner à l'utilisateur 


class Game :
    def __init__ (self): #Création de la fenêtre de jeu
        self.__fenetre = Tk()
        self.__fenetre.title("Casse brique")
        self.__canvas = Canvas(self.__fenetre, width= largeur, height = hauteur, bg ='black')
        self.__canvas.pack()
        self.__jeu_en_cours = True 
        self.boutton1()
        self.bricks = Brick(self.__canvas)
        self.__racket = Racket(self.__canvas, self.__fenetre)
        
        self.__score = 0
        self.__lines = 3
        self.__score_text = self.__canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 16), text=f"Score:{self.__score}")
        self.run_game()

        def move_ball(self):
            self.ball.move()
        #bounce off left/right wall
            if self.ball.x <= 0 or self.ball.x + self.ball.size >= 600:
                self.ball.bounce_horizontal()
        #bounce off top 
            if self.ball.y <= 0:
                self.ball.bounce_vertical()
        #bounce of paddle
            if self.ball.y + self.ball.size >= self.paddle_y:
                if(self.paddle_x < self.ball.x + self.ball.size and self.ball.x < self.paddle_x + self.paddle_width):
                    self.ball.bounce_vertical()
                    self.ball.y = self.paddle_y - self.ball.size

        #if ball falls out, you lose one life
            if self.ball.y + self.ball.size > 500:
                self.lives -= 1
                self.update_text()
                self.ball.reset(300, 300, random.choice([-5, 5]), -5)

        #bounce off bricks
            hit_brick = None
            for brick in self.bricks:
                brick_coords = self.canvas.coords(brick.id)
                bx1, by1, bx2, by2 = brick_coords
                ball_center_x = self.ball.x + self.ball.size/2
                ball_center_y = self.ball.y + self.ball.size/2
                if bx1 < ball_center_x < bx2 and by1 < ball_center_y < by2:
                    hit_brick = brick
                    break
            if hit_brick:
                self.canvas.delete(hit_brick.id)
                self.bricks.remove(hit_brick)
                self.ball.bounce_vertical()
                self.score += 10
                self.update_text()


    def run_game(self):
        self.__fenetre.mainloop()
        
            
    def stopgame(self): #Arrête le jeu et ferme la fenêtre
        self.__jeu_en_cours = False 
        self.__fenetre.destroy()

        
    def boutton1(self): #Création des boutons rejouer et stop
        self.__frame1 = Frame(self.__fenetre, relief = 'groove')
        self.__frame1.pack (side='left', padx=10, pady=10)
        self.__frame2 = Frame(self.__fenetre, relief = 'groove')
        self.__frame2.pack (side='right', padx=10, pady=10)
        Button(self.__frame1, text= 'Start', fg = 'Green').pack(padx=10, pady=10)
        Button(self.__frame2, text='Stop',command = self.stopgame, fg = 'Red').pack(padx=10, pady=20)

  

Game()
