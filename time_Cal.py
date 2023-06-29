import csv
from datetime import datetime, timedelta

def parse_transaction_log(log_file):
    parsed_logs = []

    with open(log_file, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')

            if len(parts) == 8:
                log_dict = {
                    'TransactionID': parts[0],
                    'Timestamp': parts[1],
                    'TransactionType': parts[2],
                    'Status': parts[3],
                    'UserID': parts[4],
                    'Details': parts[5],
                    'LogLevel': parts[6],
                    'StartTime': parts[7].split("End Time: ")[0].split("Start Time: ")[1].strip(),
                    'EndTime': parts[7].split("End Time: ")[1]
                }
                parsed_logs.append(log_dict)

    return parsed_logs

def calculate_time_difference(parsed_logs):
    for log in parsed_logs:
        start_time = datetime.strptime(log['StartTime'], "%H:%M:%S,%f")
        end_time = datetime.strptime(log['EndTime'], "%H:%M:%S,%f")
        time_difference = end_time - start_time
        log['TimeDifference'] = str(time_difference)

    return parsed_logs

def write_to_csv(parsed_logs, output_file):
    with open(output_file, 'w', newline='') as file:
        fieldnames = parsed_logs[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_logs)

log_file = 'log-file-example.txt'
parsed_logs = parse_transaction_log(log_file)
parsed_logs = calculate_time_difference(parsed_logs)
write_to_csv(parsed_logs, 'parsed_logs.csv')
