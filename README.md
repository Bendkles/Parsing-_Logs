# Log File Parser

This is a Python script that automates the process of parsing transaction log files and exporting the parsed data to a CSV file. It utilizes the Flask web framework for handling file uploads and the Requests module for sending HTTP requests.

## Features

- Upload log files for parsing and processing
- Automatic extraction of relevant information from log files using regular expressions
- Export parsed data to a CSV file for further analysis

## Getting Started

### Prerequisites

- Python 3.x installed
- Flask and Requests modules installed (`pip install flask requests`)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/log-file-parser.git
    ```

2. Change into the project directory:

    ```bash
    cd log-file-parser
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:

    ```bash
    python3 upload-app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000` to access the upload page.

3. Click on the "Choose File" button and select the log file you want to parse.

4. Click the "Upload" button to initiate the parsing process.

5. Once the file is uploaded and parsed successfully, you will see a confirmation message.

6. The parsed data will be saved in a file named `parsed_logs.csv` in the same directory.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.



