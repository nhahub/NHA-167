# Intelligent Credit Card Fraud Detection System
A data-engineering–focused project designed to analyze and detect fraudulent credit card transactions using Azure cloud services.  
The current version processes **historical data**, while future enhancements aim to build a real-time fraud detection platform.

---

## Current Project Status

The system currently operates on **pre-stored historical credit card transaction data** located within **Azure Data Lake**.

### Data Generation
A custom script, **generate_sample_csvs.py**, is used to generate high-quality sample datasets:

- `users.csv`
- `cards.csv`
- `merchants.csv`
- `transactions.csv`

These datasets are uploaded to **Azure Data Lake**, and ingested using **Azure Synapse Pipelines**.

### Data Processing & Storage
We built a complete Azure-based data engineering pipeline:

- Azure Synapse Pipelines for ingestion & transformation  
- Azure Data Lake for raw and curated layers  
- Azure Synapse SQL Data Warehouse for analytics and reporting  

### Power BI Dashboard
A Power BI dashboard is connected to the Data Warehouse and provides insights such as:

- Suspicious transactions  
- Fraud trends  
- Customer behavior patterns  
- Merchant activity  
- Transaction statistics over time  

At this stage, the system detects suspicious cases using historical data and predefined logic.

---

## Future Enhancements

We plan to evolve the project into a **real-time, bank-grade fraud detection system**.

### Bank-Specific Fraud Models
Each bank will have its own independent fraud model with:

- Unique ML thresholds  
- Personalized risk scoring  
- A dedicated decision API acting as the approval/decline engine  

This architecture allows full customization per bank.

---

### Real-Time Transaction Decision Engine
When a transaction is received, the engine will determine one of the following actions:

- **Accept** → Transaction is low-risk  
- **Decline** → Transaction is highly suspicious  
- **Require OTP** → Medium risk; customer verification required  

For OTP-based validation:

- OTP is sent to the customer  
- If confirmed → Approve  
- If rejected → Decline and flag the transaction  

---

### Automated WhatsApp Reporting System
If a transaction is declined due to suspicion:

- A WhatsApp report is automatically sent to the customer  
- The system waits for the customer’s response  
- If the customer identifies it as fraud → Escalation  
- If there is no response → Protective measures apply  

---

### Auto-Blocking Mechanism
If suspicious activity continues with no customer confirmation:

- The card is **automatically blocked after the second suspicious attempt**  
- Notifications are sent to both the customer and the fraud monitoring team  

---

### Admin Portal
A secure admin portal will allow:

- Editing fraud cases  
- Blocking suspicious merchants or locations  
- Updating fraud rules and thresholds  
- Reviewing WhatsApp reports  
- Managing user roles and permissions  

Role-based access control ensures each admin operates within their authorized scope.

---

## Summary
The current version includes:

Full Azure data pipeline (Data Lake → Synapse → Warehouse)  
Generated sample datasets  
Power BI dashboard with fraud insights  

Future versions aim to include:

ML-based fraud detection  
Real-time transaction scoring  
OTP validation  
Automated WhatsApp reporting  
Card auto-blocking  
Full admin portal  

---

## Technology Stack
- **Azure Data Lake**
- **Azure Synapse Analytics**
- **Azure Synapse Pipelines**
- **Azure SQL Data Warehouse**
- **Python** (Data Generation & Processing)
- **Power BI** (Visualization)

---

## Team Members

| Name | Role |
|------|------|
| **Mohamed Shosha** | Data Generation |
| **Abderahman Mohamed** | Data Warehouse |
| **Youstina Lotfy Hana** | Azure Synapse & Pipelines |
| **Menna Fadel** | Power BI |
| **Alaa Mohamed** | Azure Synapse & Pipelines |

---
