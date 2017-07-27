[1]:  http://sm-sys.us-west-2.elasticbeanstalk.com/
# Britecore-EngineeringProject

## Overview
This is an engineering project for Britecore. The goal of this project is to demonstrate my proficiency with the companies tech stack and basic engineering concepts. This project features a web app for technical member to submit feature requests for a software system. 

## Layout of Web Application
![alt-text](https://github.com/Jared-Hall/Britecore-EngineeringProject/Design/LYT.png)

## Cloud Service
Link to cloud service:  http://sm-sys.us-west-2.elasticbeanstalk.com/

## Howto
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
Click on a system in the display bar to select it. Upon selection you can click on "Manage Features" to go to the Manage Features frame.

**Manage Systems:**

*To create a new system:*
Click "New System", then fill out the form and click "Save system".

*To edit an existing system:*
First select a system from the display panel, then change system information in the form. Click "Save System" to update the existing system.

*To delete a System:*
First select a system, then click "Delete System".

*To manage a selected systems features:*
First, select a system by clicking on its label in the display bar. Then click "Manage Features" to go to the manage features frame.

**Manage Features:**

*To add a new request for a feature:*
Click "New Feature", fill out the form, and then click "Save Feature" to post the new feature rquest to the server.

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

## Interesting Details
* The portal features a context sensitive display functionality that only displays objects the user is supposed to encounter. This allows for an extremely fast application because the entier thing is loaded from the start and all that occures throughout your sue of the software is changes in databindings. This results in much less server interaction, and a safer, faster application.
* Smooth interplay between Bootstrap, KnockoutJS, and FLask. This is noticable by the data-bindings for bootstrap objects.
* Complete seperation of the Client from the server *See HLD*
* SQL-Alchemy integration and the use of SQL-Alchemy specific objects to manage feature priority *The ordering list*
* Micro cloud service published to AWS Elastic beanstalk
* Elastic beanstalk has an automated deployment feature which can grab the source directly from Github. *This is why there is a zip file in the repository.* This feature supports autonomous, continuous integration so that every time you update the master, the cloud service automatically updates as well. *This is one of those things that you don't see much code about but it is there.*
* Unit testing: A unittesting file exists under testing/ which runs a couple simple tests to demonstrate that I am familiar with automatic testing.
