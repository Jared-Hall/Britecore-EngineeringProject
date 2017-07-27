"""
Programmed by: Jared Hall
Discription: This is the database models file for the server database.
All of the SQL-Alchemy classes are in here.
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.orderinglist import ordering_list
database = SQLAlchemy()

class Users(database.Model):
	username = database.Column(database.String(30), primary_key=True, unique=True)
	password = database.Column(database.String(120))
	auth = database.Column(database.Boolean)

		
class Systems(database.Model):
	sys_id = database.Column(database.String(120), primary_key=True, unique=True)
	disc = database.Column(database.Text)
	num_feat = database.Column(database.Integer)
	status = database.Column(database.String(30))
	product_areas = database.relationship('Areas', backref='systems', lazy="dynamic")
	clients = database.relationship('Clients', backref='systems', lazy="dynamic")
	features = database.relationship('Features', order_by="Features.feat_priority", collection_class=ordering_list('feat_priority', count_from=1))

	
class Clients(database.Model):
	client_name = database.Column(database.String(60), primary_key=True,)
	sys_id = database.Column(database.String(120), database.ForeignKey('systems.sys_id'), primary_key=True,)

		
class Areas(database.Model):
	product_area = database.Column(database.String(120), primary_key=True,)
	sys_id = database.Column(database.String(120), database.ForeignKey('systems.sys_id'), primary_key=True,)

		
class Features(database.Model):
	sys_id = database.Column(database.String(120), database.ForeignKey('systems.sys_id'), primary_key=True,)
	feat_title = database.Column(database.String(120), primary_key=True,)
	feat_disc = database.Column(database.Text)
	feat_date = database.Column(database.String(10))
	client_name = database.Column(database.String(30))
	feat_priority = database.Column(database.Integer)
	feat_area = database.Column(database.String(120))

#default entries into the database
man1 = Users(username='man1', password="a722c63db8ec8625af6cf71cb8c2d939", auth=True)
emp1 = Users(username='emp1', password="c1572d05424d0ecb2a65ec6a82aeacbf", auth=False)
def_system = Systems(sys_id='Default System', disc='This is where a discription would go.', num_feat=1, status='In Planning')
client1 = Clients(client_name='Client A', sys_id='Default System')
client2 = Clients(client_name='Client B', sys_id='Default System')
client3 = Clients(client_name='Client C', sys_id='Default System')
area1 = Areas(product_area='Policies', sys_id='Default System')
area2 = Areas(product_area='Billing', sys_id='Default System')
area3 = Areas(product_area='Claims', sys_id='Default System')
area4 = Areas(product_area='Reports', sys_id='Default System')
def_feature = Features(sys_id='Default System', feat_title='Default Feature', feat_disc='This is where the feature discription would go.', feat_date='06/29/2017', client_name='Client A', feat_priority=1, feat_area='Policies')