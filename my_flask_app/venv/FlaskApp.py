from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from datetime import datetime

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/EcoTrackDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'Users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Define the DailyEmissions model
class DailyEmissions(db.Model):
    __tablename__ = 'DailyEmissions'
    emission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    emission_date = db.Column(db.Date, nullable=False)
    emission_grams = db.Column(db.Numeric(10, 2), nullable=False)
    
    user = db.relationship('User', backref=db.backref('daily_emissions', lazy=True))

# Define the WeeklyEmissions model
class WeeklyEmissions(db.Model):
    __tablename__ = 'WeeklyEmissions'
    emission_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    emission_grams = db.Column(db.Numeric(10, 2), nullable=False)
    
    user = db.relationship('User', backref=db.backref('weekly_emissions', lazy=True))

# Define the Cars model
class Car(db.Model):
    __tablename__ = 'Cars'
    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    
    user = db.relationship('User', backref=db.backref('cars', lazy=True))

# Define the Badges model
class Badge(db.Model):
    __tablename__ = 'Badges'
    badge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.user_id'), nullable=False)
    badge_name = db.Column(db.String(50), nullable=False)
    date_awarded = db.Column(db.Date, nullable=False)
    
    user = db.relationship('User', backref=db.backref('badges', lazy=True))

# Create the database tables
with app.app_context():
    db.create_all()

# Route to add a new user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    try:
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'User already exists!'}), 400

# Route to add daily emissions
@app.route('/daily-emissions', methods=['POST'])
def add_daily_emission():
    data = request.json
    try:
        new_emission = DailyEmissions(user_id=data['user_id'], emission_date=data['emission_date'], emission_grams=data['emission_grams'])
        db.session.add(new_emission)
        db.session.commit()
        return jsonify({'message': 'Daily emission added successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error adding daily emission!'}), 400

# Route to add weekly emissions
@app.route('/weekly-emissions', methods=['POST'])
def add_weekly_emission():
    data = request.json
    try:
        new_emission = WeeklyEmissions(user_id=data['user_id'], start_date=data['start_date'], end_date=data['end_date'], emission_grams=data['emission_grams'])
        db.session.add(new_emission)
        db.session.commit()
        return jsonify({'message': 'Weekly emission added successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error adding weekly emission!'}), 400

# Route to add a car
@app.route('/cars', methods=['POST'])
def add_car():
    data = request.json
    try:
        new_car = Car(user_id=data['user_id'], year=data['year'], make=data['make'], model=data['model'])
        db.session.add(new_car)
        db.session.commit()
        return jsonify({'message': 'Car added successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error adding car!'}), 400

# Route to add a badge
@app.route('/badges', methods=['POST'])
def add_badge():
    data = request.json
    try:
        new_badge = Badge(user_id=data['user_id'], badge_name=data['badge_name'], date_awarded=data['date_awarded'])
        db.session.add(new_badge)
        db.session.commit()
        return jsonify({'message': 'Badge added successfully!'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'message': 'Error adding badge!'}), 400

# Route to get user emissions
@app.route('/emissions/<int:user_id>', methods=['GET'])
def get_emissions(user_id):
    daily_emissions = DailyEmissions.query.filter_by(user_id=user_id).all()
    weekly_emissions = WeeklyEmissions.query.filter_by(user_id=user_id).all()
    
    daily_emissions_data = [{'emission_date': e.emission_date, 'emission_grams': str(e.emission_grams)} for e in daily_emissions]
    weekly_emissions_data = [{'start_date': e.start_date, 'end_date': e.end_date, 'emission_grams': str(e.emission_grams)} for e in weekly_emissions]
    
    return jsonify({
        'daily_emissions': daily_emissions_data,
        'weekly_emissions': weekly_emissions_data
    })

# Define the index route
@app.route('/')
def index():
    return "Carbon Emissions"

if __name__ == '__main__':
    app.run(debug=True)
