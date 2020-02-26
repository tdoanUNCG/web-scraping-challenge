from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars as sm

# Create an instance of Flask
app = Flask(__name__)

# use pymongo to est. conn with db
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars_db")

# pass conn var
# client = pymongo.MongoClient(conn)

# conn to db
# db = client.scrape_mars_db

# drop collection if available
mongo.db.parti.drop()
mongo.db.partii.drop()
mongo.db.partiii.drop()
mongo.db.partiv.drop()
mongo.db.partv.drop()
# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    #collections
    parti_data = mongo.db.parti.find_one()
    partii_data = mongo.db.partii.find_one()
    partiii_data = mongo.db.partiii.find_one()
    partiv_data = mongo.db.partiv.find()
    partv_data = mongo.db.partv.find_one()
    # print(partiv_data)
    #return template with parti list
    return render_template('index.html', parti_data=parti_data, partii_data=partii_data, partiii_data = partiii_data, partiv_data = partiv_data, partv_data = partv_data)

@app.route('/scrape')
def scrape_mars():
    #run scrape_mars()
    sm.scrape_mars()
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)