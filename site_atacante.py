from flask import Flask, render_template, url_for, request
import webbrowser

site = Flask(__name__)

@site.route('/', methods=['GET', 'POST'])
@site.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('site_atacante.html')

if __name__ == '__main__':
    site.run(debug=True)