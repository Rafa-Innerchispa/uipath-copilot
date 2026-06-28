# Agents - Autopilot for Agents

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/about-autopilot-for-agents
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Autopilot for Agents
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Autopilot for Agents Agents user guide

 Autopilot for Agents

 link Note: Access to Autopilot depends on the cloud platform you use. For details, refer to Agents feature availability .

 Autopilot for Agents (Preview) is a conversational AI assistant embedded in the Agent Builder in Studio Web. It provides a persistent, context-aware workspace where you can build, configure, and refine agents using natural language, without switching between tools or manually editing each component.

 Autopilot reads your current agent definition and available platform resources each time a session opens. When you describe a change, Autopilot proposes targeted edits to your agent—to its prompts, tools, schema, or context sources, which you review before applying.

 The chat interface and general interaction model are shared across all UiPath products that surface Autopilot. For a full reference of common interface elements, see Autopilot chat user interface . This page covers the capabilities and tools specific to the Agent Builder context.

 Key capabilities ​

 link
 Autopilot for Agents provides the following capabilities:

- Context retention — remembers previous inputs and decisions within a session.

- Prompt refinement — lets you adjust your prompt in real time without starting over.

- Inline suggestions — proposes changes specific to your current agent state.

- Workflow continuity — maintains context across iterative changes and refinements within a session.

- Interactive debugging — helps identify and clarify issues through follow-up questions.

- Code and logic awareness — understands the structure of your agent and provides guidance relevant to its current state.

 How Autopilot for Agents works ​

 link
 When you open the Autopilot panel using the widget on the right-side toolbar of the Agent Builder, Autopilot fetches the current state of your project, including:

- All agent runs and evaluation set runs

- The latest health score

- Available resources: RPA processes, API workflows, agent processes, and Context Grounding context sources

 This context is included with every message you send. The Agents backend initiates a streaming request to the selected large language model (LLM), combining your message with the agent definition, available resources, and a system prompt template. The response streams back to the chat panel.

 Autopilot surfaces suggested changes as previews. In the default interaction mode, you review and accept each change before it is applied to your agent.

 Interaction modes ​

 link
 The chat input area includes an Edit control that sets how Autopilot applies changes to your agent:

- Edit (default) — Autopilot proposes changes as previews. Each suggestion requires your confirmation before being applied. This mode is recommended for all agent design and production workflows.

- Agent (experimental) — Autopilot applies changes automatically without requesting confirmation. This mode is intended for exploratory or rapid iteration workflows.

 Important: Agent mode is experimental. Use it with caution when working with production agents.

 The chat interface ​

 link
 The Autopilot panel is accessed from the right-side toolbar of the Agent Builder in Studio Web. The panel provides:

- A chat input field for entering prompts and questions.

- Dynamic prompt suggestions that update alongside your agent&#x27;s current state.

- An LLM selector for choosing the language model for the session.

- File upload support for documents, images, code files, and data formats, up to 15 MB per file.

- New chat , Settings , and Chat history controls in the panel header.

 Chat history ​

 The Chat History panel provides a searchable list of conversations from the last 30 days. Selecting an entry restores its full context, letting you continue where you left off or reference previous suggestions.

 Settings ​

 The Settings panel controls how Autopilot behaves in the current Agent Builder session.

 Personalization ​

- Enable Prompt Suggestions — on by default; displays contextual suggestions after each response.

- Show Context Change Messages (Experimental) — displays messages when Autopilot updates its understanding of the agent context.

- Custom Instructions — a free-text field, up to 1,000 characters, for specifying terminology preferences, desired detail level, or constraints on Autopilot responses.

 MCP Servers ​

 Connects Autopilot to Model Context Protocol (MCP) servers to provide additional structured context. Only MCP servers created in Orchestrator are supported.

 Tools ​

 Displays the Framework Tools available in the current session. Each tool can be individually enabled or disabled. For details, see Autopilot for Agents tools .

 Save applies your current settings. Reset to Defaults reverts all settings to their original state. You can also Download conversation to export the current session as a JSON file that includes organization, tenant, and conversation settings.

 Response accuracy ​

 link
 Autopilot for Agents provides AI-powered support for agent design tasks such as configuring prompts, adding tools, and refining schemas. While it can be highly effective, it may occasionally generate responses that are inaccurate, misleading, or incomplete. This is a known limitation of large language models.

 For example:

- Autopilot may suggest tool configurations that do not match your available resources.

- It may provide explanations that are factually incorrect or based on outdated agent logic.

- When working with external resources, it may overlook important details or misinterpret source content.

 Review all suggestions before applying them, especially for production agents:

- Use the thumbs down button to flag unhelpful or incorrect responses.

- Prefer the default Edit mode over Agent mode for changes to critical agent logic.

 Autopilot is most effective as a collaborator. Your judgment remains essential for building accurate and reliable agents.

 Related topics ​

 link

- Autopilot for Agents tools — reference for Framework Tools available in the Autopilot panel

- About Autopilot chat — overview of the Autopilot chat framework across all UiPath products

- Autopilot chat user interface — full reference for the chat interface shared across all products
 On this page
- Key capabilities ​
- How Autopilot for Agents works ​
- Interaction modes ​
- The chat interface ​
- Chat history ​
- Settings ​
- Response accuracy ​
- Related topics ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Using agent templates NEXT Autopilot for Agents tools Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated