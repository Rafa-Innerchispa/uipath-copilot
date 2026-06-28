# Agents - Escalations

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-escalations-and-agent-memory
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Escalations
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Escalations Agents user guide

 Escalations

 link About escalations ​

 link
 As a developer, you may want to give your agent a way to validate business case details with a human before running a tool, or to request manual assistance if they run into issues. In other cases, there may be business exceptions in a process when you want an agent to have a human make an approval or some other type of decision.

 This is where escalations come in. Escalations are powered by Action apps in Action Center and give developers the tools to design and configure human-in-the-loop events in agent execution. Check out the Creating agent escalations with Action apps quickstart guide.

 Configuring escalations ​

 link
 You can create multiple escalations for different situations where an agent may require human assistance.

 Use the Properties panel to add and configure the escalation.

- Select an action app from your available resources. You must first deploy an app to your tenant.

- Add a Prompt to help the agent know when to use the escalation. The prompt acts as a triggering condition, guiding the agent on when this escalation is appropriate.

- In the Assignments section, add the escalation Recipient . You can assign an escalation to a specific user in your UiPath® organization.

- In the Inputs section, define the fields and values the agent will pass to the Action App. This corresponds to the Action Schema, the required fields in the selected app.
For each field, add a description to assist the agent in understanding what kind of value should be passed. These descriptions improve the agent’s ability to infer and pre-fill values based on context when raising the escalation.

- In the Outcome behavior section, specify how each outcome should be handled by the agent after an escalation was resolved. For every outcome defined in the Action App:

- Select Continue if the agent should resume its process using the inputs provided by the escalation assignee.

- Select End if the agent should terminate as soon as the outcome is selected. This setting lets you control the agent’s autonomy following human intervention.

 After you create an escalation, you can reference it from the system prompt. Use explicit instructions, such as: &quot;Before using Tool X, be sure to raise the Human Confirmation escalation and include the details for the action you&#x27;re proposing&quot;.

 Note: Agents do not support the In/Out argument type for Action Schema properties.

 On this page
- About escalations ​
- Configuring escalations ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Contexts NEXT Evaluations Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated