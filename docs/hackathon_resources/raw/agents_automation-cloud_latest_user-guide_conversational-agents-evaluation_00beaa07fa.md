# Agents - Evaluating conversational agents

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/conversational-agents-evaluation
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Evaluating conversational agents
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Evaluating conversational agents Agents user guide

 Evaluating conversational agents

 link Evaluations help ensure your conversational agent behaves reliably across varied dialogue paths. This page covers how to test your agent using Debug chat , create evaluation sets, and run automated tests.

 Debug chat ​

 link
 Debug chat provides a real-time testing environment where you can interact with your agent and inspect its behavior.

 Starting a debug session ​

- In Studio Web, open your conversational agent.

- Select Debug to open the chat interface.

- Send messages to test your agent&#x27;s responses.

 Viewing execution traces ​

 The history panel shows real-time details of the agent&#x27;s execution:

- LLM calls : The prompts sent to the model and responses received.

- Tool calls : Which tools were invoked, with arguments and outputs.

 Expand any step to see full details, including token counts and latency.

 Viewing citations ​

 When your agent uses Context Grounding, citations appear in the response showing which documents informed the answer.

- Look for citation markers in the agent&#x27;s response (typically numbered references).

- Select a citation to see the source document and relevant excerpt.

- Verify that citations accurately support the agent&#x27;s response.

 Adding conversations to evaluation sets ​

 After a successful test interaction, save it for automated testing:

- In the Chat tab, select Add to evaluation set .

- Choose an existing evaluation set or create a new one.

 The conversation is saved with:

- Conversation history : All preceding turns in the dialogue.

- Current user message : The user&#x27;s latest input.

- Expected agent response : The agent&#x27;s actual response (which you can edit).

 Evaluation sets ​

 link
 Evaluation sets are collections of test cases that validate your agent&#x27;s behavior. They support both single-turn and multi-turn testing scenarios.

 For detailed evaluation guidance, refer to Agent evaluations

 Single-turn evaluations ​

 Single-turn evaluations test isolated question-and-answer pairs without conversation history. They are evaluation tests where you test the first prompt in a conversation.

 Use single-turn evaluations for ​

- Testing specific knowledge retrieval.

- Validating tool selection for different intents.

- Checking response format and tone.

 Example ​

 User message Expected behavior &quot;How many holidays do we have in the US?&quot; Returns correct count, cites policy document &quot;Schedule a meeting with John tomorrow at 2pm&quot; Calls calendar tool with correct parameters
 Multi-turn evaluations ​

 Multi-turn evaluations test how the agent handles conversation context and follow-up questions. They are evaluation tests where the tested prompt follows previous conversation.

 Use multi-turn evaluations for ​

- Testing context retention across turns.

- Validating pronoun resolution (&quot;it&quot;, &quot;that&quot;, &quot;the same&quot;).

- Checking conversation flow and coherence.

 Example ​

 Turn Message Expected behavior 1 &quot;What&#x27;s the PTO policy?&quot; Returns PTO policy summary 2 &quot;How do I request time off?&quot; References PTO context, explains request process 3 &quot;Can I do that through email?&quot; Understands &quot;that&quot; refers to requesting time off
 Creating evaluation tests ​

 From Debug chat ​

- Run a conversation in Debug chat .

- Select Add to evaluation set from the Chat panel.

- The conversation exchange will be added as an evaluation test in your designated evaluation set.

 Using the Conversation builder ​

 The Conversation builder lets you create or edit multi-turn test cases:

- Select Evaluation Sets for your agent in Studio Web.

- Select an evaluation set or create a new one. If these options are disabled, make sure you aren&#x27;t in debug mode.

- Select Add to set or edit an existing test.

- Use the Conversation builder to:

- Add conversation history turns.

- Define the current user message.

- Use Output setup to define the assertion

- Specify the expected agent response for deterministic and LLM-as-a-judge based evaluators.

- Specify the &quot;behavior and output notes&quot; for trajectory based evaluators.

 Tool simulations ​

 Simulations let you test agent behavior without executing real tool endpoints. For each evaluation test, you can specify whether tools should actually execute or simulate their execution.

 Simulations enhance agent evaluations by enabling:

- Safe testing : Avoid unintended side effects from calling real APIs or services.

- Faster execution : Skip network latency and external service delays.

- Cost-effective runs : Reduce API costs during iterative testing.

- Reproducibility : Get consistent results by controlling tool outputs.

 You can configure simulation behavior for each evaluation test:

- Open an evaluation set.

- Select a test case to edit.

- In the test configuration, specify which tools should simulate execution.

- Define the expected simulated output for each tool.

 Generating tests with natural language ​

 Use Autopilot to generate evaluation tests from descriptions:

- In the Evaluation Sets screen, select Create then Generate new evaluation set .

- Describe the scenarios you want to test in natural language.

- Review and refine the generated test cases.

 Example prompt:

 assignment Generate test cases for an HR assistant that :
 - Answers questions about vacation policy
 - Handles requests to schedule meetings
 - Escalates when asked about salary information
 - Responds appropriately when the user is frustrated
 Generate test cases for an HR assistant that:
- Answers questions about vacation policy
- Handles requests to schedule meetings
- Escalates when asked about salary information
- Responds appropriately when the user is frustrated

 Note: Autopilot generated evaluation tests automatically use trajectory-based evaluations.

 Running evaluations ​

 link
 Running a single test ​

- Select a test case from your evaluation set.

- Select Evaluate selected .

- Review the results, comparing actual output to expected output.

 Running batch evaluations ​

- Go to Evaluation sets .

- Select Run on the desired evaluation set to execute all tests.

- Review the results showing pass/fail rates.

 Testing with different models ​

 Run the same evaluation set against different models to compare performance:

- In the evaluation set, select Evaluation Settings to add an additional target model.

- Run the evaluation.

- Compare results across models to identify the best fit for your use case.

 This helps you understand:

- Which models perform best for your specific scenarios.

- Trade-offs between response quality and latency.

- Cost implications of different model choices.

 Evaluation metrics ​

 link
 Evaluations assess multiple dimensions of agent behavior:

 Metric Description Response accuracy Does the response contain correct information? Tool selection Did the agent choose the appropriate tool? Citation quality Are citations relevant and accurate? Tone and format Does the response match expected style? Context retention Does the agent maintain context across turns?
 Evaluation best practices ​

 link
 Test both happy and unhappy paths ​

 Don&#x27;t just test ideal scenarios. Include:

- Ambiguous questions

- Out-of-scope requests

- Edge cases and error conditions

- Multi-language inputs (if supported)

 Create representative test suites ​

 Build evaluation sets that reflect real usage patterns:

- Analyze common user queries from production

- Include variations of the same question

- Test different user personas and communication styles

 Iterate based on results ​

 Use evaluation failures to improve your agent:

- Identify patterns in failed tests.

- Update system prompts or tool configurations.

- Re-run evaluations to verify improvements.

- Add new tests for discovered edge cases.

 Next steps ​

 link

- Deployment : Publish your tested agent

- Observability : Monitor production performance

- Agent evaluations : Detailed evaluation framework documentation
 On this page
- Debug chat ​
- Starting a debug session ​
- Viewing execution traces ​
- Viewing citations ​
- Adding conversations to evaluation sets ​
- Evaluation sets ​
- Single-turn evaluations ​
- Multi-turn evaluations ​
- Creating evaluation tests ​
- Running evaluations ​
- Running a single test ​
- Running batch evaluations ​
- Testing with different models ​
- Evaluation metrics ​
- Evaluation best practices ​
- Test both happy and unhappy paths ​
- Create representative test suites ​
- Iterate based on results ​
- Next steps ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Designing conversational agents NEXT Deploying conversational agents Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated