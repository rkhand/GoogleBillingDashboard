package com.homedepot.gcbillanalyzer;

import java.io.IOException;
import java.util.Date;

import com.homedepot.gcbillanalyzer.utils.Constants;
import com.homedepot.gcbillanalyzer.utils.GCUsageReportGen;

public class Main {

	public static void main(String[] args) {
		while(true){
			try {				
					initialize();
					GCUsageReportGen gen_obj = new GCUsageReportGen();					
					System.out.println("Starting to collect daily GC Usage data " + (new Date(System.currentTimeMillis()).toString()));
					Long startTime = System.currentTimeMillis();			 
					gen_obj.fetchGCUsage();
					System.out.println("Completed collecting daily GC Usage, Total time take (Seconds): "+ (System.currentTimeMillis() - startTime)/1000);
					 
			} catch (IOException e) {
				e.printStackTrace();
			} catch (Exception e){
				e.printStackTrace();
			}
			try {
				Thread.sleep(3600000); //every 1 hour
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

	}
	
	public static void initialize() throws IOException{
		Constants.setValues();
	}

}
