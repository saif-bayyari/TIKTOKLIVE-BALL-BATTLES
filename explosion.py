import arcade

# Define the path to your explosion tile images and the number of frames
EXPLOSION_PATH = "animation/"
NUMBER_OF_FRAMES = 32

class Explosion(arcade.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()

        self.center_x = center_x
        self.center_y = center_y

        # Initialize variables for animation control
        self.current_frame = 0
        self.frame_duration = 0.1  # Adjust as needed
        self.frame_timer = 0

        # Load your explosion textures
        self.explosion_textures = []
        for i in range(NUMBER_OF_FRAMES):
            texture = arcade.load_texture(f"{EXPLOSION_PATH}tile{i}.png")
            self.explosion_textures.append(texture)

        # Set the initial texture
        self.texture = self.explosion_textures[0]

    def update(self):
        # Update the frame timer
        self.frame_timer += (1/60)

        # Check if it's time to advance to the next frame
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.current_frame += 1

            # Loop the animation
            if self.current_frame >= len(self.explosion_textures):
                print('finished')
                self.kill()
                return

            # Set the current frame's texture
            self.texture = self.explosion_textures[self.current_frame]
