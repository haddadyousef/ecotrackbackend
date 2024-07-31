from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecotrack.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    car_year = db.Column(db.String(4))
    car_make = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    weekly_emissions = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def car_name(self):
        if self.car_year and self.car_make and self.car_model:
            return f"{self.car_year} {self.car_make} {self.car_model}"
        return "No car information"

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_name = db.Column(db.String(50), nullable=False)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    existing_user = User.query.filter_by(username=data['username']).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 200
    new_user = User(username=data['username'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

@app.route('/api/user/<username>/car', methods=['POST'])
def update_car_info(username):
    data = request.json
    user = User.query.filter_by(username=username).first()
    if user:
        user.car_year = data['car_year']
        user.car_make = data['car_make']
        user.car_model = data['car_model']
        db.session.commit()
        return jsonify({"message": "Car information updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/api/user/<username>/emissions', methods=['POST'])
def update_emissions(username):
    data = request.json
    user = User.query.filter_by(username=username).first()
    if user:
        user.weekly_emissions += data['emissions']
        user.last_updated = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Emissions updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/api/weekly_emissions', methods=['GET'])
def get_weekly_emissions():
    users = User.query.all()
    emissions_data = [{
        "username": user.username, 
        "weekly_emissions": user.weekly_emissions,
        "car_name": user.car_name
    } for user in users]
    return jsonify(emissions_data), 200

@app.route('/api/user/<username>/badges', methods=['GET', 'POST'])
def manage_badges(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    if request.method == 'GET':
        badges = Badge.query.filter_by(user_id=user.id).all()
        badge_list = [{"badge_name": badge.badge_name, "earned_date": badge.earned_date} for badge in badges]
        return jsonify(badge_list), 200

    elif request.method == 'POST':
        data = request.json
        new_badge = Badge(user_id=user.id, badge_name=data['badge_name'])
        db.session.add(new_badge)
        db.session.commit()
        return jsonify({"message": "Badge added successfully"}), 201

@app.route('/api/reset_weekly_emissions', methods=['POST'])
def reset_weekly_emissions():
    users = User.query.all()
    for user in users:
        user.weekly_emissions = 0
        user.last_updated = datetime.utcnow()
    db.session.commit()
    return jsonify({"message": "Weekly emissions reset successfully"}), 200

@app.route('/')
def home():
    return "Welcome to EcoTrack API"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)