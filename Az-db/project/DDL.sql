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
GO

