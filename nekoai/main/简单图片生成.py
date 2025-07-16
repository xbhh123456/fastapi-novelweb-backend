import asyncio
from nekoai import NovelAI
from nekoai.constant import Model, Resolution

async def generate_basic_image():
    # Client auto-initializes on first request
    client = NovelAI(token="your_access_token", verbose=True)
    
    try:
        # Direct parameter approach
        images = await client.generate_image(
            prompt="1girl, cute, anime style, detailed",
            model=Model.V4_5_CUR,
            res_preset=Resolution.NORMAL_PORTRAIT,
            seed=1234567890  # Fixed seed for reproducibility
        )
        
        # Save generated images
        for image in images:
            image.save(path="output")
            print(f"Image saved: {image.filename}")
            
    finally:
        await client.close()

asyncio.run(generate_basic_image())