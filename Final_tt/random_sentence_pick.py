import csv
import pandas
import random

input_path= '/Users/sakshishukla/Desktop/text_tech/'

def write_file(input_path)
    with open(input_path + 'data.csv', "rb") as csv_file:
        for row in csv_file:
            original_rows = 10019
            desired_rows = 472
            skip = sorted(random.sample(range(original_rows), original_rows-desired_rows))
            df = pandas.read_csv(csv_file, skiprows=skip)
            df.to_csv(input_path + 'new_data.csv')

def main() :
    write_file(input_path)

if __name__ == "__main__":
    pass
