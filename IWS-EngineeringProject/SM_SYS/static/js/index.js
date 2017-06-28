/*
 *Programmed by: Jared Hall
 *Discription: This javascrip file holds the view model for the web app.
 *Liscense: https://github.com/Jared-Hall/IWS-EngineeringProject/blob/master/LICENSE
 *Table of contents:
 *	Section 1. Variables
 *  	--Section 1.1 General Variables
 *  	--Section 1.2 Login Variables
 *  	--Section 1.3 Systems Variables
 *  	--Section 1.4 Features Variables
 *	Section 2. Ajax Functions
 *		--Section 2.1 Login Ajax
 *		--Section 2.2 Systems Ajax
 *		--Section 2.3 Features Ajax
 *	Section 3. ViewModel Functions
 *		--Section 3.1 General Functions
 *		--Section 3.2 Login Functions
 *		--Section 3.3 Display Systems Functions
 *		--Section 3.4 Manage Systems Functions
 *		--Section 3.5 Manage Features Function
*/
function SMSviewModel() {
	
	//==========================Section 1. Variables===========================
	/*View model variables go here. Many variables are used in multiple pages
	*So those varables go under general, the other variables are organized
	*by panel.
	*/
	
	//                             Section 1.1
	//                          General variables
	var self = this;
	self.current_panel = ko.observable("login-template");
	self.panel_header = ko.observable("Login");
	self.manage = ko.observable(false);
	self.selected = ko.observable(false);
	self.post = false;
	self.result = "";
	
	//                          Section 1.2
	//                        Login Variables
	self.ID = ko.observable();
	self.pass = ko.observable();
	self.is_man = false;
	self.logged_in = ko.observable(false);
	
	//                         Section 1.3
	//                      Systems Variables
	self.systems = ko.observableArray();
	self.sys_name = ko.observable();
	self.sys_disc = ko.observable();
	self.sys_num_feature = ko.observable(0);
	self.sys_clients = ko.observableArray();
	self.sys_client_id = ko.observable();
	self.sys_areas = ko.observableArray();
	self.sys_area_id = ko.observable();
	self.sys_status = ko.observable();
	self.sys_del = ko.observable(false);
	
	//                     Section 1.4
	//                 Features Variables
	self.features = ko.observableArray();
	self.edit = ko.observable(false);
	self.feat_title = ko.observable();
	self.feat_disc = ko.observable();
	self.feat_client = ko.observable();
	self.feat_priority = ko.observable(0);
	self.feat_date = ko.observable();
	self.feat_area = ko.observable();
	//=========================================================================

	//==========================Section 2. Ajax Functions======================
	/*The Ajax functions for communicating with the server via ReST API go here
	 *The functions are organized by panel.
	 *The callbacks may use functions from Section 3.
	 */
	
	//                            Section 2.1
	//                            Login Ajax
	
	self.post_login = function() {
		//call server to validate input username and password
		$.ajax({url: "/login",
				type: "post",
				contentType: "application/json",
				data: ko.toJSON( {"ID" : self.ID(), "pass": $.md5(self.pass())} ),
				success: function(result) {
											if (result.logged_in === true) {
												self.is_man = result.is_man;
												self.logged_in(true);
												self.load_ds();
												}
											else {
												alert("Incorrect ID/Pass");
												}
										  },
				});
	};
	
	self.get_login = function () {
		//call server to logout
		$.ajax({url: "/login",
				type: "get",
				success:function () {self.load_login();},
				error: function () {self.load_login();}
				});
	};
	
	//                            Section 2.2
	//                            Systems Ajax
	
	self.get_systems_selected = function(system) {
		//this function fetches the information for a selected system and displays it
		//get dictionary of system information from server
		$.ajax({url: "/systems/selected",
				type: 'get',
				contentType: 'application/json',
				data: {'id':system},
				success: function(result) {
											self.sys_name(result.name);
											self.sys_disc(result.disc);
											self.sys_num_feature(result.num_features);
											self.sys_clients(result.clients);
											self.sys_status(result.status);
											self.sys_areas(result.areas);
											self.selected(true);
											self.sys_del(true);
											self.post = false;
											self.edit(true);
										  }
			   });
	};
	
	self.get_systems_all = function() {
		//This function gets a list of all of the current systems in the database
		$.ajax({url: "/systems/all",
				type: 'get',
				contentType: 'application/json',
				success: function (result) {
												if (result !== false) {self.systems(result);}
												else {alert('You are not logged in'); self.get_login();}
											}
				});
	};
	
	self.update_system = function() {
		//This function updates an existing system on the server via ReST API
		$.ajax({url: "/systems/null",
				type: "update",
				contentType: "application/json",
				data: ko.toJSON({"name":self.sys_name(),
								"disc":self.sys_disc(),
								"num_feature":self.sys_num_feature(),
								"clients":self.sys_clients(),
								"status":self.sys_status(),
								"areas": self.sys_areas()}),
				success: function () {alert("The System: "+self.sys_name()+" has been successfully updated.");}
				});
	};
	
	self.post_system = function() {
		//this function creates a new system in the server via ReST API
		$.ajax({url: "/systems/null",
				type: "post",
				contentType: "application/json",
				data: ko.toJSON({"name":self.sys_name(),
								"disc":self.sys_disc(),
								"num_feature":self.sys_num_feature(),
								"clients":self.sys_clients(),
								"status":self.sys_status(),
								"areas":self.sys_areas()}),
				success: function () {alert("The system: "+self.sys_name()+" has been successfully added to the database.");
									  self.edit(true);
									  self.sys_del(true);
									  }
				});
	};
	
	self.delete_system = function() {
		$.ajax({url: "/systems/null",
			   type: "delete",
			   contentType: "application/json",
			   data: ko.toJSON({"name":self.sys_name()}),
			   success: function () {alert("The System: "+self.sys_name()+" has been successfully deleted.");}
				});	
	};
	
	//                                Section 2.3
	//                               Features Ajax
	self.get_features_all = function() {
		$.ajax({url: "/features/all",
				type: 'get',
				contentType: 'application/json',
				data: {'system':self.sys_name()},
				success: function (result) {
											if (result !== false) {self.features(result);}
											else {alert('You are not logged in'); load_login();}
											 }
				});
	};
	
	self.get_features_selected = function (feature) {
		//get dictionary of feature information from server
		$.ajax({
				url: "/features/selected",
				type: 'get',
				contentType: 'application/json',
				data: {'system': self.sys_name(), 'feature': feature},
				success: function(result) {
											self.feat_title(result.feat_title);
											self.feat_disc(result.feat_disc);
											self.feat_client(result.feat_client);
											self.feat_priority(result.feat_priority);
											self.feat_date(result.feat_date);
											self.feat_area(result.feat_area);
											self.selected(true);
											self.sys_del(false);
											self.post = false;
											self.edit(false);
										  }
			   });
	};
		
	self.update_feature = function() {
		$.ajax({url: "/features/null",
				type: "update",
				contentType: "application/json",
				data: ko.toJSON({"system":self.sys_name(),
								"feat_title":self.feat_title(),
								"feat_disc":self.feat_disc(),
								"feat_client": self.feat_client(),
								"feat_priority":self.feat_priority(),
								"feat_date":self.feat_date(),
								"feat_area":self.feat_area()}),
				success: function () {alert("The feature: "+self.feat_title()+" has been successfully updated.");}
				 });
	};
	
	self.post_feature = function() {
		$.ajax({url: "/features/null",
				type: "post",
				contentType: "application/json",
				data: ko.toJSON({"system":self.sys_name(),
								"feat_title":self.feat_title(),
								"feat_disc":self.feat_disc(),
								"feat_client": self.feat_client(),
								"feat_priority":self.feat_priority(),
								"feat_date":self.feat_date(),
								"feat_area":self.feat_area()}),
				success: function () {alert("The feature: "+self.feat_title()+" has been successfully added to the database.");
									 self.sys_del(true);}
				});
	};
	
	self.delete_feature = function() {
		$.ajax({url: "/features/null",
			   type: "delete",
			   contentType: "application/json",
			   data: {"system" : self.sys_name(), "feature": self.feat_title()},
			   success: function () {alert("The Feature: "+self.feat_title()+" has been successfully deleted.");}
				});
	};
	
	//=========================================================================
	
	//=====================Section 3. View model Functions=====================
	/*The view model functions go here.
	 *These are the functions which intereact with the view.
	 *These functions are organized by panel
	 */
	
	//                             Section 3.1
	//                           General Functions
	self.clear_memory = function () {
		//This function sets all of the variables to their initial states
		self.systems([]);
		self.sys_clients([]);
		self.sys_areas([]);
		self.features([]);
		self.sys_del(false);
		self.edit(false);
		self.selected(false);
		self.manage(false);
		self.feat_priority(0);
		self.sys_num_feature(0);
		self.ID("");
		self.pass("");
		self.sys_name("");
		self.sys_disc("");
		self.sys_client_id("");
		self.sys_area_id("");
		self.sys_status("");
		self.feat_title("");
		self.feat_disc("");
		self.feat_client("");
		self.feat_date("");
		self.feat_area("");
	};
		
	self.clear_systems = function() {
		self.edit(false);
		self.sys_client_id("");
		self.sys_area_id("");
		self.sys_disc("");
		self.sys_num_feature(0);
		self.sys_status("");
		self.sys_name("");
		self.sys_clients([]);
		self.sys_areas([]);
		self.selected(false);
		self.sys_del(false);
		self.current_panel(self.current_panel()); //reloads curent panel 
	};
	
	self.clear_features = function () {
		self.edit(false);
		self.feat_title("");
		self.feat_disc("");
		self.feat_client("");
		self.feat_priority(0);
		self.feat_date("");
		self.feat_area("");
		self.selected(false);
		self.sys_del(false);
		self.current_panel(self.current_panel()); //reloads curent panel
	};
	
	self.goto_readme = function () {
		window.open("https://github.com/Jared-Hall/IWS-EngineeringProject");
	};
	
	self.load_form = function () {
		self.clear_systems();
		self.selected(true);
		self.sys_del(false);
		self.post = true;
		self.edit(false);
	};

	//                     Section 3.2
	//                    Login Functions
	self.load_login = function () {
		self.clear_memory();
		self.is_man = false;
		self.logged_in(false);
		self.panel_header("Login");
		self.current_panel("login-template");
	};
	
	//                      Section 3.3
	//                 Display Systems Functions
	self.load_ds = function () {
		//This function loads the display systems panel
		//clears page of previous data
		self.clear_memory();
		
		//get list of systems from server and displays on panel
		self.get_systems_all();
		
		//populate panel databindings and render template
		self.panel_header("Display Systems");
		self.current_panel('DS-template'); 
	};
		
	//                       Section 3.4
	//                  Manage Systems Functions
	self.load_ms = function () {
		//clear variables of previous data
		self.clear_features();
		self.clear_systems();
		
		//get a list of systems from the server
		self.get_systems_all();
		
		//render the panel
		self.manage(true);
		self.panel_header("Manage Systems");
		self.current_panel('MS-template');
	};
	
	self.dev_status = ko.pureComputed(function () {
		//This is a descritizing function which determins the label to use for the dev status
		var style = "";
		switch(self.sys_status()) {
									case "In Planning":
										style = "label-info";
										break;
									case "In Development":
										style = "label-success";
										break;
									case "In Maintenance":
										style = "label-warning";
										break;
									case "In Repair":
										style="label-danger";
										break;
									case "Finished":
										style = "label-default";
										break;
									default:
										style="label-primary";
										break;
								  }
			return style;},self
	);
	self.valid_system = function() {
		var is_valid = true;
		if(self.sys_name() === "" || self.sys_disc() === "" || self.sys_clients() === [] || self.sys_areas() === [] || self.sys_status() === "") {
			alert("You must fill in the form completely before submitting it.");
			is_valid = false;
		}
		return is_valid;
	};
	self.save_system = function () {
		if(self.post === false ) {
			//update system data in server
			self.update_system();
			//update the systems display - because user may have changed the systems name or added systems
			self.get_systems_all();
		}
		else {
			//Sends form data to server to create a new system object with if form is filled in
			if(self.valid_system()) {
				self.post_system();
			}
		}
	};
	
	self.delete_sys = function () {
		//Calls server to delete the system from the DB
		self.delete_system();
		//reloads the display
		self.clear_systems();
		self.get_systems_all();
	};
		
	self.add_client = function () {
		if(self.sys_client_id() !== "") {
			if(self.sys_clients.indexOf(self.sys_client_id()) === -1) {
				self.sys_clients.push(self.sys_client_id());
				}
			else {alert("Client already exists.");}
		}
		else {alert("You must enter a name to add a client.");}
	};
	
	self.remove_client = function () {
		if(self.sys_client_id() !== "") {
			if(self.sys_clients.indexOf(self.sys_client_id()) !== -1) {
				self.sys_clients.remove(self.sys_client_id());
				}
			else {alert("Client does not exist.");}
		}
		else {alert("You must enter a name to remove a client.");}
	};
		
	self.add_area = function () {
		if(self.sys_area_id() !== "") {
			if(self.sys_areas.indexOf(self.sys_area_id()) === -1) {
				self.sys_areas.push(self.sys_area_id());
				}
			else {alert("Product area already exists.");}
		}
		else {alert("No product area entered.");}
	};
	
	self.remove_area = function () {
		if(self.sys_area_id() !== "") {
			if(self.sys_areas.indexOf(self.sys_area_id()) !== -1) {
				self.sys_areas.remove(self.sys_area_id());
				}
			else {alert("Product area does not exist.");}
		}
		else {alert("No product area entered.");}
	};
	
	//                      Section 3.5
	//               Manage Features Functions
	self.load_mf = function () {
		//clear previous data
		self.clear_features();
		
		//get a list of features for this system from the server
		self.get_features_all();
		
		//render panel
		self.manage(true);
		self.selected(false);
		self.panel_header("Manage Features");
		self.current_panel('MF-template');
	};
		
	self.add_feature = function () {
		//This function loads the form to add a new feature
		//clear previous data then change variables to render new template
		self.clear_features();
		self.selected(true);
		self.sys_del(false);
		self.post = true;
		self.edit(true);
	};
		
	self.edit_feature = function () {
		//This function allows the user to edit a feature
		self.edit(true);
		self.sys_del(true);
	};
	
	self.valid_feature = function() {
		var is_valid = true;
		if(self.feat_title() === "" || self.feat_disc() === "" || self.feat_client() === "" || self.feat_area() === "" || self.feat_date() === "" || self.feat_priority === "") {
			alert("You must completely fill in the form before submitting.");
			is_valid = false;
		}
		else {
			if($.isNumeric(self.feat_priority()) === false) {
				alert("The priority must be a number.");
				is_valid = false;
			}
		
			if(!/^\d{1,2}\/\d{1,2}\/\d{4}$/.test(self.feat_date())) {
				alert("Date must be in mm/dd/yyyy format.");
				is_valid = false;
			}
		}
		return is_valid;
	};
	
	self.save_feature = function () {
		if(self.post === false) {
			//update feature data in server
			self.update_feature();
			//update the features display - because user may have changed the features name or added features
			self.get_features_all();
		}
		else {
			//Sends form data to server to create a new system object with
			if(self.valid_feature()) {
			self.post_feature();
			}
		}
	};
	
	self.delete_feat = function () {
		//Calls server to delete the feature from the DB
		self.delete_feature();
		//reloads the display
		self.clear_features();
		self.get_features_all();
	};
		
	self.select_client = function (client) {
		self.feat_client(client);
	};
	
	self.select_area = function (area) {
		self.feat_area(area);
	};
	
	//=========================================================================
}


//loads script once the DOM is loaded
$(document).ready(function(){ko.applyBindings(new SMSviewModel());});
//End of Script
