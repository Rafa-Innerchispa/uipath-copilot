# Agents - Out-of-the-box guardrails

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/out-of-the-box-guardrails
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Out-of-the-box guardrails
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Out-of-the-box guardrails Agents user guide

 Out-of-the-box guardrails

 link Out-of-the-box guardrails are predefined, ready-to-use safeguards that you can enable for your agents without any custom configuration or coding. They provide immediate protection against common risks such as sensitive data exposure and prompt injection attacks, helping you build secure and trustworthy agents faster.

 Prerequisites ​

 link
 Out-of-the-box guardrails are available on the following licensing plans:

- Flex Pricing plan: Enterprise – Standard and Advanced tiers.

- Unified Pricing plan: Standard, Enterprise, App Test Platform Standard, App Test Platform Enterprise.

 If the required entitlements are not enabled for your organization, the corresponding guardrail options will not appear in the UI. If you have already configured guardrails and the necessary entitlements are later disabled, your agents will simply skip those guardrails during execution, they will not cause agent runs to fail.

 Note: Access to out-of-the-box guardrails also depends on the cloud platform you use. For details, refer to Agents feature availability .

 You can set up and configure out-of-the-box guardrails directly from your agent’s settings. The configuration applies automatically at runtime, based on the selected scope and action type.

- Open the Agent settings.

- In Studio Web , open your agent.

- Open the Agent settings panel.

- Go to the Guardrails tab and select Add guardrails .

- Choose a guardrail type from the available predefined guardrails:

- PII detection – Identifies and blocks sensitive information such as email addresses or physical addresses. This guardrail uses Azure Cognitive Services.

- Prompt injection – Detects and blocks malicious or manipulative prompts during LLM interactions. This guardrail uses Noma Security. Noma services are hosted in the United States, so data processed by these two guardrails may be handled outside your tenant’s region.

- Harmful content – Detects hate speech, self-harm, sexual content, and violence in LLM interactions. This guardrail uses Azure AI Content Safety.

- Intellectual property protection – Detects intellectual property leakage in model-generated text and code. This guardrail uses Azure AI Content Safety.

- User prompt attacks – Detects and blocks user prompt attacks, such as jailbreak or prompt injections. This guardrail uses Azure AI Content Safety.

 Configuring a PII detection guardrail ​

 link
 PII detection identifies and flags sensitive personal information — such as email addresses, phone numbers, and physical addresses — across agent interactions. You can apply it to agent prompts, LLM calls, or tool data. This guardrail uses Azure Cognitive Services.

- Add the PII detection guardrail to your agent.

- Define the guardrail details. Fill in the following fields:

- Guardrail name – Enter a descriptive name for this guardrail.

- Guardrail description – Explain what it detects or where it applies.

- Select entities to detect. From the Entities to detect dropdown, choose the types of information you want to monitor (for example, email, phone, or address).

- Set a detection threshold. For each selected entity, define a Detection threshold between 0 and 1. A higher threshold makes detection stricter (fewer false positives), while a lower threshold makes it more sensitive.

- Choose the scopes. Select where you want the guardrail to apply:

- Agent – Checks the agent’s user prompt and output.

- LLM calls – Checks LLM requests and responses.

- Tools – Checks tool input and output data. You can select one or more scopes to apply the same detection logic across multiple stages of execution.

- If you select the Tools scope, choose one or more tools from the Select tools list. This lets you reuse the same guardrail across multiple tools in the same agent.

- Define the Action type . Configure how the system should respond when PII is detected:

- Log – Records the event without interrupting agent execution. The Severity level sets the importance level for the log entry:

- Info – For general information or low-impact findings.

- Warning – For potential risks that don’t block execution.

- Error – For critical detections that require review.

- Block – Stops the agent or tool execution when the guardrail is triggered.

- Block reason – Provide a brief explanation for blocking the action (for example, “Detected PII data in tool output”).

- Escalate – Sends an escalation when a violation occurs.

- Assign app to – Choose the escalation target type: a specific user, a defined user group, or an external address.

- Recipient – Search and select the recipient (name or email).

- Action app – Select the application that will handle the escalation.

- Enable for evaluations. Toggle Enable guardrail for evaluations to run this guardrail during agent testing or evaluation.

- Save the guardrail. Once configured, the guardrail automatically monitors all LLM requests and responses and blocks execution when prompt injection attempts are detected.

 Configuring a Prompt injection guardrail ​

 link
 Prompt injection detection monitors LLM interactions for malicious or manipulative instructions that attempt to override the agent&#x27;s intended behavior. This guardrail uses Noma Security.

- Add the Prompt injection guardrail to your agent.

- Define the guardrail details. Fill in the following fields:

- Guardrail name – Enter a descriptive name for this guardrail.

- Guardrail description – Optionally explain what it detects or where it applies.

- Set the detection threshold. Specify the sensitivity level (for example, 0.8). Higher values make detection stricter and reduce false positives.

- Define the Action type . Configure how the system should handle detection events:

- Log – Records the event without interrupting agent execution. The Severity level sets the importance level for the log entry:

- Info – For general information or low-impact findings.

- Warning – For potential risks that don’t block execution.

- Error – For critical detections that require review.

- Block – Stops the agent or tool execution when the guardrail is triggered.

- Block reason – Provide a brief explanation for blocking the action.

- Escalate – Sends an escalation when a violation occurs.

- Assign app to – Choose the escalation target type: a specific user, a defined user group, or an external address.

- Recipient – Search and select the recipient (name or email).

- Action app – Select the application that will handle the escalation.

- Enable for evaluations. Toggle Enable guardrail for evaluations to run this guardrail during agent testing or evaluation.

- Save the guardrail. Once configured, the guardrail automatically monitors all LLM requests and responses and blocks execution when prompt injection attempts are detected.

 Configuring a Harmful content guardrail ​

 link
 Harmful content detection identifies hate speech, self-harm, sexual content, and violence in LLM interactions. You can apply it before the LLM call, after, or at both stages. This guardrail uses Azure AI Content Safety.

- Add the Harmful content guardrail to your agent.

- Define the guardrail details. Fill in the following fields:

- Guardrail name – Enter a descriptive name for this guardrail.

- Guardrail description – Explain what it detects or where it applies.

- Select categories to detect. From the Entities to detect list, choose one or more types of content to monitor: hate speech, self-harm, sexual content, or Violence.

- Set a detection threshold. For each selected entity, define a Detection threshold between 0 and 6. Higher values require more severe content before triggering.

- Choose the scopes. Select where you want the guardrail to apply:

- Agent – Checks the agent’s user prompt and output.

- LLM calls – Checks LLM requests and responses.

- Tools – Checks tool input and output. You can select one or more scopes to apply the same detection logic across multiple stages of execution.

- If you select the Tools scope, choose one or more tools from the Select tools list. This lets you reuse the same guardrail across multiple tools in the same agent.

- Define the Action type . Configure how the system should respond when harmful content is detected:

- Log – Records the event without interrupting agent execution. The Severity level sets the importance level for the log entry:

- Info – For general information or low-impact findings.

- Warning – For potential risks that don&#x27;t block execution.

- Error – For critical detections that require review.

- Block – Stops the agent or tool execution when the guardrail is triggered.

- Block reason – Provide a brief explanation for blocking the action.

- Escalate – Sends an escalation when a violation occurs.

- Assign app to – Choose the escalation target type: a specific user, a defined user group, or an external address.

- Recipient – Search and select the recipient (name or email).

- Action app – Select the application that will handle the escalation.

- Enable for evaluations. Toggle Enable guardrail for evaluations to run this guardrail during agent testing or evaluation.

- Save the guardrail. Once configured, the guardrail monitors LLM interactions and responds according to the configured action when harmful content is detected.

 Configuring an Intellectual Property Protection guardrail ​

 link
 IP protection detects intellectual property leakage in model-generated text and code. This guardrail applies post-execution only, checking the model&#x27;s response after the LLM call. This guardrail uses Azure AI Content Safety.

- Add the IP protection guardrail to your agent.

- Define the guardrail details. Fill in the following fields:

- Guardrail name – Enter a descriptive name for this guardrail.

- Guardrail description – Optionally explain what it detects or where it applies.

- From the Entities to detect list, choose what type of content to monitor: Text , Code , or both.

- Choose the scopes. Select where you want the guardrail to apply:

- Agent – Checks the agent’s input and output prompts.

- LLM calls – Checks the requests and responses exchanged with the model.

- Define the Action type . Configure how the system should handle detection events:

- Log – Records the event without interrupting agent execution. The Severity level sets the importance level for the log entry:

- Info – For general information or low-impact findings.

- Warning – For potential risks that don&#x27;t block execution.

- Error – For critical detections that require review.

- Block – Stops the agent or tool execution when the guardrail is triggered.

- Block reason – Provide a brief explanation for blocking the action.

- Escalate – Sends an escalation when a violation occurs.

- Assign app to – Choose the escalation target type: a specific user, a defined user group, or an external address.

- Recipient – Search and select the recipient (name or email).

- Action app – Select the application that will handle the escalation.

- Enable for evaluations. Toggle Enable guardrail for evaluations to run this guardrail during agent testing or evaluation.

- Save the guardrail. Once configured, the guardrail monitors all LLM responses and responds according to the configured action when IP leakage is detected.

 Configuring a User prompt attacks guardrail ​

 link
 User prompt attacks detects prompt injection and jailbreak attempts before they reach the LLM. This guardrails applies pre-execution only.

- Add the User prompt attacks guardrail to your agent.

- Define the guardrail details. Fill in the following fields:

- Guardrail name – Enter a descriptive name for this guardrail.

- Guardrail description – Explain what it detects or where it applies.

- Define the Action type . Configure how the system should respond when attacks are detected:

- Log – Records the event without interrupting agent execution. The Severity level sets the importance level for the log entry:

- Info – For general information or low-impact findings.

- Warning – For potential risks that don&#x27;t block execution.

- Error – For critical detections that require review.

- Block – Stops the agent or tool execution when the guardrail is triggered.

- Block reason – Provide a brief explanation for blocking the action.

- Escalate – Sends an escalation when a violation occurs.

- Assign app to – Choose the escalation target type: a specific user, a defined user group, or an external address.

- Recipient – Search and select the recipient (name or email).

- Action app – Select the application that will handle the escalation.

- Enable for evaluations. Toggle Enable guardrail for evaluations to run this guardrail during agent testing or evaluation.

- Save the guardrail. Once configured, the guardrail automatically monitors all LLM requests and responses and blocks execution when user prompt attacks are detected.
 On this page
- Prerequisites ​
- Configuring a PII detection guardrail ​
- Configuring a Prompt injection guardrail ​
- Configuring a Harmful content guardrail ​
- Configuring an Intellectual Property Protection guardrail ​
- Configuring a User prompt attacks guardrail ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Guardrails NEXT Monitoring guardrails Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated