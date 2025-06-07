from flask import Flask, render_template, url_for
from flask import request
from configparser import ConfigParser
import google.generativeai as genai

# Config Parser
config = ConfigParser()
config.read("config.ini")

genai.configure(api_key=config["Gemini"]["API_KEY"])

from google.generativeai.types import HarmCategory, HarmBlockThreshold

llm = genai.GenerativeModel(
    "gemini-2.0-flash-lite",
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
chat = llm.start_chat(history=[])

role = """
你是一位充滿智慧的圖書館管理員，已經在圖書館工作了30年。
你熱愛文學和哲學，特別喜歡與訪客分享你對書籍的見解。
你的目標是幫助訪客找到最適合他們的書籍，並分享你對閱讀的熱情。
請用這個角色回答訪客的問題，展現你的專業知識和對書籍的熱愛。
"""

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/call_llm", methods=["POST"])
def call_llm():
    if request.method == "POST":
        print("POST!")
        data = request.form
        print(data)
        to_llm = ""
        if len(chat.history) > 0:
            to_llm = data["message"]
        else:
            to_llm = role + data["message"]
        try:
            result = chat.send_message(to_llm)
        except Exception as e:
            print(e)
            return f"抱歉，發生了一些問題：{str(e)}"
        print(chat.history)
        # remove \n at the end of the result
        return result.text.replace("\n", "")