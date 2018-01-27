# ToyDBMS
It's a simple database management system with limited functionality. Run "ToyDBMS.py" and enjoy. Some sample queries are as follow:

#pars('CREATE employee (id INT,name STRING, division STRING)')
#pars('CREATE salary (id INT, salary INT)')
#pars('CREATE head (boss INT, division STRING)')
#pars('INSERT INTO employee (1, "Alicia", "Direction")')
#pars('INSERT INTO employee (2, "Bob", "Production")')
#pars('INSERT INTO salary ( 1, 100000)')
#pars('INSERT INTO salary (2, 95000)')
#pars('INSERT INTO head (2, "Production")')
#pars('SELECT * FROM employee, salary WHERE id = id')
#pars('SELECT * FROM employee, head WHERE id = boss')
#pars('SELECT name, division FROM employee')
#pars('INSERT INTO head (3, "Yaser")')
#print tables[DataDic[0][0]]
#pars('save')
#pars('SELECT * FROM employee WHERE id = 1')
