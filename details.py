import cs304dbi as dbi
conn = dbi.connect()
dbi.use('housemate_db')
curs = dbi.dict_cursor(conn)

def get_details(conn, hId):
    '''Returns the lisiting details as a list of dictionaries.'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        select * from lisiting where hId = %s;'''[hId])
    return curs.fetchall()
    