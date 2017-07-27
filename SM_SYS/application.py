import os, sys, traceback
from flask import Flask, request, session, url_for, abort, render_template, json

#creates a WSGI complient flask web app
Web_App = Flask(__name__)

#flask app reference for AWS elastic beanstalk
application = Web_App
#----------------------------------DATABASE DEFINITION--------------------------
#import the database models
from database.models import *

#Database configuration
Web_App.config.from_object(__name__)
Web_App.config.update(dict(
	SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(Web_App.root_path + "/database", "SM_SYS.db"),
	SQLALCHEMY_TRACK_MODIFICATIONS=False,
	SECRET_KEY="a722c63db8ec8625af6cf71cb8c2d939"))

#setup the database
database.init_app(Web_App)
Web_App.app_context().push()
database.create_all()

#If the default users and systems don't exist then input them
try:
	if(Users.query.filter_by(username=man1.username).first() is None):
		database.session.add(man1)
		database.session.add(emp1)
		database.session.add(def_system)
		database.session.add(area1)
		database.session.add(area2)
		database.session.add(area3)
		database.session.add(area4)
		database.session.add(client1)
		database.session.add(client2)
		database.session.add(client3)
		database.session.add(def_feature)
		database.session.commit()
		
except Exception as e:
	print("An exception was thrown while loading defaults: ", e)
#-------------------------------------------------------------------------------
#-----------------------------------WEB DEFINITION------------------------------

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
		response = Web_App.response_class(json.dumps({"logged_in":False}), content_type='application/json')
		#load user profile from DB
		profile = Users.query.filter_by(username=user['ID']).first()
		if(profile is not None):
			if(user['ID'] == profile.username and user['pass'] == profile.password):
				session['logged_in'] = True
				session['is_man'] = profile.auth
				response = Web_App.response_class(json.dumps({"logged_in":session['logged_in'], "is_man":session['is_man']}), content_type='application/json')
	elif(request.method == 'GET'):
			session.pop('logged_in', None)
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
	else:
		abort(404)
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
				temp = Systems.query.all()
				systems = [item.sys_id for item in temp]
			elif(method=='selected'):
				#if method is selected, return a dictionary containing the data of the selected system
				item = Systems.query.filter_by(sys_id=request.args.get('id')).first()
				systems = {"name": item.sys_id,
						   "num_features": item.num_feat,
						   "clients": [client.client_name for client in item.clients.all()],
						   'areas': [area.product_area for area in item.product_areas.all()],
						   "status": item.status,
						   "disc":item.disc}
			else:
				raise Exception("Method_Error")
			response = Web_App.response_class(json.dumps(systems), content_type='application/json')
			
		elif(request.method == 'POST'):
			#if request method is post, then save  new system to DB
			data = json.loads(request.data)
			if(database.session.query(Systems).filter_by(sys_id=data['name']).first() is None):
				#Add the base data
				database.session.add(Systems(
					sys_id=data['name'],
					disc=data['disc'],
					num_feat=data['num_feature'],
					status = data['status']))
				
				#add the client list
				for client in data['clients']:
					#add new client
					database.session.add(Clients(client_name=client, sys_id=data['name']))
				
				#Add the product areas
				for area in data['areas']:
					#add new area
					database.session.add(Areas(product_area=area, sys_id=data['name']))
				
				database.session.commit()
				response = Web_App.response_class(json.dumps(True), content_type='application/json')
			else:
				response = Web_App.response_class(json.dumps(False), content_type='application/json')
		
		elif(request.method == 'UPDATE'):
			#if request method is update, then overwrite system info in DB
			#get and load request data
			data = json.loads(request.data)
			#update base data for selected system
			database.session.query(Systems).filter_by(sys_id=data['sel_id']).update(dict(
				sys_id=data['name'],
				disc=data['disc'],
				num_feat=data['num_feature'],
				status = data['status']))
			
			#update the client list
			database.session.query(Clients).filter_by(sys_id=data['name']).delete()
			for client in data['clients']:
				#add new client
				database.session.add(Clients(client_name=client, sys_id=data['name']))
			
			#update the product areas
			database.session.query(Areas).filter_by(sys_id=data['name']).delete()
			for area in data['areas']:
				#add new area
				database.session.add(Areas(product_area=area, sys_id=data['name']))
	
			database.session.commit()
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
		
		elif(request.method == 'DELETE'):
			#if request method is delete, then remove system from DB
			name = json.loads(request.data)['name']
			
			#remove the areas associated with the system
			database.session.query(Areas).filter_by(sys_id=name).delete()

			#remove the clients associated with the system
			database.session.query(Clients).filter_by(sys_id=name).delete()

			#remove all features associated with the system
			database.session.query(Features).filter_by(sys_id=name).delete()
			
			#remove the system
			database.session.query(Systems).filter_by(sys_id=name).delete()
			
			database.session.commit()
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
		else:
			#an incorrect method was given
			abort(404)
	except:
		traceback.print_exc(file=sys.stdout)
		database.session.rollback()
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
				
				#First, get the system
				system = database.session.query(Systems).filter_by(sys_id=request.args.get('system')).first()
				
				#Then get a list of the feature names from the system
				feature = [item.feat_title for item in system.features ]
			elif(method=='selected'):
				#if method is selected, return a dictionary containing the data of the selected feature
				item = database.session.query(Features).filter_by(sys_id=request.args.get('system'), feat_title=request.args.get('feature')).first()
				feature = {"feat_title": item.feat_title,
						   "feat_disc": item.feat_disc,
						   "feat_client": item.client_name,
						   "feat_priority": item.feat_priority,
						   "feat_date": item.feat_date,
						   "feat_area": item.feat_area }
			else:
				raise Exception("Method_Error")
			response = Web_App.response_class(json.dumps(feature), content_type='application/json')
		elif(request.method == 'POST'):
			#if request method is post, then update the priorities first and then save the new feature
			#get a list of the current features so we can change their priority
			data = json.loads(request.data)
			
			#get the system that the new feature is associated with
			system = database.session.query(Systems).filter_by(sys_id=data['system']).first()
			
			#build a new feature
			new_feature = Features(
									sys_id = data['system'],
									feat_title = data['feat_title'],
									feat_disc = data['feat_disc'],
									client_name = data['feat_client'],
									feat_priority = data['feat_priority'],
									feat_date = data['feat_date'],
									feat_area = data['feat_area'],
									)
			
			#insert into database and update the priority of the other features
			#the ordering list manages the priorities automatically -thanks sql-alchemy!
			system.features.insert(data['feat_priority']-1, new_feature)
			
			#update the feature count in the system
			system.num_feat += 1

			database.session.commit()
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
		elif(request.method == 'UPDATE'):
			#if request method is update, then overwrite feature info in system
			data = json.loads(request.data)
			
			#Get the system associated with the feature
			system = database.session.query(Systems).filter_by(sys_id=data['system']).first()
			
			#get the feature the user wishes to update. I have to go about this weird because of the ordering list
			selected_feature = None
			for f in system.features:
				if(f.feat_title == data['sel_id']):
					selected_feature  = f
			if(selected_feature==None):
				#raise an exception if the feature was ot found, this will roll back the database transaction safely
				raise('Selected_feature was type None')
			
			#remove the old feature from the ordering list
			system.features.remove(selected_feature)
			
			#update the features info
			selected_feature.feat_title = data['feat_title']
			selected_feature.feat_disc = data['feat_disc']
			selected_feature.sys_id = data['system']
			selected_feature.client_name = data['feat_client']
			selected_feature.feat_priority = data['feat_priority']
			selected_feature.feat_date = data['feat_date']
			selected_feature.feat_area = data['feat_area']
			
			#add it to the ordering list
			system.features.insert(selected_feature.feat_priority-1, selected_feature)
			
			#Commit the session, the ordering list handels the priority -thanks sql-alchemy
			database.session.commit()
			
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
			
		elif(request.method == 'DELETE'):
			#if request method is delete, then remove feature from system
			data = json.loads(request.data)
			
			#Get the system associated with the feature
			system = database.session.query(Systems).filter_by(sys_id=data['system']).first()

			#remove the feature from the Features tables
			database.session.query(Features).filter_by(sys_id=data['system'], feat_title=data['feature']).delete()
			
			#reorder the list
			system.features.reorder()
			
			#update system
			system.num_feat -= 1
			
			database.session.commit()
			
			response = Web_App.response_class(json.dumps(True), content_type='application/json')
		else:
			#unsupported request method so we just return false
			#=======================Replace with DB==================
			response = Web_App.response_class(json.dumps(False), content_type='application/json')
			#========================================================
	except:
		traceback.print_exc(file=sys.stdout)
		database.session.rollback()
		response = Web_App.response_class(json.dumps(False), content_type='application/json')

	return response

if(__name__ == '__main__'):
	application.run(host='0.0.0.0')
	#this occures when the server has been closed
	database.session.remove()
	

