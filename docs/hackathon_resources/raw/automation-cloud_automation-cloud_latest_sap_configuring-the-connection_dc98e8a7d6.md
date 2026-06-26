# Automation Cloud - Configuring the connection

- **URL:** https://docs.uipath.com/automation-cloud/automation-cloud/latest/sap/configuring-the-connection
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Automation Cloud - Configuring the connection
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
- Introduction
- About SAP Build Process Automation, Foundation add-on by UiPath
- UiPath® products and services
- Understanding the integration
- Licensing
- Language and theme synchronization
- Getting started
- Configuring the connection
- Accessing Studio in SAP Build Process Automation
- Creating the Orchestrator infrastructure
- Configuring Automation Cloud™ Robots
- Performing automations
- Creating automations
- Monitoring automations
- Using the UiPath Connector Trigger
- Extracting document data
- Approving automation tasks
- Integrating queue triggers
- Invoke SAP Build Process Automation processes via UiPath Apps
- General data protection regulation
- General data protection regulation and the right of erasure Home Open Dropdown to choose product Automation Cloud™ ​ Automation Cloud latest Configuring the connection SAP Build Process Automation, Foundation add-on by UiPath user guide

 Configuring the connection

 link Connecting SAP Build and UiPath® ​

 link
 The process of connecting an SAP environment to a UiPath tenant is performed in the SAP Build Control Tower , on the UiPath Set-Up tile. For precise steps and details, check out the SAP documentation .

 Integration Monitoring ​

 link
 Integration Monitoring focuses on monitoring communications between business-critical systems within the on-premises landscape at the customer side as well as on communications with business partners and SAP cloud products.

 To enable reliable log transfer from UiPath to SAP, you need to configure the Application Lifecycle Management (ALM) endpoints in UiPath. For more information on how to configure the endpoints, check the Managing tenants page from the Automation Cloud™ admin guide.

 Connecting SAP Task Center to UiPath® Action Center ​

 link
 Validation tasks need to be shared between SAP Task Center and UiPath Action Center. For that to happen, the two applications need to be connected through a series of parameters.

 You can configure a connection to push updates from UiPath Action Center to SAP Task Center. This connection ensures that all task updates from Action Center are actively transferred to Task Center.

 Follow these steps to set up the connection:

-
 Access your Automation Cloud™ account and create an external application. Check out the Adding an External Application page for detailed instructions.

 Important:

- Make sure to configure the following options:

- Application type : Confidential
application

- Resources :

- Resource : Orchestrator API
Access

- Application Scope(s) : OR.Tasks

- Make sure you have a reliable place to store the
App ID and App Secret generated once the application is created.

-
 Retrieve the UiPath-specific details needed for configuring the connection in SAP Task Center:

- Task SPI : https://cloud.uipath.com/&lt;uipath_account_name&gt;/&lt;uipath_tenant_name&gt;/bupproxyservice_/orchestrator/api , where:

- &lt;uipath_account_name&gt; - the organization name in your Automation Cloud™ URL

- &lt;uipath_tenant_name&gt; - the tenant name in your Automation Cloud™ URL

- Authentication : OAuth2ClientCredentials

- Client Id : the App ID generated once the external application is created

- Client Secret : the App Secret generated once the external application is created

- Token Service URL : https://cloud.uipath.com/identity_/connect/token

- Scope : OR.Tasks

- Additional Header for each call: URL.headers.ServiceUrl:

 The resulting URL to be used is as follows: URL.headers.ServiceUrl: https://cloud.uipath.com/&lt;uipath_account_name&gt;/&lt;uipath_tenant_name&gt;/orchestrator_

 .

 On this page
- Connecting SAP Build and UiPath® ​
- Integration Monitoring ​
- Connecting SAP Task Center to UiPath® Action Center ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Language and theme synchronization NEXT Accessing Studio in SAP Build Process Automation Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated