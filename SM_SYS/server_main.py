#----------------------------------IMPORTS--------------------------------------
import argparse, pprint
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, json
from flask_sqlalchemy import SQLAlchemy
from database.DB import ServerDB
#creates a WSGI complient flask web app
#----------------------------------GLOBALS--------------------------------------
Web_App = Flask(__name__)
database = None

#----------------------------------PARSE ARGUMENTS------------------------------
def parse_args():
	disc = "This is the server script for the Software Management System."
	parser = argparse.ArgumentParser(description=disc)
	
	hint = "The install option: enter it to install the server. Usage -install <run|install>. The default is <run>"
	parser.add_argument('-install', default="run", help=hint)
	
	hint = "Use this argument to serve over the internet. Usage server_main.py -inet <inet|local>. The default is <local>."
	parser.add_argument('-inet', default="local", help=hint)
	
	
	args = parser.parse_args()
	return vars(args)

#==================================Web Section================================

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
			print(user['pass'])
			response = Web_App.response_class(json.dumps({"logged_in":session['logged_in'], "is_man":session['is_man']}), content_type='application/json')
		else:
			response = Web_App.response_class(json.dumps({"logged_in":False}), content_type='application/json')
	else:
		session.pop('logged_in', None)
		response = Web_App.response_class(json.dumps(True), content_type='application/json')
	return response

#this view allows the user to interct with the stored system data -system-wide operations are supported here
@Web_App.route('/systems/<method>', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def systems(method):
	response = None
	logged_in = False;
	is_man = False;

	try:
		#See if the user is logged in
		logged_in = session['logged_in']
		is_man = session['is_man']
		
		#users requests are sorted by rest-call
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
				systems = {"name": sys_id, "num_features": 12, "clients": ["Client A", "Client B", "Client C"], 'areas':['Polcies', 'Billing', 'Claims', 'Reports'], "status": "In Development", "disc": "This is where a discription of the softwaresystem would go."}
				#===================================================
			else:
				raise Exception("Method_Error")
			response = Web_App.response_class(json.dumps(systems), content_type='application/json')
		elif(request.method == 'POST'):
			#if request method is post, then save  new system to DB
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			#========================================================
		elif(request.method == 'UPDATE'):
			#if request method is update, then overwrite system info in DB
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			#========================================================
		elif(request.method == 'DELETE'):
			#if request method is delete, then remove system from DB
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			#========================================================
		else:
			#if request method is post, then save  new system to DB
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(False), content_type='application/json')
			#========================================================
	except:
		response = Web_App.response_class(json.dumps(False), content_type='application/json')

	return response

@Web_App.route('/features/<method>', methods=['GET', 'POST', 'UPDATE', 'DELETE'])
def features(method):
	response = None
	logged_in = False;
	is_man = False;

	try:
		#See if the user is logged in
		logged_in = session['logged_in']
		is_man = session['is_man']
		
		#users requests are sorted by rest-call
		if(request.method == 'GET'):
			#if request is get, fetch feature information for logged in user
			if(method=='all'):
				#if method is all, return a list of the current features for a given system
				system = request.args.get('system');
				#===========REPLACE WITH DB======================
				feature = ['def_feature_1', 'default_feature_2']
				#================================================
			elif(method=='selected'):
				#if method is selected, return a dictionary containing the data of the selected feature
				sys_id = request.args.get('system')
				feat_id = request.args.get('feature')
				#================REPLACE WITH DB====================
				feature = {"feat_title": "Login Button", "feat_disc":"This is were the feature discription would go.", "feat_client":"Client A", "feat_priority": 2, "feat_date": "01/09/1990", "feat_area":"Policies" }
				#===================================================
			else:
				raise Exception("Method_Error")
			response = Web_App.response_class(json.dumps(feature), content_type='application/json')
		elif(request.method == 'POST'):
			#if request method is post, then save  new feature to DB - system name is in the request for rest of methods
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			#========================================================
		elif(request.method == 'UPDATE'):
			#if request method is update, then overwrite feature info in system
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			#========================================================
		elif(request.method == 'DELETE'):
			#if request method is delete, then remove feature from system
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			#========================================================
		else:
			#if request method is post, then add new feature
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(False), content_type='application/json')
			#========================================================
	except:
		response = Web_App.response_class(json.dumps(False), content_type='application/json')

	return response

#main function
def main():
	if(__name__ == '__main__'):
		#parse the command line arguments
		args = parse_args()
		
		#initialize and fetch a new database instance
		global database
		database = ServerDB(Web_App, args['install'])

		Web_App.run()
		
main()