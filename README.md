# Flask PDF Merger

This Flask-based application allows you to merge multiple files (images and text files) into a single PDF. The app supports various file types including .png, .jpg, and .txt and provides a user-friendly interface via a web browser.

Features

    Supported File Types: Merge .png, .jpg, .jpeg, and .txt files into a single PDF.
    Automatic Encoding Detection: Handles text files with different encodings (e.g., UTF-8, ISO-8859-1).
    User-Friendly Interface: Web-based interface for uploading and merging files.
    Responsive Design: Simple and clean UI using modern web styling.

## Prerequisites

Make sure you have Python 3 installed.

## Install the required packages:
  ```pip install flask pillow fpdf```

## How to Run the Application
    Clone or download this repository.
        git clone https://github.com/etcyl/files2pdf/

    Navigate to the project folder.
        cd pdfmerge

    Run the Flask application:
        python app.py

    Open your web browser and navigate to:
        http://127.0.0.1:5000

    Upload the files you want to merge and click the "Merge Files" button. The merged PDF will be automatically downloaded.

## Example Usage

You can upload files like:

    **Images:** 
        .png, .jpg, .jpeg
    **Text Files:** 
        .txt

The application merges these files into a single PDF, maintaining the order of upload.
The final merged PDF is saved to the uploads/ directory within the project folder, and the filename is merged_output.pdf.

# Error Handling
    The application handles text files with various encodings, such as UTF-8 and ISO-8859-1, to prevent decoding errors.
    Invalid file types are ignored, ensuring smooth operation.

Future Enhancements
    Support for more file types (e.g., .docx, .pdf).
    Option to customize PDF output (e.g., page size, orientation).
    Drag-and-drop support for file uploads.

License

This project is open-source and available under the MIT License.
