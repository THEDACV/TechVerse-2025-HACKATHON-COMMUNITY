from flask import Flask, render_template, request, send_file
from fpdf import FPDF
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads directory if not exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'files[]' not in request.files:
        return 'No files selected', 400
        
    files = request.files.getlist('files[]')
    for file in files:
        if file.filename == '':
            continue
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return 'Files uploaded successfully!'

@app.route('/generate-certificate')
def generate_certificate():
    participant_name = request.args.get('name', 'Participant')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Techverse 2025 Hackathon", ln=1, align='C')
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Certificate of Participation", ln=1, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Awarded to: {participant_name}", ln=1, align='C')
    
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], 'certificate.pdf')
    pdf.output(pdf_path)
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"{participant_name}_certificate.pdf"
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)

