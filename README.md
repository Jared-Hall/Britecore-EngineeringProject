# Engineering Project

## Overview
This is an engineering project for Britecore. The goal of this project is to demonstrate my proficiency with the companies tech stack and basic engineering concepts. This project features a web app for a technical member to submit feature requests for a software system. 

## Layout of Web Application
![alt-text](https://github.com/Jared-Hall/Britecore-EngineeringProject/blob/master/Design/LYT.png)

## Cloud Service
Link to cloud service:  http://sm-sys.us-east-2.elasticbeanstalk.com/

## Deployment walkthrough
**To deploy locally *(i.e your own computer):***
1. Clone the repo to your computer
2. Make sure you have all of the packages in requirements.txt - many pip auto install scripts can read this file directly and install all needed packages. You can use setup tools for this also.
3. in a new shell or cmd prompt execute "python application.py".
4. Open your browser and go to 127.0.0.1:5000 - software should run fine

**to deploy to the cloud:**
1. I already deployed the service to the cloud so why not save yourself the trouble?
2. Use Jareds cloud service *(link above)*.

## Service Walkthrough
This howto is organized by each of the portal frames specified in the Layout section

**Login:**

Login roles: 

Manager
ID: man1
Password: pass1

Employee:
ID: emp1
Password: pass2

**Display Systems:**

*If your login role is a Manager:*
Click manage systems to manage the software systems attached to this companies platform.

*For either role:*
Click on a system in the display bar to select it. Upon selection, you can click on "Manage Features" to go to the Manage Features frame.

**Manage Systems:**

*To create a new system:*
Click "New System", then fill out the form and click "Save system".

*To edit an existing system:*
First, select a system from the display panel, then change system information in the form. Click "Save System" to update the existing system.

*To delete a System:*
First, select a system, then click "Delete System".

*To manage a selected systems features:*
First, select a system by clicking on its label in the display bar. Then click "Manage Features" to go to the manage features frame.

**Manage Features:**

*To add a new request for a feature:*
Click "New Feature", fill out the form, and then click "Save Feature" to post the new feature request to the server.

*To edit a requested feature:*
First, select the feature by clicking on its label in the display bar, then click "Edit Feature", make any changes to the form, then click "Save Feature" to update the feature in the server.

*To delete a selected feature:*
Click "Delete Feature".

# Technical Details

## Technology Stack used
Technologies used in this project:
* Flask
* SQL-Alchemy
* Bootstrap
* Knockout JS
* AWS Elastic Beanstalk
* Python 3.5
* Linux
* Git/Github

## Requested features met
* *Open Source:* All of the technologies used in the project with the exception of Amazon's Cloud platform are open source technologies.

* *Decoupled Backend:* The SPA front-end is completely decoupled from the cloud server backend. communication is done via a ReST API over AJAX.

* *Test Suites with Continuous Integration:* I included a small automated testing suite. Continous integration is handled via a git hook to AWS elastic beanstalk.

* *Automated Deployment:* Deployment and continuous integration are handled via a git hook from elastic beanstalk. So every time there is an update to the software that is committed to the master branch the cloud service automatically updates and redeploys. Deployment of the cloud platform is handled via AWS EB CLI -also automated.

* *Usable, Responsive Interface:* This project features a SPA that feels like a native application. It prerenders all of the "pages" you can go to and simply fills in the appropriate containers based on the current navigational context. This results in a very fast UI. The only noticeable latency in the UI occurs when database operations happen, as one would expect.

* *MVVM Frontend:* The front-end of the web page was designed with the Model-View-ViewModel design pattern in mind. Every element of the page has some interaction with the ViewModel as represented by the numerous data-bindings present in the HTML file. This is what is behind the navigational context: as the user clicks the various navigational buttons the appropriate data-bindings are updated resulting in an instant change in the UI.

## Extra technical details
* The portal features a context sensitive display functionality that only displays the objects the user is supposed to encounter. This allows for an extremely fast application because the entire thing is loaded from the start and all that occurs throughout your use of the software is changes in data-bindings. This results in much less server interaction, and a safer, faster application.
* Smooth interplay between Bootstrap, KnockoutJS, and Flask. This is noticeable by the data-bindings for bootstrap objects.
* The database uses of SQL-Alchemy specific objects to manage feature priority *The ordering list*
* Micro cloud service autonomously published and maintained using AWS Elastic beanstalk
* Elastic beanstalk has an automated deployment feature which can grab the source directly from Github. *This is why there is a .elasticbeanstalk file in the repository.* This feature supports autonomous, continuous integration so that every time you update the master, the cloud service automatically updates as well. *This is one of those things that you don't see much code about but it is there.*
* Unit testing:* A unit-testing file exists under testing/ which runs a couple simple tests to demonstrate that I am familiar with automatic testing.
