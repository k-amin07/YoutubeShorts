import pickle
import csv

# Path to the pickle dump file
pickle_file_path = 'mitm_data.pkl'

# Path to the CSV file
csv_file_path = 'mitm_output.csv'

# Open the pickle dump file
with open(pickle_file_path, 'rb') as pickle_file:
    # Load the data from the pickle file
    data = pickle.load(pickle_file)

# Inspect the loaded data (print to console)
for x in data:
    print(x)

# Now we write the data to a CSV file   
with open(csv_file_path, 'w', newline='') as csv_file:
    
    csv_writer = csv.writer(csv_file)
    # Writing the header fields
    csv_writer.writerow(['url', 'method', 'size', 'time', 'client_connection_established', 'server_connection_initiated', 'server_tcp_handshake', 'server_tls_handshake', 'client_tls_handshake', 'first_request_byte', 'request_complete', 'first_response_byte', 'response_complete', 'server_connection_closed', 'client_connection_closed'])


    #Given that we have the data we will iterate through each record and write it to the CSV file
    for record in data:
        csv_writer.writerow([
            record['url'],
            record['method'],
            record['size'],
            record['time'],
            record['latency_metrics']['client_connection_established'],
            record['latency_metrics']['server_connection_initiated'],
            record['latency_metrics']['server_tcp_handshake'],
            record['latency_metrics']['server_tls_handshake'],
            record['latency_metrics']['client_tls_handshake'],
            record['latency_metrics']['first_request_byte'],
            record['latency_metrics']['request_complete'],
            record['latency_metrics']['first_response_byte'],
            record['latency_metrics']['response_complete'],
            record['latency_metrics']['server_connection_closed'],
            record['latency_metrics']['client_connection_closed']
    ])

