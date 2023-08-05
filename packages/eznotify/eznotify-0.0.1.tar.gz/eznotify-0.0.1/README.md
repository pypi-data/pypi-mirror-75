# Eznotify Documentation
##### Firstly you will have to install eznotify
In the terminal/command prompt you will have to enter this command
`$pip install eznotify`

##### Importing eznotify
To use eznotify in python you will have to first import eznotify
Open the python shell and enter this command:
`import ezsend`

##### Sending a notification
The function to send a desktop notification to your computer is:
`ezsend.notify(subjectofnotification, bodyofnotification, timeyouwantthenotificationtostay)`

##### Example
Lets say I wanted to send a notification that had a subject of "Hello World!" and a body of "eznotify is awesome" and disappears after 5 seconds you would do this:
```
import ezsend
ezsend.notify('Hello World!', 'eznotify is awesome', 5)
```
