from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from IPython.display import Image, display
from configparser import ConfigParser
import base64

config = ConfigParser()
config.read("config.ini")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=config["Gemini"]["API_KEY"],
    max_tokens=8192,
)

def image4LangChain(image_url):
    if "http" in image_url:
        return image_url
    else:
        with open(image_url, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        return f"data:image/jpeg;base64,{image_data}"

user_messages = []
# append user input question
# user_input = "請描述圖片中飛機機型的詳細資訊。解釋外觀、性能、用途等差異。"
user_input = "請給我這張截圖的完整的可執行的HTML程式碼，並且包含CSS和JavaScript，讓我可以在瀏覽器中執行。"
user_messages.append({"type": "text", "text": user_input + "請使用繁體中文回答。"})

# append images

# online image
# image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/South_African_Airlink_Boeing_737-200_Advanced_Smith.jpg/960px-South_African_Airlink_Boeing_737-200_Advanced_Smith.jpg"
# user_messages.append({"type": "image_url", "image_url": image4LangChain(image_url)})

# # local image
# image_url2 = "plane.jpg"
# user_messages.append({"type": "image_url", "image_url": image4LangChain(image_url2)})

image_url = "web.png"
user_messages.append({"type": "image_url", "image_url": image4LangChain(image_url)})


human_messages = HumanMessage(content=user_messages)
result = llm.invoke([human_messages])

print("Q: " + user_input)
print("A: " + result.content)

# Display the image
display(Image(url=image_url))
# display(Image(url=image_url2))
