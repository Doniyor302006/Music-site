from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Faylni saqlash va postlar
posts = []
likes = {}
comments = {}

# Admin paroli
ADMIN_PASSWORD = '0306'  # Buni o'zingiz xohlagan raqamga almashtiring

@app.route('/')
def index():
    return render_template('index.html', posts=posts, likes=likes, comments=comments)

@app.route('/upload', methods=['POST'])
def upload_file():
    password = request.form.get('password')
    if password != ADMIN_PASSWORD:
        return 'Notog‘ri parol!', 403

    title = request.form['title']
    description = request.form['description']
    file = request.files['file']

    if file:
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        posts.append({
            'title': title,
            'description': description,
            'file': filepath
        })

    return redirect(url_for('index'))

@app.route('/like/<int:post_id>', methods=['POST'])
def like(post_id):
    likes[post_id] = likes.get(post_id, 0) + 1
    return jsonify({'likes': likes[post_id]})

@app.route('/comment/<int:post_id>', methods=['POST'])
def comment(post_id):
    comment = request.form['comment']
    comments.setdefault(post_id, []).append(comment)
    return redirect(url_for('index'))

@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    password = request.form.get('password')
    if password != ADMIN_PASSWORD:
        return 'Notog‘ri parol!', 403

    try:
        os.remove(posts[post_id]['file'])
    except:
        pass
    posts.pop(post_id)
    likes.pop(post_id, None)
    comments.pop(post_id, None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    app.run(host='0.0.0.0', port=5000)
