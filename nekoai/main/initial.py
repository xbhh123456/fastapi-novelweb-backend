import asyncio
from nekoai import NovelAI

async def main():
    # Option 1: Username/password authentication (auto-initializes)
    client = NovelAI(username="your_username", password="your_password")
    
    # Option 2: Token authentication (recommended, auto-initializes)
    client = NovelAI(token="your_access_token")
    
    # Option 3: Manual initialization with custom settings
    client = NovelAI(token="your_access_token")
    await client.init(timeout=60, auto_close=True)  # Custom timeout and auto-close
    
    # Your API calls here - client auto-initializes on first request
    
    # Close when done (optional if using auto_close=True)
    await client.close()

asyncio.run(main())