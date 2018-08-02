'''
Duplicates based off of first and last name
'''
import base
from gspread.exceptions import APIError

def main():
    names = set()
    dupes = []
    LIMIT = 1000
    OFFSET = 0
    more = True
    while more:
        base_url = 'https://api.humanitarian.id/api/v2/user?limit='+str(LIMIT)+'&offset='\
                   +str(OFFSET)+'&sort=name&access_token='
        full_url = base_url + base.ACCESS_TOKEN
        content = base.open_url(full_url)
        if len(content)!=0:
            for person in content:
                first = person['given_name']
                last = person['family_name']
                full = first.title() + ' ' + last.title()
                if full not in names:
                    names.add(full)
                else:
                    if full not in dupes:
                        dupes.append(full)
            OFFSET+=1000
        else:
            break

    # Update Google Sheet
    try:
        worksheet = base.wks.add_worksheet(title="Duplicates", rows=(len(dupes)+4), cols=10)
        worksheet.update_acell('A2', "Duplicate accounts (Based on given and family name matching)")
        worksheet.update_acell('A3', "Name")
    except APIError:
        worksheet = base.wks.worksheet("Duplicates")

    names_list = worksheet.range('A4:A'+str(len(dupes)+3))
    index = 0
    for cell in names_list:
        cell.value = dupes[index]
        index+=1
    worksheet.update_cells(names_list)

    # Update last modified
    updated = base.update_timestamp(worksheet)
    worksheet.update_acell('A1', updated)

if __name__ == '__main__':
    main()