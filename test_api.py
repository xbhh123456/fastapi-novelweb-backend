import requests
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量获取 API 地址，如果未设置则使用默认值
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/generate-image/")

# 从环境变量获取 NAI_TOKEN，如果未设置则提示
NAI_TOKEN = os.getenv("NAI_TOKEN")
if not NAI_TOKEN:
    print("错误：NAI_TOKEN 环境变量未设置。请在运行脚本前设置它。")
    print("例如：在命令行中设置 'set NAI_TOKEN=你的实际token' (Windows) 或 'export NAI_TOKEN=你的实际token' (Linux/macOS)")
    exit(1)

# 请求体数据
payload = {
    "prompt": "masterpiece, best quality, 1girl, solo, long hair, blue eyes, white dress, forest, sunlight",
    "model": "v4_5",
    "res": "normal_portrait",
    "steps": 28,
    "scale": 6.0,
    "sampler": "euler_anc",
    "params_version": 3,
    "noise_schedule": "karras",
    "uc_preset": 2
}

print(f"正在向 {API_URL} 发送请求...")
print(f"请求负载: {payload}")

try:
    # 发送 POST 请求
    response = requests.post(API_URL, json=payload)

    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功！")
        # 保存图片
        with open("generated_image.png", "wb") as f:
            f.write(response.content)
        print("图片已成功保存为 generated_image.png")
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(f"错误信息: {response.text}")

except requests.exceptions.ConnectionError:
    print("连接错误：请确保 FastAPI 服务器正在运行 (api.py)。")
    print("在命令行中运行 'python api.py' 来启动服务器。")
except Exception as e:
    print(f"发生未知错误: {e}")
