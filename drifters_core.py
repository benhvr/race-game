# moteur

import math
import random as rd


class VecteurForce:
    """ Création d'un vecteur représentant une force.
    
    L'instance a pour attribut :
        - la norme de la force (en N)
        - l'orientation du sens de la force
          (en ° avec 0° à la verticale vers le haut)
    
    """

    def __init__(self, norme, orientation):
        self.norme = norme
        self.orientation = orientation % 360
        self.x, self.y = None, None

    def __str__(self):
        return (f"\nCette force a une norme de {self.norme}N "
                f"et une orientation de {self.orientation}°.\n"
                "Elle a pour coordonnées "
                f"{(int(self.x * 100) / 100, int(self.y * 100) / 100)}.")

    def coordonnees(self):
        """ Détermine les coordonnées du vecteurs pour pouvoir le tracer.

        Crée une variable self.angle de la mesure de l'angle entre le vecteur
        et la verticale, la convertit en radians dans self.angle_rad.
        Puis calcule les coordonnées self.x et self.y à partir de la norme
        et des cosinus et sinus de l'angle.
        

        Returns
        _______

        float, float
            self.x, self.y (les coordonnées du vecteur)
        """
        if (self.orientation % 180) < 90 :
            self.angle = self.orientation % 90
        else :
            self.angle = 90 - (self.orientation % 90)
        self.angle_rad = self.angle * math.pi / 180

        signe_x, signe_y = 1, 1
        if self.orientation > 180:
            signe_x = -signe_x
        if self.orientation > 90 and self.orientation < 270:
            signe_y = -signe_y

        self.y = self.norme * math.cos(self.angle_rad) * signe_y
        self.x = self.norme * math.sin(self.angle_rad) * signe_x
        return self.x, self.y


def regress_coord(coord):
    """ Calcule la norme et l'orientaion du vecteur à partir de ses
    coordonnées.

    
    Parameters
    __________
    
    coordonnées(x, y) : (int/float, int/float)


    Returns
    _______

    float, float
        angle(0° : haut, + sens horaire), norme
    """
    x, y = coord
    alpha = math.atan2(x, y) * 180 / math.pi
    norme = math.sqrt(x ** 2 + y ** 2)
    if alpha < 0:
        alpha = 360 + alpha
    return alpha, norme


class Car:
    """ Création d'un objet {voiture}(joueur/enemie).
    
    Crée un objet {voiture} et ses attributs :
        - position(x, y)
        - acceleration
        - direction(0° vers le haut, puis sens horaire)
        - direction des roues(0° aligné à direction, + à droite, - à gauche)
        - inertie
        - mouvement(vecteur(x, y))
    
    
    Parameters
    __________

    position, direction : (int/float, int/float), int/float
    """
    
    def __init__(self, position=list, direction=int):
        self.position = position
        self.accel = 0
        self.direction = direction % 360
        self.dir_roues = 0
        self.norme_inertie = 0
        self.vect_mouv = VecteurForce(self.norme_inertie,
                                      self.direction).coordonnees()
        
    
    def update(self, inputs):
        """ Met à jour tous les attributs de {voiture}.
        
        - Ajoute à la direction la moitié de la direction des roues.
        - Divise la direction des roues par 2 si < -1 ou > 1 sinon la met à 0.
        - Met le vecteur mouvement à l'inertie du tour précédent et à la
          direction actuelle.
        - Applique ce mouvement aux coordonnées de {voiture}
        - Modifie legerement l'inertie pour la rapprocher de 0.
        - Ajoute l'acceleration à l'inertie.
        - Limite l'inertie à -50.
        """
        if inputs["z"] and not inputs["s"]:
            self.accel = -1
        elif inputs["s"] and not inputs["z"]:
            self.accel = 0.5
        elif not inputs["z"] and not inputs["s"]:
            self.accel = 0
        if self.norme_inertie != 0:
            if inputs["d"] == True:
                if -45 < self.dir_roues:
                    self.dir_roues += -3
            if inputs["q"] == True:
                if self.dir_roues < 45:
                    self.dir_roues += 3

        self.direction += self.dir_roues / 2
        self.direction %= 360
        if not inputs["q"] and not inputs["d"]:
            if not -1 <= self.dir_roues <= 1:
                self.dir_roues /= 2
            else:
                self.dir_roues = 0
        self.vect_mouv = VecteurForce(self.norme_inertie,
                                      self.direction).coordonnees()
        self.position[0] += self.vect_mouv[0]
        self.position[1] += self.vect_mouv[1]
        if -0.5 > self.norme_inertie:
            self.norme_inertie += 0.5
        elif self.norme_inertie > 0.25:
            self.norme_inertie += -0.25
        else:
            self.norme_inertie = 0
        self.norme_inertie += self.accel
        if self.norme_inertie < -50:
            if not isinstance(self, Enemie):
                self.norme_inertie = -50
            elif self.norme_inertie < -55:
                self.norme_inertie = -55
        if self.norme_inertie > 25:
            self.norme_inertie = 25


class Enemie(Car):
    """ Création d'un objet {enemie{voiture}}.

    Crée un objet {enemie} et ses attributs :
        (ensemble des attributs de {voiture})
        - cible({voiture} cible)
        - position cible(position de {voiture} cible + mouvement de {voiture})
        - vecteur objectif(vecteur(position -> objectif))
        - distance objectif(distance(position <-> objectif))
    
    (La cible de {enemie} est la {voiture} qu'il prend en chasse, l'objectif
     est l'estimation de la prochaine position de {voiture} cible)
    
    
    Parameters
    __________

    position, direction, cible : (int/float, int/float), int/float, Car
    """

    def __init__(self, position=list, direction=int, cible=Car):
        super().__init__(position, direction)
        self.cible = cible
        self.position_objctf = list(self.cible.position)
        self.vect_objctf = [self.position_objctf[0] - self.position[0],
                       self.position_objctf[1] - self.position[1]]
        self.d_objctf = math.sqrt((self.cible.position[0]
                                   - self.position[0]) ** 2
                               + (self.cible.position[1]
                                  - self.position[1]) ** 2)

    def update_objctf(self):
        """ Met à jour les attributs de {enemie}, prends les décisions de
        mouvement et met à jour les attributs de {voiture}.

        - Met l'attribut position cible à la position de {voiture} cible
        - Ajoute à position le mouvement actuel de {voiture} cible
        - Calcule le vecteur(position -> objectif)
        - Calcule la distance entre position et objectif
        - Lance la fonction decision()
        - Lance la mise à jour des attributs de {voiture}(fonction update())
        """
        self.position_objctf = list(self.cible.position)
        self.position_objctf[0] += self.cible.vect_mouv[0]
        self.position_objctf[1] += self.cible.vect_mouv[1]
        self.vect_objctf = [self.position_objctf[0] - self.position[0],
                            self.position_objctf[1] - self.position[1]]
        self.d_objctf = math.sqrt((self.cible.position[0]
                                   - self.position[0]) ** 2
                                  + (self.cible.position[1]
                                     - self.position[1]) ** 2)
        self.decisions()
        super().update({"z": True, "s": True, "q": False, "d": False})

    def decisions(self):
        """ Choisis les modifications à la direction des roues et à
        l'acceleration à appliquer.

        - Calcule l'orientation du vecteur(position -> obectif)
        - Calcule l'ecart entre cette orientation et la direction actuelle
        (Si la diference entre les deux est hors de [-180; 180] on tourne dans
         le sens contraire à la logique du jeux)
        - Modifie la direction des roues en fonction de l'ecart calcule plus
          haut
        - Verifie que l'angle des roues n'est pas trop important
        - Modifie l'acceleration en fonction de l'ecart entre l'inertie et
          la distance de l'objectif
        """
        direction_objctf = regress_coord(self.vect_objctf)[0]
        ecart_direction = (direction_objctf - self.direction) % 360
        if ecart_direction > 180: ecart_direction += -360
        
        if not -3 < ecart_direction < 3:
            if ecart_direction < 0: self.dir_roues += 3
            else: self.dir_roues += -3
            if self.dir_roues < -45 : self.dir_roues = -45
            elif self.dir_roues > 45 : self.dir_roues = 45
        
        if (-self.norme_inertie < self.d_objctf
            and abs(ecart_direction) > 135): self.accel = -1
        elif (-self.norme_inertie < self.d_objctf
              and abs(ecart_direction) < 135):
            if self.norme_inertie < -1: self.accel = 0.5
            else: self.accel = -1
        else: self.accel = 0.5


class GameState:

    def __init__(self):
        self.car = Car([rd.randint(0, 5400), rd.randint(0, 1600)],
                       rd.randint(0, 359))
        self.enemies = [
            Enemie([rd.randint(0, 5400), rd.randint(0, 1600)],
                   rd.randint(0, 359), self.car)
            for _ in range(10)
        ]
        self.running = True
    
    def update(self, inputs):
        self.car.update(inputs)
        for enemie in self.enemies:
            enemie.update_objctf()
            if (abs(enemie.position[0] - self.car.position[0]) < 25
                    and abs(enemie.position[1] - self.car.position[1]) < 25):
                self.running = False

    def to_dict(self):
        return {
            "running": self.running,
            "car": {
                "position": self.car.position,
                "direction": self.car.direction,
                "norme_inertie": self.car.norme_inertie,
                "vect_mouv": list(self.car.vect_mouv)
            },
            "enemies": [
                {
                    "position": e.position,
                    "direction": e.direction,
                    "norme_inertie": e.norme_inertie,
                    "vect_mouv": list(e.vect_mouv)
                }
                for e in self.enemies
            ]
        }
