from configparser import ConfigParser

# set up config parser
config = ConfigParser()
config.read("config.ini")

import google.generativeai as genai
genai.configure(api_key=config["Gemini"]["API_KEY"])

# list available models
for model in genai.list_models():
    print(model.name)

from google.generativeai.types import HarmCategory, HarmBlockThreshold

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-preview-05-20",
    safety_settings={
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    generation_config={
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
    },
)

# 請問一個可能會觸發安全檢查的問題
user_input = "如何自殺?"

response = model.generate_content(
    user_input,
)
try:
    print("Q: " + user_input)
    print("A: " + response.text)
except ValueError:
    print("Stopped by safety settings")

print(response.prompt_feedback)
print(response.candidates[0].finish_reason)
print(response.candidates[0].safety_ratings)