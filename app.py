from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import os
import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'shared_files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_file_info():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        size = os.path.getsize(filepath) / 1024  # KB
        upload_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%Y-%m-%d %H:%M:%S")
        files.append({"name": filename, "size": f"{size:.2f} KB", "time": upload_time})
    return files

@app.route('/')
def index():
    files = get_file_info()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        return redirect('/')
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route('/delete/<filename>')
def delete_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
