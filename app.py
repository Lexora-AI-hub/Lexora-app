import os
from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename
from utils import extract_text_from_pdf
from summarizer import summarize_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('Lexora.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'pdf' not in request.files:
        return "No file uploaded", 400

    file = request.files['pdf']
    if file.filename == '':
        return "No selected file", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    print(f"✅ File saved to {filepath}")

    # Extract and summarize
    text = extract_text_from_pdf(filepath)
    print("✅ Text extracted")
    summary_bullets = summarize_text(text)
    print("✅ Summary generated")

    pdf_name = filename.rsplit('.', 1)[0]
    summary_text = f"Summary for: {pdf_name}\n\n" + "\n".join(summary_bullets)
    # Show summary on a new page
    
    return jsonify({'summary': summary_text})
if __name__ == '__main__':
    app.run(debug=True)
