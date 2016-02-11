package com.homedepot.gcbillanalyzer.utils;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

import com.google.api.client.auth.oauth2.Credential;
import com.google.api.client.googleapis.javanet.GoogleNetHttpTransport;
import com.google.api.client.http.HttpTransport;
import com.google.api.client.json.JsonFactory;
import com.google.api.client.json.jackson2.JacksonFactory;
import com.google.api.services.storage.Storage;
import com.google.api.services.storage.model.StorageObject;

public class StorageUtil {
	
	private static Storage storage_client;
	private static final String APPLICATION_NAME = "gc_billing_report_generator";
	private static final JsonFactory JSON_FACTORY = JacksonFactory.getDefaultInstance();
	 
	public Storage getStorageClient() throws Exception{
	      return storage_client;
	}
	
	public StorageUtil() throws Exception {
		// Authorization.
	      Credential credential = (new GoogleAuthenticator()).authenticate();
	      HttpTransport httpTransport = GoogleNetHttpTransport.newTrustedTransport();
	      if(credential == null)
	    	  throw new RuntimeException();
		// Set up global Storage instance.
	      storage_client = new Storage.Builder(httpTransport, JSON_FACTORY, credential)
	          .setApplicationName(APPLICATION_NAME).build();
	}
	
	public void archiveFile(String fileName) throws IOException{ 
		  
		  Storage.Objects.Copy copyObject = storage_client.objects().copy(Constants.BUCKET_NAME,fileName ,Constants.ARCHIVE_BUCKET_NAME,fileName,null);				
		  StorageObject copy;
		  copy = copyObject.execute();		
		  		  
		  if( copy.getId() != null){
			  Storage.Objects.Delete deleteObject = storage_client.objects().delete(Constants.BUCKET_NAME,fileName);				  
			  deleteObject.execute();		 
			  System.out.printf("File %s successfully inserted into DB and archived.\n",fileName);					  
		  }
  	  
	}
	
	public Storage.Objects.List getFiles(String bucket_name) throws IOException{
		// List the contents of the bucket.
	    return storage_client.objects().list(bucket_name);
	}
	
	public ByteArrayOutputStream getSingleFile(String bucket_name, String fileName) throws IOException{
		Storage.Objects.Get fileObj = storage_client.objects().get(bucket_name, fileName);
		// Downloading data.
         ByteArrayOutputStream out = new ByteArrayOutputStream();
         // If you're not in AppEngine, download the whole thing in one request, if possible.
         fileObj.getMediaHttpDownloader().setDirectDownloadEnabled(false);
         fileObj.executeMediaAndDownloadTo(out);
         out.flush();
         return out;
	}

}
