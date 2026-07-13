import math


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
    x, y = coord
    alpha = math.atan2(x, y) * 180 / math.pi
    norme = math.sqrt(x ** 2 + y ** 2)
    if alpha < 0:
        alpha = 360 + alpha
    return alpha, norme

o = 270
n = 235
print(regress_coord(VecteurForce(n, o).coordonnees()))