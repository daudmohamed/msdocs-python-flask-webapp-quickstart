from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pyodbc

app = Flask(__name__)
server = 'daud.database.windows.net'
database = 'daud'
username = 'adminuser'
password = '{Admin123}'   
driver= '{ODBC Driver 17 for SQL Server}'

@app.route('/sql')
def sql():  # put application's code here
    string = ""
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            row = cursor.fetchone()
            while row:
                string += str(row[0]) + " " + str(row[1])
                row = cursor.fetchone()
    return string

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()