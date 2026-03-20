-- AI Detection Engine – Database Schema
-- Run this in MySQL before starting the app

CREATE DATABASE IF NOT EXISTS ai_detection_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE ai_detection_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    username   VARCHAR(80)  NOT NULL,
    email      VARCHAR(120) NOT NULL UNIQUE,
    password   VARCHAR(256) NOT NULL,
    is_admin   TINYINT(1)   NOT NULL DEFAULT 0,
    created_at DATETIME     DEFAULT CURRENT_TIMESTAMP
);

-- Detection logs table
CREATE TABLE IF NOT EXISTS detection_logs (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT           NOT NULL,
    input_type VARCHAR(10)  NOT NULL COMMENT 'url or apk',
    input_data VARCHAR(512) NOT NULL,
    result     VARCHAR(10)  NOT NULL COMMENT 'FAKE or GENUINE',
    risk_score FLOAT        NOT NULL,
    details    TEXT,
    timestamp  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Default admin user (password: admin123 — change immediately!)
INSERT INTO users (username, email, password, is_admin) VALUES (
  'admin',
  'admin@aidetection.com',
  'pbkdf2:sha256:600000$rJspKtTDcHanJ1mQ$3dd21a3e2dbd0e4b3ed5c23ae0d5d4571e2b9ec33d6e45cfe3e3be3c6e4a9c3a',
  1
) ON DUPLICATE KEY UPDATE id=id;
