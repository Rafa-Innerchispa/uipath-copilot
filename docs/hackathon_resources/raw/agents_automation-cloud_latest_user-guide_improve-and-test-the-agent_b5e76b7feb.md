# Agents - Testing the agent

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/improve-and-test-the-agent
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Testing the agent
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Testing the agent Agents user guide

 Testing the agent

 link Now it&#x27;s time to test your agent and see how you can improve it.

-
 Navigate to the toolbar above the Studio Web designer.

-
 Select the arrow next to the debugging environment, then select Debug configuration .

-
 In the Debug configuration window, confirm the resources used in the solution and the sample input.

-
 Select Save and Run .

 Note: Debug runs have a one-hour timeout. If your agent processes large files, uses many tools or tasks, or performs multiple retries, it may reach this limit and stop before completing.

-
 Use the test output to refine the agent design.

 Evaluating the agent ​

 link
 Next, go to the Evaluation sets and Evaluators panels to review and measure your agent.

- In the Evaluation sets panel, rename the default evaluation set and add test cases with expected outcomes.

- In the Evaluators panel, add evaluators to validate the agent output.

 Each evaluation links a known input with an assertion about the output.

 For details, refer to Evaluations and Configuring simulations in evaluations .

 Calculating the Agent score [Preview] ​

 link
 Select Open health score from the right-side panel to calculate the agent score. Refer to Agent score to learn how it is calculated.

 Using Autopilot to improve your agent [Preview] ​

 link
 Select Open Autopilot from the right-side panel to receive suggestions on improving prompts, tools, and other components. Such improvements support a higher Agent Score and make your agent ready for deployment.

 On this page
- Evaluating the agent ​
- Calculating the Agent score [Preview] ​
- Using Autopilot to improve your agent [Preview] ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Building an agent in Studio Web NEXT Publishing and deploying the agent Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated