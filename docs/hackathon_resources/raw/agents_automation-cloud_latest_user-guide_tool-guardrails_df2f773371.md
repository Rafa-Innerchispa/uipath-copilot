# Agents - Custom guardrails

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/tool-guardrails
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Custom guardrails
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Custom guardrails Agents user guide

 Custom guardrails

 link Custom guardrails provide a mechanism to control unexpected behaviors within tool calls deterministically. They allow developers to configure conditions for human intervention and ensure that escalations occur precisely when defined conditions are met.

 Briefly, the role of guardrails is to:

- Address unpredictable tool call inputs and outputs at runtime.

- Reduce the need for human-in-the-loop (HITL) interventions for correction and validation tasks.

- Enable developers to create custom rules at the individual tool level.

 How it works ​

 link
 You define guardrails for each agent tool, as follows:

- There can be one or more guardrails per tool.

- Each guardrail contains one or more rules and one action. Rules are evaluated against the inputs and outputs of the tool.

- An action is triggered when all rules are met. The action can happen before and/or after tool execution.

 Guardrails are displayed in the Properties panel for every type of tool (automations, activities, or other agents). The Guardrail builder is where you define the list of rules that trigger the guardrail and the action to be applied when all the rules are met.

 At runtime, guardrails are checked from top to bottom in the order they appear in the list. You can reorder guardrails as necessary by a drag and drop action using the menu icon on the left.

 Use the Enable guardrail for evaluations option to apply the selected guardrail during evaluation runs as well.

 Configuring guardrails ​

 link
 To configure guardrails for a tool:

- Add any tool to your agent.

- Select the tool and open the Properties panel.

- In the Custom guardrail builder , set the guardrail name and description.

- Next, configure the rule and action types.

- Select Save . Tools with guardrails are marked with a shield icon.

 Figure 1. An activity tool with guardrails applied

 Rule types ​

 The following rule types are available:

- Always enforce the guardrail (default) – This guardrail always triggers the action regardless of input or output. It is applicable to the agent input (pre-execution), output (post-execution), or both (pre and post-execution).

- String – This guardrail applies to available input and output fields. The rule is applicable to string fields, including nested JSON fields, and supports various operators (contains, starts with, ends with, equals, is empty, etc.)

- Number – This guardrail applies to available input and output fields. The rule is applicable to number fields, including nested JSON fields, and supports various operators (contains, starts with, ends with, equals, is empty, etc.).

- Boolean – This guardrail applies to available input and output fields. The rule is applicable to boolean fields, including nested JSON fields, and supports the Equals operator, with True or False values.

 Action types ​

 For each rule, you enforce the action to occur when all the rules are met.

 The following action types are available:

- Log – Sets a severity level for logging. This action is useful for sending custom events for dashboard monitoring

- Filter – Removes selected fields from the input and/or output of a tool, as follows:

-
 Inputs: Selected fields are not sent to the tool API request.

-
 Outputs: Selected fields are not returned to the agent.

 Note: The quality of the agent may be impacted if critical information is filtered out.

- Block – Prevents tool execution when conditions are met. When using this option, you must provide a reason for blocking. Blocking a tool can result in agent failure.

- Escalate – Assigns an escalation to a user through a compatible escalation app.

 Executing guardrails ​

 link
 After running the agent, the output panel displays:

- The successful execution status.

- The presence of guardrails in the trace.

- The details of applied or skipped guardrails.

 Using an escalation app for guardrails ​

 link
 The Escalate action requires a compatible action app. A template is available in the UiPath Marketplace under the following name: Agent Tool Guardrail Escalation App .

 To make the app available for guardrails, take the following steps:

- Download the app template from Marketplace and import the .uip file into a new Studio project. For details, see Importing app projects in the Studio Web user guide.

- You can add new controls and events to the app, but do not change the underlying action schema. Altering the schema renders the app incompatible with guardrail escalations.

- Publish the app, as described in Publishing app projects .

- Go to Orchestrator and deploy the app in a shared folder, as described in Deploying app projects .
Make sure the folder has serverless robots available, to prevent errors when running the escalation.

- Return to your agent and select the recently deployed app for your guardrails.
 On this page
- How it works ​
- Configuring guardrails ​
- Rule types ​
- Action types ​
- Executing guardrails ​
- Using an escalation app for guardrails ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Building effective agent tools NEXT Configuring simulations for agent tools Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated