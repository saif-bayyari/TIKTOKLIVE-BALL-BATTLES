import arcade
import random 
from explosion import Explosion

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
UPDATES_PER_FRAME = 2
explosion = arcade.Sound("explosion.mp3")


class Particle(arcade.SpriteCircle):
    def __init__(self,typeName, owner, explosionList):
        
        
        self.typeName = typeName
        self.owner = owner
        self.radius = 10
        self.max_health = 100
        self.current_health = 100
        self.score = 0
        

        if self.typeName == "Red":
            super().__init__(self.radius, arcade.color.RED)
            
        if self.typeName == "Blue":
            super().__init__(self.radius, arcade.color.BABY_BLUE)
           
        
        self.center_x = random.uniform(10,SCREEN_WIDTH - 10)
        self.center_y = random.uniform(10,360)
        self.velocity_x = 3
        self.velocity_y = 3
        self.exploded = False
        self.explosionList = explosionList
        self.e = None


    def update(self):

                if self.exploded == True:
                    self.velocity_x = 0
                    self.velocity_y = 0

                    if not self.e:
                        self.e = Explosion(self.center_x, self.center_y)
                        self.explosionList.append(self.e)
                        explosion.play()

                    self.kill()
                    


                    
                    
                    
                else:
                    self.center_x += self.velocity_x
                    self.center_y += self.velocity_y
        #print(str(self.center_x) + "," + str(self.center_y))

                    if self.center_x >= (SCREEN_WIDTH - 1):
              
                        self.velocity_x = -self.velocity_x
                    if self.center_x <= (0):
               
                        self.velocity_x = abs(self.velocity_x)
                    if self.center_y <= (0):
                
                        self.velocity_y = abs(self.velocity_y)
                    if self.center_y >= (360):
                        self.velocity_y = -self.velocity_y

    
        
    
            