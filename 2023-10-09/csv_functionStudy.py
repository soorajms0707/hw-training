import csv

# functions of csv module
# csv.reader

# with open('op.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     for row in csv_reader:
#         print(row)
#         print(row[1])

# methods and attributes in reader object
# next()

# with open('op.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)
#     for row in csv_reader:
#         print(row)

# csv_reader.dialect

# with open('op.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     print(csv_reader.dialect.delimiter)

# csv_reader.line_num

with open('op.csv', 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(f'Line {csv_reader.line_num}: {row}')


# csv.writer
# csvwriter.writerow

# with open('op.csv', 'w', newline='') as file:
#     csv_writer = csv.writer(file)
#     csv_writer.writerow(['Name', 'Age', 'City'])
#     csv_writer.writerow(['John Doe', 30, 'New York'])

# csvwriter.writerows

# with open('test.csv', 'w', newline='') as file:
#     csv_writer = csv.writer(file)
#     csv_writer.writerows([
#         ['Name', 'Age', 'City'],
#         ['John Doe', 30, 'New York'],
#         ['abhishek', 20, 'New York']
#     ])


# csv.register_dialect

# csv.register_dialect('my_dialect', delimiter='|')

# with open('op.csv', 'r', newline='') as file:
#     csv_reader = csv.reader(file, dialect='my_dialect')
#     for row in csv_reader:
#         print(row)

# csv.register_dialect('example1', delimiter='|')
# with open('example1.csv', 'w', newline='') as file:
#     csv_writer = csv.writer(file, dialect='example1')
#     csv_writer.writerow(['Name', 'Age', 'City'])
#     csv_writer.writerow(['John Doe', 30, 'New York'])

# csv.register_dialect('example2', delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# with open('example2.csv', 'w', newline='') as file:
#     csv_writer = csv.writer(file, dialect='example2')
#     csv_writer.writerow(['Name', 'Age', 'City'])
#     csv_writer.writerow(['John,Doe', 30, 'New "York"']) 


#csv.DictReader

# with open('example.csv', 'r') as file:
#     csv_reader = csv.DictReader(file)
#     for row in csv_reader:
#         print(row)

# csv.DictWriter(

# fieldnames = ['Name', 'Age', 'City']

# with open('output.csv', 'w', newline='') as file:
#     csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
#     csv_writer.writeheader()
#     csv_writer.writerow({'Name': 'John Doe', 'Age': 30, 'City': 'New York'})
#     csv_writer.writerow({'Name': 'Jane Smith', 'Age': 25, 'City': 'San Francisco'})

# csv.sniffer

# with open('ex.csv', 'r') as file:
#     sample = file.read(4096) 

# sniffer = csv.Sniffer()
# dialect = sniffer.sniff(sample)

# with open('ex.csv', 'r') as file:
#     csv_reader = csv.reader(file, dialect=dialect)
#     for row in csv_reader:
#         print(row)