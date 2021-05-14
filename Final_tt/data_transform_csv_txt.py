import csv

folder_name = '/Users/sakshishukla/Desktop/text_tech/'

# transforming .csv files into .txt
# according to LAF/GrAF standards
def transform_data_type(folder_name):
    with open(folder_name + 'priamry_data.csv', 'r') as inp, open(folder_name + 'tweets-emotions.txt', 'w+') as out:
        for line in inp:
            line = line.replace(',', '.')
            out.write(line)
    with open(folder_name + 'annotation_data.csv', 'r') as inp, open(folder_name + 'annotation_data.txt', 'w+') as out:
        for line in inp:
            line = line.replace(',', '.')
            out.write(line)
    with open(folder_name + 'segmentation_data.csv', 'r') as inp, open(folder_name + 'segmentation_data.txt', 'w+') as out:
        for line in inp:
            line = line.replace(',', '.')
            out.write(line)

def main() :
    transform_data_type(folder_name)

if __name__ == '__main__':
    main()
            