#qui : Angelica/ Raku 
#quand : 07/10/2025
#quoi : Création du casse brique 


from tkinter import *


#Variable utiles

largeur = 400

hauteur = 500

#Paramètre du jeu 

difficulté= 3 #à faire sélectionner à l'utilisateur 


class Game :
    def __init__ (self): #Création de la fenêtre de jeu
        self.__fenetre = Tk()
        self.__fenetre.title("Casse brique")
        self.__canvas = Canvas(self.__fenetre, width= largeur, height = hauteur, bg ='black')
        self.__canvas.pack()
        self.__jeu_en_cours = True 
        self.boutton1()
        self.boutton_menu()
        self.briques()
        
        self.__score = 0
        self.__lines = 3
        self.__score_text = self.__canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 16), text=f"Score:{self.__score}")
        self.run_game()

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

    def boutton_menu(self): #Création des boutons rejouer et stop
        self.__frame3 = Frame(self.__fenetre, relief = 'groove')
        self.__frame3.pack (side='left', padx=100, pady=50)
        Button(self.__frame1, text= 'Menu',command = self.menu(), fg = 'Black').pack(padx=10, pady=10)
        
    def menu(self):
        self.__fenetre_menu = Tk()
        self.__fenetre_menu.title = 'Menu'
        self.__canvas_menu = Canvas(self.__fenetre, width= largeur-100, height = hauteur-200, bg ='black')
        self.__frame3 = Frame(self.__fenetre, relief = 'groove')
        self.__frame3.pack (side='left', padx=100, pady=50)
             
        
    def briques(self):
        larg_briques = largeur/5
        haut_briques = 20 
        x1= 0 
        y1= 0 
        x2=larg_briques
        y2=haut_briques
        list_brick= []
        for j in range(difficulté):
           x1, x2 = 0, larg_briques  # réinitialiser la position horizontale à chaque ligne
           for i in range(5):
             brick = self.__canvas.create_rectangle(x1, y1, x2, y2, fill='red')
             list_brick.append(brick)
             x1, x2 = x2, x2 + larg_briques
           y1, y2 = y2, y2 + haut_briques  # décaler vers le bas pour la prochaine ligne
        print(list_brick)



        
Game()
