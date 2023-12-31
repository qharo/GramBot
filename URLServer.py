from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Set up the necessary parameters
api_token = os.environ.get("TOKEN")
webhook_url = os.environ.get("myUrl")


# Webhook endpoint
@app.route('/secret_endpoint', methods=['POST'])
def webhook():
    # Retrieve the JSON data from Telegram
    update = request.get_json()

    send_message(f"I got your message, it was: {update['message']['text']}")

    return 'OK'

# Send a message using the Telegram Bot API
def send_message(text):
    # Construct the URL for the sendMessage endpoint
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'    
    chat_id = '6090938484'
    
    # Set up the request payload
    payload = {
        'chat_id': chat_id,
        'text': text
    }

    # Make the POST request
    response = requests.post(url, json=payload)

    # Check the response status code
    if response.ok:
        return True
    else:
        return False

@app.route('/send_message', methods=['POST'])
def sendMessage():
    if request.json and 'text' in request.json:
        text = request.json['text'] # Replace with the chat ID you want to send the message to

    if(send_message(text=text)):
        return {"status": "OK"}
    return {'error': 'Invalid request'}


# Set up the webhook
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    # Construct the URL for the setWebhook endpoint
    url = f'https://api.telegram.org/bot{api_token}/setWebhook?url={webhook_url}/secret_endpoint'

    # Make the request to set the webhook
    response = requests.get(url)

    # Check the response status code
    if response.ok:
        print('Webhook set successfully!')
    else:
        print('Failed to set the webhook.')

    return 'OK'

if __name__ == '__main__':
    # Set the webhook
    set_webhook()

    # Run the Flask app
    app.run(debug=True)
