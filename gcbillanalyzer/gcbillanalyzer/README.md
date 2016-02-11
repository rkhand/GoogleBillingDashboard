<h1> Overview </h1>

This program can be used to parse the billing json files from the google storage bucket and store it in the mysql database. There is a seperate UI project that will read the entries in database and provide charts.

<h3> Setup </h3>

It requires Java 7+ and MySQL database. After downloading the project, update config.properties with proper values. If running from non-google machine, set google_account_id and google_p12_key_path.

<h3> Execution </h3>

<code>java -jar gcbillanalyzer-1.0.0-jar-with-dependencies.jar</code>