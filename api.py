from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import io
from dotenv import load_dotenv



load_dotenv()

from nekoai import NovelAI
from nekoai.constant import Model, Noise, Resolution, Sampler
from nekoai.types import EmotionOptions, EmotionLevel

app = FastAPI()

token = os.environ.get("NAI_TOKEN")
client = NovelAI(token=token)

class ImageRequest(BaseModel):
    prompt: str
    negative_prompt: str  # 添加负向提示词
    model: str = "v4"
    res: str = "normal_portrait"
    steps: int = 28
    scale: float = 6.0
    sampler: str = "euler_anc"
    params_version: int = 3
    noise_schedule: str = "karras"
    uc_preset: int = 2

@app.get("/")
async def root():
    return {"message": "NekoAI API is running"}

@app.post("/generate-image/")
async def generate_image(request: ImageRequest):
    token = os.environ.get("NAI_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="NAI_TOKEN environment variable not set")

    async with NovelAI(token=token) as client:
        try:
            # Map string inputs to enum members
            model_map = {
                "v3": Model.V3,
                "v3_inp": Model.V3_INP,
                "v4": Model.V4,
                "v4_inp": Model.V4_INP,
                "v4_cur": Model.V4_CUR,
                "v4_cur_inp": Model.V4_CUR_INP,
                "v4_5": Model.V4_5,
                "v4_5_inp": Model.V4_5_INP,
                "v4_5_cur": Model.V4_5_CUR,
                "v4_5_cur_inp": Model.V4_5_CUR_INP,
                "furry": Model.FURRY,
                "furry_inp": Model.FURRY_INP,
            }
            res_map = {
                "small_portrait": Resolution.SMALL_PORTRAIT,
                "small_landscape": Resolution.SMALL_LANDSCAPE,
                "small_square": Resolution.SMALL_SQUARE,
                "normal_portrait": Resolution.NORMAL_PORTRAIT,
                "normal_landscape": Resolution.NORMAL_LANDSCAPE,
                "normal_square": Resolution.NORMAL_SQUARE,
                "large_portrait": Resolution.LARGE_PORTRAIT,
                "large_landscape": Resolution.LARGE_LANDSCAPE,
                "large_square": Resolution.LARGE_SQUARE,
                "wallpaper_portrait": Resolution.WALLPAPER_PORTRAIT,
                "wallpaper_landscape": Resolution.WALLPAPER_LANDSCAPE,
            }
            sampler_map = {
                "euler": Sampler.EULER,
                "euler_anc": Sampler.EULER_ANC,
                "dpm2s_anc": Sampler.DPM2S_ANC,
                "dpm2m": Sampler.DPM2M,
                "dpm2msde": Sampler.DPM2MSDE,
                "dpmsde": Sampler.DPMSDE,
                "ddim": Sampler.DDIM,
            }
            noise_map = {
                "native": Noise.NATIVE,
                "karras": Noise.KARRAS,
                "exponential": Noise.EXPONENTIAL,
                "polyexponential": Noise.POLYEXPONENTIAL,
            }

            model_val = model_map.get(request.model.lower().replace('.', '_').replace('-', '_'))
            if not model_val:
                raise HTTPException(status_code=400, detail=f"Invalid model: {request.model}. Available: {list(model_map.keys())}")

            res_preset_val = res_map.get(request.res.lower())
            if not res_preset_val:
                raise HTTPException(status_code=400, detail=f"Invalid resolution: {request.res}. Available: {list(res_map.keys())}")

            sampler_val = sampler_map.get(request.sampler.lower())
            if not sampler_val:
                raise HTTPException(status_code=400, detail=f"Invalid sampler: {request.sampler}. Available: {list(sampler_map.keys())}")

            noise_schedule_val = noise_map.get(request.noise_schedule.lower())
            if not noise_schedule_val:
                raise HTTPException(status_code=400, detail=f"Invalid noise schedule: {request.noise_schedule}. Available: {list(noise_map.keys())}")

            images = await client.generate_image(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,  # 添加这行
                model=model_val,
                res_preset=res_preset_val,
                steps=request.steps,
                scale=request.scale,
                sampler=sampler_val,
                params_version=request.params_version,
                noise_schedule=noise_schedule_val,
                uc_preset=request.uc_preset,
            )

            if not images:
                raise HTTPException(status_code=500, detail="Image generation failed")

            # For simplicity, return the first image
            image_bytes = images[0].data
            return StreamingResponse(io.BytesIO(image_bytes), media_type="image/png")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


# Helper for Director Tools
async def process_director_tool(tool_name: str, image_bytes: bytes, **kwargs):
    token = os.environ.get("NAI_TOKEN")
    if not token:
        raise HTTPException(status_code=500, detail="NAI_TOKEN environment variable not set")

    async with NovelAI(token=token) as client:
        try:
            # Get the specific tool function from the client instance
            tool_function = getattr(client, tool_name)
            
            # Call the tool function with the image and any other arguments
            result_image = await tool_function(image_bytes, **kwargs)
            
            if not result_image:
                raise HTTPException(status_code=500, detail=f"Image processing with '{tool_name}' failed")

            image_bytes_result = result_image.data
            return StreamingResponse(io.BytesIO(image_bytes_result), media_type="image/png")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# Director Tool Endpoints

@app.post("/lineart/")
async def lineart(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return await process_director_tool("lineart", image_bytes)

@app.post("/sketch/")
async def sketch(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return await process_director_tool("sketch", image_bytes)

@app.post("/background-removal/")
async def background_removal(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return await process_director_tool("background_removal", image_bytes)

@app.post("/declutter/")
async def declutter(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return await process_director_tool("declutter", image_bytes)

@app.post("/colorize/")
async def colorize(
    file: UploadFile = File(...),
    prompt: str = Form(""),
    defry: int = Form(0)
):
    image_bytes = await file.read()
    return await process_director_tool("colorize", image_bytes, prompt=prompt, defry=defry)

@app.post("/change-emotion/")
async def change_emotion(
    file: UploadFile = File(...),
    emotion: EmotionOptions = Form(...),
    prompt: str = Form(""),
    emotion_level: EmotionLevel = Form(EmotionLevel.NORMAL)
):
    image_bytes = await file.read()
    return await process_director_tool(
        "change_emotion", 
        image_bytes, 
        emotion=emotion, 
        prompt=prompt, 
        emotion_level=emotion_level
    )


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
