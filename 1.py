import csv

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

                # Reset the start and end times for the next transaction
                start_time = ''
                end_time = ''

            # Count the number of ERROR indications on the INFO column
            if 'ERROR' in columns[4]:
                error_count += 1

        # Print the number of ERROR indications on the INFO column
        print(f'The number of ERROR indications on the INFO column is {error_count}.')

