#Ping bot 5p 1 lần để giữ bot luôn hoạt động
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Hello. We are still awake!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()