import csv
from jinja2 import Template
import subprocess

# Function to read CSV file and return data
def read_csv(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader)
        for row in reader:
            neighbor = {
                'ip': row[2],
                'remote_as': int(row[3]),
                'networks': row[4].split(','),
                'redistribute': row[5].lower() == 'true'
            }
            data.append({'hostname': row[0],
                         'as_number': int(row[1]),
                         'neighbors': [neighbor]})
    print(f'Data: {data[0]}')
    return data


# Function to generate running config using Jinja2 template
def generate_config(template_file, data):
    with open(template_file, 'r') as file:
        template = Template(file.read())
    return template.render(data=data[0])  # Assuming there's only one set of data in the CSV

# Function to start FRR router with generated config
def start_frr(config_file):
    try:
        subprocess.run(['sudo', 'cp', config_file, '/etc/frr/frr.conf'])
        print("FRR config file copied")
        subprocess.run(['sudo', 'systemctl', 'restart', 'frr'])
        print("Restarting FRR Router...")
    except:
        print("Unable to start FRR Router. Please check configuration settings")

def main():
    csv_file = 'frr_bgp_config.csv'
    template_file = 'frr_bgp_template.j2'
    config_file = 'frr_config.conf'

    # Read data from CSV
    try:
        data = read_csv(csv_file)
        print("FRR Configurations Received...")
    except:
        print("Unable to obtain input data. Please make sure file exists...")        

    # Generate running config
    try:
        running_config = generate_config(template_file, data)
        print("FRR Config Generated...")
    except:
        print("Unable to generate FRR config file...")
        SystemExit

    # Write config to file
    with open(config_file, 'w') as file:
        file.write(running_config)

    # Start FRR router with generated config
    start_frr(config_file)

if __name__ == "__main__":
    main()
