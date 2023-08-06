"""
This module defines the GameObject class; an elementary class from which all visible game
objects inherit.

Classes:
    GameObject

Functions:
    GameObject(image, pos, window)
    GameObject.draw()
    GameObject.move()
    GameObject.is_colliding(other)
    GameObject.set_velocity()
    GameObject.bounce_horizontal()
    GameObject.bounce_vertical()
    GameObject.get_position()
    GameObject.get_velocity()
"""


class GameObject:
    """
    An elementary class from which all visible game objects inherit.

    Args:
        image (pygame.Surface): The visual image associated with the object.
        pos (list): A list denoting the object's position as a pair of cartesian coordinates.
        window (pygame.Surface): The game window on which to draw the object.

    Attributes:
        image: The image associated with the object.
        pos: The present position of the object as a pair of cartesian coordinates.
        window: The game window on which to draw the object.
        velocity: The present velocity of the object as a 2-dimensional vector.
    """
    def __init__(self, image, pos, window):
        self.image = image
        self.pos = pos
        self.window = window
        self.velocity = [0, 0]

    def draw(self):
        """
        Draw the object to the screen.

        Takes no arguments and returns nothing.
        """
        self.window.blit(self.image, self.pos)

    def move(self):
        """
        Update the position of the object according to its coordinates and velocity.

        Takes no arguments and returns nothing.
        """
        new_x_pos = self.pos[0] + self.velocity[0]
        new_y_pos = self.pos[1] + self.velocity[1]
        self.pos = [new_x_pos, new_y_pos]

    def is_colliding(self, other):
        """
        Detects if object is colliding with another game object.

        Args:
            other (GameObject): Another game object against which to test for collision.

        Returns:
            bool: True if colliding, false otherwise.
        """
        self_rect = self.image.get_rect(topleft=self.pos)
        other_rect = other.image.get_rect(topleft=other.pos)
        return self_rect.colliderect(other_rect)

    def set_velocity(self, new_velocity):
        """
        Set a new velocity for the object.

        Args:
            new_velocity (list): A 2-dimensional vector representing the new velocity.

        Returns:
            None.
        """
        self.velocity = new_velocity

    def bounce_horizontal(self):
        """
        Bounce the object in the horizontal axis by reversing its x-velocity.

        Takes no arguments and returns nothing.
        """
        self.velocity[0] *= -1

    def bounce_vertical(self):
        """
        Bounce the object in the vertical axis by reversing its y-velocity.

        Takes no arguments and returns nothing.
        """
        self.velocity[1] *= -1

    def get_position(self):
        """ Returns the object's position """
        return self.pos

    def get_velocity(self):
        """ Returns the object's velocity """
        return self.velocity
