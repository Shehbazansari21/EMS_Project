import pymysql
from flask import Flask,render_template,redirect,request
app=Flask(__name__)
@app.route('/')
def index():
    return render_template('ems_pro_01_insert.html')
@app.route('/insertrecord',methods=['POST'])
def insert():
    empid=int(request.form['Employee_ID'])
    name=request.form['Name']
    mno=request.form['Mobile_No']
    email=request.form['Email_id']
    gender=request.form['Gender']
    city=request.form['City']
    state=request.form['State']
    dep=request.form['Department']
    #now we creat connection
    try:
        conn=pymysql.connect(host='localhost',user='root',
                             password='',db='employee_managment_system01')
    except Exception as e:
        msg="Connection Error"
    else:
        msg="Connection Create Successfully"
        
    #now we create insert query
    query="INSERT into ems_project values(%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(empid,name,mno,email,gender,city,state,dep)
    #will create cursor for run the sql query
    cur=conn.cursor()
    #now will call the object of cursor
    try:
        cur.execute(query,val)
    except Exception as e:
        msg="Query Error"
    else:
        msg="Record insert successfully"
        conn.commit()
        conn.close()
    return render_template('result.html',msg=msg)
    
#to show record:
@app.route('/showrecord')
def show():
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',
                       db='employee_managment_system01')
    except Exception as e:
        msg='Connection Error'
    else:
        msg='Connection created successfully'

    # to fire query:
    query="select * from ems_project"
    cur=conn.cursor()
    try:
        cur.execute(query)
    except Exception as e:
        msg="Query failed"
    else:
        result=cur.fetchall()
        conn.commit()
        conn.close()
    return render_template("ems_pro_01_show.html",result=result)

# to update record:
@app.route('/update/<int:Employee_ID>')
def update(Employee_ID):
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',
                       db='employee_managment_system01')
    except Exception as e:
        msg='not connected'
    else:
        msg='Connection created successfully'
        
    cur = conn.cursor()
    query="select * from ems_project where Employee_ID=%s"
    cur.execute(query,Employee_ID)
    result=cur.fetchall()
    conn.commit()
    conn.close()
    if result: # condition true
        return render_template("ems_pro_01_update.html",result=result)
    else:
        msg="Record Not found"
        return render_template("result.html",msg=msg)

@app.route('/updaterecord', methods=['POST'])
def updaterecord():
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',
                       db='employee_managment_system01')
    except Exception as e:
        msg='not connected'
    else:
        msg='Connection successful'
    msg = ''
    if request.method == "POST":
        data = request.form
        empid = data["Employee_ID"]
        name = data["Name"]
        mno = data["Mobile_no"]
        email = data["Email_id"]
        gender = data["Gender"]
        city = data["City"]
        state = data["State"]
        dep = data["Department"]
        t=(name,mno,email,gender,city,state,dep,empid)
        cur=conn.cursor()
        query = "update ems_project set Name=%s,Mobile_no=%s,Email_id=%s,Gender=%s,City=%s,State=%s,Department=%s where Employee_ID=%s"
        cur.execute(query,t)
        conn.commit()
        msg = "Employee Record Updated !"
        return redirect('/showrecord')
    return render_template('ems_pro_01_update.html')

# to delete record
@app.route('/delete/<int:Employee_ID>')
def delete(Employee_ID):
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',
                       db='employee_managment_system01')
    except Exception as e:
        msg='not connected'
    else:
        msg='Connection successfull'

    cur=conn.cursor()
    query="delete from ems_project where Employee_ID=%s"
    cur.execute(query,Employee_ID)
    conn.commit()
    conn.close()
    return redirect('/showrecord')


# to search record:
@app.route('/search/<int:Employee_ID>')
def search(Employee_ID):
    try:
        conn=pymysql.connect(host='localhost',user='root',password='',
                       db='employee_managment_system01')
    except Exception as e:
        msg='not connected'
    else:
        msg='Connection successfull'
    
    cur=conn.cursor()
    query="select * from ems_project where Employee_ID=%s"
    cur.execute(query,Employee_ID)
    result=cur.fetchall()
    conn.commit()
    conn.close()
    if result: # condition true
        return render_template("ems_pro_01_search.html",result=result)
    else:
        msg="Record not found"
        return redirect('/showrecord')
    return render_template("result.html",msg=msg)



#main program
app.run(debug=True,use_reloader=False)
