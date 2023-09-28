import arcade
from particle import Particle
from laser import Laser
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, GiftEvent
import threading
from explosion import Explosion
from HealthBar import HealthBar

import random
import asyncio

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = arcade.color.WHITE


music = arcade.Sound("FRENCH.mp3")
laser = arcade.Sound("laser.mp3")


    
client: TikTokLiveClient = TikTokLiveClient(unique_id="@aldeenofficial")

def TikTokThread():
    client.run()

my_thread = threading.Thread(target=TikTokThread)
my_thread.start()

def spawnLaser(particle, particleList, laserList, amountofTimes):
            
            if not amountofTimes:
            
                laser.play()
                        
                l = Laser(particle, particleList)
                laserList.append(l)
                
            else:
                for _ in range(amountofTimes):
                    laser.play()   
                    l = Laser(particle, particleList)
                    laserList.append(l)


def increaseParticleHealth(particle, rate, numTimes):
    for i in range (numTimes):
        if particle.current_health == particle.max_health:
            break
        else:
            particle.current_health += rate

             
    

            
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Player Class Example")
        self.game_paused = False
        arcade.set_background_color(BACKGROUND_COLOR)
        
        
    def setup(self):
        
        
        self.particles = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        
        self.Red = self.addParticle("Red", "Trump", self.explosions)
        self.Blue= self.addParticle("Blue", "Biden", self.explosions)
        spawnLaser(self.Red, self.particles,self.lasers, None)
        spawnLaser(self.Blue, self.particles,self.lasers, None)
        self.red_health_bar = HealthBar(self.Red)
        self.blue_health_bar = HealthBar(self.Blue)



        @client.on("gift")
        async def on_gift(event: GiftEvent):
            if event.gift.streakable and not event.gift.streaking:
                if event.gift.info.name == "Rose":
                    increaseParticleHealth(self.Red,10,event.gift.count)
                elif event.gift.info.name == "GG":
                    increaseParticleHealth(self.Blue,10,event.gift.count)
            


        async def on_comment(event: CommentEvent):

            if event.comment == "/trump.shoot" or event.comment == "Trump 2024":
                spawnLaser(self.Red, self.particles, self.lasers,None)

            if event.comment == "/biden.shoot" or event.comment == "Biden 2024":
                spawnLaser(self.Blue, self.particles,self.lasers, None)

        client.add_listener("comment", on_comment)
        
    # It's not type 1, which means it can't have a streak & is automatically over
   
        client.add_listener("gift", on_gift)

    def on_draw(self):
        if not self.game_paused:
            arcade.start_render()

            if len(self.explosions) is not 0:
                self.explosions.draw()

            self.red_health_bar.draw()
            self.blue_health_bar.draw()

            self.particles.draw()
            if len(self.lasers) is not 0:
                self.lasers.draw()
            
            arcade.draw_text("1 Rose = more health for Trump (red ball)", 30, 450, arcade.color.BLACK,
                             font_size=12, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("1 GG = more health for Biden (blue ball)", 400, 450, arcade.color.BLACK,
                             font_size=12, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("trump shoots: /trump.shoot", 30, 400, arcade.color.BLACK,
                             font_size=14, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("biden shoots: /biden.shoot", 350, 400, arcade.color.BLACK,
                             font_size=14, bold=True, italic=True, anchor_x="left", anchor_y="baseline")

            arcade.draw_text("Trump (Red) Score: " + str(self.Red.score), 30, 500, arcade.color.BLACK,
                             font_size=25, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("Biden (Blue) Score: " + str(self.Blue.score), 400, 500, arcade.color.BLACK,
                             font_size=25, bold=True, italic=True, anchor_x="left", anchor_y="baseline")

    def on_update(self, delta_time):
        if not self.game_paused:
            
            self.particles.update()
            self.lasers.update()
            self.explosions.update()
            self.red_health_bar.update(self.Red.current_health)
            self.blue_health_bar.update(self.Blue.current_health)

            if self.Red.exploded == True:
                currentRedScore = self.Red.score
                self.Red = self.addParticle("Red", "Trump", self.explosions)
                self.red_health_bar = HealthBar(self.Red)
                self.Red.score = currentRedScore
            if self.Blue.exploded == True:
                currentBlueScore = self.Blue.score
                self.Blue = self.addParticle("Blue", "Biden", self.explosions)
                self.blue_health_bar = HealthBar(self.Blue)
                self.Blue.score = currentBlueScore
                        
           
            
            
            
           

    def addParticle(self, typeName, ownerID,explosionList):
        
        newParticle = Particle(typeName, ownerID,explosionList=explosionList)
        self.particles.append(newParticle)

        return newParticle

    def on_hide_view(self):
        self.game_paused = True

    def on_show_view(self):
        self.game_paused = False

    def on_key_press(self, symbol, modifiers):
  
             if symbol == arcade.key.SPACE:
                spawnLaser(self.Red, self.particles,self.lasers, None)

             if symbol == arcade.key.BACKSPACE:
                spawnLaser(self.Blue, self.particles,self.lasers, None)




def main():
    game = MyGame()
    game.setup()
    music.play(volume=0.5, loop=True)
    arcade.run()

if __name__ == "__main__":
    main()
