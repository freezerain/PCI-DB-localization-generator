import csv


def read_data():
    with open('data.csv', newline='') as f:
        reader = csv.DictReader(f)
        data = []
        for row in reader:
            if not row[reader.fieldnames[0]]:
                continue
            data.append(row)
        return data
