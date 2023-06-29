import csv

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

def write_to_csv(parsed_logs, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=parsed_logs[0].keys())
        writer.writeheader()
        writer.writerows(parsed_logs)

parsed_logs = parse_transaction_log('log-file-example.txt')
write_to_csv(parsed_logs, 'parsed_logs.csv')
