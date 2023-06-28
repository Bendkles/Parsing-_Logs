from flask import Flask, render_template, request, redirect, send_from_directory
import os
import csv

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
DOWNLOAD_FOLDER = os.path.join(app.root_path, 'downloads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


def parse_transaction_log(log_file):
    with open(log_file, 'r') as file:
        logs = file.readlines()

    parsed_logs = []
    for log in logs:
        log_dict = {}
        parts = log.strip().split(' - ')
        if len(parts) == 6:
            log_dict['TransactionID'] = parts[0]
            log_dict['Timestamp'] = parts[1]
            log_dict['TransactionType'] = parts[2]
            log_dict['Status'] = parts[3]
            log_dict['UserID'] = parts[4]
            log_dict['Details'] = parts[5]
            parsed_logs.append(log_dict)

    return parsed_logs


def write_to_csv(parsed_logs, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=parsed_logs[0].keys())
        writer.writeheader()
        writer.writerows(parsed_logs)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="No file selected.")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="No file selected.")
        
        if file.filename.endswith('.txt'):
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            parsed_logs = parse_transaction_log(file_path)
            
            if len(parsed_logs) > 0:
                output_file = os.path.join(DOWNLOAD_FOLDER, 'parsed_logs.csv')
                write_to_csv(parsed_logs, output_file)
                return redirect('/download')
            else:
                return render_template('index.html', error="Failed to parse the file.")
        else:
            return render_template('index.html', error="Invalid file format. Only .txt files are supported.")
    else:
        return render_template('index.html', error="")


@app.route('/download')
def download():
    file_name = 'parsed_logs.csv'
    file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    
    if os.path.exists(file_path):
        return send_from_directory(DOWNLOAD_FOLDER, file_name, as_attachment=True)
    else:
        return render_template('index.html', error="Failed to download the file.")


if __name__ == '__main__':
    app.run(debug=True)
