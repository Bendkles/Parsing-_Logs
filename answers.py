"""with open('log-file.txt', 'r') as f:
    first_line = f.readline()

print(first_line) 
"""

"""
with open("log-file.txt", 'r') as f:
    lines = f.readlines()

err_count = 0
for line in lines:
    temp_list = line.split("\t")
    if temp_list[1] == "ERROR":
        err_count +=1

print(err_count) 
"""

"""
# Transactions Counter
with open("log-file.txt", 'r') as f:
    lines = f.readlines()

transact_count = 0
for line in lines:
    temp_list = line.split("\t")
    if ("transaction" in temp_list[4]) and ("begun" in temp_list[4]):
        transact_count +=1

print(transact_count) 

"""
from datetime import datetime, timedelta

with open("log-file.txt", 'r') as f:
    lines = f.readlines()

transaction_list = []

for line in lines:
    temp_list = line.split("\t")
    trans_dict = {}  # Create a new dictionary for each transaction

    if "transaction" in temp_list[4] and "begun" in temp_list[4]:
        trans_dict = {
            "transaction_id": temp_list[4].split()[1],
            "start_time": datetime.strptime(temp_list[0], "%d-%m-%Y %H:%M:%S.%f")
        }
    if "transaction done" in temp_list[4]:
        end_time = datetime.strptime(temp_list[0], "%d-%m-%Y %H:%M:%S.%f")
        trans_dict["end_time"] = end_time
        time_difference = (end_time - trans_dict.get("start_time", end_time)).total_seconds() * 1000
        trans_dict["time_difference"] = time_difference
        transaction_list.append(trans_dict)

print(transaction_list)




