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
