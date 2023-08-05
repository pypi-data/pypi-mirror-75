import pygame
from coopstructs.vectors import Vector2
from coopgame.colors import Color

class MySprite(pygame.sprite.Sprite):
    def __init__(self, id:str, init_pos: Vector2, width: int, height: int):
        super().__init__()

        self.id = id

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.surf = pygame.Surface([width, height])
        self.surf.fill(Color.WHITE.value)
        self.surf.set_colorkey(Color.WHITE.value)


        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.surf.get_rect()

        self.set_pos(init_pos)

    def set_pos(self, pos: Vector2):
        self.rect = self.surf.get_rect(
            center=(
                pos.x,
                pos.y
            )
        )

class RectangleSprite(MySprite):
    def __init__(self, id:str, init_pos: Vector2, color: Color, width: int, height: int):
        # Call the parent class (Sprite) constructor
        MySprite.__init__(self, id, init_pos, width, height)

        pygame.draw.rect(self.surf, color.value, [0, 0, width, height])