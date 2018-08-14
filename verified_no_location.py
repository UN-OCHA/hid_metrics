'''
Verified profiles without location (no auth users)
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
        base_url = 'https://api.humanitarian.id/api/v2/user?verified=true&authOnly=false&limit='+\
                   str(LIMIT)+'&offset='+str(OFFSET)+'&access_token='
        full_url = base_url + base.API_KEY
        content = base.open_url(full_url)
        print('Getting', LIMIT, 'new records...')

        if len(content) != 0:
            for user in content:
                try:
                    location = user['locations']
                    if (location == None) or (len(location) == 0):
                        ids.append(user['_id'])
                        firsts.append(user['given_name'])
                        lasts.append(user['family_name'])
                    else:
                        continue
                except KeyError:
                    ids.append(user['_id'])
                    firsts.append(user['given_name'])
                    lasts.append(user['family_name'])
            OFFSET+=1000
        else:
            more = False

    # Update Google Sheet
    try:
        worksheet = base.wks.worksheet("Verified - No Location")
    except APIError as e:
        print("{}: {}".format(type(e).__name__, e))
        try:
            worksheet = base.wks.add_worksheet(title="Verified - No Location", rows=(len(ids)+4), cols=10)
            worksheet.update_acell('A2', "Verified profiles without location (excludes auth users)")
            worksheet.update_acell('A3', "User ID")
            worksheet.update_acell('B3', "Given Name")
            worksheet.update_acell('C3', "Family Name")
        except:
            print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])
    except:
        print("Unexpected error:", sys.exc_info()[0], sys.exc_info()[1])

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