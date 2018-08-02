'''
How many people are using the "connections" feature at all?
'''
import base

def main():
    LIMIT = 100
    OFFSET = 0
    CONNECTIONS_COUNT = 0
    more = True
    while more:
        base_url = 'https://api.humanitarian.id/api/v2/user?sort=-connections&limit='+\
                   str(LIMIT)+'&offset='+str(OFFSET)+'&access_token='
        full_url = base_url + base.ACCESS_TOKEN
        content = base.open_url(full_url)
        if len(content)==0:
            more = False
        for user in content:
            connection = user['connections']
            num_connections = len(connection)
            if num_connections == 0:
                more = False
            else:
                CONNECTIONS_COUNT+=1
        OFFSET+=100
    print(CONNECTIONS_COUNT)

if __name__ == '__main__':
    main()