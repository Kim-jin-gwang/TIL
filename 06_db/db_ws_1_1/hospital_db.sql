


CREATE TABLE patients(
    patient_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    birthday DATE NOT NULL,
    phone_number VARCHAR(15),
    email VARCHAR(50) UNIQUE,
    address VARCHAR(200)
);

ALTER TABLE patients
ADD COLUMN gender VARCHAR(10);

ALTER TABLE patients
MODIFY COLUMN phone_number VARCHAR(20);

TRUNCATE TABLE patients;