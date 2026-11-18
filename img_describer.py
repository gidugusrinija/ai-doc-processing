
import base64


from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


# Initialize vision model
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

# Local image path
image_path = r"C:\Users\Srinija\Downloads\lordrama.jpg"

# Read image and convert to Base64
with open(image_path, "rb") as image_file:
    image_bytes = image_file.read()

base64_image = base64.b64encode(
    image_bytes
).decode("utf-8")

# Create multimodal message
message = HumanMessage(
    content=[
        {
            "type": "text",
            "text": "Describe this image in detail."
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}",
                "detail": "high"
            }
        }
    ]
)

# Invoke LLM
response = llm.invoke([message])

print(response.content)
