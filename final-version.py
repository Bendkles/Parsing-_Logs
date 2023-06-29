import csv
from datetime import datetime, timedelta

# Define the functions
def calculate_time_difference(parsed_logs):
    for log in parsed_logs:
        start_time = datetime.strptime(log['StartTime'], "%d-%m-%Y %H:%M:%S.%f")
        end_time = datetime.strptime(log['EndTime'], "%d-%m-%Y %H:%M:%S.%f")
        time_difference = end_time - start_time
        log['TimeDifference'] = time_difference

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

# Open the log file
with open('log-file.txt', 'r') as f:
    # Create a CSV file to write the extracted data
    with open('output.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row to the CSV file
        writer.writerow(['TimeStamp', 'Level', 'Process ID', 'Thread ID', 'INFO', 'Transaction ID', 'Start Time', 'End Time'])

        # Initialize variables to store the start and end times of each transaction
        start_time = ''
        end_time = ''
        parsed_logs = []

        # Initialize a variable to count the number of ERROR indications on the INFO column
        error_count = 0

        # Loop through each line in the log file
        for line in f:
            # Split the line into columns
            columns = line.split('\t')

            # Extract the Transaction ID, start time, and end time from the INFO column
            if 'transaction' in columns[4] and 'begun' in columns[4]:
                transaction_id = columns[4].split()[2]
                start_time = columns[0]
            elif 'transaction done' in columns[4]:
                transaction_id = columns[4].split('=')[1].strip()
                end_time = columns[0]

                # Write the extracted data to the CSV file
                writer.writerow([columns[0], columns[1], columns[2], columns[3], columns[4], transaction_id, start_time, end_time])

                # Add the parsed log to the list
                parsed_logs.append({
                    'TransactionID': transaction_id,
                    'StartTime': start_time,
                    'EndTime': end_time
                })

                # Reset the start and end times for the next transaction
                start_time = ''
                end_time = ''

            # Count the number of ERROR indications on the INFO column
            if 'ERROR' in columns[1]:
                error_count += 1

        # Print the number of ERROR indications on the INFO column
        print(f'Thenumber of ERROR indications on the INFO column is {error_count}.')

# Calculate the time difference for each transaction
calculate_time_difference(parsed_logs)

# Get the fastest transaction
fastest_transaction = get_fastest_transaction(parsed_logs)
print(f'The fastest transaction is {fastest_transaction}.')

# Get the slowest transaction
slowest_transaction = get_slowest_transaction(parsed_logs)
print(f'The slowest transaction is {slowest_transaction}.')

# Get the average transaction time
average_time = get_average_transaction_time(parsed_logs)
print(f'The average transaction time is {average_time} milliseconds.')
