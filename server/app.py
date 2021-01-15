import subprocess

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/crawl", methods=['POST'])
def crawl():
    data = request.get_json(force=True)
    source = data['source']
    process = subprocess.Popen(['python3.7', 'crawl.py', '--source', source], stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    return 'done'

@app.route("/", methods=['GET'])
def hello():
    return 'Hello world.'


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)