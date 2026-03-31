# OrchestraFlow - Pipeline Architecture

## The Process flow
The system showcases a modular, fault-tolerant approach relying on Apache Airflow context passing and conditional triggers.

### The DAG Interaction diagram
```mermaid
graph TD;
    subgraph DAG 1: ecom_ingestion_pipeline
      Start1[start_ingestion] -->|Parallel Bash| ExtSales[extract_sales_data];
      Start1 -->|Parallel Bash| ExtInv[extract_inventory_data];
      ExtSales -->|Retries handled| End1[end_ingestion];
      ExtInv --> End1;
    end

    subgraph External System
      End1 -.Writes.-> RawDisk[Local /data/raw/]
    end

    subgraph DAG 2: ecom_transformation_pipeline
      Start2[start_transform] --> TG1{TaskGroup: wait_for_data}
      TG1 --> FS1((FileSensor: Sales)) -.Polls.-> RawDisk
      TG1 --> FS2((FileSensor: Inventory)) -.Polls.-> RawDisk

      FS1 --> TG3{TaskGroup: process_sales_data}
      TG3 --> CS[clean_sales] --> QCS[quality_check_sales]
      
      FS2 --> TG4{TaskGroup: process_inventory_data}
      TG4 --> CI[clean_inventory] --> QCI[quality_check_inventory]
      
      QCS --> End2[end_transform]
      QCI --> End2
    end

    subgraph DAG 3: ecom_reporting_pipeline
      Start3[start_reporting] --> BranchDecision{BranchPythonOperator: decide_report_type}
      
      BranchDecision -->|Day >= 5| Wknd[generate_weekend_report]
      BranchDecision -->|Day < 5| Wkdy[generate_weekday_report]
      
      Wknd -.TriggerRule: MIN_1_SUCCESS.-> JoinReports[join_reports]
      Wkdy -.TriggerRule: MIN_1_SUCCESS.-> JoinReports
      
      JoinReports --> Notify[send_success_notification]
    end
```

## Description of components
1. **Mock Extractors**: Short python scripts wrapped by `BashOperator`. Useful when Airflow manages dependencies outside Python libraries (e.g. running dbt, Go binaries, Node).
2. **File Sensors**: `mode='poke'` actively monitors specific output locations preventing transformation failures if upstream systems take longer than expected.
3. **Trigger Rules**: Branching natively skips one path. `JoinReports` implements `TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS` instead of the default `all_success` to prevent the final node from being skipped.
