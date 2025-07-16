import asyncio
from nekoai import NovelAI, Metadata
from nekoai.constant import Model, Resolution, Sampler

async def generate_with_metadata():
    client = NovelAI(token="your_access_token", verbose=True)
    
    try:
        # Create metadata object with structured parameters
        metadata = Metadata(
            prompt="1girl, cute, anime style, detailed",
            model=Model.V4_5_CUR,
            res_preset=Resolution.NORMAL_PORTRAIT,
            steps=30,
            scale=5,
            sampler=Sampler.EULER_ANC,
            n_samples=1
        )
        
        # Generate using metadata object
        images = await client.generate_image(metadata)
        
        for image in images:
            image.save("output")
            
    finally:
        await client.close()

asyncio.run(generate_with_metadata())