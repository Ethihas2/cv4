import os
import cv2
import numpy as np
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    operation_selection = request.form['image_type_selection']
    image_file = request.files['file']
    filename = secure_filename(image_file.filename)
    reading_file_data = image_file.read()
    image_array = np.fromstring(reading_file_data, dtype='uint8')
    decode_array_to_img = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)


    # Write code for Select option for Gray and Sketch
    if operation_selection == 'gray':
        file_data = make_grayscale(decode_array_to_img)
    elif operation_selection == 'sketch':
        file_data = image_sketch(decode_array_to_img)
    elif operation_selection == 'oil':
        file_data = oil_effect(decode_array_to_img)
    elif operation_selection == 'rgb':
        file_data = rgb_effect(decode_array_to_img)
    elif operation_selection == 'water':
        file_data = water_effect(decode_array_to_img)
    elif operation_selection == 'invert':
        file_data = invert_effect(decode_array_to_img)
    elif operation_selection == 'hdr':
        file_data = hdr_effect(decode_array_to_img)
    elif operation_selection == 'edge':
        file_data = edge_effect(decode_array_to_img)
    else:
        print('no image selected')


    # Ends here

    with open(os.path.join('static/', filename),
                  'wb') as f:
        f.write(file_data)

    return render_template('upload.html', filename=filename)

def make_grayscale(decode_array_to_img):

    converted_gray_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_RGB2GRAY)
    status, output_image = cv2.imencode('.PNG', converted_gray_img)

    return output_image


# Write code for Sketch function
def image_sketch(decode_array_into_img):


    converted_gray_image = cv2.cvtColor(decode_array_into_img, cv2.COLOR_BGR2GRAY)
    sharpening_image = cv2.bitwise_not(converted_gray_image)
    blur_image = cv2.GaussianBlur(sharpening_image, (111, 111), 0)
    sharpening_blur_img = cv2.bitwise_not(blur_image)
    sketch_img = cv2.divide(converted_gray_image, sharpening_blur_img, scale=256.0)
    status, output_img = cv2.imencode('.PNG', sketch_img)

    return output_img

def oil_effect(decode_array_to_img):
    oil_effect_img = cv2.xphoto.oilPainting(decode_array_to_img, 7, 1)
    status, output_img = cv2.imencode('.PNG',oil_effect_img)

    return output_img
# Ends Here
# Starts RGB Effect function From here
def rgb_effect(decode_array_to_img):
    rgb_effect_img = cv2.cvtColor(decode_array_to_img, cv2.COLOR_BGR2RGB)
    status, output_img = cv2.imencode('.PNG',rgb_effect_img)

    return output_img

def water_effect(decode_array_img):
    water = cv2.stylization(decode_array_img, sigma_s=60, sigma_r=0.6)
    status, output_img = cv2.imencode('.PNG', water)
    return output_img

def invert_effect(decode_array_img):
    invert = cv2.bitwise_not(decode_array_img)

    status, output_img = cv2.imencode('.PNG', invert)
    return output_img


def hdr_effect(decode_array_img):
    hdr = cv2.detailEnhance(decode_array_img, sigma_s=12, sigma_r=0.15)

    status, output_img = cv2.imencode('.PNG',hdr)
    return output_img

def edge_effect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    status, output_img = cv2.imencode('.PNG',edged)
    return output_img
# Ends here


@app.route('/display/<filename>')
def display_image(filename):

    return redirect(url_for('static', filename=filename))



if __name__ == "__main__":
    app.run()










