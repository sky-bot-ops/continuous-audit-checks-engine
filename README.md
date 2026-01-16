# Continuous Audit Checks Engine

A lightweight audit analytics tool that runs rule based checks on transaction extracts and produces an Excel-based exception report for fast and reliable review.

## Purpose
Audit and compliance teams frequently receive large transaction extracts from ERP systems such as SAP and Oracle. Manual review of these datasets is time consuming and error prone.

This tool automates common audit checks and generates audit ready exception outputs, helping teams reduce manual effort, improve consistency, and accelerate audit timelines.

## Checks included
- Negative transaction amounts  
- Missing or blank vendor names  
- Weekend postings  
- Duplicate invoice IDs  

## Input format (CSV)
Expected columns:
- `invoice_id`  
- `vendor`  
- `amount` 
- `posting_date` (YYYY-MM-DD)

## Output
Generates an Excel exception report containing:
- `sample_input` – first rows of the source dataset  
- `exceptions` – flagged records with the corresponding rule name  
- `summary` – count of exceptions per rule  
