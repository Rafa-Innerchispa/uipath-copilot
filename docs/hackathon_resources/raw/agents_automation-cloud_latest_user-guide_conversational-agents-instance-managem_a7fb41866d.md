# Agents - Instance Management

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/conversational-agents-instance-management
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Instance Management
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Instance Management Agents user guide

 Instance Management

 link Overview ​

 link
 Instance Management provides the full-featured chat interface for conversational agents. It serves as the primary access point for administrators and internal users during development, testing, and internal operations.

 Intended users: Administrators, developers, and internal team members who build, test, manage, or use conversational agents.

 Feature availability ​

 link
 Instance Management includes all available chat features. Use this as the baseline when comparing other channels.

 Feature Available Start new chat ✅ Chat history ✅ Delete chat session ✅ Settings ✅ Starting prompts ✅ File uploads ✅ Citations ✅ HTML preview ✅ Copy response ✅ Feedback (thumbs) ✅ Debug dump (Ctrl+Alt+D) ✅
 Prerequisites ​

 link
 No additional setup is required. Instance Management is available automatically for any deployed conversational agent.

 Requirements ​

- A published conversational agent.

- Access to the UiPath Automation Cloud portal and Instance Management.

- Appropriate permissions to view the agent.

 Accessing the agent ​

 link

- Go to the UiPath Automation Cloud portal.

- Navigate to Agents &gt; Deployed Agents .

- Find your conversational agent in the list.

- Select Chat to start a conversation.

 Chat features ​

 link
 This section describes all available chat features. Other channels may support a subset of these features.

 Starting a new chat ​

 Select the New chat button to begin a fresh conversation with an agent of your choice. This clears the current context and starts a new session.

 Accessing chat history ​

 Access previous conversations from the chat history panel:

- Select the Chat history icon in the chat interface.

- Browse or search previous conversations.

- Select a conversation to continue where you left off.

 Deleting chat sessions ​

 Remove conversations from your chat history:

- Select the Chat history icon to open the history panel.

- Find the conversation you want to delete.

- Select the Delete icon next to the conversation.

 Deleted conversations are permanently removed and cannot be recovered.

 Customizing chat settings ​

 Access chat settings to customize your experience:

- Select the Settings icon in the chat interface.

- Adjust available options, such as Profile Information.

 Send files to the agent for analysis:

- Select the Attach file(s) icon or drag and drop a file into the chat.

- Add a message describing what you want to do with the file.

- Send the message.

 A file analysis tool such as Analyze files or IXP is required to process the file.

 Supported file types for Analyze Files tool ​

- Images: GIF, JPE, JPEG, PNG, WEBP

- Documents: PDF (must be under 5MB)

 Citations ​

 When an agent uses knowledge sources to generate a response, citations appear to show the origin of the information:

- Look for numbered citation markers in the agent&#x27;s response.

- Select a citation to view the source details.

- The Sources panel displays the source document and page (if applicable) referenced.

 Note: Citation preview is only available for PDF documents.

 Citations help verify information accuracy and provide transparency into how the agent formulates responses.

 HTML preview ​

 When agent responses contain HTML content, Instance Management renders an interactive preview:

- The agent generates HTML as part of its response.

- A preview panel displays the rendered HTML.

- You can interact with the preview or copy the HTML code.

 Note: HTML preview is only available in Instance Management. Other channels display the raw HTML or markdown representation.

 Copying responses ​

 Copy agent responses to your clipboard:

- Select the Copy icon below an agent response.

- The response text is copied to your clipboard.

 Providing feedback ​

 Help improve the agent by providing feedback on responses:

- After an agent response, select Thumbs up or Thumbs down .

- (Optional for positive feedback) Add a comment explaining your feedback.

- Submit the feedback.

 Feedback is collected and available for review in the Instance Management feedback menus. Administrators can access aggregated feedback to identify areas for agent improvement. For more information, see Observability .

 Debug dump ​

 Generate a debug dump for troubleshooting issues:

- While in the chat interface, press Ctrl+Alt+D (Windows) or Cmd+Option+D (Mac).

- Debug logs will be copied to your clipboard:

- Conversation history

- Trace information

- System metadata

 Share this file with support or development teams when troubleshooting issues.

 Note: Debug dump is only available in Instance Management. Other channels do not support this feature.

 Limitations ​

 link
 Instance Management provides the complete feature set. There are no feature limitations compared to other channels.

 Next steps ​

 link

- Observability : Monitor dashboards and review feedback

- Managing UiPath agents : Full Instance Management documentation
 On this page
- Overview ​
- Feature availability ​
- Prerequisites ​
- Requirements ​
- Accessing the agent ​
- Chat features ​
- Starting a new chat ​
- Accessing chat history ​
- Deleting chat sessions ​
- Customizing chat settings ​
- Citations ​
- HTML preview ​
- Copying responses ​
- Providing feedback ​
- Debug dump ​
- Limitations ​
- Next steps ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Deploying conversational agents NEXT Autopilot for Everyone Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated