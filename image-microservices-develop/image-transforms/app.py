from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
from io import BytesIO
import urllib

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/transform", methods=['POST'])
def transform_image():
    if request.method == 'POST':

        # Get the image to be transformed, this can be any of the following:
        # - image uploaded as a file
        # - url of a publicaly accessible image
        # - the image_id of an iamge stored in the image_storage microservice
        image = None
        quality = 100

        url = request.form.get('url')
        if url is not None:
            file = BytesIO(urllib.request.urlopen(url).read())
            if not allowed_file(url):
                return jsonify({'error': 'This file type is not allowed'}), 400
            image = Image.open(file)

        image_file = request.files.get('image')
        if image_file is not None:
            if not allowed_file(image_file.filename):
                return jsonify({'error': 'This file type is not allowed'}), 400
            image = Image.open(request.files['image'])

        image_id = request.form.get('image_id')
        if image_id is not None:
            file = BytesIO(urllib.request.urlopen('http://image-storage:5000/images/'+image_id).read())
            image = Image.open(file)

        if image is None:
            return jsonify({'error': 'Could not find an image to transform'}), 400

        # Parse the query string and apply the transformation
        try:
            for command in request.query_string.split(b'&'):
                # Split the command in a key and value
                command_list = command.split(b'=')
                key = command_list[0]
                if key == b'':
                    continue
                value = float(command_list[1])

                # Perform the transform
                if key == b'rotate':
                    image = image.rotate(value, expand=True)
                elif key == b'thumb':
                    iamge = image.thumbnail((value, value))
                elif key == b'compress':
                    quality = min(quality, int(value))
                elif key == b'blur':
                    image = image.filter(ImageFilter.GaussianBlur(value))
        except:
            return jsonify({'error': 'Could not parse filter list: {}'.format(key)}), 400

        # Return the transformed image from memory
        mem_file = BytesIO()
        image.save(mem_file, "JPEG", quality=quality)
        mem_file.seek(0)
        return send_file(mem_file, attachment_filename='_.jpg')

@app.route("/transform/healthcheck")
def healthcheck():
    return jsonify({'service': 'image-transform', 'status': 'okay'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)