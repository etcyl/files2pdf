from flask import Flask, render_template, request, send_file
import os
from PIL import Image
from PyPDF2 import PdfMerger, PdfReader
from fpdf import FPDF
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set upload and output folders
UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'output_pdfs/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the necessary folders exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Helper function to merge files into a single PDF
def merge_files_to_pdf(file_paths, output_filename):
    pdf = FPDF()
    pdf_merger = PdfMerger()

    image_extensions = ['.png', '.jpg', '.jpeg', '.PNG', '.JPG', '.JPEG']
    text_extension = '.txt'
    pdf_extension = '.pdf'

    for file_path in file_paths:
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext in image_extensions:
            try:
                image = Image.open(file_path)
                image = image.convert('RGB')
                pdf.add_page()
                pdf.image(file_path, 10, 10, 190)  # Adjust image size to fit the page
            except Exception as e:
                print(f"Error processing image {file_path}: {e}")

        elif file_ext == text_extension:
            try:
                pdf.add_page()
                # Try reading the file with UTF-8 encoding first
                try:
                    with open(file_path, 'r', encoding='utf-8') as text_file:
                        content = text_file.read()
                except UnicodeDecodeError:
                    # Fallback to ISO-8859-1 encoding
                    with open(file_path, 'r', encoding='ISO-8859-1') as text_file:
                        content = text_file.read()

                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font('Arial', size=12)
                pdf.multi_cell(0, 10, content)
            except Exception as e:
                print(f"Error processing text file {file_path}: {e}")

        elif file_ext == pdf_extension:
            try:
                pdf_merger.append(file_path)
            except Exception as e:
                print(f"Error processing PDF file {file_path}: {e}")

    # Save the FPDF-generated content (images and text) first
    temp_output_path = os.path.join(UPLOAD_FOLDER, "temp_output.pdf")
    if pdf.page_no() > 0:  # Only save if there are any pages added
        pdf.output(temp_output_path)
        pdf_merger.append(temp_output_path)

    # Save the merged PDF in the output_pdfs folder
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    with open(output_path, 'wb') as output_file:
        pdf_merger.write(output_file)
    pdf_merger.close()

    # Clean up temporary files
    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)

    return output_path

# Route to display the file upload page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the output filename from the form
        output_filename = request.form.get("output_filename", "merged_output.pdf")
        if not output_filename.endswith(".pdf"):
            output_filename += ".pdf"  # Ensure the file has a .pdf extension

        # Save uploaded files
        uploaded_files = request.files.getlist("files")
        file_paths = []
        for file in uploaded_files:
            if file:
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)

        if file_paths:
            output_pdf = merge_files_to_pdf(file_paths, output_filename)
            return send_file(output_pdf, as_attachment=True, download_name=output_filename)

    return render_template("index.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
