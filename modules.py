# modules for app.py

import cs304dbi as dbi


def get_details(conn, hId):
    '''Returns the lisiting details as a list of dictionaries.'''
    curs = dbi.dict_cursor(conn)
    curs.execute('''select * from listing where hId = %s;''',[hId])
    return curs.fetchone()
    

def insertListing(conn, address, listingTitle, username,
                             price, city, state, bedroomNum, roommatesNum, bathroomNum, sqrft, 
                             area, nearbySchools, openDate, closeDate, description, availability):
    '''Inserts  new listing to the table '''
    curs = dbi.dict_cursor(conn)
    curs.execute('''Insert into listing(address, listingTitle, username, price, 
                    city, state, bedroomNum, roommatesNum, bathroomNum, sqrft, area,
                    nearbySchools, openDate, closeDate, description, availability) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s)''', [address, listingTitle, username,
                             price, city, state, bedroomNum, roommatesNum, bathroomNum, sqrft, 
                             area, nearbySchools, openDate, closeDate, description, availability])
    conn.commit() 

def searchListings(conn, city, state, bedroomNum):
        """Retrieves listings that match searched criteria"""
        curs = dbi.dict_cursor(conn)
        curs.execute('''select hId, city, state, bedroomNum, description from 
        listing where city like %s and state = %s and bedroomNum = %s''',
        [city, state, bedroomNum])
        return curs.fetchall()


def listStatesWithListings(conn):
    """ Returns the state's of the available listing for
        the drop down menu in the search form"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''select distinct state from listing ''')
    return curs.fetchall()
