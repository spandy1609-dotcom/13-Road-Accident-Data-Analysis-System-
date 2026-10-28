CREATE DATABASE IF NOT EXISTS road_accident_analysis;
USE road_accident_analysis;

CREATE TABLE IF NOT EXISTS locations (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(100) NOT NULL,
    road_name VARCHAR(150) NULL
);

CREATE TABLE IF NOT EXISTS accidents (
    accident_id INT AUTO_INCREMENT PRIMARY KEY,
    accident_datetime DATETIME NULL,
    location_id INT NOT NULL,
    vehicle_type VARCHAR(50) NULL,
    severity ENUM('Minor', 'Serious', 'Fatal', 'Unknown') NOT NULL DEFAULT 'Unknown',
    weather VARCHAR(50) NULL,
    CONSTRAINT fk_accident_location
        FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- Example analysis queries:
-- Accident counts by month
SELECT DATE_FORMAT(accident_datetime, '%Y-%m') AS accident_month,
       COUNT(*) AS recorded_accidents
FROM accidents
GROUP BY DATE_FORMAT(accident_datetime, '%Y-%m')
ORDER BY accident_month;

-- Severity distribution
SELECT severity, COUNT(*) AS record_count
FROM accidents
GROUP BY severity
ORDER BY record_count DESC;

-- Regions with most recorded accidents
SELECT l.region, COUNT(*) AS record_count
FROM accidents a
JOIN locations l ON a.location_id = l.location_id
GROUP BY l.region
ORDER BY record_count DESC;
