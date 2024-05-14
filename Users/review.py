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


@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM reviews")
    

        column_name = [i[0] for i in cursor.description]


        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_name, row)))
        cursor.close()  
        return jsonify(data)
    
    elif request.method == 'POST':
        nama_product = request.json['nama_product']
        review_product = request.json['review_product']
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO reviews (nama_product, review_product) VALUES (%s,%s)"
        val = (nama_product,  review_product)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data added success'})


@app.route('/detail_review',methods=['GET'])
def detail_review():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM reviews WHERE id = %s "
        val = (request.args['id'],)
        cursor.execute(sql, val)

        column_name = [i[0] for i in cursor.description]


        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_name, row)))

        cursor.close()
        return jsonify(data)

@app.route('/deletereview',methods=['DELETE'])
def delete_review():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM reviews WHERE id = %s "
        val = (request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data deleted success'})

@app.route('/updatereview',methods=['PUT'])
def edit_review():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE reviews SET nama_product = %s, review_product = %s WHERE id = %s "
        val = (data['nama_product'], data['review_product'], request.args['id'])
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data update success'})

if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=52,debug=True)