package com.homedepot.gcbillanalyzer.utils;

import java.io.File;
import java.util.Collections;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.googleapis.auth.oauth2.GoogleCredential;
import com.google.api.client.googleapis.compute.ComputeCredential;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.storage.StorageScopes;


public class GoogleAuthenticator {
	  
	  
	  private static HttpTransport httpTransport = null;

	  public Credential authenticate() throws Exception{
		  

		  httpTransport = GoogleNetHttpTransport.newTrustedTransport();
		  
		  //Comment this try block if testing from non-google machine
		  try{
			  
			  JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();

			  //Comment this line if using from non-google machine
			  ComputeCredential credential = new ComputeCredential.Builder(httpTransport, JSON_FACTORY)
					  .build();
			  
			  return credential;
			 
			  /*
			   //Uncomment this if using this program from non-google machine
				  try{		
					  GoogleCredential user_credential = new GoogleCredential.Builder()
					      .setTransport(httpTransport)
					      .setJsonFactory(JSON_FACTORY)
					      .setServiceAccountId(Constants.GOOGLE_ACCOUNT)
					      .setServiceAccountPrivateKeyFromP12File(new File(Constants.GOOGLE_KEY))
					      .setServiceAccountScopes(Collections.singleton(StorageScopes.DEVSTORAGE_FULL_CONTROL))
					      .build();
					  return user_credential;
				  }catch(Exception e){
					  e.printStackTrace();
			*/		  
				  
				  
				  
		  }catch(Exception e){
			  e.printStackTrace();
		  }
		  return null;
	}
	
}
