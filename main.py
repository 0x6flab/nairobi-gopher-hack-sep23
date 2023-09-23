import os
from twilio.rest import Client
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from requests.auth import HTTPBasicAuth

account_sid = os.environ.get('TWILIO_ACCOUNT_SID', "")
auth_token = os.environ.get('TWILIO_AUTH_TOKEN', "")
print(account_sid)
client = Client(account_sid, auth_token)


app = Flask(__name__)

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
        
        file_res = requests.get(file_url, auth=HTTPBasicAuth(account_sid, auth_token))
        if file_res.status_code == 200:
            local_filepath = "statement.pdf"
            with open(local_filepath, 'wb') as local_file:
                local_file.write(file_res.content)
            msg = response.message("Some sage advice for you")
        else:
            msg = response.message("Failed to retieve file")
    return str(response)


if __name__ == "__main__":
    app.run()

