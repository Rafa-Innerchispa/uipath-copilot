# Agents - Getting started with conversational agents

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/conversational-agents-getting-started
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Getting started with conversational agents
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Getting started with conversational agents Agents user guide

 Getting started with conversational agents

 link This guide walks you through building your first conversational agent: a simple HR assistant that answers questions about company policies using document search.

 Prerequisites ​

 link
 Before you begin, ensure you have:

- Access to Studio Web

- An Orchestrator folder with:

- An unattended robot assigned

- A Context Grounding index with your knowledge base documents

 Tip: If you don&#x27;t have a Context Grounding index yet, you can still complete this tutorial. Your agent will respond based on its general knowledge.

 Step 1: Create the agent ​

 link

- Go to studio.uipath.com .

- Select Create New , then select Agent .

- Select Conversational .

- Describe your agent to Autopilot to generate a starter configuration. For example: &quot;An HR assistant that helps employees find information about company policies, benefits, and onboarding procedures.&quot; If you prefer not to use Autopilot, select Start fresh .

 Step 2: Configure the system prompt ​

 link
 The system prompt defines your agent&#x27;s persona and behavior. A well-crafted prompt helps the agent respond consistently and appropriately.

- In the System prompt section, define your agent&#x27;s identity and guidelines. For example:

 assignment You are a friendly HR assistant for Contoso Corporation . Your role is to help employees find information about company policies , benefits , and HR procedures .

 Guidelines :
 - Always be professional and helpful
 - If you don&#x27;t know the answer , say so
 - When citing policies , reference the specific document name
 - Keep responses concise but complete
 You are a friendly HR assistant for Contoso Corporation. Your role is to help employees find information about company policies, benefits, and HR procedures.

Guidelines:
- Always be professional and helpful
- If you don&#x27;t know the answer, say so
- When citing policies, reference the specific document name
- Keep responses concise but complete

- Select the Model for your agent. Different models offer varying capabilities and performance characteristics.

 Step 3: Add tools ​

 link
 Tools give your agent the ability to take actions and retrieve information. For this HR assistant, add the Context Grounding index you previously configured as a Context tool.

- Select Add context .

- Select your HR documents index.

- Provide a description. For example:

 assignment Provides information about company policies , benefits , and HR procedures .
 Provides information about company policies, benefits, and HR procedures.

- (Optional) Add additional tools such as:

- Analyze files : Allow users to upload documents for analysis.

- Integration Service connectors : Connect to external systems like calendar or email.

 For detailed tool configuration options, refer to the Design section.

 Step 4: Test in Debug chat ​

 link
 Before publishing, test your agent to ensure it behaves as expected.

- Select Debug then Save &amp; Debug to open the chat interface.

- Send a test message, such as: &quot;How many holidays do we have in the US?&quot;.

- Review the agent&#x27;s response and check citations (if using Context Grounding).

- View the execution trace in the History tab to see:

- LLM calls and responses

- Tool calls with arguments and outputs

- If the response is good, select Add to evaluation set to save this conversation for future testing.

 Step 5: Publish and deploy ​

 link
 Once you&#x27;re satisfied with your agent&#x27;s behavior, publish it to make it available to users.

- Select Stop in the top toolbar to stop debug execution.

- Rename your Solution and Agent in the Explorer to &quot;HR Assistant&quot;.

- Select Publish in the top toolbar.

- Choose &quot;Orchestrator Tenant&quot; as the Location.

- Select Publish .

 The publish process will begin and you will receive a message once the package is ready to be deployed.

- Select Check package in the message.

- Select Deploy package (rocket icon on the far right).

- Choose the target Orchestrator folder (must have unattended robot account assigned).

- Select Activate immediately .

- Select Deploy .

 Your agent is now published and deployed and available through Instance Management.

 Step 6: Access your agent ​

 link
 After publishing, you can interact with your agent in several ways:

- Instance Management : Go to Agents &gt; Deployed agents in Automation Cloud and select Chat on your Conversational agent.

- Autopilot for Everyone : Access your agent from the Autopilot picker dropdown.

- Teams or Slack : If configured, interact with your agent through the Autopilot plug-in.

 You&#x27;ve built and deployed your first conversational agent. To learn more:

- Design : Configure advanced options like escalations, agent memory, and model selection

- Evaluation : Create comprehensive test suites for your agent

- Observability : Monitor performance and collect user feedback

- Licensing : Understand consumption and pricing for your deployment
 On this page
- Prerequisites ​
- Step 1: Create the agent ​
- Step 2: Configure the system prompt ​
- Step 3: Add tools ​
- Step 4: Test in Debug chat ​
- Step 5: Publish and deploy ​
- Step 6: Access your agent ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Conversational agents NEXT Licensing for conversational agents Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated