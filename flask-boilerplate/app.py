#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

tests = [
    {
        "test": "Lipid Panel",
        "date": "10/10/23",
        "testId": 0,
        "results": [
            {
            "name": "Total Cholesterol",
            "normal": "Normal Range: 0 - 199 mg/dl",
            "value": 125
            },
            {
            "name": "Triglycerides",
            "normal": "Normal value: 0.00 - 150.00 mg/dL",
            "value": 90
            },
            {
            "name": "HDL Cholesterol",
            "normal": "Normal range: above >40 mg/dL",
            "value": 50
            },
            {
            "name": "HDL Cholesterol",
            "normal": "Normal range: above >40 mg/dL",
            "value": 50
            },
            {
            "name": "Non-HDL Cholesterol",
            "normal": "A reasonable goal for non-HDL cholesterol is one that is 30 mg/dL higher than the LDL cholesterol goal.",
            "value": 75
            },
            {
            "name": "CHOL/HDL Ratio",
            "normal": "Normal range: 0.0 - 5.0",
            "value": 2.5
            }
        ]
    },
    {
        "test": "Hemoglobin A1C",
        "date": "10/10/23",
        "testId": 1,
        "results": [
            {
            "name": "Hemoglobin A1C",
            "normal": "Normal value: 0 - 5.6 %",
            "value": 4.9
            }
        ]
    },
    {
        "test": "HSV TYPE 2 SPECIFIC ANTIBODY, IGG",
        "date": "10/10/23",
        "testId": 2,
        "results": [
            {
            "name": "Herpes Simplex Virus 2 IgG",
            "normal": "Normal value: Negative",
            "value": "Negative"
            },
            {
            "name": "Herpes Simples Virus 2 IgG, Quant",
            "normal": "Normal value: 0.0 - 0.8 AI",
            "value": "<0.2"
            }
        ]
    },
]

def getInfo(data):
    #will be used to call chatGPT but for now it is just gonna have some words
    return "I am chartchat and I am answering things"

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html', tests=tests, len=len(tests))


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/testData/<int:test_index>')
def testData(test_index):
    data = tests[test_index]
    info = getInfo(data)
    return render_template('pages/placeholder.testData.html', data=data, info=info)

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
