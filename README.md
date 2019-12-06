# Project 7: Brevet time calculator with Ajax MongoDB, api, and login security

Reimplement the RUSA ACP controle time calculator with flask, ajax, and mongoDB.

Credits to Michal Young for the initial version of this code.

## ACP controle times

That's "controle" with an 'e', because it's French, although "control" is also accepted. Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location.   

The algorithm for calculating controle times is described here (https://rusa.org/pages/acp-brevet-control-times-calculator). Additional background information is given here (https://rusa.org/pages/rulesForRiders). The description is ambiguous, but the examples help. Part of finishing this project is clarifying anything that is not clear about the requirements, and documenting it clearly.  

We are essentially replacing the calculator here (https://rusa.org/octime_acp.html). We can also use that calculator to clarify requirements and develop test data.  

## AJAX, Flask, and mongoDB reimplementation with restful links and API

The RUSA controle time calculator is a Perl script that takes an HTML form and emits a text page in the above link. 

This implementation  fills in the miles or km fields using Ajax and Flask and then puts the start and end times in a mongodb (data base).
the time is placed in the data base by clicking the submit button
to see all of the entries click the display button
to clear all of the entries in the data base click the reset button
if a letter or no entry is input an error apears in the notes section and the input will not be put in the data base
if a brevet distance in more than 20% longer than the races total distance, the entry in not put in mongoDB and an error also apears in the notes section
alerting the user to the issue.
if the user clicks display but they haven't entered any times an error apears in the notes section describing the error
If a user enters a negative distance it also alerts the user to the issue in the notes section
to see the the start and end times click the display button 
they appear in a decending order based on distance from start

* the logic in acp_times.py is based on the algorithm given above. 
based off the brevet calucaltion rules given here https://rusa.org/pages/acp-brevet-control-times-calculator) I used the row that first defined what min and max speed for edge cases that are defined twice ie for brevet distance 200 i used 34 instead of 32 based on the origininal calcualtor
I also made the last brevet close time for a 200 km 13.5 hours after the start based on randonneurs rules

the restful architecture includes the following links:
"http://<host:port>/listAll" should return all open and close times in the database
"http://<host:port>/listOpenOnly" should return open times only
"http://<host:port>/listCloseOnly" should return close times only

"http://<host:port>/listAll/csv" should return all open and close times in CSV format
"http://<host:port>/listOpenOnly/csv" should return open times only in CSV format
"http://<host:port>/listCloseOnly/csv" should return close times only in CSV format

"http://<host:port>/listAll/json" should return all open and close times in JSON format
"http://<host:port>/listOpenOnly/json" should return open times only in JSON format
"http://<host:port>/listCloseOnly/json" should return close times only in JSON format

http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format

** "http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format

It also includes a consumer programs that uses the api service created by the original app. The consumer is in the website folder and it uses php. It runs on port 5000. It dispalyes the start and close times in two lists.
It isn't acitve anymore becuase the api are now login ptotected

## loging in and security 
A login is required to access anything in the web aplication. To login simply hit the regiter buton or click the link at the top pf the page that says "register as a new user". afer entering a password and username you will be redirected to the login page where you can use that to login
I used a mongo database to keep track of users. I also have the two new resources /api/token and /api/register.
the first returns a valid token the second can be used to get the resource of any user in the system using thier id and the url /api/register/<userid>. All of the other previosly mentioned recorces are protected by login and token varifaction. Renember me functionality for if the user exits the tab is also implamented, but stops working when their token becomes invalid.  Flask CSRF protection is implamented as well.


## Using this web app
enter the proj7-auth-ux folder and go the the folder DockerMongo (proj7-auth-ux/DockerRestAPI)
there is a run.sh shell file that starts the application included
it can be run in a bash shel with the command
$ ./run.sh
The aplication runs on localhost:5001 The consumer aplication from project 6 runs on port 5000 and it redirects you to a login becuase one is now required to access the data.
To stop the web app in the shel it is running press Ctrl + c to stop the container then to remove it enter the command 
$ ./stop.sh


## Testing

A suite of nose test cases is also included
it tests the algorithium producing times




