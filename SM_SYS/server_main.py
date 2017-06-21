import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json

#creates a WSGI complient flask web app
Web_App = Flask(__name__)


#=================================Database Section=============================
#configures db
Web_App.config.update(dict(
	DATABASE=os.path.join(Web_App.root_path, 'SM_SYS.db'),
	SECRET_KEY='dev key',
	USERS = {"admin":"password"}
))

def connect_db():
	db = sqlite3.connect(Web_App.config["DATABASE"])
	db.row_factory = sqlite3.Row
	return db

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db

@Web_App.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

def init_db():
	db = get_db()
	with Web_App.open_resource('db.sql', mode='r') as fin:
		db.cursor().executescript(fin.read())
	db.commit()
	
@Web_App.cli.command('initdb')
def initdb_command():
	init_db()
	print('Database initialized.')

#==============================================================================

#==================================Web Model================================

#The index page serves as the "landing zone" for all initial web traffic.
#It handels the login
@Web_App.route('/', methods=['GET', 'POST'])
def index():
	error = None
	return render_template('index.html', error=error)

#this implements the login from the server side: fetches user profile from DB, validates input and logs user in/out
@Web_App.route('/login', methods=['GET', 'POST'])
def login():
	if(request.method == 'POST'):
		#get input
		user = request.json
		response = None
		#load user profile from DB
		#=====================INSERT DB METHOD===================
		#========================================================
		#Validate
		if(user['ID']=='admin' and user['pass']!=''):
			session['logged_in'] = True
			session['is_man'] = True
			response = Web_App.response_class(json.dumps({"logged_in":session['logged_in'], "is_man":session['is_man']}), content_type='application/json')
		else:
			response = Web_App.response_class(json.dumps({"logged_in":False}), content_type='application/json')
	else:
		session.pop('logged_in', None)
		response = Web_App.response_class(json.dumps(True), content_type='application/json')
	return response

#this view allows the user to interct with the stored system data -system-wide operations are supported here
@Web_App.route('/systems/<method>', methods=['GET', 'POST', 'DELETE'])
def systems(method):
	response = None
	logged_in = False;
	is_man = False;

	try:
		#STEP-1: See if the user is logged in
		logged_in = session['logged_in']
		is_man = session['is_man']
		
		#STEP-2: users requests are sorted by rest-call
		if(request.method == 'GET'):
			#if request is get, fetch system information for logged in user
			if(method=='all'):
				#if method is all, return a list of the current systems on the platform
				#===========REPLACE WITH DB======================
				systems = ['def_sys_1', 'def_sys_2', 'def_sys_3']
				#================================================
			elif(method=='selected'):
				#if method is selected, return a dictionary containing the data of the selected system
				sys_id = request.args.get('id')
				#================REPLACE WITH DB====================
				systems = {"name": sys_id, "num_features": 12, "cust_id": "Massive Dynamic", "status": "In Development", "disc": "This is where a discription of the softwaresystem would go."}
				#===================================================
			else:
				raise Exception("Method_Error")
			response = Web_App.response_class(json.dumps(systems), content_type='application/json')
	except:
		response = Web_App.response_class(json.dumps(False), content_type='application/json')

	return response

if __name__ == '__main__':
	Web_App.run()