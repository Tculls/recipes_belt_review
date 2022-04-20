from flask import Flask



app = Flask(__name__)

app.secret_key = "oijaefswojiefsa"

# flash messages get saved into session