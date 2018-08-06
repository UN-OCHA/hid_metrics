'''
How many users choose the option for ONLY verified users to see their profile?
'''
import base

def main():
    LIMIT = 100
    OFFSET = 0
    ONLY_VER_VIS_COUNT = 0 # keeps track of how many users specify only verified can view their email
    more = True
    while more:
        base_url = 'https://api.humanitarian.id/api/v2/user?emailsVisibility=verified&limit='+str(LIMIT)+\
                   '&offset='+str(OFFSET)+'&access_token='
        full_url = base_url + base.API_KEY
        content = base.open_url(full_url)
        count = len(content)
        if count==0:
            more = False
        else:
            ONLY_VER_VIS_COUNT+=count
        OFFSET+=100
    print(ONLY_VER_VIS_COUNT)

if __name__ == '__main__':
    main()
