function SMSviewModel() {
	var self = this;
	
	//General variables
	self.current_panel = ko.observable("login-template");
	self.panel_header = ko.observable("Login");
	self.manage = ko.observable(false);
	self.logged_in = ko.observable(false);
	
	//Panel specific variables
	self.ID = ko.observable();
	self.pass = ko.observable();
	self.is_man = false;
	
	//Display Systems Variables
	self.selected = ko.observable(false);
	self.systems = ko.observableArray();
	self.sys_name = ko.observable();
	self.sys_disc = ko.observable();
	self.sys_num_feature = ko.observable();
	self.sys_cust_id = ko.observable();
	self.sys_status = ko.observable();
	
	//General ViewModel Functions
	
	//ViewModel data functions for the login panel
	self.login = function() {
		//call server to validate input username and password
		$.ajax({
				url: "/login",
				type: "post",
				contentType: "application/json",
				data: ko.toJSON( {"ID" : self.ID(), "pass": $.md5(self.pass())} ),
				success: function(result) {
											if (result.logged_in === true) {
												self.is_man = result.is_man;
												self.logged_in(true);
												self.load_ds();}
											else {alert("Incorrect ID/Pass");}
										  }
				});
	};
	
	self.logout = function () {
		//call server to logout
		self.is_man = false;
		$.ajax({
				url: "/login",
				type: "get",
				success:function () {
										self.logged_in(false);
										self.load_login();
									}
				});
		};
		
	//Viewmodel functions for display systems
	
	self.clear_display = function() {
		self.selected(false);
		self.current_panel('DS-template'); 
		};
	
	//this function fetches the information for a selected system and displays it
	self.display_selected = function(system) {
		//get dictionary of system information from server
		$.ajax({
				url: "/systems/selected",
				type: 'get',
				contentType: 'application/json',
				data: {'id':system},
				success: function(result) {
											self.sys_name(result.name);
											self.sys_disc(result.disc);
											self.sys_num_feature(result.num_features);
											self.sys_cust_id(result.cust_id);
											self.sys_status(result.status);
											self.selected(true);
										  }
			   });
	};
	
	self.dev_status = ko.pureComputed(function () { var style = "";
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
														return style;
												  },
									 self);
	
	self.goto_readme = function () {window.open("https://github.com/Jared-Hall/IWS-EngineeringProject");};
	
	self.load_login = function () {
		self.manage(false);
		self.selected(false);
		self.panel_header("Login");
		self.current_panel("login-template");
		};
	//This loads the display systems template with data retrieved from the server	
	self.load_ds = function () {
		//get list of systems from server
		$.ajax({
				url: "/systems/all",
				type: 'get',
				contentType: 'application/json',
				success: function (result) {
											if (result !== false) {self.systems(result);}
											else {alert('You are not logged in'); self.current_panel('login-template');}
											 }
				});
		//populate variables with data from server
		//render template
		self.manage(false);
		self.selected(false);
		self.panel_header("Display Systems");
		self.current_panel('DS-template'); 
		};
	
	//loads the default page for manage systems
	self.load_ms = function () {
		//render template
		self.manage(true);
		self.selected(false);
		self.panel_header("Manage Systems");
		self.current_panel('MS-template');
		};
	
	//loads the default page for manage features
	self.load_mf = function () {
		//render template
		self.manage(true);
		self.selected(false);
		self.panel_header("Manage Features");
		self.current_panel('MF-template');
		};

}


//loads script once the DOM is loaded
$(document).ready(function(){ko.applyBindings(new SMSviewModel());});
