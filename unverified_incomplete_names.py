'''
Unverified profiles without complete last name or first name
'''
import base
from gspread.exceptions import APIError

def main():
    LIMIT = 1000
    OFFSET = 0
    ids = []
    firsts = []
    lasts = []
    more = True
    while more:
        base_url = 'https://api.humanitarian.id/api/v2/user?verified=false&sort=name&limit='+str(LIMIT)+\
                   '&offset='+str(OFFSET)+'&access_token='
        full_url = base_url + base.ACCESS_TOKEN
        content = base.open_url(full_url)
        if len(content) != 0:
            for user in content:
                id = user['_id']
                first = user['given_name']
                last = user['family_name']
                if (len(first)<=1) or (len(last)<=1):
                    ids.append(id)
                    firsts.append(first)
                    lasts.append(last)
            OFFSET+=1000
        else:
            more = False

    # Update Google Sheet
    try:
        worksheet = base.wks.add_worksheet(title="Unverified - Incomplete", rows=(len(ids)+4), cols=10)
        worksheet.update_acell('A2', "Unverified profiles with potentially incomplete names")
        worksheet.update_acell('A3', "User ID")
        worksheet.update_acell('B3', "Given Name")
        worksheet.update_acell('C3', "Family Name")
    except APIError:
        worksheet = base.wks.worksheet("Unverified - Incomplete")

    # Select range
    id_list = worksheet.range('A4:A'+str(len(ids)+3))
    first_list = worksheet.range('B4:B'+str(len(firsts)+3))
    last_list = worksheet.range('C4:C'+str(len(lasts)+3))

    index = 0
    for cell in id_list:
        cell.value = ids[index]
        index+=1

    index = 0
    for cell in first_list:
        cell.value = firsts[index]
        index+=1

    index = 0
    for cell in last_list:
        cell.value = lasts[index]
        index+=1

    # Update in batch - avoids API timeout problem
    worksheet.update_cells(id_list)
    worksheet.update_cells(first_list)
    worksheet.update_cells(last_list)

    # Update last modified
    updated = base.update_timestamp(worksheet)
    worksheet.update_acell('A1', updated)

if __name__ == '__main__':
    main()