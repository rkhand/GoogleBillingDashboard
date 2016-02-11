package com.homedepot.gcbillanalyzer.utils;

import java.io.IOException;
import java.io.InputStream;
import java.util.Map;
import java.util.Properties;

public class Constants {
	public static Properties p = new Properties();
	public static String MYSQL_HOST = null;
	public static String MYSQL_USER = null;
	public static String MYSQL_AUTHZ=null;
	public static String MYSQL_DB=null;
	public static String BUCKET_NAME = null;
	public static String ARCHIVE_BUCKET_NAME = null;
	public static String GOOGLE_ACCOUNT = null;
	public static String GOOGLE_KEY = null;
	
	public static void setValues() throws IOException{
		try{
			InputStream is = Constants.class.getResourceAsStream("/config.properties");
			p.load(is);
			
		}catch(IOException fe){
			throw fe;
		}
		Map<String, String> env = System.getenv();
		for (String envName : env.keySet()) {
            if (envName.equalsIgnoreCase("GCBILLANALYZER_PORT_3306_TCP_ADDR"))                              
            	MYSQL_HOST = env.get(envName);
        }
		if (MYSQL_HOST == null)			
			MYSQL_HOST = p.getProperty("mysql_hostname");
		System.out.println("Mysql Hostname: "+ MYSQL_HOST);
		MYSQL_USER = p.getProperty("mysql_user");
		MYSQL_AUTHZ=p.getProperty("mysql_authz");
		MYSQL_DB=p.getProperty("mysql_dbname");
		BUCKET_NAME = p.getProperty("billing_bucket");
		ARCHIVE_BUCKET_NAME = p.getProperty("archive_bill_bucket");
		GOOGLE_ACCOUNT = p.getProperty("google_account_id");
		GOOGLE_KEY = p.getProperty("google_p12_key_path");
	}
}
