import arcade

class HealthBar(arcade.Sprite):
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.max_health = character.max_health
        self.current_health = character.max_health
        self.width = 100  # Width of the health bar
        self.height = 10  # Height of the health bar
        self.dead = False
        self.text_x = self.character.center_x
        self.text_y = self.character.center_y + 20

    def draw(self):
        arcade.draw_text(self.character.owner, self.text_x, self.text_y, arcade.color.BLACK, font_size=12, anchor_x="center")
        bar_width = (self.current_health / self.max_health) * self.width

        # Calculate the position of the health bar above the character
        x = self.character.center_x - self.width / 2
        y = self.character.center_y + self.character.height / 2 + 10  # Adjust the vertical position as needed

        # Draw the health bar background (full width)
        arcade.draw_rectangle_filled(x + self.width / 2, y, self.width, self.height, arcade.color.BLACK)

        # Draw the health bar based on the current health (calculated width)
        arcade.draw_rectangle_filled(x + bar_width / 2, y, bar_width, self.height, arcade.color.GREEN)

    def update(self, current_health):
        # Update the current health
        self.current_health = current_health
        self.text_x = self.character.center_x
        self.text_y = self.character.center_y + 40

        if self.current_health < 1:
            self.kill()
