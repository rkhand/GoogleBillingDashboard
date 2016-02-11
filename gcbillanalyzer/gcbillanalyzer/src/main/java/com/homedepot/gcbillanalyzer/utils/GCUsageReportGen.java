package com.homedepot.gcbillanalyzer.utils;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

import com.google.api.services.storage.Storage;
import com.google.api.services.storage.model.StorageObject;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.homedepot.gcbillanalyzer.dao.Dbconnector;

public class GCUsageReportGen {
	 	 
	public void fetchGCUsage() throws Exception{
		 
		 List<BillingModel[]> list_of_bills = null;
			try {
				StorageUtil storageUtil = new StorageUtil();
				Storage.Objects.List listObjects = storageUtil.getFiles(Constants.BUCKET_NAME);
			     
			      com.google.api.services.storage.model.Objects objects = null;
			      do {
			    	  
			    	  try{
			    		objects = listObjects.execute();
				        List<StorageObject> items = objects.getItems();
				        if (null == items) {
				          break;
				        }
				        
				        //Iterate through each json files and insert entries in DB
				        for (StorageObject object : items) {
				          list_of_bills = new ArrayList<BillingModel[]>();    
				          System.out.printf("Processing file :%s \n",object.getName());
				          ByteArrayOutputStream fileObjStream =storageUtil.getSingleFile(Constants.BUCKET_NAME, object.getName());      			          			          
				          list_of_bills.add(parseJson(fileObjStream));	
				          updateReportingDb(list_of_bills);		
				          storageUtil.archiveFile(object.getName());
				        }
				        listObjects.setPageToken(objects.getNextPageToken());
			    	  }catch(Exception e){
			    		  e.printStackTrace();
			    		  continue;
			    	  }
			      } while (null != objects.getNextPageToken());
			      
			    } catch (IOException e) {
			    	throw e;
			    } 			  
	 }
	 
	 private BillingModel[] parseJson(ByteArrayOutputStream fileObjStream) throws Exception{

         int i=0;
         BillingModel[] bill_items = null;
         try{
        	 
        	 JsonParser parser = new JsonParser();			       
	          JsonArray array = parser.parse(fileObjStream.toString()).getAsJsonArray();

	          bill_items = new BillingModel[array.size()];
	          for(JsonElement e:array){
	        	  bill_items[i] = new BillingModel();
	        	  JsonObject obj = e.getAsJsonObject();
	        	  Gson gson = new Gson();
	        	  bill_items[i].setAccountId(gson.fromJson(obj.get("accountId"),String.class));			        	  
	        	  bill_items[i].setLineItemId(gson.fromJson(obj.get("lineItemId"),String.class).substring(25));
	        	  Date startTime = new GsonBuilder().setDateFormat("yyyy-MM-dd'T'HH:mm:ssX")
	        			  .create().fromJson(obj.get("startTime"),Date.class);

	        	  bill_items[i].setStartTime(startTime);
	        	  bill_items[i].setEndTime(new GsonBuilder().setDateFormat("yyyy-MM-dd'T'HH:mm:ssX").
	        			  create().fromJson(obj.get("endTime"),Date.class));
	        	  String project_id = gson.fromJson(obj.get("projectNumber"),String.class);
	        	  if (project_id == null)
	        	  {

	        		  project_id = "Not Available";
	        	  }else{
	        		  project_id = "ID-"+project_id;
	        	  }
	        	  bill_items[i].setProjectNumber(project_id);

	        	  JsonArray measurements =obj.get("measurements").getAsJsonArray();
	        	  BillingModel.Measurements[] bill_measures = new BillingModel.Measurements[measurements.size()];

	        	  int j=0;
	        	  for(JsonElement a:measurements){
	        		  bill_measures[j] = bill_items[i]. new Measurements();
	        		  JsonObject obja = a.getAsJsonObject();
	        		  Gson gsona = new Gson();
	        		  bill_measures[j].setUsageValue(gsona.fromJson(obja.get("sum"),double.class));
	        		  bill_measures[j].setUnit( gsona.fromJson(obja.get("unit"),String.class));
	        		  j++;
	        	  }
	        	  bill_items[i].setMeasurements(bill_measures);
	        	  BillingModel.Cost cost_obj = gson.fromJson(obj.get("cost"),BillingModel.Cost.class);

	        	  if(cost_obj.getAmount() == 0.0000d ){

	        		  continue;
	        	  }
	        	  double finalCost = cost_obj.getAmount();


	        	  //check if there were any credits

	        	  try{
	        		  JsonElement creditsobj = obj.get("credits");
	        		  if(creditsobj != null){
	        			  JsonArray credits = creditsobj.getAsJsonArray();
	        			  BillingModel.Credits[] bill_credits = new BillingModel.Credits[credits.size()];
	        			  int k = 0;
	        			  for(JsonElement creditobj: credits){
	        				  bill_credits[k] = bill_items[i]. new Credits();
	        				  JsonObject creditJson = creditobj.getAsJsonObject();
	        				  Gson creditgson = new Gson();
	        				  double creditamount = creditgson.fromJson(creditJson.get("amount"),double.class);
	        				  bill_credits[k].setAmount(creditamount);
	        				  //bill_credits[k].setCreditType(creditgson.fromJson(creditJson.get("creditId"),String.class));
	        				  //bill_credits[k].setCurrency(creditgson.fromJson(creditJson.get("currency"),String.class));
	        				  finalCost = finalCost + creditamount;
	        				  k++;
	        			  }
	        		  }
	        	  }catch(Exception ex){
	        		  ex.printStackTrace();
	        		  continue;
	        	  }
	        	  cost_obj.setAmount(finalCost);
	        	  bill_items[i].setCost(cost_obj);

	        	  i++;
	          }   
         }catch(Exception e)
         {
        	 throw e;
         }
         return bill_items;
	 }
	 
	 
	 private void updateReportingDb(List<BillingModel[]> bill) throws ClassNotFoundException, SQLException{
		 Connection conn = Dbconnector.getConnectionObj();
		 if (conn == null)
			 return;
			// create a sql date object so we can use it in our INSERT statement

		 try{
			 List<BillingModel[]> list_of_bills = bill;
			 if(list_of_bills == null)
				 return;
			 for(BillingModel[] bill_items:list_of_bills){

				 for(BillingModel item:bill_items){
					 try{	 
						 // the mysql insert statement
						 String query = "INSERT INTO `reporting`.`usage`(`usage_date`,`cost`,`project_id`,`resource_type`,`account_id`,`usage_value`,`measurement_unit`)"
								 + "VALUES(?,?,?,?,?,?,?);";
						 
						 // create the mysql insert preparedstatement
						 PreparedStatement preparedStmt = conn.prepareStatement(query);
						 preparedStmt.setDate(1,new java.sql.Date(item.getStartTime().getTime()));
						 preparedStmt.setDouble(2, item.getCost().getAmount());
						 preparedStmt.setString(3, item.getProjectNumber());
						 preparedStmt.setString(4, item.getLineItemId());
						 preparedStmt.setString(5, item.getAccountId());
						 preparedStmt.setDouble(6, (item.getMeasurements())[0].getUsageValue());
						 preparedStmt.setString(7, (item.getMeasurements())[0].getUnit());

						 // execute the preparedstatement
						 preparedStmt.execute();
					 }catch(NullPointerException ne){
						 continue;
					 }

				 }		   
			 }

			 conn.close();

		 } catch (SQLException e) {
			 throw e;
		 }
		 finally{
			 if (conn != null)
			 {
				 try{
					
					 conn.close();
					 

				 }catch(Exception e){}
			 }
		 }
	 }
	 
	 /*
	 private void generateCSVReport(Date dt) throws ClassNotFoundException, SQLException{
		 Connection conn = Dbconnector.getConnectionObj();
		 SimpleDateFormat simpledt = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
		 String filename = "GCUsage-"+simpledt.format(Calendar.getInstance().getTime()) + ".csv";
		 Statement stmt;
	     String query;
	     
	     File newFile = new File(filename);
	     BufferedWriter writer = null;
	     
	        try {
	        	 Calendar previousDT = Calendar.getInstance();
	 			previousDT.setTime(dt);
	 			previousDT.add(Calendar.DAY_OF_MONTH, -1);
	 			Calendar nextDT = Calendar.getInstance();
	 			nextDT.setTime(dt);
	 			nextDT.add(Calendar.DAY_OF_MONTH, 1);
	 			 
	            stmt = conn.createStatement(ResultSet.TYPE_SCROLL_SENSITIVE,
	                    ResultSet.CONCUR_UPDATABLE);
	             
	            //For comma separated file
	            query = "SELECT project_id,resource_type,usage_date,sum(cost) as cost,sum(usage_value) as usage_value, "
	            		+ "measurement_unit FROM reporting.`usage` where usage_date > '"+ simpledt.format(previousDT.getTime())+"' group by project_id,resource_type;";
	            //"SELECT id,text,price into OUTFILE  '"+filename+ "' FIELDS TERMINATED BY ',' FROM testtable t";
	            ResultSet rs = stmt.executeQuery(query);
	            if(rs != null)
	            	writer =new BufferedWriter(new FileWriter(newFile));
	            writer.write("Project_ID,Resource_Type,Usage_Date,Dollar_Cost,Usage,Usage_Unit");
	            writer.newLine();
	            writer.newLine();
	            while(rs.next()){
	            	writer.write( rs.getString(1) + ","+rs.getString(2) +","+rs.getDate(3)+","+rs.getDouble(4)+","+rs.getDouble(5)+","+rs.getString(6));
	            	writer.newLine();
	            	writer.flush();
	            }
	            if(writer != null)
	            	writer.close();
	            
	        } catch(Exception e) {
	            e.printStackTrace();
	            stmt = null;
	        }
		 
	 }
	 */
	 

	}


