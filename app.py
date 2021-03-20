from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi

import random
import modules
conn = dbi.connect()

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True


# route for home page
@app.route('/')
def index():
    states = modules.listStatesWithListings(conn)
    return render_template('main.html', states = states)

# route for listing page specified by house ID
@app.route('/listing/<int:hId>')
def listing(hId):
    house = modules.get_details(conn, hId)
    return render_template('listing.html', 
        address = house['address'], listingTitle = house['listingTitle'], 
        username = house['username'], price = house['price'], 
        city = house['city'], state = house['state'], 
        bedroomNum  = house['bedroomNum'], roommatesNum = house['roommatesNum'],
        bathroomNum = house['bathroomNum'], sqrft = house['sqrft'], 
        area = house['area'], nearbySchools = house['nearbySchools'],
        openDate = house['openDate'], closeDate = house['closeDate'], 
        description = house['description'], availability = house['availability'])


# route for submiting a listing
@app.route('/submitListing/', methods=['GET','POST'])
def submitListing():
    conn = dbi.connect()
    #renders form if get
    if request.method == 'GET':
        stateCodes = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
                  "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
                  "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
                  "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
                  "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

        return render_template('submitListing.html', stateCodes = stateCodes)
    #otherwise adds inserted data into listing table
    else: 
        address = request.form.get('address')
        listingTitle = request.form.get('listingTitle')
        username = request.form.get('username')
        price = request.form.get('price')
        city = request.form.get('city')
        state = request.form.get('state')
        bedroomNum = request.form.get('bedroomNum')
        roommatesNum = request.form.get('roommatesNum')
        bathroomNum = request.form.get('bathroomNum')
        sqrft = request.form.get('sqrft')
        area = request.form.get('area')
        nearbySchools = request.form.get('nearbySchools')
        openDate = request.form.get('openDate')
        closeDate = request.form.get('closeDate')
        description = request.form.get('description')
        availability = request.form.get('availability')

        modules.insertListing(conn, address, listingTitle, username,
                             price, city, state, bedroomNum, roommatesNum, bathroomNum, sqrft, 
                             area, nearbySchools, openDate, closeDate, description, availability)
        flash("Listing successfully submitted!")
        return render_template('submitListing.html')


# route for searching for a listing
# currently only using the details for state, city, and number of bedrooms
@app.route('/search/', methods=['GET'])
def search():
    state = request.args.get('state')
    city = request.args.get('city')
    bedroomNum = request.args.get('bedroomNum')
    matches = modules.searchListings(conn, city, state, bedroomNum)

    #goes straight to listing page if only one matching result
    if len(matches) == 1:     
        return redirect(url_for('listing', hId = matches[0]['hId']))
    #goes to list if more than one result
    elif len(matches) > 1:
        return render_template('listingResults.html', listings = matches)
    else:
        flash("No listings fit your search criteria")
        states = modules.listStatesWithListings(conn)
        return render_template('main.html', states = states)

@app.before_first_request
def init_db():
    dbi.cache_cnf()
    dbi.use('housemate_db') 

if __name__ == '__main__':
    import sys, os
    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    app.debug = True
    app.run('0.0.0.0',port)