from flask import Flask, request, jsonify, send_file
import json
import modules.commands as commands
import os
from flask_executor import Executor

app = Flask(__name__)
executor = Executor(app)

# Custom verification token
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']


@app.route('/', methods=['GET', 'HEAD'])
def index():
  if request.method == 'HEAD':
    custom_header = {'Amogus': 'Sus'}
    return 'keep-alive', 200, custom_header
  else:
    return 'Stars Browser'


@app.route('/file/<filename>')
def get_file(filename):
  file_path = f'static/{filename}'
  return send_file(file_path, as_attachment=True)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'GET':
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if token == VERIFY_TOKEN:
      return challenge
    else:
      return jsonify({'error': 'Invalid verification token'}), 403

  elif request.method == 'POST':
    data = json.loads(request.get_data(as_text=True))
    value = data['entry'][0]['changes'][0]['value']

    executor.submit(commands.build_response, value)

    return 'Processing webhook event', 200

  return jsonify({'error': 'Invalid request'}), 400


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
