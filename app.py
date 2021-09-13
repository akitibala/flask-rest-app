from os import error
from flask import Flask , jsonify,request,make_response
import jsonschema
from jsonschema.exceptions import ValidationError
from werkzeug.wrappers import response
from utils import process_csv 
import json
from jsonschema import validate
from validator import Schema
app = Flask(__name__)

@app.route('/search/text', methods=['POST'])
def welcome():
    data=''
    try:
        request_data = request.get_json()
        validate(request_data,schema=Schema)

        filename = request_data["file_name"]
        positions = request_data["position"]
        data = process_csv(filename=filename,points=positions)
    except  jsonschema.exceptions.ValidationError as e:
        # print(e)
        return make_response(jsonify(error="Validation Error"),422)
    # logic to process co-ordinates
    except FileNotFoundError as e:
        return make_response(jsonify(error="File Not Found"),404)



    return jsonify({"text":data})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)