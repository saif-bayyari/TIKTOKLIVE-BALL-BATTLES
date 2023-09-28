SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
import arcade

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2

        self.speed = 5

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Keep the player within the screen boundaries
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1