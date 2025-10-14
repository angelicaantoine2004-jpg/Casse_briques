import tkinter 


#Variable utiles

largeur = 400

hauteur = 500

#Paramètres du jeu 

difficulté= 3 #à faire sélectionner à l'utilisateur 

class Brick :

     def __init__ (self, canvas): #Création de la fenêtre de jeu
        self.__larg_briques = largeur/5
        self.__haut_briques = 20 
        self.__x1= 0 
        self.__y1= 0 
        self.__x2=self.__larg_briques
        self.__y2=self.__haut_briques
        self.__list_brick= []
        self.colors = ['lightcoral', 'lightpink', 'lightyellow', 'aquamarine', 'lightblue' ]
        for j in range(difficulté): #nombre de colonnes 
           self.__x1, self.__x2 = 0, self.__larg_briques  # réinitialiser la position horizontale à chaque ligne
           for i in range(5):
             brick = canvas.create_rectangle(self.__x1, self.__y1, self.__x2, self.__y2, fill= self.colors[i])
             self.__list_brick.append(brick)
             self.__x1, self.__x2 = self.__x2, self.__x2 + self.__larg_briques
           self.__y1, self.__y2 = self.__y2, self.__y2 + self.__haut_briques  # décaler vers le bas pour la prochaine ligne
        print(self.__list_brick)
    