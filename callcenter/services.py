import csv
from django.conf import settings

def filter_csv(Case_Number=None, phone=None, first_name=None, family_name=None, id_number=None):
    results = []
    with open(settings.CSV_FILE_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if Case_Number and row['Case_Number'] != Case_Number:
                continue
            if phone and not (row['HoH_Mobile'] == phone or row['Alt_Mobile'] == phone):
                continue
            if first_name and family_name:
                if not (row['HoH_FirstName_Ar'] == first_name and row['HoH_FamilyName_Ar'] == family_name) or \
                   not (row['Alt_FirstName_Ar'] == first_name and row['Alt_FamilyName_Ar'] == family_name) or \
                   not (row['HoH_FirstName_En'] == first_name and row['HoH_FamilyName_En'] == family_name) or \
                   not (row['Alt_FirstName_En'] == first_name and row['Alt_FamilyName_En'] == family_name):
                    continue
            if id_number and row['id_number'] != id_number:
                continue
            results.append(row)
    return results
