CREATE DATABASE pharmacy_db;
USE pharmacy_db;
CREATE TABLE medicines (
    Med_id VARCHAR(10) PRIMARY KEY,
    Med_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INT NOT NULL
);

-- Insert sample data into the medication_details table
INSERT INTO medicines VALUES ('M001', 'Paracetamol', 5.00, 500);
INSERT INTO medicines VALUES ('M002', 'Aspirin', 7.50, 300);
INSERT INTO medicines VALUES ('M003', 'Amoxicillin', 15.00, 150);
SELECT*FROM medicines;