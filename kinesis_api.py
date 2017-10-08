from api_version import version as api_version
import time
import json
import boto3
import os

from flask import Flask, request, session, g, url_for, Response, request, jsonify

# create our app
app = Flask(__name__)

# enable CORS on everything
from flask_cors import CORS
CORS(app)

# helper function to get the current time in millis()
current_milli_time = lambda: int(round(time.time() * 1000))

#default return type to JSON, since this is really what we use
class JSONResponse(Response):
    default_mimetype = 'application/json'

# will return 400 when called
@app.errorhandler(400)
def bad_request(error=None):
        """
        Handle 400 cases
        :param error: String, the error to return
        :return:
        """
        message = {
            'status': 400,
            'error': 'BadRequest: ' + request.url,
            "message": error if error is not None else '',
        }
        resp = jsonify(message)
        resp.status_code = 400

        return resp

# will return 500 when called
@app.errorhandler(500)
def internal_error(error=None):
        """
        Handle 500 cases
        :param error: String, the error to return
        :return:
        """
        message = {
            'status': 500,
            'error': 'ServerError: ' + request.url,
            "message": error if error is not None else '',
        }
        resp = jsonify(message)
        resp.status_code = 500

        return resp

# Routes
# ------------------------------------------------------------------------------
@app.route('/kinesis/version')
def version():
    return json.dumps({'version': api_version})

@app.route('/kinesis/<string:muns>', methods=['POST'])
def kinesis(stream_name):
    try:
        params = get_payload(request)

        event = params['event']
        region = 'us-west-2'
        if 'region' in params:
            region = params['region']

        partition_key = "1"
        if 'partition_key' in params:
            partition_key = params['partition_key']

    except:
        return bad_request("Invalid parameters")

    try:
        client = boto3.client('kinesis', region_name=region)
        client.put_record(
            StreamName=stream_name,
            PartitionKey=partition_key,
            Data=json.dumps(event)
        )
    except Exception as ex:
        return internal_error(ex.message)

    return JSONResponse(json.dumps({"message": "ok"}))

# Helper functions
# ------------------------------------------------------------------------------
def get_payload(request):

    if request.method == 'POST':
        # if POST, the data may be in the data array as json or form, depending on how it was handed in
        # Postman seems to hand it in as json while others seem to hand it in through form data
        data = request.get_json(force=True, silent=True)
        return data if data is not None else request.form
    else:
        return request.args

# Main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run()