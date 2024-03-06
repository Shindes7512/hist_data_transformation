import csv
from datetime import datetime, timedelta

# Function to parse date string into datetime object
def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%d")
    else:
        return None

# Function to format date as string
def format_date(date):
    if date:
        return date.strftime("%Y-%m-%d")
    else:
        return ''

# Function to generate historical records for an employee
def generate_records(employee_data):
    records = []
    last_compensation = None
    last_pay_raise_date = None

    for i, data in enumerate(employee_data):
        effective_date = parse_date(data['Date of Joining'])
        end_date = parse_date(data['Date of Exit']) if data['Date of Exit'] else datetime(2100, 1, 1) - timedelta(days=1)
        compensation = int(data['Compensation'])
        variable_pay = 0
        performance_rating = None
        engagement_score = None

        if data['Compensation 1 date']:
            pay_raise_date = parse_date(data['Compensation 1 date'])
            last_pay_raise_date = pay_raise_date
            last_compensation = int(data['Compensation 1'])
        elif data['Compensation 2 date']:
            pay_raise_date = parse_date(data['Compensation 2 date'])
            last_pay_raise_date = pay_raise_date
            last_compensation = int(data['Compensation 2'])

        if last_pay_raise_date:
            variable_pay = last_compensation - compensation

        if data['Review 2 date']:
            performance_rating = float(data['Review 2'])
        elif data['Review 1 date']:
            performance_rating = float(data['Review 1'])

        if data['Engagement 2 date']:
            engagement_score = float(data['Engagement 2'])
        elif data['Engagement 1 date']:
            engagement_score = float(data['Engagement 1'])

        records.append({
            'Employee Code': data['Employee Code'],
            'Manager Employee Code': data['Manager Employee Code'],
            'Last Compensation': last_compensation,
            'Compensation': compensation,
            'Last Pay Raise Date': format_date(last_pay_raise_date),
            'Variable Pay': variable_pay,
            'Tenure in Org': None,  # Not provided in input data
            'Performance Rating': performance_rating,
            'Engagement Score': engagement_score,
            'Effective Date': format_date(effective_date),
            'End Date': format_date(end_date)
        })

    return records

# Function to read input CSV file and generate output CSV file
def transform_data(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = ['Employee Code', 'Manager Employee Code', 'Last Compensation', 'Compensation', 
                      'Last Pay Raise Date', 'Variable Pay', 'Tenure in Org', 'Performance Rating', 
                      'Engagement Score', 'Effective Date', 'End Date']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        current_employee_data = []
        current_employee_code = None

        for row in reader:
            if row['Employee Code'] != current_employee_code:
                records = generate_records(current_employee_data)
                for record in records:
                    writer.writerow(record)
                current_employee_data = []
                current_employee_code = row['Employee Code']
            current_employee_data.append(row)

        # Process last employee's data
        records = generate_records(current_employee_data)
        for record in records:
            writer.writerow(record)

# Usage
transform_data('input.csv', 'output.csv')
