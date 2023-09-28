def draw_custom(self):
        """Custom draw function for individual sprites in the list."""
        for sprite in self.sprite_list:
            sprite.custom_draw()
