from flask import Flask, render_template, url_for, redirect
import requests
import time
import json

site = Flask(__name__)

@site.route('/', methods=['GET', 'POST'])
@site.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('site_atacante.html')

@site.route('/req', methods=['GET', 'POST'])
def req():
    r = requests.post('http://localhost:5000/login', 
                    data=json.dumps({'email':'ola@diga.com', 'password':'lui'}), 
                    headers={'content-type': 'application/json'})
    response = r.json()
    print(response)
    
    response = requests.get('http://127.0.0.1:5000/login?include_auth_token', headers={"Content-Type": "application/json"})
    print(response.text)
    time.sleep(10)
    return redirect(url_for('index'))

if __name__ == '__main__':
    site.run(debug=True, port=5001)