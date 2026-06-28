# Document Understanding - Automations in Document Understanding™

- **URL:** https://docs.uipath.com/document-understanding/automation-cloud/latest/user-guide/automations-in-document-understanding
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Document Understanding - Automations in Document Understanding™
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
-
- search Search ​ Language translate English expand_more ​ Sign in document-understanding latest false Document Understanding Automation Cloud · latest - Collapse
- Overview
- About Document Understanding™
- Introduction
- Document Understanding™ migration to UiPath® IXP
- Document types
- Fundamental capabilities
- Key concepts
- Document Understanding modern projects feature availability
- Getting started
- Choosing the deployment type
- Enable Document Understanding™
- Role-based access control
- Choosing the project type
- Migrating classic projects
- Choosing the automation type
- Document Understanding Process template
- Building models
- Introduction
- Create a project
- Trainable splitter (Preview)
- Import documents
- Build
- Measure
- Publish
- Migrating modern projects
- Monitor
- UiPath® Helix Extractor 1.0
- Using the new UiPath Helix Extractor 2.0 (Preview)
- Infrastructure
- Known limitations
- Consuming models
- Automations in Document Understanding™
- Activities
- Create a new automation starting from a file
- API calls
- Generative features
- Consuming models from different environments
- Model Details
- Public endpoints for Automation Cloud and Test Cloud
- Public endpoints for Automation Cloud and Test Cloud Public Sector
- Pre-trained document types
- 1040 - document type
- 1040 Schedule C - document type
- 1040 Schedule D - document type
- 1040 Schedule E - document type
- 1040x - document type
- 3949a - document type
- 4506T - document type
- 709 - document type
- 941x - document type
- 9465 - document type
- ACORD125 - document type
- ACORD126 - document type
- ACORD131 - document type
- ACORD140 - document type
- ACORD25 - document type
- Bank Statements - document type
- Bills Of Lading - document type
- Certificate of Incorporation - document type
- Certificate of Origin - document type
- Checks - document type
- Children Product Certificate - document type
- CMS 1500 - document type
- EU Declaration of Conformity - document type
- Financial Statements - document type
- FM1003 - document type
- I9 - document type
- ID Cards - document type
- Invoices - document type
- Invoices2 - document type
- Invoices Australia - document type
- Invoices China - document type
- Invoices Hebrew - document type
- Invoices India - document type
- Invoices Japan - document type
- Invoices Shipping - document type
- Packing Lists - document type
- Payslips - document type
- Passports - document type
- Purchase Orders - document type
- Receipts - document type
- Receipts2 - document type
- Receipts Japan - document type
- Remittance Advices - document type
- UB04 - document type
- US Mortgage Closing Disclosures - document type
- Utility Bills - document type
- Vehicle Titles - document type
- W2 - document type
- W9 - document type
- Supported languages
- Overview
- OCR
- ML models and capabilities
- Insights dashboards
- AI units consumption dashboards
- [Preview] AI units consumption overview
- IxP AI Unit consumption dashboard
- FAQ and troubleshooting
- Data and security
- Customer-Managed Keys
- Data residency
- Data storage
- Legal information
- Logging
- Audit logs
- Licensing
- API Key
- Cloud and on-premises usage
- Metering and charging logic (Unified Pricing)
- Metering and charging logic (Flex Plan)
- How to
- Annotate documents
- Tables and group table rows
- Checkboxes and signatures
- Annotation best practices
- Classify documents automatically
- Start a training run
- Retrain extractors
- Train a classifier
- Evaluate project success
- Troubleshooting
- About troubleshooting
- Moving Document Understanding™ modern projects between tenants or organizations Home Open Dropdown to choose product Document Understanding ​ Automation Cloud latest Automations in Document Understanding™ Document Understanding user guide

 Automations in Document Understanding™

 link There are several ways in which you can consume Document Understanding TM capabilities:

- The DocumentUnderstanding.Activities package is available in Studio Web, Studio X, and Studio Desktop and is pre-configured for you either when you create a new automation starting from a file, or if you continue your journey after publishing a project version.

- Using the IntelligentOCR package, which is designed for Windows and Windows Legacy projects, and pre-configured in the Document Understanding process template.

- Using cloud API calls, consuming Document Understanding as a service via the programming language of your choice.

 Choosing the right automation ​

 link
 Check the following table to select the optimal automation method that aligns efficiently with your needs and works best for your projects.

 Table 1. Choosing automations
   IntelligentOCR activities package DocumentUnderstanding.Activities package Document Understanding Cloud APIs Deployment

- Automation Cloud™ and Test Cloud

- Automation Suite

- Standalone

- Automation Cloud™ and Test Cloud

- Automation Suite

- Automation Cloud™ and Test Cloud

- Automation Suite

 Best suited for RPA developers

- RPA developers

- Citizen developers

 Users with previous programming experience Integrated development environment (IDE) Studio Desktop

- Studio Desktop

- Studio X

- Studio Web

 IDE of your choice Benefits

- Flexibility
- You can modify the taxonomy and extraction results at runtime using custom code.

- Extensible and open framework
- You can bring your own classifier, extractor, or OCR engine using the respective interfaces.

- You have full control over the configuration as an RPA developer.

- Fully compatible with the Document Understanding Process Template, which is based on the REFramework. This enables faster development using a standardized, best-practice workflow.

- Ease of adoption:
- Easy to use, available on cloud, no setup required for consuming out-of-the-box models.

- Can be consumed using the Create Automation option in Document Understanding and Marketplace.

- Suggested by UiPath® Autopilot TM in workflows.

- Seamlessly integrated with Document Understanding modern projects, isolated configuration in a Document Understanding project, enabling reusability.

- Relying on Document Understanding cloud APIs, leading to quicker bug fixes.

- Single input/output object, Document Data .

- Not dependent on a particular technology.

- Can be consumed from cloud or on-premises environments.

- Executing without the need of a robot.

 Drawbacks

- Complex configuration, reducing reusability

- Passing explicit arguments from one activity to the other repeatedly:
- Taxonomy

- Document Object Model

- Text

- Classification reults

- Extraction results

 Compared to IntelligentOCR, there are some missing features, which are planned to be added:

- Splitting

- Taxonomy Manager Business Rules

- Support for multiple extraction methods per document type

- Requires previous programming experience to be adopted.

 Use case Use this for complex Document Understanding scenarios that require high flexibility and full control over the extraction pipeline.

 Use this package if you are just getting started with Document Understanding. Use for new automations relying on:

- Modern projects

- Generative capabilities

- Out-of-the-box specialized models

 Use API calls to integrate Document Understanding into your applications and systems, including microservices or SaaS architectures.

 On this page
- Choosing the right automation ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Known limitations NEXT Activities Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated