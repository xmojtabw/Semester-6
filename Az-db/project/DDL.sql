-- Create the database
CREATE DATABASE HospitalDB;
GO

-- Use the newly created database
USE HospitalDB;
GO

-- Departments Table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY NOT NULL,
    name NVARCHAR(100),
    location NVARCHAR(100)
);

-- Persons Table
CREATE TABLE Persons (
    national_id INT PRIMARY KEY NOT NULL,
    name NVARCHAR(100),
    last_name NVARCHAR(100),
    birth_year INT,
    address NVARCHAR(200),
    phone_number NVARCHAR(20)
);

-- Insurance Table
CREATE TABLE Insurance (
    insurance_id INT PRIMARY KEY NOT NULL,
    company_name NVARCHAR(100),
    discount DECIMAL(5, 2)
);

-- Patients Table
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY NOT NULL,
    national_id INT NOT NULL,
    department_id INT,
    insurance_id INT,
    description NVARCHAR(255),
    FOREIGN KEY (national_id) REFERENCES Persons(national_id),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id),
    FOREIGN KEY (insurance_id) REFERENCES Insurance(insurance_id)
);

-- Employees Table
CREATE TABLE Employees (
    employee_id INT PRIMARY KEY NOT NULL,
    national_id INT NOT NULL,
    department_id INT,
    title NVARCHAR(100),
    FOREIGN KEY (national_id) REFERENCES Persons(national_id),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

-- Doctors Table
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY NOT NULL,
    national_id INT NOT NULL,
    skill NVARCHAR(100),
    education NVARCHAR(100),
    FOREIGN KEY (national_id) REFERENCES Persons(national_id)
);

-- Drug Table
CREATE TABLE Drug (
    drug_id INT PRIMARY KEY NOT NULL,
    price_per_unit DECIMAL(10, 2),
    description NVARCHAR(255),
    name NVARCHAR(100)
);

-- Bill Table
CREATE TABLE Bill (
    bill_id INT PRIMARY KEY NOT NULL,
    doctor_pay DECIMAL(10, 2),
    drugs_pay DECIMAL(10, 2),
    total DECIMAL(10, 2),
    date DATE,
    status NVARCHAR(50)
);

-- BillItem Table
CREATE TABLE BillItem (
    billitem_id INT PRIMARY KEY NOT NULL,
    bill_id INT NOT NULL,
    drug_id INT NOT NULL,
    quantity INT,
    unit_price DECIMAL(10, 2),
    FOREIGN KEY (bill_id) REFERENCES Bill(bill_id),
    FOREIGN KEY (drug_id) REFERENCES Drug(drug_id)
);

-- Visits Table
CREATE TABLE Visits (
    visit_id INT PRIMARY KEY NOT NULL,
    patient_id INT NOT NULL,
    doctor_id INT NOT NULL,
    bill_id INT,
    status NVARCHAR(50),
    patient_feedback NVARCHAR(255),
    doctor_feedback NVARCHAR(255),
    start_date DATE,
    end_date DATE,
    diagnosis NVARCHAR(255),
    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),
    FOREIGN KEY (bill_id) REFERENCES Bill(bill_id)
);


-- Insert into Departments
INSERT INTO Departments (department_id, name, location) VALUES
(1, 'Cardiology', 'Building A'),
(2, 'Neurology', 'Building B'),
(3, 'Pediatrics', 'Building C');

-- Insert into Persons
INSERT INTO Persons (national_id, name, last_name, birth_year, address, phone_number) VALUES
(1001, 'John', 'Doe', 1980, '123 Main St', '555-1234'),
(1002, 'Jane', 'Smith', 1990, '456 Maple Ave', '555-5678'),
(1003, 'Emily', 'Clark', 1985, '789 Oak Dr', '555-9012'),
(1004, 'Michael', 'Brown', 1975, '321 Pine Rd', '555-3456');

-- Insert into Insurance
INSERT INTO Insurance (insurance_id, company_name, discount) VALUES
(1, 'HealthCare Plus', 10.00),
(2, 'LifeSecure', 15.50);

-- Insert into Patients
INSERT INTO Patients (patient_id, national_id, department_id, insurance_id, description) VALUES
(1, 1001, 1, 1, 'Routine checkup'),
(2, 1002, 2, 2, 'Migraine treatment');

-- Insert into Employees
INSERT INTO Employees (employee_id, national_id, department_id, title) VALUES
(1, 1003, 3, 'Nurse'),
(2, 1004, 1, 'Surgeon');

-- Insert into Doctors
INSERT INTO Doctors (doctor_id, national_id, skill, education) VALUES
(1, 1004, 'Cardiothoracic Surgery', 'Harvard Medical School');

-- Insert into Drug
INSERT INTO Drug (drug_id, price_per_unit, description, name) VALUES
(1, 5.00, 'Painkiller', 'Paracetamol'),
(2, 20.00, 'Anti-inflammatory', 'Ibuprofen');

-- Insert into Bill
INSERT INTO Bill (bill_id, doctor_pay, drugs_pay, total, date, status) VALUES
(1, 150.00, 25.00, 175.00, '2025-04-15', 'Paid'),
(2, 200.00, 40.00, 240.00, '2025-04-16', 'Unpaid');

-- Insert into BillItem
INSERT INTO BillItem (billitem_id, bill_id, drug_id, quantity, unit_price) VALUES
(1, 1, 1, 5, 5.00),
(2, 1, 2, 1, 20.00),
(3, 2, 2, 2, 20.00);

-- Insert into Visits
INSERT INTO Visits (visit_id, patient_id, doctor_id, bill_id, status, patient_feedback, doctor_feedback, start_date, end_date, diagnosis) VALUES
(1, 1, 1, 1, 'Completed', 'Very helpful', 'Routine case', '2025-04-15', '2025-04-15', 'Hypertension'),
(2, 2, 1, 2, 'Ongoing', NULL, 'Monitoring symptoms', '2025-04-16', NULL, 'Migraine');


GO

