# Google Cloud Billing Dashboard

## Introduction
This application collects and displays charts of Google Cloud Billing exports to facilitate analysis of overall cloud spend.

The app consistes of 3 main components: A Database for storing and quering the line items, An import tool to pull export files off Google Storage and load to the database, and of course the Web UI that queries the database and displays the data.

### Quick Start
The easiset way to try out the system is to use [Docker](https://docs.docker.com/) and [Docker Compose](https://docs.docker.com/compose/). The following commands will install, link and run the components.

  $ docker-compose build
  $ docker-compose up

Once running you'll be able to access the app on port 80 of your docker host IP.

On a mac simply run:

  $ open "http://$(docker-machine ip default)/"



## Additional Configurations

###  Google Storage Bucket Details
1. Enable Billing Export
  - Google provides the ability to [export your billing](https://support.google.com/cloud/answer/6293835?rd=1) information to a storage bucket. The process runs nightly so you'll need to wait until it runs after you enable the feature.
2. Tell the loader where the export bucket is
  - Update gcbillanalyzer/gcbillanalyzer/src/main/resources/config.properties with the google storage bucket details

### Database Settings
1. Modify ./docker_compose.yml
  * MYSQL_ROOT_PASSWORD=password
  * MYSQL_DATABASE=db_name
  * MYSQL_USER=db_user
  * MYSQL_PASSWORD=db_password
2. Update the database connection values for the Loader and the UI Apps:
  - web/billing-app/apps/config/apps_config.py.
  - gcbillanalyzer/src/main/resources/config.properties


### Rebuild the Jar with the updated changes
Build the jar file and copy it in gcbillanalyzer folder of python application.
  1. Run the maven build on the google bill importer application in gcbillanalyzer






## License
Open source under Apache License v2.0 (http://www.apache.org/licenses/LICENSE-2.0)





