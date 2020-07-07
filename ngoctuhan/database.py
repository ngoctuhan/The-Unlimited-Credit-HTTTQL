import pyodbc 


class SQL_Server:

    def __init__(self):
        server = 'DESKTOP-P9HDQV8' 
        database = 'db_Credit_TheUnlimited' 
        username = 'sa' 
        password = '12101998' 
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        

    def insert(self, query):

        cursor = self.cnxn.cursor()
        cursor.execute(query)
        self.cnxn.commit()

    def select(self, query):
        cursor = self.cnxn.cursor()
        cursor.execute(query)

        data = []
        for row in cursor:
            data.append(row)
        return data

if __name__ == "__main__":

    query = 'SELECT * FROM dbo.ThanhVien'

    sql = SQL_Server()

    cusor = sql.select(query)

    for row in cusor:
        print(row)
