# Agents - IXP

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/ixp
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - IXP
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
- search Search ​ Language translate English expand_more ​ Sign in agents latest false Agents Automation Cloud · latest - Collapse
- Getting started
- About this guide
- About agents
- Agent capabilities in the UiPath Platform™
- Agents feature availability
- UiPath Agents in Studio Web
- About UiPath Agents
- Licensing
- Getting started with UiPath Agents
- Agents workspaces
- Prerequisites
- Agents governance
- Data residency and supported models
- Limitations
- Building an agent in Studio Web
- Testing the agent
- Publishing and deploying the agent
- Running the agent
- Using agent templates
- Autopilot for Agents
- Autopilot for Agents tools
- Coded agents in Studio Web
- Clone a low-code agent as coded
- Running agents
- Conversational agents
- Getting started with conversational agents
- Licensing for conversational agents
- Designing conversational agents
- Evaluating conversational agents
- Deploying conversational agents
- Instance Management
- Autopilot for Everyone
- Microsoft Teams
- Dedicated Microsoft Teams App
- Slack
- IFrame and Apps embedding
- Anonymous access setup
- UiPath TypeScript SDK
- Observability for conversational agents
- Limitations and FAQ
- Best practices
- Agents and workflows
- Best practices for building agents
- Choosing the best model for your agent
- Best practices for publishing and deploying agents
- Best practices for context engineering
- Best practices for DeepRAG and Batch Transform: JIT vs. index-based strategies
- Prompts
- Prompt editor
- Defining arguments
- Working with files
- Guardrails
- Out-of-the-box guardrails
- Monitoring guardrails
- Tools
- Activities
- Agents
- API workflows
- Automations
- IXP
- MCP Servers
- MCP compliance guidelines
- Built-in tools
- Analyze files
- Batch transform
- DeepRAG
- Building effective agent tools
- Custom guardrails
- Configuring simulations for agent tools
- Contexts
- Escalations
- Evaluations
- Agent traces
- Agent score
- Managing UiPath agents
- UiPath Coded agents
- About coded agents
- Licensing for coded agents
- Building and deploying coded agents
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest IXP Agents user guide

 IXP

 link Note: Access to IXP as a tool depends on the cloud platform you use. For details, refer to Agents feature availability .

 Agents can use custom-built IXP models for document data extraction. By integrating IXP as a tool, agents can delegate the extraction tasks to state-of-the-art extraction models and use the output for further reasoning or subsequent tool calls. By integrating IXP as a tool, agents can interpret document content, extract high-confidence data points, and use these extracted values in reasoning or subsequent tool calls.

 Additionally, you can use the Document Validation Station interface as an escalation mechanism to review and validate extractions before or after the agent’s execution.

 Prerequisites ​

 link
 Before adding IXP as a tool:

- Ensure you have an IXP project and a published model. For details, refer to Creating a project .

- The models must have a deployment tag to be made available to the agent (staging or live). For details, refer to Managing published projects .

- If your IXP model consumes file inputs, confirm your agent is configured to pass or produce attachments as input arguments.

 Adding an IXP project as a tool ​

 link

-
 From your agent canvas, open the Toolbox panel.

-
 Select IXP .

-
 Choose your IXP project and select the published model.

-
 Specify the model version, identified by tag (staging or live).

-
 Provide a tool description that aligns with the intended system and user prompts for the agent.

6. Open the taxonomy viewer to inspect the fields your model extracts. Use this to guide how your agent should interpret or act on specific field groups or values.

7. If your agent processes document files:

- Define an input argument of type File in the Data Manager panel. Alternatively, use another tool or workflow that outputs a file attachment, which the IXP tool can consume.

- Optionally, add a specific description for the attachment field if the agent handles multiple files during runtime.

 Validation Station escalation ​

 link
 You can enable human validation of extracted data through Document Validation Station. Validation Station is an out-of-the-box action app that lets you review, validate, and modify extractions executed by the model. As with other escalations, any data modified by the reviewer is sent back to the agent as it continues its trajectory.

 Note: Decide whether to trigger the validation station mid-trajectory (before other actions) or after the agent completes execution.

 To configure:

- Add an escalation node to your agent.

- Choose escalation type Document Validation Task .

- Link it to the specific IXP tool instance.

- Select a storage bucket for validation results (used for auditing and re-use).

- Optionally, define a task title and priority.

 Testing and debugging ​

 link
 After you&#x27;re done configuring your agent, run the agent in Debug mode and review traces for the IXP tool execution. The trace output includes the full schema defined in your IXP project, showing input attachments, field groups, and confidence scores.

 If you&#x27;ve added a validation escalation, check out the trace metadata. It includes a link to the Action Center task, automatically created for validation.

 In Action Center, assign the task to yourself, then check extracted fields, view confidence scores, and manually update values, if needed. When submitted, the updated data is sent back to the agent for continued processing.

 On this page
- Prerequisites ​
- Adding an IXP project as a tool ​
- Validation Station escalation ​
- Testing and debugging ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Automations NEXT MCP Servers Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated