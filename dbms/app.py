from flask import Flask, render_template, redirect, request, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'pharmacy_project'

# MySQL Database Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '777111'  # Replace with your MySQL password
app.config['MYSQL_DB'] = 'pharmacy_db'  # Your pharmacy database name
mysql = MySQL(app)

# Route to render the home page
@app.route('/')
def index():
    return render_template('index.htm')

# Route to display all available medicines
@app.route('/medicines')
def medicines():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medicines")  # Query to fetch all medicines
    medicines_info = cur.fetchall()
    cur.close()
    return render_template('medicines.htm', medicines=medicines_info)

# Route to search medicines by ID or Name
@app.route('/search', methods=['POST', 'GET'])
def search():
    search_results = []
    if request.method == "POST":
        search_term = request.form['search_term']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM medicines WHERE med_id LIKE %s OR med_name LIKE %s"
        cur.execute(query, ('%' + search_term + '%', '%' + search_term + '%'))
        search_results = cur.fetchall()  # Fetch all matching results
        cur.close()
        return render_template('medicines.htm', medicines=search_results)

# Route to insert a new medicine
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        med_id = request.form['med_id']
        med_name = request.form['med_name']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicines (med_id, med_name, price, stock_quantity) VALUES (%s, %s, %s, %s)",
                    (med_id, med_name, price, stock_quantity))
        mysql.connection.commit()
        cur.close()
        flash("Medicine added successfully!", "success")
        return redirect(url_for('medicines'))
    return render_template('insert_medicine.htm')

# Route to delete a medicine
@app.route('/delete/<string:med_id>', methods=['GET'])
def delete(med_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM medicines WHERE med_id=%s", (med_id,))
    mysql.connection.commit()
    cur.close()
    flash("Medicine deleted successfully!", "success")
    return redirect(url_for('medicines'))

# Route to edit medicine details (Display the Edit Form)
@app.route('/edit/<string:med_id>', methods=['GET'])
def edit(med_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medicines WHERE med_id=%s", (med_id,))
    medicine = cur.fetchone()  # Fetch the medicine details to edit
    cur.close()
    return render_template('edit_medicine.htm', medicine=medicine)

# Route to handle the update of medicine details
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        med_id = request.form['med_id']
        med_name = request.form['med_name']
        price = request.form['price']
        stock_quantity = request.form['stock_quantity']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE medicines SET med_name=%s, price=%s, stock_quantity=%s WHERE med_id=%s",
                    (med_name, price, stock_quantity, med_id))
        mysql.connection.commit()
        cur.close()
        flash("Medicine updated successfully!", "success")
        return redirect(url_for('medicines'))

if __name__ == "__main__":
    app.run(debug=True)
