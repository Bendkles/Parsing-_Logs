def count_transactions(log_file):
    transaction_count = 0
    transaction_started = False

    with open(log_file, 'r') as file:
        for line in file:
            if "start" in line:
                transaction_started = True
                transaction_count += 1
            elif "end" in line:
                if transaction_started:
                    transaction_started = False
                else:
                    # Ignore "end" messages without corresponding "start" messages
                    pass

    return transaction_count


# Example usage
log_file = '/mnt/d/Cyber-HUB/LAB/Scripts Tools/log-file-example.txt'
num_transactions = count_transactions(log_file)
print("Number of transactions:", num_transactions)
