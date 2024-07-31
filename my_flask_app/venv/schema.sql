-- Create database if it does not exist
CREATE DATABASE IF NOT EXISTS EcoTrackDB;

-- Use the created database
USE EcoTrackDB;

-- Table to store user information
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to store daily carbon emissions for users
CREATE TABLE IF NOT EXISTS DailyEmissions (
    emission_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    emission_date DATE NOT NULL,
    emission_grams DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, emission_date)
);

-- Table to store weekly carbon emissions for users
CREATE TABLE IF NOT EXISTS WeeklyEmissions (
    emission_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    emission_grams DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, start_date, end_date)
);

-- Table to store car information
CREATE TABLE IF NOT EXISTS Cars (
    car_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    year VARCHAR(4) NOT NULL,
    make VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Table to store badges for users
CREATE TABLE IF NOT EXISTS Badges (
    badge_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    badge_name VARCHAR(50) NOT NULL,
    date_awarded DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Sample data insertions (for testing purposes)
INSERT INTO Users (username, email) VALUES ('john_doe', 'john.doe@example.com');
INSERT INTO DailyEmissions (user_id, emission_date, emission_grams) VALUES (1, '2024-07-21', 120.50);
INSERT INTO WeeklyEmissions (user_id, start_date, end_date, emission_grams) VALUES (1, '2024-07-15', '2024-07-21', 750.75);
INSERT INTO Cars (user_id, year, make, model) VALUES (1, '2020', 'Toyota', 'Camry');
INSERT INTO Badges (user_id, badge_name, date_awarded) VALUES (1, 'Eco Warrior', '2024-07-21');
