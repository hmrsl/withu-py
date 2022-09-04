import base64
import os
import pathlib
import random

from flask import Flask, request, render_template, send_from_directory

import functions

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return "Good bye"


@app.route('/bad-word')
def bad_word():  # put application's code here
    a = random.randint(0, 1)
    bad = 0
    if a == 0:
        bad = 0
    else:
        bad = random.randint(1, 99)

    return render_template("text.html", data=f'{bad}')


@app.route('/count', methods=["POST"])
def face_count():  # put application's code here
    image = request.files["image"]
    post_id = request.form["id"]

    root = os.path.join(app.instance_path, 'res')
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)
    file = os.path.join(app.instance_path, 'res', "post", f'{post_id}.png')
    image.save(file)

    count = functions.count_faces(root, post_id)
    images = []

    for i in range(count + 1):
        with open(os.path.join(root, 'post', 'face', f"{post_id}", f'{i}.png'), "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
            print(images)
            images.append(encoded_string)

    return render_template("text.html", data=f'{count}')


@app.route('/audio', methods=["POST"])
def save_audio():  # put application's code here
    image = request.files["audio"]
    space_id = request.form["id"]

    root = os.path.join(app.instance_path, 'res')
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)
    file = os.path.join(app.instance_path, 'res', "audio", f'{space_id}.mp3')
    image.save(file)

    return "Saved"


@app.route('/detect', methods=["POST"])
def detect_emotion():  # put application's code here
    image = request.files["image"]

    root = os.path.join(app.instance_path, 'res')
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)

    e_id = random.randint(0, 1000)

    file = os.path.join(app.instance_path, 'res', "emotion", f'{e_id}.png')
    image.save(file)

    # emotion = functions.detect_emotion(file)
    emotion = "Sad"

    return emotion


@app.route('/train-admin', methods=["POST"])
def train_admin():  # put application's code here
    image = request.files["image"]

    admin_id = request.form["id"]

    root = os.path.join(app.instance_path, 'res', "admin")
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)

    file = os.path.join(app.instance_path, 'res', "admin", f'{admin_id}.png')
    image.save(file)

    # TODO NOT Implemented
    # functions.train_admin(file)

    return "0"


@app.route('/is-admin', methods=["POST"])
def is_admin():  # put application's code here
    image = request.files["image"]

    admin_id = request.form["id"]

    root = os.path.join(app.instance_path, 'res', "admin", "check")
    pathlib.Path(root).mkdir(parents=True, exist_ok=True)

    file = os.path.join(app.instance_path, 'res', "admin", "check", f'{admin_id}.png')
    image.save(file)

    # admin = functions.is_admin(admin_id, file)
    admin = random.randint(0, 1)

    if admin:
        return render_template("text.html", data=f'{1}')

    return "0"


def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')


@app.route('/get-image', methods=["GET"])
def get():
    # POST, FACE
    img_type = request.args.get('type')
    images = []
    if img_type == "POST":
        post_id = request.args.get("id")
        file = os.path.join(app.instance_path, 'res', 'post', f"{post_id}.png")
        url = image_to_data_url(file)
        images.append(url)

    elif img_type == "FACE":
        post_id = request.args.get("id")
        file = os.path.join(app.instance_path, 'res', 'post', 'face', f"{post_id}")
        i = 0
        while True:
            f = os.path.join(file, f'{i}.png')
            try:
                url = image_to_data_url(f)
                if url is None:
                    break
                images.append(url)
            except:
                break
            i += 1

    return render_template("image.html", data=images)


@app.route('/get-audio', methods=["GET"])
def get_audio():
    post_id = request.args.get("id")
    file = os.path.join(app.instance_path, 'res', 'audio')
    return send_from_directory(file, f"{post_id}.mp3")


@app.route('/gen-icon', methods=["POST"])
def gen_icon():  # put application's code here
    image = request.files["image"]
    user_id = request.form["id"]

    file = os.path.join(app.instance_path, 'res', "profile", f'{user_id}.png')
    result = os.path.join(app.instance_path, 'res', "profile", f'{user_id}')
    pathlib.Path(result).mkdir(parents=True, exist_ok=True)
    image.save(file)
    functions.gen_icons(file, result)

    images = []

    i = 1
    while True:
        f = os.path.join(result, f'{i}.png')
        try:
            url = image_to_data_url(f)
            if url is None:
                break
            images.append(url)
        except:
            break
        i += 1

    return render_template("image.html", data=images)


if __name__ == '__main__':
    app.run()
