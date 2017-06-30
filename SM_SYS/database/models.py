"""
Programmed by: Jared Hall
Discription: This is the database models file for the server database.
All of the SQL-Alchemy classes are in here
"""

class Users(db.Model):
	username = db.Column(db.String(30), primary_key=True, unique=True)
	password = db.Column(db.String(120))
	auth = db.Column(db.Boolean)
	
	def __init__(self, username, password, auth):
		self.username = username
		self.password = password
		self.auth = auth
		
class System(db.Model):
	sys_id = db.Column(db.String(120), primary_key=True, unique=True)
	disc = db.Column(db.Text)
	num_feat = db.Column(db.Integer)
	status = db.Column(db.String(30))
	product_areas = db.relationship('Areas', backref='system', lazy='dynamic')
	
	def __init__(self, sys_id, disc, num_feat, status):
		self.sys_id = sys_id
		self.disc = disc
		self.num_feat = num_feat
		self.status = status
	
class Clients(db.Model):
	client_name = db.Column(db.String(60), primary_key=True,)
	sys_id = db.Column(db.String(120), primary_key=True,)
	
	def __init__(self, client_name, sys_id):
		self.client_name = client_name
		self.sys_id = sys_id
		
class Areas(db.Model):
	product_area = db.Column(db.String(120), primary_key=True,)
	sys_id = db.Column(db.String(120), primary_key=True,)
	
	def __init__(self, product_area, sys_id):
		self.product_area = product_area
		self.sys_id = sys_id
		
class Features(db.Model):
	sys_id = db.Column(db.String(120), primary_key=True,)
	feat_title = db.Column(db.String(120), primary_key=True,)
	feat_disc = db.Column(db.Text)
	feat_date = db.Column(db.String(10))
	client_name = db.Column(db.String(30),)
	feat_priority = db.Column(db.Integer)
	
	def __init__(self, sys_id, feat_title, feat_disc, feat_date, client_name, feat_priority):
		self.sys_id = sys_id
		self.feat_title = feat_title
		self.feat_disc = feat_disc
		self.feat_date = feat_date
		self.client_name = client_name
		self.feat_priority = feat_priority