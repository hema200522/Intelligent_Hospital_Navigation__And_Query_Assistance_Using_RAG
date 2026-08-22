import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("NVIDIA_API_KEY")

if key:
    print("NVIDIA API key loaded successfully")
    print("Key starts with:", key[:10])
else:
    print("NVIDIA API key NOT found")