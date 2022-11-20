from flask import Flask, render_template, request,redirect,session
import os;from hashlib import md5;import datetime
import ibm_db;from smtp2go.core import Smtp2goClient

api_key = os.environ['api_key']
bassward = os.environ['bassward']

d = (
	"HOSTNAME=182.169.41.2;"
	"PORT=50000;"
	"UID=dbint4me;"
	f"PWD={bassward};"
	"DATABASE=gabshorn;"
	)

client = Smtp2goClient(api_key=api_key)
con = ibm_db.connect(d,"","")
ibm_db.exec_immediate(con,'DROP TABLE users IF EXISTS;')
ibm_db.exec_immediate(con,'DROP TABLE knab IF EXISTS;')

ibm_db.exec_immediate(con,
	"""CREATE TABLE IF NOT EXISTS users(
	userid INT GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1) PRIMARY KEY,
	email VARCHAR(60) UNIQUE NOT NULL,
	username VARCHAR(60) UNIQUE NOT NULL,
	password VARCHAR(35),
	fname VARCHAR(20),
	lname VARCHAR(20),
	accnum VARCHAR(19),
	cvv INTEGER,
	ed VARCHAR(20),
	esent BOOLEAN DEFAULT FALSE);""")

ibm_db.exec_immediate(con,
	"""CREATE TABLE IF NOT EXISTS knab(
	userid INT NOT NULL, FOREIGN KEY (userid) REFERENCES users(userid),
	dayte DATE NOT NULL,
	description VARCHAR(32) NOT NULL,
	type VARCHAR(7) NOT NULL,
	amount INT DEFAULT 0,
	timstmp TIMESTAMP NOT NULL
	);""")

ibm_db.exec_immediate(con,f"INSERT INTO users(email,username,password,fname,lname,accnum,cvv,ed)VALUES('a@a.com','admin','{md5(b'admin').digest().hex()}','Lucifer','Morningstar','1234-1234-1234-9999',123,'12-2022')")
ibm_db.exec_immediate(con,"""INSERT INTO knab(userid,dayte,description,type,amount,timstmp) VALUES
	(1,CURRENT_DATE,'one','expense','2000',CURRENT_TIMESTAMP),
	(1,CURRENT_DATE + 1 MONTH,'two','expense','208',CURRENT_TIMESTAMP),
	(1,CURRENT_DATE - 2 DAY,'two','expense','208',CURRENT_TIMESTAMP),
	(1,CURRENT_DATE - 3 DAY,'thr','expense','2070',CURRENT_TIMESTAMP),
	(1,CURRENT_DATE - 4 DAY,'fou','expense','2006',CURRENT_TIMESTAMP),
	(1,CURRENT_DATE - 5 DAY,'fiv','expense','5000',CURRENT_TIMESTAMP),
	(1,CURRENT_DATE - 6 DAY,'six','income','12005',CURRENT_TIMESTAMP)""")

app = Flask(__name__,template_folder="",static_folder="assets")
app.secret_key = os.urandom(32).hex()

alert = '''<script>alert("{}");</script><meta http-equiv="refresh" content="0;url='/{}'"/>'''

def get_uid():
	usrmail = session['namauwa']
	q = ibm_db.exec_immediate(con,f"SELECT userid FROM users WHERE email='{usrmail}' or username='{usrmail}'")
	return ibm_db.fetch_tuple(q)[0]

def get_day():
	tday = datetime.date.today()
	fday = datetime.date(tday.year, tday.month, 1)
	lday = datetime.date(tday.year, tday.month+1, 1) - datetime.timedelta(days=1)
	return fday,tday,lday

def last7days():
	b = datetime.date.today()
	fs = [str((b-datetime.timedelta(days=i)).day)+'/'+str((b-datetime.timedelta(days=i)).month) for i in range(7)][::-1]
	return str(fs).replace("'","&quot;")

def createtr(a,b,c,d):
	trclass = ['success' if i=='income' else "danger" for i in c]
	return [f"<tbody><tr class='text-{trclass[i]}'><td class='font-monospace'>{a[i]}</td><td class='font-monospace'>{b[i]}</td><td class='font-monospace'>{c[i]}</td><td class='font-monospace'>{d[i]}</td></tr></tbody>" for i in range(len(a))]

def ftabledata(tdata):
	l = len(tdata)
	tdatda = [];tdatde = [];tdatty = [];tdatam = []
	for i in range(l):
		tdatda.append(str(tdata[i][0].day) + "/" + str(tdata[i][0].month) + "/" + str(tdata[i][0].year))
		tdatde.append(tdata[i][1])
		tdatty.append(tdata[i][2])
		tdatam.append(tdata[i][3])		
	return tdatda,tdatde,tdatty,tdatam

def fetch_table(uid,l=500):
	q = ibm_db.exec_immediate(con,f"SELECT dayte,description,type,amount FROM knab where userid='{uid}' ORDER BY dayte DESC , timstmp DESC")
	tdata = []
	while (ibm_db.fetch_row(q) != False) and (len(tdata) != l):
		tdata.append([ibm_db.result(q,i) for i in range(4)])
	return "".join(createtr(*ftabledata(tdata)))

def fetch_tablebymonth(uid,select):
	q = ibm_db.exec_immediate(con,f"SELECT dayte,description,type,amount FROM knab where userid='{uid}' and MONTH(dayte) = '{select}' ORDER BY dayte DESC , timstmp DESC")
	tdata = []
	while (ibm_db.fetch_row(q) != False):
		tdata.append([ibm_db.result(q,i) for i in range(4)])
	return "".join(createtr(*ftabledata(tdata)))

def fetch_cash(uid,fday,lday):
	inc = ibm_db.exec_immediate(con,f"SELECT SUM(amount) FROM knab where userid='{uid}' and type='income' and dayte > '{fday}' and dayte <= '{lday}'")
	income = ibm_db.fetch_tuple(inc)[0]
	income = 0 if income == None else income
	exp = ibm_db.exec_immediate(con,f"SELECT SUM(amount) FROM knab where userid='{uid}' and type='expense' and dayte > '{fday}' and dayte <= '{lday}'")
	expense = ibm_db.fetch_tuple(exp)[0]
	expense = 0 if expense == None else expense
	return income,expense

def fetch_csv(uid,tday):
	csvi = []
	csve = []
	for idate in [str(tday-datetime.timedelta(days=i)) for i in range(7)][::-1]:
		q1 = ibm_db.exec_immediate(con,f"SELECT sum(amount) FROM knab where userid='{uid}' and type='income' and dayte = '{idate}'")
		tmp1 = ibm_db.fetch_tuple(q1)[0]
		q2 = ibm_db.exec_immediate(con,f"SELECT sum(amount) FROM knab where userid='{uid}' and type='expense' and dayte = '{idate}'")
		tmp2 = ibm_db.fetch_tuple(q2)[0]
		csvi.append(str(0 if tmp1 == None else tmp1))
		csve.append(str(0 if tmp2 == None else tmp2))
	return str(csvi).replace("'","&quot;"),str(csve).replace("'","&quot;")

def cash_freq(cho):
	if cho == "daily":
		return [i for i in range(7)],"day"
	elif cho == "weekly":
		return [7*i for i in range(4)],"day"
	elif cho == "monthly":
		return [i for i in range(12)],"month"
	else:
		return [0],"day"

def send_mail(select = 0,balance=0):
	if (select == 0):
		subject = "Registration Completed"
		html = f'<html><body><div style="text-align: center;"><h3>You&apos;ve successfully signed in into</h3><h3 style="color: green;">Un - dee</h3><h4>Manage all your expenses without breaking a leg.<br>Have a nice day ahead 💙.</h4><h5>Username : {username}</h5></div></body></html>'
		q = ibm_db.exec_immediate(con,f"SELECT email FROM users WHERE username='{username}'")
	else:
		subject = "Alert! Take care of expenses"
		html = f'<html><body><div style="text-align: center;"><h3 style="color: green;">Un - dee</h3><h4 style="color: orangered;">You&apos;ve have more expenses than your income, make sure to control it to keep it flowing. Plan your budget consciously.</h4><h5>Your current balance : ₹ {balance}<br>Have a wealthy life ahead 💰.</h5></div></body></html>'
		uid = get_uid()
		q = ibm_db.exec_immediate(con,f"SELECT email FROM users WHERE userid='{uid}'")
	eid = ibm_db.fetch_tuple(q)[0]
	payload = {
	"sender": "810019106006@smartinternz.com",
	"recipients" : [eid],
	"subject": subject,
	"text" : "Thanks for Signing in",
	"html" : html
	}
	response = client.send(**payload)
	return response._success()

def get_estat():
	uid = get_uid()
	q = ibm_db.exec_immediate(con,f"SELECT esent from users where userid='{uid}' ")
	estat = ibm_db.fetch_tuple(q)[0]
	return estat

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/aboutus")
def about():
	return render_template("aboutus.html")

@app.route("/login",methods=['GET','POST'])
def login():
	if request.method=="POST":
		usrmail = request.form['email'].lower()
		password = request.form['password']
		if (password=="" or usrmail==""):
			return alert.format("Please fill all the inputs.","login")
		else:
			q = ibm_db.exec_immediate(con,f"select count(*) from users where (email='{usrmail}' or username='{usrmail}') and password='{md5(password.encode()).digest().hex()}'")
			if(ibm_db.fetch_tuple(q)[0] == 1):
				session['kozakzipazapugazh'] = os.urandom(32).hex()+"sus"
				session['namauwa'] = usrmail
				return redirect("/dashboard")
			else:
				return alert.format("Wrong Credentials","login")
	return render_template("login.html")

@app.route("/signup",methods=['GET','POST'])
def signup():
	if request.method=="POST":
		global username
		email =  request.form['email'].lower()
		username = request.form['username'].lower()
		password =  request.form['password']
		if (password=="" or email=="" or username==""):
			return alert.format("Please fill all the inputs.","signup")
		else:
			q1 = f"SELECT COUNT(*) FROM users WHERE email='{email}' or username='{username}'"
			q = ibm_db.exec_immediate(con,q1)
			if(ibm_db.fetch_tuple(q)[0] == 1):
				return alert.format("Username or Email already registered","signup")
			else:
				q1 = f"INSERT INTO users(email,username,password) VALUES('{email}','{username}','{md5(password.encode()).digest().hex()}')"
				ibm_db.exec_immediate(con,q1)
				return redirect("/fillup")
	else:
		render_template("signup.html")
	return render_template("signup.html")

@app.route("/fillup",methods=['GET','POST'])
def fillup():
	if request.referrer != None:
		if request.method=="POST":
			fname = request.form['fn']
			lname = request.form['ln']
			accnum = request.form['acn']
			cvv = request.form['cvv']
			ed = request.form['ed']			
			if (fname == "" or lname == "" or accnum == "" or ed == "" or cvv == ""):
				return alert.format("Please fill all the inputs.","fillup")
			else:
				q4 = f"UPDATE users SET fname='{fname}',lname='{lname}',accnum='{accnum}',cvv='{cvv}',ed='{ed}' where username = '{username}'"
				ibm_db.exec_immediate(con,q4)
				sm = send_mail()
				if (sm):
					return alert.format(f"Registration Complete, Check your mail","login")
				else:
					return alert.format(f"Something went wrong, Can't send mail","login")
	else:
		return alert.format("Don't skip steps, signup and then fillup","signup")			
	return render_template("fillup.html")

@app.route("/dashboard",methods=['GET','POST'])
def dashboard():
	if request.method == "GET":
		try:
			alert.format(session['kozakzipazapugazh'],"")
			fday,tday,lday = get_day()
			uid = get_uid()
			q = ibm_db.exec_immediate(con,f"SELECT username,fname,lname,accnum,ed FROM users WHERE userid = '{uid}'")
			usr,fn,ln,acn,ed = ibm_db.fetch_tuple(q)
			ed = ed.split("-")
			income,expense = fetch_cash(uid,fday,lday)
			csvi,csve = fetch_csv(uid,tday)
			tbody = fetch_table(uid,10)
			sav = income-expense
			if (get_estat() == False) and (sav < 0):
				send_mail(1,sav)
				ibm_db.exec_immediate(con,f"UPDATE users SET esent = True where userid = '{uid}'")
			if (sav > 0):
				ibm_db.exec_immediate(con,f"UPDATE users SET esent = False where userid = '{uid}'")
			return render_template("nav.html",username=usr,acn=acn[-4:],em=ed[0],ey=ed[1][-2:],fn=fn,ln=ln,expense=expense,income=income,sav=sav,csvi=csvi,csve=csve,tbody=tbody,label=last7days())
		except:
			return redirect("404.html")
	else:
		cho = request.form['tcho']
		sel = request.form['tsel']
		cash = request.form['cash']
		descr = request.form['descr']
		uid = get_uid()
		trange,tstr = cash_freq(cho)
		for tint in trange:
			timedata = f"{tint} {tstr}"
			ibm_db.exec_immediate(con,f"INSERT INTO knab(userid,dayte,description,type,amount,timstmp) VALUES('{uid}',CURRENT_DATE + {timedata},'{descr}','{sel}','{cash}',CURRENT_TIMESTAMP + {timedata})")
		return redirect("/dashboard")

@app.route("/rst")
def rst():
	try:
		alert.format(session['kozakzipazapugazh'],"")
		uid = get_uid()
		ibm_db.exec_immediate(con,f"DELETE FROM knab WHERE userid = '{uid}' ")
		return redirect("/dashboard")
	except:
		return redirect("404.html")

@app.route("/transactions",methods=['GET','POST'])
def transactions():
	if(1):
		alert.format(session['kozakzipazapugazh'],"")
		if request.method == "POST":
			msel = request.form['msel']
			uid = get_uid()
			if ( msel == 'all'):			
				tbody = fetch_table(uid)
			else:
				tbody = fetch_tablebymonth(uid,msel)
			return render_template("history.html",tbody=tbody)
		else:
			uid = get_uid()
			tbody = fetch_table(uid)
			return render_template("history.html",tbody=tbody)
	else:
		return redirect("404.html")


@app.route("/clock")
def clock():
	try:
		alert.format(session['kozakzipazapugazh'],"")
		return render_template("clock.html")
	except:
		return redirect("404.html")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

@app.errorhandler(404)
def not_found(error404):
	return render_template("404.html")

app.run(port=81)