import csv


# read CSV file
def read_data():
    with open('data.csv', newline='') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            # skip empty lines
            if not row[reader.fieldnames[0]]:
                continue
            data.append(row)
        return data
