from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from datetime import datetime


app = Flask(__name__)
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tugasEai'
app.config['MYSQL_HOST'] = 'localhost'  

mysql = MySQL(app)


@app.route('/')
def root():
    return 'Selamat datang di Toserba'


@app.route('/users', methods=['GET', 'POST'])
def user():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users")
    

        column_name = [i[0] for i in cursor.description]


        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_name, row)))
        cursor.close()  
        return jsonify(data)
    
    elif request.method == 'POST':
        nama = request.json['nama']
        username = request.json['username']
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO users (nama,username) VALUES (%s,%s)"
        val = (nama, username)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data added success'})


@app.route('/detail_user',methods=['GET'])
def detail_user():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE id = %s "
        val = (request.args['id'],)
        cursor.execute(sql, val)

        column_name = [i[0] for i in cursor.description]


        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_name, row)))

        cursor.close()
        return jsonify(data)

@app.route('/deleteuser',methods=['DELETE'])
def delete_user():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM users WHERE id = %s "
        val = (request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data deleted success'})

@app.route('/updateuser',methods=['PUT'])
def edit_user():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE users SET nama = %s, username = %s WHERE id = %s "
        val = (data['nama'], data['username'], request.args['id'])
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data update success'})

if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=50,debug=True)