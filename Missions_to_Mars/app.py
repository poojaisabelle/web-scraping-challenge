from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo 
import scrape_mars

# Create an instance of the Flask app
app = Flask(__name__)

# Use PyMongo to establish a Mongo Connection 
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_data = mongo.db.mars_data   
    # Run the scrape function and save the results to a variable
    results = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    mars_data.update({}, results, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

