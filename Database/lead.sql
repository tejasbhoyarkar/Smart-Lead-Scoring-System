CREATE DATABASE lead_scoring_db;
USE lead_scoring_db;


SELECT * FROM lead_data LIMIT 10;


DESCRIBE leads;
ALTER TABLE lead_data
CHANGE `Traffic Source` traffic_source VARCHAR(50);

SELECT * FROM lead_data;

SELECT * FROM lead_data ORDER BY Name DESC LIMIT 5;


SELECT * FROM lead_data WHERE name = 'John';



SELECT * FROM lead_data ORDER BY id DESC LIMIT 5;
SELECT * FROM lead_data WHERE name = 'Sara';

DELETE FROM lead_data
WHERE name = 'Sara'
LIMIT 2;

SELECT * FROM lead_data ORDER BY name;

SELECT * FROM lead_data ORDER BY id DESC;

ALTER TABLE lead_data
ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY;
SELECT * FROM lead_data ORDER BY id DESC;
select * from lead_data;

DELETE FROM lead_data
WHERE name = 'John'
LIMIT 1;

DELETE FROM lead_data
WHERE name = 'Sara'
LIMIT 2;



DROP TRIGGER IF EXISTS after_lead_insert;
DROP TRIGGER IF EXISTS after_lead_update;
DROP TABLE IF EXISTS lead_logs;

CREATE TABLE lead_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    lead_id INT,
    action_type VARCHAR(50),
    old_score INT,
    new_score INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


DELIMITER $$

CREATE TRIGGER after_lead_insert
AFTER INSERT ON lead_data
FOR EACH ROW
BEGIN
    INSERT INTO lead_logs (lead_id, action_type, new_score)
    VALUES (NEW.id, 'INSERT', NEW.Converted);
END $$

DELIMITER ;


DELIMITER $$

CREATE TRIGGER after_lead_update
AFTER UPDATE ON lead_data
FOR EACH ROW
BEGIN
    INSERT INTO lead_logs (lead_id, action_type, old_score, new_score)
    VALUES (OLD.id, 'UPDATE', OLD.Converted, NEW.Converted);
END $$

DELIMITER ;

UPDATE lead_data
SET Converted = 1
WHERE id = 101;

SELECT * FROM lead_logs;


USE lead_scoring_db;

SELECT * FROM lead_data;

DESCRIBE lead_data;

SELECT COUNT(*) FROM lead_data;

SHOW TABLES;