# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import boto3
import os
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# AWS Configuration
def get_aws_client():
    """
    Configure boto3 client based on environment (local vs production)
    """
    if os.getenv('FLASK_ENV') == 'development':
        return boto3.client(
            's3',
            endpoint_url='http://localstack:4566',  # LocalStack endpoint
            aws_access_key_id='test',
            aws_secret_access_key='test',
            region_name='us-east-1'
        )
    else:
        return boto3.client('s3')

# S3 bucket configuration
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'my-file-upload-bucket')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """
    Display uploaded files and upload form
    """
    s3_client = get_aws_client()
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        files = response.get('Contents', [])
        return render_template('index.html', files=files)
    except ClientError as e:
        flash(f"Error retrieving files: {str(e)}")
        return render_template('index.html', files=[])

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload to S3
    """
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        s3_client = get_aws_client()
        try:
            s3_client.upload_fileobj(file, BUCKET_NAME, filename)
            flash('File successfully uploaded')
        except ClientError as e:
            flash(f"Error uploading file: {str(e)}")
    else:
        flash('Invalid file type')
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """
    Download file from S3
    """
    s3_client = get_aws_client()
    try:
        file_obj = BytesIO()
        s3_client.download_fileobj(BUCKET_NAME, filename, file_obj)
        file_obj.seek(0)
        return send_file(
            file_obj,
            download_name=filename,
            as_attachment=True
        )
    except ClientError as e:
        flash(f"Error downloading file: {str(e)}")
        return redirect(url_for('index'))

@app.route('/delete/<filename>')
def delete_file(filename):
    """
    Delete file from S3
    """
    s3_client = get_aws_client()
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=filename)
        flash('File successfully deleted')
    except ClientError as e:
        flash(f"Error deleting file: {str(e)}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)