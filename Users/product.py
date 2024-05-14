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


@app.route('/product', methods=['GET', 'POST'])
def product():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM products")
    

        column_name = [i[0] for i in cursor.description]


        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_name, row)))
        cursor.close()  
        return jsonify(data)
    
    elif request.method == 'POST':
        nama_product = request.json['nama_product']
        deskripsi_product = request.json['deskripsi_product']
        price_product = request.json['price_product']
        cursor = mysql.connection.cursor()
        sql = "INSERT INTO products (nama_product, deskripsi_product, price_product) VALUES (%s,%s,%s)"
        val = (nama_product,  deskripsi_product,price_product)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data added success'})


@app.route('/detail_product',methods=['GET'])
def detail_product():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "SELECT * FROM products WHERE id = %s "
        val = (request.args['id'],)
        cursor.execute(sql, val)

        column_name = [i[0] for i in cursor.description]


        data = []
        for row in cursor.fetchall():
            data.append(dict(zip(column_name, row)))

        cursor.close()
        return jsonify(data)

@app.route('/deleteproduct',methods=['DELETE'])
def delete_product():
    if 'id' in request.args:
        cursor = mysql.connection.cursor()
        sql = "DELETE FROM products WHERE id = %s "
        val = (request.args['id'],)
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data deleted success'})

@app.route('/updateproduct',methods=['PUT'])
def edit_product():
    if 'id' in request.args:
        data = request.get_json()

        cursor = mysql.connection.cursor()
        sql = "UPDATE products SET nama_product = %s, deskripsi_product = %s, price_product = %s WHERE id = %s "
        val = (data['nama_product'], data['deskripsi_product'],data['price_product'], request.args['id'])
        cursor.execute(sql, val)

        mysql.connection.commit()
        cursor.close()
        return jsonify({'message' : 'data update success'})

if __name__ ==  '__main__':
    app.run(host='0.0.0.0', port=51,debug=True)