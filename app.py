# To run this script, you'll need to open a Anaconda Prompt, Navigate to the directory of this file, and run
# set FLASK_APP=app.py
# THEN type
# flask run
# In the returned information, copy the URL after "Running on" and paste it into the browser


#import flask dependency
from flask import Flask

# You probably noticed the __name__ variable inside of the Flask() function. Let's pause for a second and identify what's going on here.

# You can use the __name__ variable to determine if your code 
# is being run from the command line or if it has been imported into another piece of code. 
# Variables with underscores before and after them are called magic methods in Python.
app = Flask(__name__)

# we need to define the starting point, also known as the root
@app.route('/')
def hello_world():
    return 'Hello world'

