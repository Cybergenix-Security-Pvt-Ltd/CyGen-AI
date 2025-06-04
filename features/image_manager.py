import asyncio
import os
from pathlib import Path
from random import randint

import ollama
import requests

from features.base import Base


class ImageManager(Base):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
        self.headers = {"Authorization": f"Bearer {os.getenv('HUGGING')}"}

    def check_trigger(self, query: str) -> bool:
        if query.startswith(("generate image", "vision")):
            return True
        return False

    def read_img(self, file: Path, question: str) -> str:
        print(str(file.absolute()))
        with open(file, "rb") as f:
            image_data = f.read()
            digest = ollama.generate(
                model="llama3.2-vision", prompt=question, images=[image_data]
            )
            return digest.response.strip()

    def generate(self, prompt: str) -> None:
        asyncio.run(self.generate_images(prompt))

    async def query(self, payload):
        response = await asyncio.to_thread(
            requests.post, self.api_url, headers=self.headers, json=payload
        )
        return response.content

    async def generate_images(self, prompt: str):

        tasks = []

        for _ in range(1):
            payload = {
                "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed = {randint(0, 1000000)}",
            }
            task = asyncio.create_task(self.query(payload))
            tasks.append(task)

        image_bytes_list = await asyncio.gather(*tasks)

        for i, image_bytes in enumerate(image_bytes_list):
            with open(rf"images/{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
                f.write(image_bytes)
        os.system("sxiv images; rm -rf images")


def cli():
    im = ImageManager()
    # print(
    #     im.read_img(
    #         Path("/home/knownblackhat/Downloads/computational.png"), "what do you see"
    #     )
    # )
    im.generate("iron man")


if __name__ == "__main__":
    cli()
