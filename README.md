# paper-clip-server
Flask app for paper-clip-app. Uses poetry as a dependency manager, to run:

1. Install Poetry
2. Run 'poetry install'
3. Run 'poetry run python ./server_config.py'

Using ngrok to port localhost:
1. Install ngrok
2. Run 'ngrok http 5000' (or whichever localhost port app is running on)
3. Update url in paper-clip-app server-conn.js file