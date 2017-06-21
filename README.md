# IWS-EngineeringProject
This is an engineering project for IWS. The goal of this project is to demonstrate my proficiency with the companies tech stack and basic engineering concepts. This project features a web app for technical member to submit feature requests to an existing piece of software.

#Technologies used in this project
*Flask
*SQL-Alchemy
*Bootstrap
*Knockout JS
*Sammy Js

#General layout (UI)
The general layout of the UI is based upon bootstrap conventions.
It starts with a three row layout wrapped in a bootstrap container:
-a header row
-a portal row (more on this later)
-a footer row

##The header row and footer rows
Both ofthese rows do not contain anything particularly interesting.
They just have some text in a solid background color.

##The portal row
This contains the main part of the UI that the user will be interacting with.
It largly consists of a box with changing elements based upon the hash-page the user is currently
on.

To run this program simply double click run.cmd and point a browser to 127.0.0.1:5000
Requires: flask, 
