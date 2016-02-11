package com.homedepot.gcbillanalyzer.utils;

import java.util.Date;


public class BillingModel {
	public String getAccountId() {
		return accountId;
	}
	public void setAccountId(String accountId) {
		this.accountId = accountId;
	}
	public String getLineItemId() {
		return lineItemId;
	}
	public void setLineItemId(String lineItemId) {
		this.lineItemId = lineItemId;
	}
	public Date getStartTime() {
		return startTime;
	}
	public void setStartTime(Date startTime) {
		this.startTime = startTime;
	}
	public Date getEndTime() {
		return endTime;
	}
	public void setEndTime(Date endTime) {
		this.endTime = endTime;
	}
	public String getProjectNumber() {
		return projectNumber;
	}
	public void setProjectNumber(String projectNumber) {
		this.projectNumber = projectNumber;
	}
	public Measurements[] getMeasurements() {
		return measurements;
	}
	public void setMeasurements(Measurements[] measurements) {
		this.measurements = measurements;
	}
	public Cost getCost() {
		return cost;
	}
	public void setCost(Cost cost) {
		this.cost = cost;
	}
	private String accountId;
	private String lineItemId;
	private Date startTime;
	private Date endTime;
	private String projectNumber;
	private Measurements[] measurements;
	class Measurements{
		public String getMeasurementId() {
			return measurementId;
		}
		public void setMeasurementId(String measurementId) {
			this.measurementId = measurementId;
		}
		
		public String getUnit() {
			return unit;
		}
		public void setUnit(String unit) {
			this.unit = unit;
		}
		public double getUsageValue() {
			return usageValue;
		}
		public void setUsageValue(double usageValue) {
			this.usageValue = usageValue;
		}
		private String measurementId;
		private double usageValue;
		private String unit;

	}
	private Cost cost;
	 class Cost{
		public double getAmount() {
			return amount;
		}
		public void setAmount(double amount) {
			this.amount = amount;
		}
		public String getCurrency() {
			return currency;
		}
		public void setCurrency(String currency) {
			this.currency = currency;
		}
		private double amount;
		private String currency;
		
	}
	 private Credits[] credits;
	 public Credits[] getCredits() {
		return credits;
	}
	public void setCredits(Credits[] credits) {
		this.credits = credits;
	}
	class Credits{
		 private String creditType;
			private double amount;
			private String currency;
			public String getCreditType() {
				return creditType;
			}
			public void setCreditType(String creditType) {
				this.creditType = creditType;
			}
			public double getAmount() {
				return amount;
			}
			public void setAmount(double amount) {
				this.amount = amount;
			}
			public String getCurrency() {
				return currency;
			}
			public void setCurrency(String currency) {
				this.currency = currency;
			}
		 
	 }
}
