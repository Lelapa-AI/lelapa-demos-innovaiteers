#!/bin/bash

# loading env variables...
source .env
pip install -r requirements.txt
# making sure ngrok is installed and authenticated
# curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
#   sudo gpg --dearmor -o /etc/apt/keyrings/ngrok.gpg && \
#   echo "deb [signed-by=/etc/apt/keyrings/ngrok.gpg] https://ngrok-agent.s3.amazonaws.com buster main" | \
#   sudo tee /etc/apt/sources.list.d/ngrok.list && \
#   sudo apt update && sudo apt install ngrok
ngrok config add-authtoken $NGROK_AUTHTOKEN
#running the server
python main.py & sleep 8 &
ngrok http --domain=tolerant-terribly-flea.ngrok-free.app 5000
