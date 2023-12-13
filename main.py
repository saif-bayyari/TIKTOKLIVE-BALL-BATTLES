import arcade
from particle import Particle
from laser import Laser
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, GiftEvent
import threading
from arcade.gui import UIManager
from explosion import Explosion
from HealthBar import HealthBar
import tkinter as tk


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = arcade.color.WHITE


music = arcade.Sound("FRENCH.mp3")
laser = arcade.Sound("laser.mp3")


    

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




             
class TkinterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Live Ball Battles")

        
        
        # Set the resolution to 800x600
        self.root.geometry("400x200")

        # Variable to store the TikTok username
        self.username_var = tk.StringVar()

        # Create a label and an entry widget for the username
        self.username_label = tk.Label(root, text="Enter TikTok Username:")
        self.username_label.pack()

        self.username_entry = tk.Entry(root, textvariable=self.username_var, state=tk.DISABLED)
        self.username_entry.pack()


        # Variable to store the mode choice (Test Mode or Normal Mode)
        self.mode_var = tk.StringVar()
        self.mode_var.set("Normal Mode")  # Default mode


        def enable_disable_text_field():
            if self.mode_var.get() == "Live Mode":
                self.username_entry.config(state=tk.NORMAL)
            else:
                self.username_entry.config(state=tk.DISABLED)


        # Create radio buttons
        self.test_mode_button = tk.Radiobutton(root, text="Test Mode", variable=self.mode_var, value="Test Mode", command=enable_disable_text_field)
        self.test_mode_button.pack()

        self.normal_mode_button = tk.Radiobutton(root, text="Live Mode (you must be live on Tiktok before running this)", variable=self.mode_var, value="Live Mode", command=enable_disable_text_field)
        self.normal_mode_button.pack()

        self.run_button = tk.Button(root, text="Run Game", command=self.run_game)
        self.run_button.pack(pady=20)

    def run_game(self):
        self.root.destroy()  # Close the Tkinter window
        game = MyGame()

        

        game.setup(self.mode_var.get(), self.username_var.get())
        print(self.mode_var.get())
        
        arcade.run()
       
   

            
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Player Class Example")
        self.game_paused = False
        arcade.set_background_color(BACKGROUND_COLOR)
        self.ui_manager = UIManager()
        self.error_popup = None

    def show_error_popup(self, exception_type, exception_details):
        self.error_popup = arcade.gui.UIManager()

        error_popup = arcade.gui.UIInputBox(300, 200, 400, 300)
        error_popup.text = f"An {exception_type} occurred:\n\n{exception_details}"
        error_popup.center_x = self.width // 2
        error_popup.center_y = self.height // 2

        self.ui_manager.add_ui_element(error_popup)

        
        
    def setup(self, testMode ,username):
        
        
        self.particles = arcade.SpriteList()
        self.lasers = arcade.SpriteList()
        self.explosions = arcade.SpriteList()
        
        
        self.Red = self.addParticle("Red", "Trump", self.explosions)
        self.Blue= self.addParticle("Blue", "Biden", self.explosions)
        spawnLaser(self.Red, self.particles,self.lasers, None)
        spawnLaser(self.Blue, self.particles,self.lasers, None)
        self.red_health_bar = HealthBar(self.Red)
        self.blue_health_bar = HealthBar(self.Blue)
        music.play(volume=0.5, loop=True)

        if testMode == "Live Mode" and (username != None and username != ""):


            try:
                
            
                client: TikTokLiveClient = TikTokLiveClient(unique_id="@"+username)

                def TikTokThread():
                    client.run()
            
                my_thread = threading.Thread(target=TikTokThread)
                my_thread.start()


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
            except Exception as e:
                 exception_type = type(e).__name__
                 exception_details = str(e)
                 self.show_error_popup(exception_type, exception_details)

    def on_draw(self):
        if not self.game_paused:
            arcade.start_render()

            if len(self.explosions) != 0:
                self.explosions.draw()

            self.red_health_bar.draw()
            self.blue_health_bar.draw()

            self.particles.draw()
            if len(self.lasers) != 0:
                self.lasers.draw()
            
            arcade.draw_text("1 Rose = more health for Trump ", 30, 450, arcade.color.BLACK,
                             font_size=17, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("1 GG = more health for Biden", 410, 450, arcade.color.BLACK,
                             font_size=17, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("trump shoots: /trump.shoot", 30, 400, arcade.color.BLACK,
                             font_size=20, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("biden shoots: /biden.shoot", 400, 400, arcade.color.BLACK,
                             font_size=20, bold=True, italic=True, anchor_x="left", anchor_y="baseline")

            arcade.draw_text("Trump (Red) Score: " + str(self.Red.score), 30, 500, arcade.color.BLACK,
                             font_size=25, bold=True, italic=True, anchor_x="left", anchor_y="baseline")
            arcade.draw_text("Biden (Blue) Score: " + str(self.Blue.score), 400, 500, arcade.color.BLACK,
                             font_size=25, bold=True, italic=True, anchor_x="left", anchor_y="baseline")

    def on_update(self, delta_time):
        self.ui_manager.on_update(delta_time)
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
    root = tk.Tk()
    app = TkinterWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
