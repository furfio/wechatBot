# -*- coding: utf-8 -*-
import os
import logging
import datetime

import openai
openai.api_type = "azure"
openai.api_version = "2023-03-15-preview" 
# openai.api_base = os.getenv("OPENAI_API_BASE")  # Your Azure OpenAI resource's endpoint value.
openai.api_base = "https://testdizzybot.openai.azure.com/"  # Your Azure OpenAI resource's endpoint value.
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "84d92a3043f140228239e0a84206b221"

from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

# set token or get from environments
TOKEN = os.getenv("WECHAT_TOKEN", "123456")
AES_KEY = os.getenv("WECHAT_AES_KEY", "")
APPID = os.getenv("WECHAT_APPID", "wxcea8c9bd48f22718")

app = Flask(__name__)
log_dir = os.path.join(app.root_path, 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'app.log')

handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

@app.before_request
def log_request_info():
    logger.debug('UTC time: %s', datetime.datetime.utcnow())
    logger.debug('Request message: %s %s', request.method, request.url)
    logger.debug('Request data: %s', request.get_data())

@app.after_request
def log_response_info(response):
    logger.debug('Response message: %s', response.status)
    logger.debug('Response data: %s', response.get_data())
    return response

@app.errorhandler(Exception)
def handle_error(e):
    logger.error('An error occurred: %s', str(e), exc_info=True)
    return 'An error occurred.', 500

def askGPT(question):
    answer = ""
    try:
        response = openai.ChatCompletion.create(
        engine="bot002", # The deployment name you chose when you deployed the ChatGPT or GPT-4 model.
        messages=[
            {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "user", "content": question}
        ],
        temperature=0,
        max_tokens=500
        )
        answer = response['choices'][0]['message']['content']
    except:
        answer = "Model is busy, try again later."
    return answer


@app.route("/")
def index():
    host = request.url_root
    return render_template("index.html", host=host)

@app.route("/hello")
def hello():
    return "hello"

@app.route("/helloq")
def helloq():
    return askGPT("怎么做鱼香肉丝?")


@app.route("/wechat", methods=["GET", "POST"])
def wechat():
    signature = request.args.get("signature", "")
    timestamp = request.args.get("timestamp", "")
    nonce = request.args.get("nonce", "")
    encrypt_type = request.args.get("encrypt_type", "raw")
    msg_signature = request.args.get("msg_signature", "")
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "GET":
        echo_str = request.args.get("echostr", "")
        return echo_str

    # POST request
    if encrypt_type == "raw":
        # plaintext mode
        msg = parse_message(request.data)
        if msg.type == "text":
            reply = create_reply(askGPT(msg.content), msg)
        else:
            reply = create_reply("Sorry, can not handle this for now", msg)
        return reply.render()
    else:
        # encryption mode
        from wechatpy.crypto import WeChatCrypto

        crypto = WeChatCrypto(TOKEN, AES_KEY, APPID)
        try:
            msg = crypto.decrypt_message(request.data, msg_signature, timestamp, nonce)
        except (InvalidSignatureException, InvalidAppIdException):
            abort(403)
        else:
            msg = parse_message(msg)
            if msg.type == "text":
                reply = create_reply(msg.content, msg)
            else:
                reply = create_reply("Sorry, can not handle this for now", msg)
            return crypto.encrypt_message(reply.render(), nonce, timestamp)


if __name__ == "__main__":
    app.run("127.0.0.1", 5000)