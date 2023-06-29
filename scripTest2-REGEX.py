import re
import csv

def parse_transaction_log(log_file):
    parsed_logs = []

    with open(log_file, 'r') as file:
        logs = file.readlines()

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
                log_dict['LogLevel'] = match.group(6).split()[0]  # Extract the log level (e.g., "ERROR")
                log_dict['StartTime'] = match.group(6).split(':')[1]  # Extract the start time
                log_dict['EndTime'] = match.group(6).split(':')[3]  # Extract the end time

                parsed_logs.append(log_dict)

    return parsed_logs

def write_to_csv(parsed_logs, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=parsed_logs[0].keys())
        writer.writeheader()
        writer.writerows(parsed_logs)

parsed_logs = parse_transaction_log('log-file-example.txt')
write_to_csv(parsed_logs, 'parsed_logs.csv')
