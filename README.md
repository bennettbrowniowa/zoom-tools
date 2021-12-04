# zoom-tools

For teachers using Zoom, this repo offers tools that consume zoom usage reports and saved chat files, and that programmatically open zoom meetings and have access to the chat client.

## Indpendent components:
### Attendance after class:
A web-based tool for making it easier to use Zoom data for teachers who lack integrations with zoom for attendance and analysis of participation. 

### In-meeting robot
Programmatic presence to start and join meetings, and to access chat and attendance inside a zoom meeting.

### Chat analysis
Collect saved chat files. Report participation and histogram display of polls. (collate zoom chat.py)

## Attendance after class
Paste Zoom's usage report into this web page. Returns alphabetical by last-name. 
Paste InfCampus or PowerSch roster in another text field. Compares the two lists and color codes.
(zoom attendance.html)

## In-meeting robot
A git-ignored file contains meeting names, numers, and passwords, and user api key pair. Python consumes this file, communicates with Zoom to generate signatures, and creates a JavaScript file containing those signatures. A web page contains the Zoom interfect from the Zoom Meeting SDK and successfull joins (and can start meeting if host=1) the last meeting from the git-ignored file. Chat client is not accessible and question posted in Zoom Developer Forum. If Zoom account with school email has apikey generation disabled, but you can join your meeting from a personal zoom account, the robot can access your class meeting once it is started but the signature must be generated with host=0. 
(zoom meeting sdk * , zoom web meeting * , zoomTeacherBot.js)

## Chat analysis
A Python program iterates accross saved meeting folders and digests the saved_meeting_chat files. Histogram displays profile across class minutes of participation. Coming soon, historgrams of numeric responses 1 to 5 during a timed window in class.
Independently, a web page offers paste int a text box from the chat.txt file or in-meeting chat to show participation counts. This code hosted at codepen and not version controlled in git.
