package com.homedepot.gcbillanalyzer.dao;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

import static com.homedepot.gcbillanalyzer.utils.Constants.*;

public class Dbconnector {
	
	
	public static Connection getConnectionObj() throws ClassNotFoundException, SQLException{
		String url = null;
		try{

			Class.forName("com.mysql.jdbc.Driver");
			  url = "jdbc:mysql://address=(protocol=tcp)(host="+MYSQL_HOST+")(port=3306)(user="+MYSQL_USER+")(password="+MYSQL_AUTHZ+")/"+MYSQL_DB;
			Connection conn = DriverManager.getConnection(url);
			return conn;
			
		}catch(ClassNotFoundException c){
			throw c;
		}
		catch(SQLException s){
			throw s;
		}
	}
	
}
