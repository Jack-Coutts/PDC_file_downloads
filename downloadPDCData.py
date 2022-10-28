# This is a sample Python script to batch download PDC data files in to your local computer
# Save this script as downloadPDCData.py in your local directory
# Provide downloaded PDC File manifest as a command line parameter
# Ex:  python3 downloadPDCData.py <PDC File manifest>
# Users may improvise using awk, sed and rewrite in perl, python, etc.

import sys
import csv
import os
import shutil
import requests
import logging
import pandas as pd
from datetime import datetime


def download_organize(file_name, delimiter, output_directory):

    # Initiate logger
    logging.basicConfig(filename=file_name.replace('.csv', '.log').replace('.tsv', '.log'), encoding='utf-8', level=logging.INFO)
    # Open the export manifest csv
    with open(file_name) as f:

        reader = csv.DictReader(f, delimiter=delimiter)  # read rows into a dictionary format

        file_num = len(pd.read_csv(file_name))  # Total number of files
        count = 0  # Initiate a counter to keep track of how many files left to download

        print(f'Downloads starting .... {datetime.now()}')
        logging.info(f'Downloads starting.... {datetime.now()}')

        for row in reader:  # read a row as {column1: value1, column2: value2,...}
            count += 1
            fname = row['File Name']
            folder = row['Run Metadata ID']
            pdc_study_id = row['PDC Study ID']
            study_version = row['PDC Study Version']
            data_category = row['Data Category']
            file_type = row['File Type']
            url_link = row['File Download Link']
            # Expected file structure: PDC Study ID/ PDC Study Version/Data category/Run Metadata ID/File Type/File
            if folder == "" or folder == 'null':
                folder_name = os.path.join(pdc_study_id, study_version, data_category, file_type)
            else:
                folder_name = os.path.join(pdc_study_id, study_version, data_category, folder, file_type)
            # Download file
            url = requests.get(url_link)  # Download the file from a url
            folder_path = os.path.join(output_directory, folder_name)  # Output file directory
            if os.path.isfile(os.path.join(folder_path, fname)):  # Do not add to directory if already there
                logging.info(f'{fname} already exists. Skipping download ... File {count} of {file_num} - {datetime.now()}')
            else:  # Add to specified directory
                logging.info(f'Downloading {fname}. File {count} of {file_num} - {datetime.now()}')
                open(fname, 'wb').write(url.content)
                # Move file to destination
                if not (os.path.exists(folder_path)):
                    os.makedirs(folder_path)
                shutil.move(fname, folder_path)

        print(f'Downloads Complete! - {datetime.now()}')
        logging.info(f'Downloads Complete! - {datetime.now()}')


def main():
    if sys.argv and len(sys.argv) > 1:
        file_name = sys.argv[1]
        output_directory = sys.argv[2]
        if os.path.isfile(file_name):
            # check if the file is in a supported format (CSV or TSV) and set table delimiter
            if file_name.lower().endswith('.csv'):
                delimiter = ','
            elif file_name.lower().endswith('.tsv'):
                delimiter = '\t'
            else:
                exit(f'Input file has an invalid extension. File must be in TSV (.tsv) or CSV (.csv) format')

            download_organize(file_name, delimiter, output_directory)

        else:
            print(f'File {file_name} does not exist in the current directory.')
    else:
        print(f'Please enter a file name.\nUsage: python3 downloadPDCData.py <PDC File manifest>')


if __name__ == "__main__":
    main()

