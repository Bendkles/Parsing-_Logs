# Import the necessary modules
import re
import csv

# Define a function to parse the log file
def parse_transaction_log(log_file):
    # Open the log file
    with open(log_file, 'r') as file:
        # Read all lines from the log file
        logs = file.readlines()

    # Initialize an empty list to store the parsed logs
    parsed_logs = []

    # Loop over each line in the log file
    for log in logs:
        # Initialize an empty dictionary to store the parsed log
        log_dict = {}

        # Define a regular expression pattern to match the log format
        pattern = r'(\w+) - (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - (\w+) - (\w+) - (\w+) - (.*)'
        
        # Use the regular expression to match the log line
        match = re.match(pattern, log.strip())

        # If the log line matches the pattern
        if match:
            # Extract the matched groups and store them in the dictionary
            log_dict['TransactionID'] = match.group(1)
            log_dict['Timestamp'] = match.group(2)
            log_dict['TransactionType'] = match.group(3)
            log_dict['Status'] = match.group(4)
            log_dict['UserID'] = match.group(5)
            log_dict['Details'] = match.group(6)

            # Add the dictionary to the list of parsed logs
            parsed_logs.append(log_dict)

    # Return the list of parsed logs
    return parsed_logs

# Define a function to write the parsed logs to a CSV file
def write_to_csv(parsed_logs, output_file):
    # Open the output file in write mode
    with open(output_file, 'w', newline='') as file:
        # Create a CSV writer
        writer = csv.DictWriter(file, fieldnames=parsed_logs[0].keys())

        # Write the header row
        writer.writeheader()

        # Write the parsed logs
        writer.writerows(parsed_logs)

# Parse the log file
parsed_logs = parse_transaction_log('log-file-example.txt')

# Write the parsed logs to a CSV file
write_to_csv(parsed_logs, 'parsed_logs.csv')
