import os
import datetime
from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from peewee import *
from playhouse.shortcuts import model_to_dict

# Load environment variables
load_dotenv()

# Create Flask app instance with template folder path
app = Flask(__name__, template_folder='app/templates')

# Database initialization
if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
    mydb = MySQLDatabase(
        os.getenv("MYSQL_DATABASE"),
        user=os.getenv("MYSQL_USER","root"),
        password=os.getenv("MYSQL_PASSWORD"),
        host=os.getenv("MYSQL_HOST", "mysql"),
        port=3306
    )

# Peewee model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

# Link DB to model
TimelinePost._meta.database = mydb

# Initialize database connection
try:
    mydb.connect()
    mydb.create_tables([TimelinePost])
    print("Database connected successfully")
except Exception as e:
    print(f"Database connection error: {e}")

# User data classes
class User:
    def __init__(self, name, pic, about, education, work, hobbies, places):
        self.name = name
        self.pic = pic
        self.about = about
        self.education = education
        self.work = work
        self.hobbies = hobbies
        self.places = places

class Education:
    def __init__(self, school, grad, major):
        self.school = school
        self.grad = grad
        self.major = major

class Work:
    def __init__(self, title, company, description):
        self.title = title
        self.company = company
        self.description = description

class Hobbies:
    def __init__(self, hobby, img):
        self.hobby = hobby
        self.img = img

class Places:
    def __init__(self, city, country):
        self.city = city
        self.country = country

# Create user object
Aria = User(
    "Arianna Richardson",
    "/static/img/me.jpg",
    "Hello! My name is Arianna and I am from Bowie, MD! I enjoy coding and creating digital media...",
    Education("University of Maryland, Baltimore County", "Graduated 2025", "Information Systems"),
    [
        Work("Undergraduate Researcher", "", ["Designed UI dashboards using Unreal Engine."]),
        Work("Platform Engineer Intern", "", ["12-week internship at Disney Experiences."]),
        Work("Google CSSI", "", ["Virtual program teaching JavaScript."]),
        Work("Communications Intern", "", ["Redesigned school website, edited media, etc."]),
    ],
    [Hobbies("Digital Art", "./static/img/DigitalArt.jpg")],
    [Places("Bowie", "USA"), Places("Baltimore", "USA")]
)

@app.route("/api/timeline_post", methods=['POST'])
def post_time_line_post():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    content = request.form.get('content', '').strip()

    if not name:
        return jsonify({"error": "Invalid name"}), 400
    if not email or '@' not in email:
        return jsonify({"error": "Invalid email"}), 400
    if not content:
        return jsonify({"error": "Invalid content"}), 400

    timeline_post = TimelinePost.create(name=name, email=email, content=content)
    return jsonify(model_to_dict(timeline_post)), 201

@app.route('/api/timeline_post', methods=['GET'])
def get_timeline_post():
    posts = TimelinePost.select().order_by(TimelinePost.created_at.desc())
    return jsonify({'timeline_posts': [model_to_dict(p) for p in posts]})

@app.route('/timeline')
def timeline():
    return render_template('timeline.html', title="Timeline")

@app.route('/')
def index():
    return render_template('base.html', title="MLH Fellow", user=Aria)

@app.route('/hobbies')
def hobbies():
    return render_template('Hobbies.html', title="Hobbies", user=Aria)

@app.route('/places')
def places():
    return render_template('Places.html', title="Places", user=Aria)

# Make sure the app is exposed at the module level
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)