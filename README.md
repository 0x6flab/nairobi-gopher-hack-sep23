# nairobi-gopher-hack-sep23

## Introduction

Welcome to FinAdvise, an AI-powered WhatsApp bot designed to provide personalized financial advice based on your bank statements. This README will guide you through the setup and usage of the FinAdvise bot. With FinAdvise, you can effortlessly gain insights into your spending habits, identify savings opportunities, and receive budget recommendations, all through the convenience of WhatsApp.

## Prerequisites

Before you get started with FinAdvise, make sure you have the following prerequisites installed:

1. Python 3.7 or higher
2. Twilio account with an active phone number and API credentials
3. OpenAI API key
4. Requirements listed in requirements.txt

You can install the required Python packages using pip by running:

```bash
pip install -r requirements.txt
```

## Installation

Clone the FinAdvise repository to your local machine:

```bash
git clone https://github.com/0x6flab/nairobi-gopher-hack-sep23/
cd nairobi-gopher-hack-sep23
pip install -r requirements.txt
```

## Configuration

To configure FinAdvise, you need to set up environment variables. Create a .env file in the project directory and add the following information:

```env
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
OPENAI_API_KEY=your_openai_api_key
```

Replace your_twilio_account_sid, your_twilio_auth_token, and your_openai_api_key with your actual credentials.

## Usage

Run the FinAdvise bot:

```bash
python app.py
```

Connect your WhatsApp to Twilio and set up a webhook to handle incoming messages. Refer to Twilio's documentation on how to do this.

Start a conversation with the FinAdvise bot on WhatsApp. You can send a PDF of your bank statement.

The bot will analyze the statement and provide financial insights and budget recommendations.

Enjoy personalized financial advice at your fingertips!

## Contributing

We welcome contributions to FinAdvise. If you have any ideas for improvements or find any issues, please submit them to our GitHub repository.

## License

This project is licensed under the MIT License. Feel free to use and modify it according to your needs.

Thank you for using FinAdvise! We hope this bot helps you gain better control of your finances.
