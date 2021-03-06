
class DbConnection:
    def __init__(self, database):
        from mysql import connector
        self.__dsn = {
            "host": "localhost",
            "user": "flaskuser",
            "passwd": "flaskpassword",
            "db": database,
        }
        self.__connection = connector.connect(**self.__dsn)

    # for reading
    def query(self, query: str, data: dict = None, dictionary=False):
        cursor = self.__connection.cursor(dictionary=dictionary)
        cursor.execute(query, data)
        result = cursor.fetchall()
        cursor.close()
        return result

    # for writing
    def execute(self, query: str, data: dict = None):
        cursor = self.__connection.cursor()
        cursor.execute(query, data)
        result = cursor.lastrowid
        self.__connection.commit()
        cursor.close()
        return result

    # get data from tables
    def getDataFrom_TableBook(self):
        #get all data from table
        sqlQuery = "SELECT * FROM Book"
        result = self.query(sqlQuery, dictionary=True)
        return result

    # get data from database with condition
    def getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(self, condition):
        # receive data only when condition is fulfilled

        sqlQuery = "SELECT * FROM Book WHERE ISBN13 = %(param1)s"
        sqlData = {"param1": condition}

        result = self.query(sqlQuery, sqlData, dictionary=True)

        return result

    def getDataFrom_TableUser_ColumnUserID_ConditionForUSerID(self, condition):
        # receive data only when condition is fulfilled

        sqlQuery = "SELECT * FROM User WHERE UserID = %(param1)s"
        sqlData = {"param1": condition}

        result = self.query(sqlQuery, sqlData, dictionary=True)

        return result

    def getDataFrom_TableUser_ColumnEmail_ConditionEmail(self, condition):
        # receive data only when condition is fulfilled

        sqlQuery = "SELECT * FROM User WHERE Email = %(param1)s"
        sqlData = {"param1": condition}

        result = self.query(sqlQuery, sqlData, dictionary=True)

        return result

    def getDataFrom_TablePlace(self):
        # receive data only when condition is fulfilled

        sqlQuery = "SELECT * FROM Place"

        result = self.query(sqlQuery, dictionary=True)

        return result

    def getDataFrom_TablePlace_ColumnPlaceID_ConditionBook(self, condition):
        # receive data only when condition is fulfilled

        sqlQuery = "SELECT * FROM Place WHERE Book = %(param1)s"
        sqlData = {"param1": condition}

        result = self.query(sqlQuery, sqlData, dictionary=True)

        return result

    # update tables
    def addValue_TableBook_ColumnBorrowedAmount_ConditionForISBN13(self, updatevalue, conditionvalue):
        # updatevalue = new value to replace old one
        # conditionvalue = value of condition
        sqlQuery = "UPDATE Book SET BorrowedAmount = %(param1)s WHERE ISBN13 = %(param2)s"
        sqlData = {'param1': updatevalue,
                   'param2': conditionvalue}

        self.execute(sqlQuery, sqlData)

    def addValue_TablePlace_ColumnBook_ConditionForBook(self, updatevalue, conditionvalue):
        # updatevalue = new value to replace old one
        # conditionvalue = value of condition
        sqlQuery = "UPDATE Place SET Book = %(param1)s WHERE Book = %(param2)s"
        sqlData = {'param1': updatevalue,
                   'param2': conditionvalue}

        self.execute(sqlQuery, sqlData)

    def addValue_TablePlace_ColumnBook_ConditionForPlaceID(self, updatevalue, conditionvalue):
        # updatevalue = new value to replace old one
        # conditionvalue = value of condition
        sqlQuery = "UPDATE Place SET Book = %(param1)s WHERE PlaceID = %(param2)s"
        sqlData = {'param1': updatevalue,
                   'param2': conditionvalue}

        self.execute(sqlQuery, sqlData)

    def addValue_TableUser_ColumnBorrowedBooks_ConditionForUserID(self, updatevalue, conditionvalue):
        # updatevalue = new value to replace old one
        # conditionvalue = value of condition
        sqlQuery = "UPDATE User SET BorrowedBooks = %(param1)s WHERE UserID = %(param2)s"
        sqlData = {'param1': updatevalue,
                   'param2': conditionvalue}

        self.execute(sqlQuery, sqlData)

    def addRow_TableContact(self, name, email, message):
        sqlQuery = "INSERT INTO Contact (Name, Email, Message) VALUES (%(param1)s, %(param2)s, %(param3)s)"
        sqlData = {'param1': name,
                   'param2': email,
                   'param3': message
                  }

        self.execute(sqlQuery, sqlData)

