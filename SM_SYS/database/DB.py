import os, sqlite3
from flask_sqlalchemy import SQLAlchemy

class ServerDB():
	"""
	This class initializes the database and provides usefull methods for common interactions
	between the server and the database. It also provides a layer of abstraction between the model layer and the data layer.
	This is usefull for both security and for future updates as you would not need to take the server down
	to update the dB, just insert code changes into this file then reboot the server.
	"""
	
	def __init__(self, app, mode):
		#load default database config
		app.config.from_object(__name__)
		app.config.update(dict(
			DATABASE=os.path.join(app.root_path + "\database", "SM_SYS.db"),
			SQLALCHEMY_DATABASE_URI='sqlite:////database/SM_SYS.db',
			SQLALCHEMY_TRACK_MODIFICATIONS=False,
			SECRET_KEY="dev key",
			USERNAME='admin',
			PASSWORD='default'))

		
		self.db = SQLAlchemy(app)
		
		
		if(mode=='install'):
			#connect to the database
			db = sqlite3.connect(app.config['DATABASE'])
			#initialize the database if server was just installed
			with open(os.path.join(app.root_path + "\database", "SM_SYS.sql"), 'r') as infile:
				db.cursor().executescript(infile.read())
			db.commit()
			db.close()
			print("* Database successfully initialized")
			
		#initialize SQL-Alchemy DB
		
			
		
		
	def __del__(self):
		#destructor for the class, closses database connection and cleans up

		
		print("* Database connection closed successfully")
		
	def get_user(self, username):
		return True
	
	def add_user(self):
		#will implement at a later date - just an idea
		return True
	
	def get_systems(self):
		return True
	
	def get_system(self, sys_id):
		return True
	
	def add_system(self, system):
		return True
	
	def update_system(self, system):
		return True
	
	def delete_system(self):
		return True
	
	def get_features(self):
		return True
	
	def get_feature(self):
		return True
	
	def add_feature(self):
		return True
	
	def update_feature(self):
		return True
	
	def delete_feature(self):
		return True