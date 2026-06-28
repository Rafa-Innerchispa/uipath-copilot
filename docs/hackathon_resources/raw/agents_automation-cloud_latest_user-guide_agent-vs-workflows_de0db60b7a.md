# Agents - Agents and workflows

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-vs-workflows
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Agents - Agents and workflows
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
- Troubleshooting coded agents Home Open Dropdown to choose product Agents ​ Automation Cloud latest Agents and workflows Agents user guide

 Agents and workflows

 link When designing intelligent automation systems, it is important to distinguish between agents and workflows, two distinct but often complementary paradigms. This section outlines what each entails, how they differ, and how to choose the right model for your use case.

 Use this section to better understand:

- What is an agent vs. what is a workflow.

- Decision criteria and use-case examples for when to consider either.

 What is an agent? ​

 link
 An agent is a software system driven by large language models (LLMs) that can reason, act, and adapt dynamically toward a goal. Unlike traditional automation logic, agents do not follow a rigid set of instructions. Instead, they make decisions in real time, selecting tools, interpreting results, and adjusting actions based on current context and memory.

 Agents shine when the path to the outcome can’t be hard-coded, or when hard-coded logic is super complex. They reason, decide and act over dynamic, often unstructured inputs.

 Agents can have different operating modes:

- Autonomous : Triggered by time or programmatic events typically as part of broader workflows.

- Conversational : Uses natural-language message dialog to interpret user input and responds contextually to complete tasks or provide information.

- Ambient : Embedded in an environment or device that continuously senses context and proactively performs helpful actions or notifications without explicit user prompts.

 Agents are especially valuable in ambiguous, open-ended tasks where inputs are unstructured and the optimal path to resolution is not known in advance. They are also designed to learn from prior interactions, making them suitable for environments where adaptability and reasoning are critical.

 Key traits ​

- Autonomy: Chooses which tool or API to call next.

- Stateful memory: Remembers context, prior steps, and feedback.

- Dynamic control-flow: Branches, loops, or asks clarifying questions on the fly.

- Human-in-the-loop hooks: Escalates when confidence is low or rules are breached.

 Typical fits ​

- Ambiguous tasks (for example, diagnosing a support ticket, researching a market).

- Highly variable inputs / paths.

- Situations where learning from each run adds value.

 What is a workflow? ​

 link
 A workflow is a structured sequence of steps executed in a fixed order. It often integrates LLMs, APIs, or human input, but lacks the self-directed planning capabilities of agents. Each step in a workflow is predefined, and transitions between steps follow deterministic logic.

 Workflows excel in high-volume, repeatable processes with clear business rules and predictable outcomes. They provide transparency, governance, and are easy to benchmark in terms of cost, time, and compliance.

 Key traits ​

- Deterministic paths: Every run follows the same branches given the same inputs.

- Stateless between runs: Each execution starts fresh (unless you persist data explicitly).

- Transparent cost and timing: Easy to benchmark and budget.

- Governance-ready: Aligns with compliance and audit needs.

 Typical fits ​

- High-volume, routine tasks (for example, invoice extraction → validation → ERP entry).

- Strict service-level agreements or regulatory constraints.

- Scenarios where outputs must be identical for identical inputs.

 Agentic workflows: the hybrid approach ​

 link
 An agentic workflow blends the adaptability of agents with the structure of workflows. It allows agents to reason, act, and learn within or across defined steps, enabling dynamic decision-making where traditional workflows fall short.

 This hybrid approach handles ambiguity and variability while maintaining orchestration and governance. Agentic Orchestration in Maestro blends the two: agents handle the dynamic decisions, then hand off to predictable workflows for execution.

 Choosing between agents and workflows ​

 link
 Use the following considerations to guide your decision:

- Input type: Choose agents when inputs are unstructured, multimodal, or require contextual understanding; use workflows when inputs are structured and well-defined.

- Control flow: Agents dynamically plan actions based on intermediate results. Workflows follow a static path determined at design time.

- Adaptability: Agents adapt on the fly, learning or re-prompting as needed. Workflows require manual redesign for any changes.

- Governance and predictability: Workflows offer strong compliance, cost control, and consistency. Agents offer experimentation and flexibility, with higher variance in cost and outcomes.

- Runtime reasoning: If decisions or branching must happen at runtime based on partial or evolving context, agents are the right choice.

 Table 1. Agent vs Workflow decision framework

 Criteria Agent Workfow Tasks which are repetitive and rules-based ❌ ✅ Tasks which are highly ambiguous ✅ ❌ Deterministic outcomes ❌ ✅ Dynamic reasoning and adaptation ✅ ❌

 Table 2. Agent vs workflow attribute cheat sheet

 Dimension

 Agent

 Workflows

 Control flow

 Dynamic planning &amp; tool selection/generation

 Predefined sequence with predefined tools

 Input type

 Unstructured, multi-modal

 Structured records/forms

 Adaptability

 Learns or is re-prompted on the fly

 Requires design-time changes

 Reliability

 Variable; depends on guardrails and evaluations

 High if inputs stay in spec

 Governance load

 Higher (agent anarchy risk)

 Mature policies/tools exist

 Cost predictability

 Medium-low (LLM/token variance)

 High

 Typical ROI horizon

 Fast experimentation, uncertain scaling

 Steady savings once scripted

 Skill barrier

 Similar for low-code vs. code

 Table 3. Agent vs workflow use case comparison

 Use case Agent Workflow Support ticket triage ✅ Diagnoses from logs and routes dynamically ❌ Too ambiguous for predefined paths Sales email generation ✅ Tailored, adaptive outreach ❌ Cannot personalize across dynamic buyer contexts Invoice processing ❌ Too rule-based and repeatable ✅ Follows a fixed, reliable path Employee onboarding ❌ No ambiguity involved ✅ Straightforward process steps
 Multi-agent systems ​

 link
 A multi-agent system consists of multiple autonomous agents that interact and coordinate at runtime to achieve a shared or negotiated objective. Unlike a standard workflow, which follows a predefined path, or a single agent that operates in isolation, a multi-agent setup supports emergent behavior, flexible task distribution, and dynamic collaboration.

 Multi-agent systems are best suited for open-ended, high-complexity goals such as collaborative RAG pipelines or dynamic supply chain responses.

 The following table compares classic workflow orchestration with true multi-agent systems across several key dimensions:

 Dimension Classic workflow (can invoke agents) True multi-agent system Control logic Designed up-front: “Step A → Step B → Step C.” Branches are fixed by the author. Emerges at runtime: agents plan their own steps and may re-assign work to peers dynamically. Planning entity Workflow engine decides the order; individual agents (if any) just execute their slice. Each agent plans locally; a coordination layer (or peer protocols) resolves conflicts on the fly. Adaptability Limited to the decision tree modeled by humans. Can form new sub-plans, split/merge roles, renegotiate objectives. Multi-agent swarms can re-allocate tasks or spawn helper agents for failure handling. State and memory Typically stateless between runs (unless you persist it). Each agent can keep its own memory; a shared memory or blackboard lets them write/read context for others. Governance and observability Straightforward: one orchestrator, deterministic trace. Harder: many autonomous loops need global tracing, policy enforcement, and safety fences. Typical fit Repetitive processes with clear hand-offs (for example, “extract invoice → validate → post to ERP”). Complex, open-ended goals that benefit from division of labor (for example, RAG researcher ↔ planner ↔ coder collaborating to ship a micro-feature). On this page
- What is an agent? ​
- Key traits ​
- Typical fits ​
- What is a workflow? ​
- Key traits ​
- Typical fits ​
- Agentic workflows: the hybrid approach ​
- Choosing between agents and workflows ​
- Multi-agent systems ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Best practices NEXT Best practices for building agents Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated