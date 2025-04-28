from flask import Flask, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp3', 'mp4'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Eski kodlaringiz (login, post chiqarish va h.k.) shu yerda turadi

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Fayl topilmadi'
    file = request.files['file']
    if file.filename == '':
        return 'Fayl tanlanmadi'
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return f'Fayl yuklandi: {filename}'
    else:
        return 'Noto‘g‘ri fayl turi'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
