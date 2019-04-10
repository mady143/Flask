from flask import Flask,flash, render_template,session, request,redirect,url_for
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def home():
   if  not session.get('logged_in'):
      return render_template('login.html')
   else:
      return render_template('home.html')



@app.route('/login',methods = ['POST','GET'])
def login():
   if request.method == 'POST':
      if request.form['username']=='admin' and request.form['password']=='password':
         session['logged_in'] = True
         return list()
      else:
         flash('wrong password')
         return home()


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    
    return home()
@app.route('/editpage')
def edit():
   return render_template('edit.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         fname   = request.form['fname']
         lname   = request.form['lname']
         email   = request.form['email']
         address = request.form['address']
         city    = request.form['city']
         pincode = request.form['pincode']
         
         with sql.connect("testing.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (firstname,lastname,email,address,city,pincode) VALUES (?,?,?,?,?,?)",(fname,lname,email,address,city,pincode) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("testing.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

@app.route('/edit_article/<string:id>',methods = ['POST', 'GET'])
def edit_article(id):
   print("hiiiii")
   #create cursor
   with sql.connect("testing.db") as con:
      c = con.cursor()

      result = c.execute("SELECT * from students WHERE id = ?",[id])
      rows = result.fetchone()

   if request.method == 'POST':
      try:
         fname   = request.form['fname']
         lname   = request.form['lname']
         email   = request.form['email']
         address = request.form['address']
         city    = request.form['city']
         pincode = request.form['pincode']
         
         with sql.connect("testing.db") as con:
            c = con.cursor()
            
            x =c.execute("UPDATE students SET firstname = ?,lastname = ?,email = ?,address = ?,city = ?,pincode = ? WHERE id = ?",(fname,lname,email,address,city,pincode,id))
            
            con.commit()
            flash('Record Updated successfully','success')
      except:
         con.rollback()
         flash('error in Update operation','success')
      
      finally:
         return redirect(url_for('list'))
         con.close()

@app.route("/delete_article/<string:id>",methods = ['POST'])
def delete_article(id):
   if request.method == 'POST':
      try:
         with sql.connect("testing.db") as con:
            c = con.cursor()

            c.execute("DELETE FROM students WHERE id = ?",[id])

            con.commit()

            flash('You were successfully Deleted')

      except:
         con.rollback()
         flash('Record Delet Fail','success')
      finally:
            return redirect(url_for('list'))
            con.close()


if __name__ == '__main__':
   app.run(debug = True)