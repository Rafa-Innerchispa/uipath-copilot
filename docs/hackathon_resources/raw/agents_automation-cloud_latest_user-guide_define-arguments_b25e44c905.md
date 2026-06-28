# Agents - Defining arguments

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/define-arguments
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Defining arguments
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Defining arguments Agents user guide

 Defining arguments

 link Arguments pass runtime information into and out of an agent, just as inputs and outputs do for activities or processes. Define input and output arguments in the Data Manager panel, then reference them in the user prompt so the agent can use them at runtime.

 Define input and output arguments ​

 link

- In the Data Manager panel, open the Input or Output tab.

- For each argument, configure the Name , Type , Description , and whether it is Required .

 To generate arguments from an existing JSON payload, select Generate from payload . To switch between the property builder and JSON editor views, select the angle brackets icon.

 Note: Provide a description for every argument. An accurate description helps the agent understand how to use the argument effectively.

 Result: The argument appears in the Data Manager and is available to select from the @ picker in the user prompt.

 Reference arguments in the user prompt ​

 link
 The agent sees only arguments that are explicitly referenced in the user prompt.

- In the user prompt, enter @ and select the argument by name from the picker.

- The argument is inserted as {{argumentName}} in the stored prompt format and is substituted with its runtime value when the agent runs.

 Note: Argument names are case-sensitive. Selecting the argument from the @ picker ensures the name matches exactly.

 Result: The agent receives the argument&#x27;s value in its context window when triggered.

 Supported argument types ​

 link

- String

- Number

- Integer

- Boolean

- Object

- Array
 On this page
- Define input and output arguments ​
- Reference arguments in the user prompt ​
- Supported argument types ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Prompt editor NEXT Working with files Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated