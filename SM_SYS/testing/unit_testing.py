"""
Programmed by: Jared Hall
Discription: a sample unit testing file whih runs 2 tests:
both adding and removing a system. I wrote this just to demonstrate that I am familiar
with the unit testing concept and pythons unit testing module.
"""
import os, unittest, json
from flask_testing import TestCase

from server_main import Web_App
from database.models import *

class SampleUnitTest(TestCase):
	
	def create_app(self):
		Web_App.config.from_object(__name__)
		Web_App.config.update(dict(
			SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(Web_App.root_path + "\database", "SM_SYS_Testing.db"),
			SQLALCHEMY_TRACK_MODIFICATIONS=False,
			SECRET_KEY="a722c63db8ec8625af6cf71cb8c2d939",
			TESTING=True))
		database.init_app(Web_App)
		Web_App.app_context().push()
		return Web_App
	
	def setUp(self):
		#setup the database
		database.create_all()

	def tearDown(self):
		database.session.remove()
		database.drop_all()
		
	def test_add_system(self):
		#Fist login to the system
		with self.client.session_transaction() as ses:
			ses['logged_in'] = True
			ses['is_man'] = True
		#do the test
		system = {"name": "test_system",
				"disc": "Testing.",
				"num_feature": 0,
				"clients": ['A', 'B', 'C'],
				"status": "In Planning",
				"areas": ['A1', 'A2']}
		response = self.client.post('/systems/null', data=json.dumps(system))
		self.assertEqual(response.json, True, msg="Failed to add system.")
		print("Test: Add System -- OK")
		
	
	def test_remove_system(self):
		#Fist login to the system
		with self.client.session_transaction() as ses:
			ses['logged_in'] = True
			ses['is_man'] = True
		#objects for test
		database.session.add(Systems(sys_id="test_system",
				disc="Testing.",
				num_feat = 0,
				status= "In Planning"))
		
		for client in ['A', 'B', 'C']:
			database.session.add(Clients(client_name=client, sys_id="test_system"))
			
		for area in ['A1', 'A2']:
			database.session.add(Areas(product_area=area, sys_id="test_system"))
			
		database.session.commit()
		#tests
		
		response = self.client.delete('/systems/null', data=json.dumps({'name':'test_system'}))
		self.assertEqual(response.json, True, msg="Failed to remove system.")
		print("Test: Remove System -- OK")

if __name__ == '__main__':
	unittest.main()