from app import mysql, session
from blockchain import Block, Blockchain ,updatehash
from hashpdf import hashpdf
from CreateDiploma import CreateDiplomat
from ExtractCoordinates import Extract 


#custom exceptions for transaction errors
class InvalidTransactionException(Exception): pass
class InsufficientFundsException(Exception): pass

#what a mysql table looks like. Simplifies access to the database 'crypto'
class Table():
    #specify the table name and columns
    #EXAMPLE table:
    #               blockchain
    # number    hash    previous   data    nonce
    # -data-   -data-    -data-   -data-  -data-
    #
    #EXAMPLE initialization: ...Table("blockchain", "number", "hash", "previous", "data", "nonce")
    def __init__(self, table_name, *args):
        self.table = table_name
        self.columns = "(%s)" %",".join(args)
        self.columnsList = args

        #if table does not already exist, create it.
        if isnewtable(table_name):
            create_data = ""
            for column in self.columnsList:
                create_data += "%s varchar(100)," %column

            cur = mysql.connection.cursor() #create the table
            cur.execute("CREATE TABLE %s(%s)" %(self.table, create_data[:len(create_data)-1]))
            cur.close()

    #get all the values from the table
    def getall(self):
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s" %self.table)
        data = cur.fetchall(); return data

    #get one value from the table based on a column's data
    #EXAMPLE using blockchain: ...getone("hash","00003f73gh93...")
    def getone(self, search, value):
        data = {}; cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM %s WHERE %s = \"%s\"" %(self.table, search, value))
        if result > 0: data = cur.fetchone()
        cur.close(); return data

    #delete a value from the table based on column's data
    def deleteone(self, search, value):
        cur = mysql.connection.cursor()
        cur.execute("DELETE from %s where %s = \"%s\"" %(self.table, search, value))
        mysql.connection.commit(); cur.close()

    #delete all values from the table.
    def deleteall(self):
        self.drop() #remove table and recreate
        self.__init__(self.table, *self.columnsList)

    #remove table from mysql
    def drop(self):
        cur = mysql.connection.cursor()
        cur.execute("DROP TABLE %s" %self.table)
        cur.close()

    #insert values into the table
    def insert(self, *args):
        data = ""
        for arg in args: #convert data into string mysql format
            data += "\"%s\"," %(arg)

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO %s%s VALUES(%s)" %(self.table, self.columns, data[:len(data)-1]))
        mysql.connection.commit()
        cur.close()

#execute mysql code from python
def sql_raw(execution):
    cur = mysql.connection.cursor()
    cur.execute(execution)
    mysql.connection.commit()
    cur.close()

#check if table already exists
def isnewtable(tableName):
    cur = mysql.connection.cursor()

    try: #attempt to get data from table
        result = cur.execute("SELECT * from %s" %tableName)
        cur.close()
    except:
        return True
    else:
        return False

#check if user already exists
def isnewuser(username):
    #access the users table and get all values from column "username"
    users = Table("users", "name", "email", "username", "password","type")
    data = users.getall()
    usernames = [user.get('username') for user in data]

    return False if username in usernames else True

#check if etudiant already exists
def isnewstudent(mat):
    #access the students table and get all values from column "matricule"
    students = Table("students", "familyname", "lastname","matricule","email","date","place","major")
    data = students.getall()
    mats = [student.get('matricule') for student in data]

    return False if mat in mats else True

# create diplome and add new block to blockchain 
def add_diplome(university, student_mat,mention):
    
    #verify that the Student has already a diplome and block in the blockchain
    if get_diplome(student_mat) != '':
        raise InsufficientFundsException("Student has already a diploma and block in our BlockChain")
    
    #verify that the student exists
    elif isnewstudent(student_mat):
        raise InvalidTransactionException("Student Does Not Exist.")

    #get student information
    #access the students table and get  values  matricule = student_mat
    students = Table("students", "familyname", "lastname","matricule","email","date","place","major")
    student=students.getone('matricule',student_mat)
    student_data=[student.get('familyname'),student.get('lastname'),student_mat,student.get('date'),student.get('place'),student.get('major'),mention,university]
    CreateDiplomat(student_data)
    #update the blockchain and sync to mysql
    blockchain = get_blockchain()
    number = len(blockchain.chain) + 1
    data = "%s-->%s-->%s" %(university, student_mat, updatehash(student.get('familyname'),student.get('lastname'),student_mat,student.get('date'),student.get('place'),student.get('major'),mention,university))
    blockchain.mine(Block(number, data=data))
    sync_blockchain(blockchain)
    
#diplome_Verification

def diplome_Verification(diplome): 
    diplome_data = Extract(diplome)

    diplome_hash = updatehash(diplome_data[0],diplome_data[1],diplome_data[2],diplome_data[3],diplome_data[4],diplome_data[5],diplome_data[6],diplome_data[7])
    
    #verify that the Student has already a diplome and block in the blockchain
    if isnewstudent(diplome_data[2]):
        raise InvalidTransactionException("Student Does Not Exist.")
    elif get_diplome(diplome_data[2]) == '':
        raise InsufficientFundsException("Student has not  already a diploma and block in our BlockChain --> ADD Diploma ")
    
    #verify that the student exists
    elif isnewstudent(diplome_data[2]):
        raise InvalidTransactionException("Student Does Not Exist.")
    return False if diplome_hash != get_diplome(diplome_data[2]) else True
    
#get the diplome of a student
def get_diplome(mat):
    diplome = ''
    blockchain = get_blockchain()

    #loop through the blockchain and get diplome where matricule = mat
    for block in blockchain.chain:
        data = block.data.split("-->")
        if mat == data[1]:
            diplome = data[2]
            break
    return diplome

#get the blockchain from mysql and convert to Blockchain object
def get_blockchain():
    blockchain = Blockchain()
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    for b in blockchain_sql.getall():
        blockchain.add(Block(int(b.get('number')), b.get('previous'), b.get('data'), int(b.get('nonce'))))

    return blockchain

#update blockchain in mysql table
def sync_blockchain(blockchain):
    blockchain_sql = Table("blockchain", "number", "hash", "previous", "data", "nonce")
    blockchain_sql.deleteall()

    for block in blockchain.chain:
        blockchain_sql.insert(str(block.number), block.hash(), block.previous_hash, block.data, block.nonce)
