import os
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from requests.auth import HTTPBasicAuth
from gpt.lib import GPT
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', "")
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', "")
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', "")

client = Client(ACCOUNT_SID, AUTH_TOKEN)


app = Flask(__name__)
gpt = GPT(token=OPENAI_API_KEY)

@app.route("/whatsapp", methods=["GET", "POST"])
def reply_whatsapp():

    try:
        num_media = int(request.values.get("NumMedia"))
    except (ValueError, TypeError):
        return "Invalid request: invalid or missing parameter", 400
    response = MessagingResponse()
    if not num_media:
        msg = response.message("Send us a pdf of your statment!")
    else:
        file_url = request.values.get("MediaUrl0")
        
        file_res = requests.get(file_url, auth=HTTPBasicAuth(ACCOUNT_SID, AUTH_TOKEN))
        if file_res.status_code == 200:
            local_filepath = "statement.pdf"
            with open(local_filepath, 'wb') as local_file:
                local_file.write(file_res.content)
            gpt_response = gpt.chat_with_file(file=local_filepath)
            msg = response.message(gpt_response)
        else:
            msg = response.message("Failed to retieve file")
    
    return str(response)


if __name__ == "__main__":
    app.run()

