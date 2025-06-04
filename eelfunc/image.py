import logging

from features.image_manager import ImageManager

image_manager = ImageManager()


def generate_image(query: str):
    logging.info(f"generating image for {query}")
    image_manager.generate(query)
