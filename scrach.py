if self.image.width > 300 and self.image.height > 100: 
            self.setFixedSize(self.image.width, self.image.height)
        elif self.image.width <= 300 and self.image.height > 100:
            self.setFixedSize(300, self.image.height)
        elif self.image.width > 300 and self.image.height <= 100:
            self.setFixedSize(self.image.width, 100)
        else:   # si la taille de l'image est trop petite que pour que la taille de la fenêtre soit en fonction de la taille de l'image
            self.setFixedSize(300, 100)