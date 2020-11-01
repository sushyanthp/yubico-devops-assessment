#!/usr/bin/python3

from flask import Flask
from datetime import datetime
import json

app = Flask("Yubico_DevOps")        # Flask App Name

@app.route('/', methods=['GET'])
def index():
    """This method is used to return the current date in ISO 8601 format.
    
    Value of the date is stored in a dictionary and returned as JSON."""
    date_dict={}
    date_today=(datetime.now().strftime('%Y-%m-%d'))
    date_dict["today"] = date_today
    return json.dumps(date_dict, indent=4)

def main():
    """ Starting the application and making it accessible on port 80"""
    app.run(host='0.0.0.0', port=80)

if __name__ == '__main__':
    main()
