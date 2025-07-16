#!/usr/bin/env python3
"""
Example script for generating an image with NovelAI API using the V4.5 curated model.
Authentication is done with a direct access token.
"""

import asyncio
import os

from nekoai import NovelAI
from nekoai.constant import Model, Resolution, Sampler


async def main():
    # Use your NAI token (replace with your actual token)
    token = os.environ.get("NAI_TOKEN")

    # Initialize client with token authentication
    client = NovelAI(token=token, verbose=True)

    try:
        # Generate an image with V4.5 curated model
        images = await client.generate_image(
            prompt="1girl, cute",
            negative_prompt="1234",
            ucPreset=3,
            scale=5,
            seed="3417044607",
            steps=30,
            n_samples=1,
            model=Model.V4_5,
            res_preset=Resolution.NORMAL_PORTRAIT,
            sampler=Sampler.EULER_ANC,
        )

        # Save the generated image(s)
        for i, image in enumerate(images):
            # Create output directory if it doesn't exist
            os.makedirs("../output", exist_ok=True)
            # Save the image
            image.save("../output", f"v4_5_result_{i}.png")
            print(f"Image saved as output/v4_5_result_{i}.png")

    finally:
        # Close the client
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
