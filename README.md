# ToyDBMS
It's a simple database management system with limited functionality. Run "ToyDBMS.py" and enjoy. Some sample queries are as follow:

CREATE employee (id INT,name STRING, division STRING)<br>
CREATE salary (id INT, salary INT)<br>
CREATE head (boss INT, division STRING)<br>
INSERT INTO employee (1, "Alicia", "Direction")<br>
INSERT INTO employee (2, "Bob", "Production")<br>
INSERT INTO salary ( 1, 100000)<br>
INSERT INTO salary (2, 95000)<br>
INSERT INTO head (2, "Production")<br>
SELECT * FROM employee, salary WHERE id = id<br>
SELECT * FROM employee, head WHERE id = boss<br>
SELECT name, division FROM employee<br>
INSERT INTO head (3, "Yaser")<br>
SELECT * FROM employee WHERE id = 1
