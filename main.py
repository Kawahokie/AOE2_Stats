import requests
import json
import csv

response = requests.get("https://aoe2.net/api/matches?game=aoe2de&since=1658725251&count=2&leaderboard_id=4&map_type_id=16")
print(response.status_code)
#print(response.json())

data = response.json()
print(data)
with open('data.json', 'w') as f:
    json.dump(data, f)

with open('data.json') as json_file:
    datafile = json.load(json_file)

print(datafile[0]['players'][0]['civ'])


# Opening JSON file and loading the data
# into the variable data
# jsonkeylist = json.loads(keylist)

# for key in jsonkeylist:
#     print(key)

# with open('response.csv', 'w', newline='') as csvfile:
#     fieldnames = ['name', 'city', 'Height']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     for row in data:
#         writer.writerow(row)

######## Attempt 2
# employee_data = data['emp_details']
 
# # now we will open a file for writing
# data_file = open('data_file.csv', 'w')
 
# # create the csv writer object
# csv_writer = csv.writer(data_file)
 
# # Counter variable used for writing
# # headers to the CSV file
# count = 0
 
# for emp in employee_data:
#     if count == 0:
 
#         # Writing headers of CSV file
#         header = emp.keys()
#         csv_writer.writerow(header)
#         count += 1
 
#     # Writing data of CSV file
#     csv_writer.writerow(emp.values())
 
# data_file.close()
