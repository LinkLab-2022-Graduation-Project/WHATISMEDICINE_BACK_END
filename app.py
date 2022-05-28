from flask import Flask, request, Response
import json

from exception.s3_exception_class import s3Exception
from util import s3

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['file']
    connected_s3 = s3.s3_connection()
    if s3.s3_put_object(connected_s3, file, file.filename):
        return s3.s3_get_image_url(connected_s3, file.filename)
    else:
        return "Failed"


@app.errorhandler(s3Exception)
def handle_error(e):

    response = Response()

    response.data = json.dumps({
        'exception_name': e.get_exception_name(),
        'message': e.get_message(),
        'error_code': e.get_error_code()
    })
    response.content_type = 'application/json'
    response.status_code = 500

    return response


if __name__ == '__main__':
    app.run()