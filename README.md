# Project 5: Brevet time calculator with Ajax and MongoDB

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

Also a query parameter to get top "k" open and close times in incluced. For examples, see below.
"http://<host:port>/listOpenOnly/csv?top=3" should return top 3 open times only (in ascending order) in CSV format
"http://<host:port>/listOpenOnly/json?top=5" should return top 5 open times only (in ascending order) in JSON format
"http://<host:port>/listCloseOnly/csv?top=6" should return top 5 close times only (in ascending order) in CSV format
"http://<host:port>/listCloseOnly/json?top=4" should return top 4 close times only (in ascending order) in JSON format

It also includes a consumer programs that uses the api service created by the original app. The consumer is in the website folder and it uses php. It runs on port 5000. It dispalyes the start and close times in two lists.

## Using this web app
enter the proj6-rest folder and go the the folder DockerMongo (proj6-rest/DockerRestAPI)
there is a run.sh shell file that starts the application included
it can be run in a bash shel with the command
$ ./run.sh
it should run on port 5001, so you can access it at url localhost:5000 then you calculate all the times!
to stop it in the shel it is running in press Ctrl + c to stop the container then to remove it enter the command
the apacje php runs consumer app runs on port 5000
$ ./stop.sh


## Testing

A suite of nose test cases is also included
it tests the algorithium producing times




