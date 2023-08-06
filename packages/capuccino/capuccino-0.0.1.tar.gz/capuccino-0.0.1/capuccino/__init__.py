import pyodbc
from pandas import read_csv

class SQLReturn:
    def __init__(self, columns, rowData, callback, father = None):
        # initialize seting default values to manipulate
        self.rowCount = 0
        self.columns = columns
        self.rowData = rowData
        self.callback = callback
        self.isRunning = False
        self.father = father

    def ReturnData(self):
        # verify if nothing is running
        if not self.isRunning:
            self.isRunning = True
            if len(self.rowData) > 0:
                for i in range(len(self.rowData)):
                    # get the number of the counter
                    self.rowCount = i
                    # if there is a function, i run
                    if self.callback:
                        self.callback(self.father, self)

    def getDataByName(self, name):
        index = -1
        for idx, column in enumerate(self.columns):
            if column == name:
                index = idx
                break
        if index == -1:
            print('This field does not exist.')
        else:
            return self.rowData[self.rowCount][index]

class SQL:
    def __init__(self, server, database, username, password, driver = '{ODBC Driver 17 for SQL Server}', father = None):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.trustedConnection = ';UID=' + username + ';'r'PWD=' + password if self.username and self.password is not None else ';Trusted_Connection=yes;'
        print(self.trustedConnection)
        self.SQLConnection = pyodbc.connect(
            r'DRIVER=' + driver + ';'
            r'SERVER=' + server + ';'
            r'DATABASE=' + database + '{}'.format(self.trustedConnection)
        )
        self.cursor = self.SQLConnection.cursor()
        self.father = father 

    def RunQuery(self, query, callback = None):
        try:
            self.rowData = []
            self.cursor.execute(query)

            if self.cursor.description is not None and len(self.cursor.description) > 0:
                # get the cols and rows of the query
                self.columns = [column[0] for column in self.cursor.description]
                self.rowData = list(self.cursor)
                

                # pass the values of the query
                QueryResult = SQLReturn(self.columns, self.rowData, callback, self.father)
                QueryResult.ReturnData()

            self.SQLConnection.commit()
            pass
        except:
            print('An error occurred in the query: "' + query + '"')
            pass


class Data:
    @staticmethod
    def extractCSV(filename, sep = ','):
        data = read_csv(filename, sep=sep)
        return data.values

class Table:
    class Field:
        def __init__(self, name, dataType, key = '', specification = '', required = False, data = None):
            self.name = name
            self.data = data
            self.dataType = dataType
            self.required = required
            self.key = key
            self.specification = specification

        def setData(self, data):
            self.data = data


    def __init__(self, name, fields = [], conn = None):
        self.conn = conn
        self.name = name
        self.fields = fields

    def setConnection(self, conn):
        self.conn = conn

    def setFields(self, fields):
        self.fields = fields

    def insertInto(self, data):
        if self.conn is not None:
            query = """
                insert into """ + self.name + """ 
            """
            for row in range(len(data)):
                query += ' select '
                for col in range(len(data[row])):
                    final =  ', ' if col < len(data[row])-1 else ''
                    query += "'" + str(data[row][col]) + "'" + final
                
                if row < len(data)-1:
                    query += ' union all '

            self.conn.RunQuery(query)
        else:
            print('Please, set a connection')


    def deleteWhere(self, stringKey = '', value = '', customSyntax = '', operator = '='):
        if self.conn is not None:
            query = ''
            
            if customSyntax <> '':
                query = """
                    delete from """ + self.name + """
                    where """ + customSyntax
            
            else:
                query = """
                    delete from """ + self.name + """
                    where 
                        """ + stringKey + """ """ + operator + """ '""" + value + """'
                    """

            self.conn.RunQuery(query)
        else:
            print('Please, set a connection')
            

    def create(self):
        if self.conn is not None:
            query = """
                if not exists (select * from sysobjects where name='""" + self.name + """' and xtype='U')
                    create table """ + self.name + """ (
            """

            for index, field in enumerate(self.fields):
                required = ' not null ' if field.required == True else ' '
                final =  ',' if index < len(self.fields)-1 else ''
                tempString = field.name + ' ' + field.dataType + required + field.key + ' ' + field.specification + final
                query += tempString

            query += " )"

            self.conn.RunQuery(query)
        else:
            print('Please, set a connection')