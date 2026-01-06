# Data Governance Policies

## Microsoft Fabric – Urban Analytics Platform

### 1. Governance Objectives

The governance framework for this project was designed to ensure:

- Data reliability – consistent and trusted analytical results
- Traceability – full lineage from source systems to analytics
- Controlled access – clear separation of responsibilities
- Scalability – ability to extend governance rules without redesign
- Auditability – explainable transformations and decisions

The governance model aligns with Microsoft Fabric best practices and enterprise data platform standards.

### 2. Governance Scope

Governance policies apply to:

- Data ingestion (Bronze)
- Data transformation (Silver)
- Analytical modeling (Gold)
- Analytics & visualization layer
- Orchestration and automation
- Documentation and versioning

### 3. Medallion-Based Governance Model

Governance is enforced through layer-specific responsibilities in the Medallion Architecture.


#### 3.1 Bronze Layer – Raw Data Governance

**Purpose:**
Preserve raw source data exactly as received.

**Policies:**

- No business logic applied
- No filtering unless technically required (e.g., pagination)
- No deduplication
- No schema enforcement
- Raw timestamps preserved
- Source metadata retained (sensor_id, API identifiers, file origin)

**Rationale:**
Bronze acts as a system of record. Any future reprocessing, audits, or logic changes can always start from an untouched baseline.


#### 3.2 Silver Layer – Data Quality & Standardization Governance

**Purpose:**
Create clean, validated, and standardized datasets.

**Policies:**

- Schema normalization across heterogeneous sources
- Explicit data validation rules:
    - Null checks for critical fields
    - Logical consistency checks (e.g., pickup ≤ dropoff)
- Controlled filtering:
    - Removal of invalid or corrupt records
    - Outlier handling using statistical bounds (quantiles)
- Date normalization to UTC
- Retention of granular data where future re-aggregation may be required (e.g., air quality measurements)

**Rationale:**
Silver balances data quality with traceability.
Transformations are deterministic and explainable, but not overly aggregated.


#### 3.3 Gold Layer – Analytical Governance

**Purpose:**
Expose analytics-ready data optimized for reporting and decision-making.

**Policies:**

- Star schema modeling
- Clear separation of facts and dimensions
- Aggregation rules are applied in Silver or Gold depending on reuse and business grain stability, and are fully documented
- No row-level mutations after aggregation
- Metrics definitions frozen and versioned
- Only business-approved metrics exposed

**Rationale:**
Gold represents the single source of truth for analytics.
Changes here have direct business impact and must be deliberate.


### 4. Data Quality Governance

#### 4.1 Validation Rules

| Dataset     | Rule                               | Rationale                  |
| ----------- | ---------------------------------- | -------------------------- |
| Taxi Trips  | pickup_datetime ≤ dropoff_datetime | Logical consistency        |
| Taxi Trips  | trip_distance ≥ 0                  | Invalid physical values    |
| Air Quality | value IS NOT NULL                  | Sensor reliability         |
| FX Rates    | rate IS NOT NULL                   | Financial accuracy         |
| GDP         | yearly granularity enforced        | Macro-economic consistency |


#### 4.2 Handling Missing & Partial Data

- Missing values are not imputed by default
- Partial sensor coverage is preserved and documented
- Visualizations reflect actual data availability
- Gaps are explained in analytical commentary

**Rationale:**
Avoids introducing artificial trends or misleading correlations.


### 5. Lineage & Traceability
#### 5.1 Automated Lineage

Microsoft Fabric automatically captures lineage across:

- Dataflows Gen2
- Pipelines
- Notebooks
- Lakehouse tables
- Warehouse tables

This enables:

- End-to-end traceability
- Impact analysis
- Auditing of transformations

#### 5.2 Manual Documentation

Complementary documentation includes:

- Data Dictionary
- Transformation rationale per notebook
- Metric definitions
- Known limitations

**Rationale:**
Automated lineage shows how it was done, documentation explains why certain decisions were made.

### 6. Access Control & Security Model
#### 6.1 Role-Based Access Concept (Conceptual)


| Role          | Access                 |
| ------------- | ---------------------- |
| Data Engineer | Bronze / Silver / Gold |
| Analyst       | Gold only              |
| Business User | Aggregated Gold / BI   |
| Admin         | Full platform          |

**Note:**
RLS is conceptually defined but not enforced due to project scope.

#### 6.2 Sensitive Data Handling

- No PII present in datasets
- Open-source datasets only
- No personal identifiers stored
- Compliance risk is minimal


### 7. Change Management & Versioning
#### 7.1 Code Governance

- All transformation logic is versioned in GitHub
- Logical code separated from Fabric UI configuration
- Notebooks treated as code artifacts

#### 7.2 Schema Evolution Rules

- Bronze: no schema enforcement
- Silver: backward-compatible changes only
- Gold: schema changes require:
    - Metric redefinition
    - Documentation update
    - Downstream impact review

### 8. Orchestration & Operational Governance
#### 8.1 Pipelines

- Separate pipelines per domain:
    - Mobility
    - Air Quality
    - Economy
- Clear dependency order:
    - Bronze → Silver → Gold
- Fail-fast philosophy for transformations

#### 8.2 Scheduling

- Ingestion scheduled based on source update frequency
- Transformations triggered after successful ingestion
- No parallel Spark-intensive notebooks to avoid capacity exhaustion

### 9. Observability & Monitoring
#### 9.1 Operational Monitoring

- Fabric pipeline run history
- Notebook execution logs
- Spark capacity usage

#### 9.2 Data Monitoring

- Record counts per run
- Date range validation
- Metric sanity checks

### 10. Governance Trade-Offs & Design Decisions

| Decision                             | Reason                         |
| ------------------------------------ | ------------------------------ |
| Keep detailed measurements in Silver | Enables future re-aggregation  |
| No forced sensor completeness        | Reflects real-world conditions |
| No median metrics                    | Out of scope per requirements  |
| No hard-coded date filters           | Supports historical backfill   |
| Separate pipelines                   | Isolation & fault containment  |


### 11. Alignment with Project Requirements

This governance framework directly supports:

- Unified analytics platform
- Cross-domain correlation
- Auditable transformations
- Enterprise-ready architecture
- Microsoft Fabric best practices

### 12. Future Governance Extensions

Potential enhancements:

- Purview catalog activation
- Automated data quality checks
- Column-level lineage
- Power BI RLS enforcement
- SLA-based monitoring
- Threshold-based alerts can be added to detect sudden drops in record counts or unexpected metric deviations
