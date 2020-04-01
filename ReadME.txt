Open terminal and run "pip install -r requirements.txt"

Download chrome driver from this website.
https://chromedriver.storage.googleapis.com/index.html?path=77.0.3865.40/
In the app.py file change the variable "CHROMEDRIVER_PATH" at line 21 to the location of "chromedriver"


In the app.py file change the variable "options.binary_location" at line 24 to the location of "Google Chrome Application"


Now in the terminal, Run the flask server using the command : 
"python app.py"
The flask server will run at : "http://0.0.0.0:4444"
