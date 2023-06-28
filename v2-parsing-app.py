from flask import Flask, request, render_template, send_file
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = '/mnt/d/Cyber-HUB/LAB/Scripts Tools'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def parse_transaction_log(log_file):
    """
    Parses the transaction log file and returns the parsed logs as a list of dictionaries.

    Args:
        log_file (str): Path to the log file.

    Returns:
        list: Parsed logs as a list of dictionaries.
    """
    parsed_logs = []
    with open(log_file, 'r') as file:
        for line in file:
            data = line.strip().split(' - ')
            if len(data) == 6:
                log_dict = {
                    'TransactionID': data[0],
                    'Timestamp': data[1],
                    'TransactionType': data[2],
                    'Status': data[3],
                    'UserID': data[4],
                    'Details': data[5]
                }
                parsed_logs.append(log_dict)
    return parsed_logs


@app.route('/')
def index():
    """
    Renders the index.html template, serving as the main menu for the web GUI.
    """
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handles the file upload functionality.

    Returns:
        str: Response message.
    """
    if 'file' not in request.files:
        return 'No file part in the request.'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file.'

    file.save(f"{app.config['UPLOAD_FOLDER']}/{file.filename}")

    return 'File uploaded successfully.'


@app.route('/parse')
def parse_logs():
    """
    Parses the uploaded log file and saves the parsed logs as a CSV file.

    Returns:
        str: Response message.
    """
    log_file = f"{app.config['UPLOAD_FOLDER']}/log-file-example.txt"
    parsed_logs = parse_transaction_log(log_file)
    df = pd.DataFrame(parsed_logs)
    csv_file = f"{app.config['UPLOAD_FOLDER']}/parsed_logs.csv"
    df.to_csv(csv_file, index=False)
    return 'Log file parsed and CSV file saved.'


@app.route('/download')
def download_file():
    """
    Allows the user to download the parsed CSV file.

    Returns:
        file: The parsed CSV file.
    """
    csv_file = f"{app.config['UPLOAD_FOLDER']}/parsed_logs.csv"
    return send_file(csv_file, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
