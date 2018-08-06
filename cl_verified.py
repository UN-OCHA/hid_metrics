'''
How many custom lists use the ONLY for verified users option?
'''
import base

def main():
    LIMIT = 100
    OFFSET = 0
    VERIFIED_COUNT = 0
    more = True
    while more:
        base_url = 'https://api.humanitarian.id/api/v2/list?visibility=verified&limit='+str(LIMIT)+'&offset='\
                   +str(OFFSET)+'&access_token='
        full_url = base_url + base.API_KEY
        content = base.open_url(full_url)
        page_count = len(content)
        if page_count==0:
            more = False
        else:
            VERIFIED_COUNT+=page_count
        OFFSET+=100
    print(VERIFIED_COUNT)

if __name__ == '__main__':
    main()
