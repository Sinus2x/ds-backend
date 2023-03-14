import logging
from flask import Flask, request
from models.plate_reader import PlateReader, InvalidImage
import logging
import io
import requests


app = Flask(__name__)
plate_reader = PlateReader.load_from_file('./model_weights/plate_reader_model.pth')
IMAGES_URL = 'http://51.250.83.169:7878/images/'

def process_response(im):
    im = io.BytesIO(im)
    try:
        res = plate_reader.read_text(im)
    except InvalidImage:
        logging.error('invalid image')
        return 'invalid image', 400

    return {
        'plate_number': res,
    }

@app.route('/')
def hello():
    user = request.args['user']
    return f'<h1 style="color:red;"><center>Hello {user}!</center></h1>'

# url: ?ids=["10022", "9965"]
@app.route('/readNumbersByID')
def get_numbers_by_id():
    # if 'ids' not in request.args:
    #     return 'field "ids" not found', 400
    ids = request.form.getlist('ids')
    res = []
    for id in ids:
        im = requests.get(
            f'{IMAGES_URL}{id}'
        )
        if not im.ok:
            return "image with this id doesn't exist or image-server error", 500
        res.append(process_response(im.content))
    return {'result': res}

# url: ?id=10022
@app.route('/readNumberByID')
def get_number_by_id():
    if 'id' not in request.json:
        return 'field "id" not found', 400
    id = request.json['id']
    if not id.isnumeric():
        return 'field "id" must be integer', 400
    if not int(id) >= 0:
        return '"id" must be non-negative', 400
    
    im = requests.get(
        f'{IMAGES_URL}{id}'
    )
    if not im.ok:
        return "image with this id doesn't exist or image-server error", 500
    return process_response(im.content)
    
    

# <url>:8080/greeting?user=me
# <url>:8080 : body: {"user": "me"}
# -> {"result": "Hello me"}
@app.route('/greeting', methods=['POST'])
def greeting():
    if 'user' not in request.json:
        return {'error': 'field "user" not found'}, 400

    user = request.json['user']
    return {
        'result': f'Hello {user}',
    }


# <url>:8080/readPlateNumber : body <image bytes>
# {"plate_number": "c180mv ..."}
@app.route('/readPlateNumber', methods=['POST'])
def read_plate_number():
    im = request.get_data()
    return process_response(im)


if __name__ == '__main__':
    logging.basicConfig(
        format='[%(levelname)s] [%(asctime)s] %(message)s',
        level=logging.INFO,
    )

    app.config['JSON_AS_ASCII'] = False
    app.run(host='0.0.0.0', port=8080, debug=True)
