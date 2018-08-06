'''
List of organizations by number of contacts
'''
import base
from gspread.exceptions import APIError

def main():
    LIMIT = 100
    OFFSET = 0
    more = True
    ids = []
    names = []
    counts = []
    while more:
        base_url = 'https://api.humanitarian.id/api/v2/list?type=organization&sort=-count&limit='+str(LIMIT)+\
                   '&offset='+str(OFFSET)+'&access_token='
        full_url = base_url + base.API_KEY
        content = base.open_url(full_url)
        if len(content)==0:
            more = False
        for org in content:
            ids.append(org['_id'])
            names.append(org['label'])
            counts.append(org['count'])
        OFFSET+=100

    # Update Google Sheet
    try:
        worksheet = base.wks.add_worksheet(title="Organizations", rows=(len(ids)+4), cols=10)
        worksheet.update_acell('A2', "List of organizations by number of contacts")
        worksheet.update_acell('A3', "Org ID")
        worksheet.update_acell('B3', "Organization")
        worksheet.update_acell('C3', "Num Contacts")
    except APIError:
        worksheet = base.wks.worksheet("Organizations")

    # Select range
    id_list = worksheet.range('A4:A'+str(len(ids)+3))
    name_list = worksheet.range('B4:B'+str(len(names)+3))
    count_list = worksheet.range('C4:C'+str(len(counts)+3))

    index = 0
    for cell in id_list:
        cell.value = ids[index]
        index+=1

    index = 0
    for cell in name_list:
        cell.value = names[index]
        index+=1

    index = 0
    for cell in count_list:
        cell.value = counts[index]
        index+=1

    # Update in batch - avoids API timeout problem
    worksheet.update_cells(id_list)
    worksheet.update_cells(name_list)
    worksheet.update_cells(count_list)

    # Update last modified
    updated = base.update_timestamp(worksheet)
    worksheet.update_acell('A1', updated)

if __name__ == '__main__':
    main()