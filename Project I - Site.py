from flask import Flask, render_template, redirect, request, session, flash
import os

app = Flask(__name__)
app.secret_key = '123456789'

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    # get info from form
    import model.pwdhash as pwdhash
    from model.DbConnection import DbConnection
    db = DbConnection("P1_Database")

    #if form got send
    if request.method == 'POST':
        # get data from form and save in variable
        email = request.form['email']
        password = request.form['password']
        # check whether data was correct
        loggedIn = pwdhash.verify_credentials(email, password)
        # if data was correct
        if(loggedIn == True):
            session["user"] = db.getDataFrom_TableUser_ColumnEmail_ConditionEmail(email)[0]
            session["login"] = True
        # if data was wrong
        else:
            return render_template("login.html", info="Something went wrong, please try again")

    # if user was already logged in
    if(session.get("login") == True):
        return render_template('account.html', firstname=session["user"]["FirstName"])

    #if user just got registered
    if(session.get("registered") == True):
        session["registered"] = None
        return render_template("login.html", info="Registration was successful!")

    # if nothing special happened
    else:
        return render_template("login.html", info="")

@app.route('/register', methods=['GET', 'POST'])
def register():
    import model.pwdhash as pwdhash
    # if form got send
    if (request.method == 'POST'):
        # get data from form
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        # add user to database
        pwdhash.add_user(firstname, lastname, email, password)
        # save cookie for login-page
        session["registered"] = True
        return redirect('/login')
    # if nothing special happened
    return render_template("register.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # if log-out button on Aaccount" page got clicked, clear cookies
    if(request.method == 'POST'):
        session.clear()
    return redirect('/')

@app.route('/bookshelf')
def bookshelf():
    from model.DbConnection import DbConnection
    import model.GenerateGraph as graph
    db = DbConnection("P1_Database")
    books = db.getDataFrom_TableBook()
    places = db.getDataFrom_TablePlace()
    graph.createGraph(books)
    return render_template('bookshelf.html', books=books, places=places)

@app.route('/book/<isbn>')
def book(isbn):
    from model.DbConnection import DbConnection
    db = DbConnection("P1_Database")
    book = db.getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(isbn)[0]
    place = db.getDataFrom_TablePlace_ColumnPlaceID_ConditionBook(book["ISBN13"])
    return render_template('book.html', book=book, place=place, buttonLink="#")

@app.route('/borrowedBooks')
def borrowedBooks():
    from model.DbConnection import DbConnection
    db = DbConnection("P1_Database")
    borrowedBooks_string = session["user"]["BorrowedBooks"]
    #if borrowed books are not empty
    if(borrowedBooks_string != None):
        # split string into list
        borrowedBooks_list = borrowedBooks_string.split("-")
        borrowedBooks = []
        # if user has borrowed books before, a "-" could be in front so here it gets taken care of
        if(borrowedBooks_list[0] == ""):
            for borrowedBook in borrowedBooks_list[1:]:
                borrowedBooks.append(db.getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(borrowedBook))
        else:
            for borrowedBook in borrowedBooks_list:
                borrowedBooks.append(db.getDataFrom_TableBook_ColumnISBN13_ConditionForISBN13(borrowedBook))
        return render_template('borrowedBooks.html', borrowedBooks=borrowedBooks)
    else:
        return render_template('borrowedBooks.html', borrowedBooks="empty")

@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    from model.DbConnection import DbConnection
    db = DbConnection("P1_Database")
    # if button on "Info" page got clicked
    if request.method == 'POST':
        # get data from form
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # add data to database
        db.addRow_TableContact(name, email, message)
    # if nothing special happened
    return render_template('info.html')

# run server
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    host="0.0.0.0"
    app.run(host=host, port=port, debug=True)

