import arcade
import random 
import math
from explosion import Explosion
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


host_options = ["Top", "Bottom", "Left", "Right"]


def check_collision(hp,rect, circ):
        # Calculate the closest point on the rectangle to the circle
        closest_x = max(rect.center_x, min(circ.center_x, rect.center_x + rect.width))
        closest_y = max(rect.center_y, min(circ.center_y, rect.center_y + rect.height))

        # Calculate the distance between the circle's center and the closest point
        distance = math.sqrt((closest_x - circ.center_x)**2 + (closest_y - circ.center_y)**2)

        
        return distance <= circ.radius 


class Laser(arcade.Sprite):
    def __init__(self,hostParticle, particleList):
        super().__init__()
        
        self.explosion = None
        self.originPoint = random.sample(host_options, 1)
        print(self.originPoint)
        self.particle = hostParticle
        self.particleList = particleList
        
        self.width = 20
        self.height = 20
        self.exited = False
        self.velocity_x = random.randint(4, 6)
        self.velocity_y = random.randint(4, 6)
        self.hit = False

        if self.particle.typeName == "Red":
            self.texture = arcade.make_soft_square_texture(20, (255,0,0), 255)
        elif self.particle.typeName == "Blue":
            self.texture = arcade.make_soft_square_texture(20, (0,0,255), 255)



        if self.originPoint[0] == "Top":

            self.center_x = self.particle.center_x 
            self.center_y = self.particle.center_y + 2
            

          

        if self.originPoint[0] == "Bottom":

            self.center_x = self.particle.center_x 
            self.center_y = self.particle.center_y - 2
            

            

        if self.originPoint[0] == "Left":

            self.center_x = self.particle.center_x - 2
            self.center_y = self.particle.center_y
            

        if self.originPoint[0] == "Right":

            self.center_x = self.particle.center_x + 2
            self.center_y = self.particle.center_y 
            
            
            
        print(str(self.velocity_x) + "," + str(self.velocity_y))
        
        


    def update(self):

        if self.center_x >= (SCREEN_WIDTH - 1):
               
                self.velocity_x = -self.velocity_x
        if self.center_x <= (0):
               
                self.velocity_x = abs(self.velocity_x)
        if self.center_y <= (0):
                
                self.velocity_y = abs(self.velocity_y)
        if self.center_y >= (360):
                self.velocity_y = -self.velocity_y
                
        

        self.center_x += self.velocity_x
        self.center_y += self.velocity_y

      
        for p in self.particleList:
            self.hit = check_collision(self.particle,self,p) 
            if self.hit == True and p != self.particle:
                
                
                p.current_health -= 10
                if p.current_health <= 0:

                    p.exploded = True
                    self.particle.score += 1
                
                
                self.velocity_x = 0
                self.velocity_y = 0
                self.kill()
                
                
                
            

                
        
               

   



    

    
    
        
        
