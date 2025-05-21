from pathlib import Path

import ollama

from features.base import Base


class ImageManager(Base):
    def check_trigger(self) -> bool:
        if self.query.startswith(("generate image", "vision")):
            return True
        return False

    def read_img(self, file: Path, question: str) -> str:
        print(str(file.absolute()))
        with open(file, 'rb') as f:
            image_data = f.read()
            digest = ollama.generate(
                model="llama3.2-vision",
                prompt=question,
                images=[image_data]
            )
            return digest.response.strip()

def cli():
    im = ImageManager("vision what do you see")
    print(im.read_img(Path('/home/knownblackhat/Downloads/computational.png'), "what do you see"))


if __name__ == "__main__":
    cli()

