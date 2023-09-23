import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request, Response

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/prompt", methods=["POST"])
def prompt():
    messages = request.json['messages']
    conversation = build_conversation_dict(messages)

    return Response(event_stram(conversation), mimetype='text/event-stream')



def build_conversation_dict(messages:list) -> list[dict]:
    result = []
    for i, message in enumerate(messages):
        result.append({"role": "user" if i % 2 == 0 else "assistant", "content" : message})
    return result


def event_stram(conversation: list[dict]) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        stream=True
    )
    for line in response:
        text = line.choices[0].delta.get('content', '')
        if len(text):
            yield text


if __name__ == '__main__':
    app.run(debug=True, host="192.168.1.77", port=5000)
    # conversation = build_conversation_dict(messages=["Bonjour, comment ça va ?", "ça va bien et toi ?"])
    # for line in event_stram(conversation):
    #     print(line)