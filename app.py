from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug.utils import secure_filename
app = Flask(__name__)

# one or the other of these. Defaults to MySQL (PyMySQL)
# change comment characters to switch to SQLite

import cs304dbi as dbi
# import cs304dbi_sqlite3 as dbi

import random
#import details 
import modules


app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/')
def index():
    return render_template('main.html',title='Hello')

@app.route('/listing/<int:hId>', methods=["GET", "POST"])
def listing():
    if request.method == 'GET':
        return render_template('listing.html', title='Customized Greeting')
    else:
        return redirect

@app.route('/submitListing/', methods=['GET','POST'])
def submitListing():
    conn = dbi.connect()
    if request.method == 'GET':
        return render_template('submitListing.html')
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
        return render_template('submitListing.html')

        #not sure if this is exactly right but something like this
        # return redirect(url_for('listing', hId = select_inserted_id()))

@app.route('/search/', methods=['GET'])
def search():
    conn = dbi.connect()
    curs = dbi.dict_cursor(conn)
    state = request.args.get('state')
    city = request.args.get('city')
    bedroomNum = request.args.get('bedroomNum')
    matches = searchListings(conn, city, state, bedroomNum)
    if len(matches) == 1:     
        return render_template('listing.html', variables...)
    else:
        return render_template('listingResults.html', listings = matches)

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