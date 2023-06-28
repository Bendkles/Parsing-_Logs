# Import the necessary modules
from flask import Flask, request
import os
import re
import csv
import requests

app = Flask(__name__)  # Create the Flask application instance

# Define the path to the upload folder
UPLOAD_FOLDER = '/mnt/d/Cyber-HUB/LAB/Scripts Tools'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define a function to parse the log file
def parse_transaction_log(log_file):
    with open(log_file, 'r') as file:
        logs = file.readlines()

    parsed_logs = []
    for log in logs:
        log_dict = {}
        pattern = r'(\w+) - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (\w+) - (\w+) - (.*)'
        match = re.match(pattern, log.strip())

        if match:
            log_dict['TransactionID'] = match.group(1)
            log_dict['Timestamp'] = match.group(2)
            log_dict['TransactionType'] = match.group(3)
            log_dict['Status'] = match.group(4)
            log_dict['UserID'] = match.group(5)
            log_dict['Details'] = match.group(6)

            parsed_logs.append(log_dict)

    return parsed_logs

# Define a function to write the parsed logs to a CSV file
def write_to_csv(parsed_logs, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=parsed_logs[0].keys())
        writer.writeheader()
        writer.writerows(parsed_logs)

# Define a route for uploading files
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part in the request.'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file.'

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    parsed_logs = parse_transaction_log(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    write_to_csv(parsed_logs, 'parsed_logs.csv')

    return 'File uploaded and parsed successfully.'

if __name__ == '__main__':
    app.run(debug=True)

# Specify the URL of your Flask application
url = 'http://127.0.0.1:5000/upload'

# Specify the path to your log file
file_path = '/mnt/d/Cyber-HUB/LAB/Scripts Tools/log-file-example.txt'  # Update the path for WSL

# Open the file in binary mode
file = open(file_path, 'rb')

# Send a POST request with the file
response = requests.post(url, files={'file': file})

# Close the file
file.close()

# Print the response from the server
print(response.text)



""" 
1. run the app and the flask 
2. Use this command to upload and pars the log file: 
    curl.exe -X POST -F "file=@D:/Cyber-HUB/LAB/Scripts Tools/log-file-example.txt" http://127.0.0.1:5000/upload

This script first starts a Flask server that listens 
for file uploads. Then it sends a POST request 
to the server with a specified log file. 
The server saves the file, parses it, 
and writes the parsed logs to a CSV file.

Please note that you should run the Flask server 
and the POST request in separate Python processes. 
The Flask server needs to be running before you send 
the POST request. You can split the script into two 
separate scripts, one for the server and one for 
the POST request, to achieve this.
"""