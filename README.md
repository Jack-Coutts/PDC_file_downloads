## Download raw data files from Proteomic Data Commons

---

Python script for batch downloading data from the Proteomic Data Commons using export manifest csv file containing file download urls. Instructions for how to create the export manifest file can be found [here](https://pdc.cancer.gov/pdc/faq/Download_Data). This script is adapted from the one provided by the Proteomic Data Commons.

---

### Usage Instructions:

1. Create a directory containing the downloadPDCData.py file and download the dependancies in the requirements.txt file.
2. Add the created export manifiest csv file to the same directory.
3. To execute the script navigate to the directroy containing the above files and enter: python3 downloadPDCData.py export_manifest.csv output/directory/
4. E.g. python3 downloadPDCData.py PDC_file_manifest_10282022_103445.csv /Users/couttsj/Desktop/


While running the script will produce a .log file in the same directory as the downloadPDCData.py file which shows which files have been downloaded and when. Both the .log file and the terminal will informthe user when the downloads start and finish.


