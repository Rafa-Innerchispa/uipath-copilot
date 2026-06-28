# Automation Cloud - API rate limits for Identity Server

- **URL:** https://docs.uipath.com/automation-cloud/automation-cloud/latest/api-guide/api-rate-limits-for-identity-server
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Automation Cloud - API rate limits for Identity Server
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
- search Search ​ Language translate English expand_more ​ Sign in automation-cloud latest false Automation Cloud™ Automation Cloud · latest - Collapse
- Getting started
- About this guide
- Getting started with External APIs
- Available resources
- API endpoint URL structure
- Enumeration List
- Authentication
- Authentication methods
- External Applications (OAuth)
- Personal Access Tokens
- Using Personal Access Tokens for API Authentication
- FAQs
- Other API access methods
- Scopes and permissions
- About scopes and permissions
- Platform Management scopes and permissions
- Platform Management APIs
- API rate limits for Identity Server
- Retrieving partitionGlobalId for API use
- Alerts
- Audit Logs
- Get audit events
- Download events
- External client
- External client — Federated credentials
- Groups
- Get All Groups
- Get Specific Group
- Delete Specific Group
- Create a New Local Group
- Get Local Group Members
- Update Group
- Access restriction policies
- Get organization access policy
- Update organization access policy
- Directory
- Search Directory
- Resolve Directory Entity
- Resolve Directory Entity by Name
- Bulk Resolve Directory Entities
- Bulk Resolve Directory Entities by Name
- Robot Account
- Get All Robot Accounts
- Delete Robot Accounts
- Get Specific Robot Account
- Delete Specific Robot Account
- Create a New Robot Account
- Update Robot Account
- Rule
- Get all rules in bulk
- Get single rule
- Create rule
- Update rule
- Delete single rule
- Delete multiple rules
- User
- Update User
- Delete Specific User
- Delete Users
- Settings
- Get Settings
- Update Settings
- Message Template
- Get Message Template
- Update a Message Template
- Get Message Template by Name
- SAML certificates
- Upload primary certificate
- Upload secondary certificate
- Switch certificates
- Get current certificate
- Delete certificate
- License Management
- Licensing product codes
- Allocate Licenses to a Group
- Get Group License Allocation with Quota
- Allocate Licenses to a Group with Quota
- Get Groups Rules with Quotas
- Get Bulk User Allocations From Group
- Allocate Licenses to a User
- User role assignments
- Export user role assignments
- Consumption
- Get Tenant Consumption Summary
- Get Tenant Consumption Summary by Tenant
- Get Tenant Consumption by Folder
- Get Tenant Daily Consumption by Service Home Open Dropdown to choose product Automation Cloud™ ​ Automation Cloud latest API rate limits for Identity Server Automation Cloud API guide

 API rate limits for Identity Server

 link Note: This feature is available for Automation Cloud only. It is not available for Automation Cloud Public Sector or Automation Cloud Dedicated.

 The Identity Service enforces rate limits on API requests to ensure consistent performance and availability for all customers. Rate limits are applied per organization and measured over a five-minute interval.

 When you exceed a rate limit, the service returns HTTP 429 (Too Many Requests) responses. Plan your integration to stay within these limits to avoid request throttling.

 Table 1. Rate limits

 HTTP method Maximum requests per 5 minute per organization GET 300 POST 24.000 PUT 160 PATCH 160 DELETE 160
 Note: All limits are evaluated in five-minute windows per organization.

 Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Platform Management scopes and permissions NEXT Retrieving partitionGlobalId for API use Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated