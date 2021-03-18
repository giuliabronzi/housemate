import cs304dbi as dbi



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

