import pygame
from math import ceil


def load_anim_images(path, start, stop, size=None):
    """
    :param path: Path to the items' directory with <> for location of iterator
    :param start: Start position in # (inclusive)
    :param stop: Stop position in # (inclusive)
    :param size: Size of the items to rescale if necessary
    :return: Dictionary with all the items
    """

    images_dict = {}
    placeholder_pre, placeholder_post = path.find("<"), (path.find(">") + 1)

    for x in range(start, stop + 1):
        formatted_path = path[:placeholder_pre] + str(x) + path[placeholder_post:]
        tmp = pygame.image.load(formatted_path).convert_alpha()

        if size is not None:
            tmp = pygame.transform.scale(tmp, (round(size[0]), round(size[1]))).convert_alpha()

        images_dict[x] = tmp

    return images_dict


def rot_center(image, angle, x, y):
    """ Rotate the provided image from the center point.
    :param image: The image being rotated
    :param angle: The angle of rotation
    :param x: The image's X position
    :param y: The image's Y position
    :return: A valid surface object & new X/Y position
    """
    rotated_image = pygame.transform.rotate(image, ceil(angle))  # Rotate the image
    new_rect = rotated_image.get_rect(center=image.get_rect(center=(x, y)).center)  # Get the new rectangle from center

    return rotated_image, new_rect

# ROUNDED RECTANGLES FUNCTION | CREATE ROUNDED RECTANGLES | ISAAC KOGAN


def rounded_rectangle(r_rect, r_colour, r_radius=0.6):  # A simple function to create a rounded rectangle
    """Creates a rounded rectangle on a given surface.

    :param r_surface: The surface in which the rounded rectangle will be drawing on
    :param r_rect: The rectangle's information such as x-coordinate, y-coordinate width, height in a tuple
    :param r_colour: The RGB (or RGBA) colour
    :param r_radius: The curve of the rectangle
    :return: Returns the blitted object
    """

    # Declarations/ Definitions
    r_rect = pygame.Rect(r_rect)           # Defining it as a Rect object
    r_colour = pygame.Color(*r_colour)     # Defining its a color object
    alpha = r_colour.a              # Also accepting alpha (RGBA)
    r_colour.a = 0                  # Setting def. value
    pos = r_rect.topleft            # Setting position to top left
    r_rect.topleft = 0, 0           # 0, 0
    rectangle = pygame.Surface(r_rect.size, pygame.SRCALPHA)  # Working with the provided "Surface" to create rectangle information

    # Calculations
    circle = pygame.Surface([min(r_rect.size) * 3] * 2, pygame.SRCALPHA)  # Calculating circle
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)   # Calculating ellipse
    circle = pygame.transform.smoothscale(circle, [int(min(r_rect.size) * r_radius)] * 2)  # Calculating transformations w/ the circle to create rounded edges

    # Blitting
    r_radius = rectangle.blit(circle, (0, 0))   # Blitting based on radius in initial value (top left)

    r_radius.bottomright = r_rect.bottomright   # Going to bottom right
    rectangle.blit(circle, r_radius)            # Blitting based on radius

    r_radius.topright = r_rect.topright         # Going to top right
    rectangle.blit(circle, r_radius)            # Blitting based on radius

    r_radius.bottomleft = r_rect.bottomleft     # Going to bottom left
    rectangle.blit(circle, r_radius)            # Blitting based on radius

    # Filling
    rectangle.fill((0, 0, 0), r_rect.inflate(-r_radius.w, 0))   # Filling area via radius
    rectangle.fill((0, 0, 0), r_rect.inflate(0, -r_radius.h))   # Filling more area via radius
    rectangle.fill(r_colour, special_flags=pygame.BLEND_RGBA_MAX)      # More filling
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)   # Final Filling

    # Returning a rounded rectangle (surface) with its position
    return rectangle

    # Call Example:
    # rounded_rectangle((20, 20, 1220, 130), DARK_TURQUOISE, 0.2)
