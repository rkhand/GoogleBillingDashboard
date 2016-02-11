# Billing App

Billing app is a easy way to represent the cost incurred in an year or month or project or resource for a google based project. 
It is built using Flask for api calls , AngularJS for front end , D3.js for data visualization, SQL DB to store the data
 and a Java based process to read the JSON file created by Google and update the DB.    


# Introduction
The app has a landing page that displays all the cost centers and the cost for the current month. If there are no 
cost centers associated then all the projects are placed under 'Other'. Clicking on the cost center names will load 
the chart for the overall cost for the year in that center. From there you can get other details by changing the drop 
down or by clicking on the graph.  
**URLs**  :  
   **/** -- Landing page  
   **/billing** -- Billing Cost per cost center
   **/billing/cost_center/#?year=2015&month=all&cost_center=all&project=all&resource=all** -- Overall cost for all cost centers.  
   By changing the parameters in the url you can get the corresponding data.  
   There is a login button that will control who can add project into info into the 'Project' table.    
This README will give a detailed steps need to get the python app and running assuming the DB is already set up and data populated by the Java utility.  


# Requirements
* [Docker] -- Container based development setup if using Docker
* Google Compute Instance account if using this for development

---
# Setup/Installation Instructions

### Installation for Development in Google Compute Instance

You need to have Ubuntu OS in that Instance

    1. Update the Database values accordingly in apps_config.py
    2. Update the following parameters in start_script_ubuntu.sh  with your info
        * APP_RELEASE
        * APP_VERSION
        * APP_NAME
        * BUCKET_NAME
    3. Use the start_script_ubuntu.sh as the startup script while creating the instance
    
Once above is completed, you should have your app up and running in your instance at <instance_url>/.

### Installation for Development Using Docker

You need to have docker installed and the process running. 

    1. Update the Database values accordingly in apps_config.py
    2. Use the dockerfile and run the following once inside the deployment folder
      docker build -t container_name --build-arg DEPLOY_ARTIFACT=deployment_artifact.zip .
    3. Run docker with
        docker run –p 80:8080 –d container_name
    
Once above is completed, you should have your app up and running.

# Additional Information
### Other Projects
* [Java Utility Repo] -- Billing Analyzer Java project can be used to parse the billing JSON file and store it in the database       

### Database Info
There are 2 tables needed for this app to work

        * usage --  This table has information about the cost per day based on the data updated from
         the the Java utility that uses JSON file provided by Google
        * projects -- This is updated through the UI, this table has information about the project,   
        like which cost center they belong to and who is the director for the same.

The sql file for updating the DB and schema file is [reporting.db]

### Login Feature
By default the app is visible to all, however if you need to add cost centers then only certain users are
 given access and this can be controlled by the login feature. In this code the sample username and password is test/test in login.py.  

### Technologies

* Python > 2.0
* [Flask] -- Render the main page and API calls that make DB calls
* SQLAlchemy -- Used so that any DB SQLITE or MYSQL can be used as backend
* [AngularJS] -- Front End routing, templating,etc.
* [Twitter Bootstrap] -- For RWD
* [node.js] --  For Build Process
* [Grunt] -- Minify and Concat all the assets
* [jQuery] -- For some Js features
* [D3.js] -- Data visualization
* [NVD3.js] -- Data visualization library based on D3.js
 

License
----

Open source under Apache License v2.0 (http://www.apache.org/licenses/LICENSE-2.0)

---

   [Billing App Flask Repo]: <https://git.hdtechlab.com/cloud/billing-app.git>
   [Java Utility Repo]:<https://git.hdtechlab.com/cloud/gcbillsimporter.git>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [AngularJS]: <http://angularjs.org>
   [Grunt]: <http://gruntjs.com>
   [D3.js]: <http://d3js.org>
   [NVD3.js]:  <http://nvd3.org/>
   [Flask]: <flask.pocoo.org>
   [reporting.db]: <https://git.hdtechlab.com/cloud/billing-app/blob/master/reporting.db>


