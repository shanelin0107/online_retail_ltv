# Data Preparation

## Objective
Create a reliable customer-level dataset from raw online retail transactions for KPI reporting and Tableau dashboarding.

## Preparation Workflow

### 1) Data Cleaning
- Remove transactions with missing `customer_id` for customer-level analysis.
- Validate and standardize types:
  - `invoice_date` → date/datetime
  - `quantity`, `unit_price` → numeric
- Identify abnormal records:
  - negative quantity
  - zero/negative price
  - canceled invoice patterns
- Apply business-approved filters to produce a clean base table.

### 2) Revenue Engineering
- Compute transaction revenue:
  - `revenue = quantity * unit_price`
- Validate revenue distribution and check extreme outliers.

### 3) Customer Aggregation
Aggregate cleaned transactions to one row per customer:
- `customer_ltv = SUM(revenue)`
- `order_frequency = COUNTD(invoice_no)`
- `avg_order_value = customer_ltv / order_frequency`
- `repeat_customer_flag = 1 if order_frequency > 1 else 0`

### 4) Analytical Features
- Derive `invoice_year` from `invoice_date`.
- Build `ltv_bin` categories for value distribution analysis.
- Add optional helper fields for quality checks and segmentation.

### 5) KPI Layer
Create KPI-ready fields:
- `total_customers`
- `repeat_customers`
- `repeat_customer_pct`
- `average_ltv`
- `average_repeat_ltv`

## Output Artifacts
- Clean transaction table (optional intermediate).
- Customer-level analytical table for Tableau.
- Exported file in `data/processed/` for workbook connection.

## Data Quality Considerations
- Reconcile invoice count before/after cleaning to quantify excluded records.
- Keep a simple exclusion log (missing customer, abnormal price/quantity, canceled order).
- Document any threshold-based outlier treatment.
