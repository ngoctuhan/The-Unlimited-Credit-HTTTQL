import pyodbc 


class SQL_Server:

    def __init__(self):
        server = "DESKTOP-UMNF1BJ\MSSQLSERVER02" 
        database = 'TheUnlimited' 
        username = 'sa' 
        password = '123' 
        self.cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        

    def insert(self, query):

        cursor = self.cnxn.cursor()
        cursor.execute(query)
        self.cnxn.commit()

    def select(self, query):
        cursor = self.cnxn.cursor()
        cursor.execute(query)
        data = [i for i in cursor]
        return data
if __name__ == '__main__':

    # query = "INSERT INTO db_TheUnlimited.dbo.HoTen (Ho, Dem, Ten) VALUES ('Le','Nguyen','Ngoc Viet')"
    sql = SQL_Server()

    # sql.insert(query)
    query = "SELECT * FROM TheUnlimited.dbo.HopDongTraGop"
    tmp = sql.select(query)
    for row in tmp:
        print(row)