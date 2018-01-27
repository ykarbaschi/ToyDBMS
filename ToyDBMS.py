#First read the last file
import os.path
import pickle

global exit

DataDic=[]
tables={}

if not(os.path.exists('DataDic.pkl')):
	DDopen=open('DataDic.pkl','w')
	DDopen.close()
else:
	#check if last time saved or quit withoutsave
	if ((os.path.getsize('DataDic.pkl')) > 0):
		DDopen=open('DataDic.pkl')
		DataDic=pickle.load(DDopen)
			#just create table name with empty list to avoid making duplicate tables
		for i in range(len(DataDic)):
			if not(DataDic[i][0] in tables):# check for not to make duplicate table
				tables[DataDic[i][0]]=[]
		DDopen.close()
	else:
		print "Probably, Last time you didn't save your Database"
	


def createTable(DD,tables,tableName,attrib):
	fieldName=''
	fieldType=''
	for i in DD:
		if (i[0]==tableName):
			print "There is a table with the same name!"
			return
	for i in range(len(attrib)):
		fieldTemp=attrib[i].split()
		fieldType=fieldTemp[1]
		fieldName=fieldTemp[0]
		DD+=[[tableName,fieldName,fieldType,""]]

	if not(tableName in tables):
		tables[tableName]=[]
	return

def insertData(tables,tableName,fieldName,fieldValue):
	tables[tableName][len(tables[tableName])-1]\
		[fieldName]=fieldValue

#def selectData(tableName,fieldName,condition):

#	print 'this is select function'

#def showDataDic():
#	print 'this is show data dic'

def saveToFile():
	DDopen=open('DataDic.pkl','w')
	pickle.dump(DataDic,DDopen)
	DDopen.close()

	#print 'len data dic:'+ str(len(DataDic))
	#print 'len tables employee:'+ str(len(tables[DataDic[0][0]]))

	for i in range(len(DataDic)):
		if not(os.path.exists('tables_'+DataDic[i][0]+'.pkl')):
			fileCreate=open('tables_'+DataDic[i][0]+'.pkl','w')
			for j in range(len(tables[DataDic[i][0]])):
				pickle.dump(tables[DataDic[i][0]][j],fileCreate)
			fileCreate.close()
		else:# First read all of them to memory then write all of that
			#fileOpen= open('tables_'+DataDic[i][0]+'.pkl')
			with open('tables_'+DataDic[i][0]+'.pkl') as f:
				unpickled = []
				while True:
					try:
						unpickled.append(pickle.load(f))
					except EOFError:
						break
			for k in range(len(unpickled)):
				if not(unpickled[k] in tables[DataDic[i][0]]):
					tables[DataDic[i][0]].append(unpickled[k])
			#fileOpen.close()

			fileCreate=open('tables_'+DataDic[i][0]+'.pkl','w')
			for j in range(len(tables[DataDic[i][0]])):
				pickle.dump(tables[DataDic[i][0]][j],fileCreate)
			fileCreate.close()


def pars(command):

	if (command=='save'):
		saveToFile()
		global exit
		exit =1
		return

	sentence= command.split()
	
	if (sentence[0].upper() == 'CREATE'):
		#print 'create method'
		tableName= sentence[1]
		fields=""
		for i in range(2,len(sentence)):
			fields+=sentence[i]

		for char in fields:
			if char in '()':
				fields=fields.replace(char,'')
		fields = fields.replace('INT', ' INT');
		fields = fields.replace('STRING', ' STRING');

		attr = fields.split(',')
		createTable(DataDic,tables,tableName,attr)

	elif (sentence[0].upper() == 'INSERT'):
		#print 'insert method'
		if not(sentence[1].upper() == 'INTO'):
				print 'You missed INTO or mistyped it. Check for spaces!'
				return

		tableName = sentence[2]
		fields=""

		for i in range(3,len(sentence)):
			fields+=sentence[i]

		for char in fields:
			if char in '()':
				fields=fields.replace(char,'')

		attr = fields.split(',')
		tables[tableName]+=[{}]

		numAttr=0
		found=0
		for i in range(len(DataDic)):
			if DataDic[i][0] == tableName:
				insertData(tables,tableName,DataDic[i][1],attr[numAttr])
				numAttr+=1
				found=1
		if not found:
			print 'There is no table whit this name'
	
	elif (sentence[0].upper() == 'SELECT'):
		#print 'select method'
		tempSen=''
		if not(sentence[2].upper() == 'FROM'):
				print 'You missed FROM or mistyped it. Check for spaces!'
				return

		if (sentence[1] == '*'):

			for i in range(3,len(sentence)):
				tempSen+=sentence[i]
				#should show from table names to end
			try:
				tableNameTemp=tempSen[0:tempSen.upper().index('WHERE')]
				tableName=tableNameTemp.split(',')
			except:
				print 'You missed WHERE clause!'

			condTemp = tempSen[(tempSen.upper().index('WHERE')+5):]
			cond=condTemp.split('=')
			#should show just condiotns

			fieldName=cond[0]# if there was condition
			fieldValue=cond[1]

			if(len(tableName)==1):# it should be comparison in one table
				found=0
				for i in range(len(DataDic)):
					if ((DataDic[i][0] == tableName[0])and(DataDic[i][1]==fieldName)):
						with open('tables_'+DataDic[i][0]+'.pkl') as f:
							found=0;
							while True:
								try:
									unpickled=pickle.load(f)
									#compare if the value of the key is equal to cond[1]
									if unpickled[cond[0]]==cond[1]:
										print str(unpickled)+'\n'
										found=1
								except EOFError:
									if not(found):
										print 'There is no entry with this condition in the table'
									break
				if not found:
					print 'There is no table with this name or table does not have this field name'
						#for entry in tables[tableName]:
						#	if entry[cond[0]]==cond[1]:
						#		print entry+'\n'
			else:# comparison between two table and comparison between same field or diff field
				found=0
				for i in range(len(DataDic)):
					for j in range(i+1,len(DataDic)):	
						if (DataDic[i][0] == tableName[0])and(DataDic[j][0] == tableName[1]) \
						and(DataDic[i][1]==cond[0])and(DataDic[j][1]==cond[1]):
							found =1
							with open('tables_'+DataDic[i][0]+'.pkl') as firstTable:
								while True:
									try:
										unpickledFirst=pickle.load(firstTable)
										with open('tables_'+DataDic[j][0]+'.pkl') as SecondTable:
											found=0;
											while True:
												try:
													unpickledSecond=pickle.load(SecondTable)
										#compare if the value of the key is equal to cond[1]
													if unpickledFirst[cond[0]]==unpickledSecond[cond[1]]:
														print str(unpickledFirst)+'\n'+str(unpickledSecond)+'\n'
														found=1
												except EOFError:
													break
									except EOFError:
										if not(found):
											print 'There is no entry with this condition in the tables'
										break
				if not found:
					print 'one or none of the tables exist or one of the fileds missing from one table'
							#for entry1st in tables[tableName[0]]:
							#	for entry2nd in tables[tableName[1]]:
							#		if entry1st[cond[0]]==entry2nd[cond[1]]:
							#			print str(entry1st) + "\n"+ str(entry2nd)+ '\n'

		else:# this is the condition if dont use * after SELECT command
			tempSen=''
			for i in range(1,len(sentence)):
				tempSen+=sentence[i]
				#should show from filed names and From and Table Name
			try:
				fieldNameTemp=tempSen[0:tempSen.upper().index('FROM')]
				fieldName=fieldNameTemp.split(',')
			except:
				print 'You missed FROM clause!'
			# we should have name of fields in fieldName[0], fieldName[1]
			tableName=tempSen[(tempSen.upper().index('FROM')+4):]
			# it is the table name at end of command
			for i in range(len(DataDic)):
				if (DataDic[i][0] == tableName):
					with open('tables_'+DataDic[i][0]+'.pkl') as f:
						found=0
						while True:
							try:
								unpickled=pickle.load(f)
								print fieldName[0]+' '+str(unpickled[fieldName[0]])
								print fieldName[1]+' '+str(unpickled[fieldName[1]])
								found=1#there is at least one tuple
							except EOFError:
								if not found:
									print 'There is no entry in this table'
								break
					#for j in range(len(tables[tableName])):
					#	print fieldName[0]+' '+tables[tableName][j][fieldName[0]]
					#	print fieldName[1]+' '+tables[tableName][j][fieldName[1]]
	else:
		print 'It seems you didnt type SELECT or CREATE or INSERT at the first!'
	return


print 'Welcome to Toy Relational DBMS! \n \
To save all your work, type "save". Then the program will save and quit.'
exit=0
while not(exit):	
	command = raw_input ("What's next? \n")
	print '\n'
	pars(command)

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