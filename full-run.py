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
        log['TimeDifference'] = time_difference

    return parsed_logs

def write_to_csv(parsed_logs, output_file):
    with open(output_file, 'w', newline='') as file:
        fieldnames = parsed_logs[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(parsed_logs)

def get_fastest_transaction(parsed_logs):
    fastest_time = timedelta.max
    fastest_transaction = {}
    for log in parsed_logs:
        time_difference = log['TimeDifference']
        if time_difference < fastest_time:
            fastest_time = time_difference
            fastest_transaction = log
    return fastest_transaction

def get_slowest_transaction(parsed_logs):
    slowest_time = timedelta()
    slowest_transaction = {}
    for log in parsed_logs:
        time_difference = log['TimeDifference']
        if time_difference > slowest_time:
            slowest_time = time_difference
            slowest_transaction = log
    return slowest_transaction

def get_average_transaction_time(parsed_logs):
    total_time = timedelta()
    for log in parsed_logs:
        time_difference = log['TimeDifference']
        total_time += time_difference
    average_time = total_time / len(parsed_logs)
    return average_time.total_seconds() * 1000

log_file = 'log-file-example.txt'
parsed_logs = parse_transaction_log(log_file)
parsed_logs = calculate_time_difference(parsed_logs)
write_to_csv(parsed_logs, 'parsed_logs.csv')

fastest_transaction = get_fastest_transaction(parsed_logs)
slowest_transaction = get_slowest_transaction(parsed_logs)
average_transaction_time = get_average_transaction_time(parsed_logs)

print("Fastest Transaction:")
print("Transaction ID:", fastest_transaction['TransactionID'])
print("Time Difference (ms):", fastest_transaction['TimeDifference'].total_seconds() * 1000)
print("\nSlowest Transaction:")
print("Transaction ID:", slowest_transaction['TransactionID'])
print("Time Difference (ms):", slowest_transaction['TimeDifference'].total_seconds() * 1000)
print(f"\nAverage Transaction Time (ms): {average_transaction_time:.3f}")
