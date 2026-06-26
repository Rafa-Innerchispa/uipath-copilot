# Maestro - Understanding Process implementation

- **URL:** https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/understanding-process-implementation
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Maestro - Understanding Process implementation
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
- search Search ​ Language translate English expand_more ​ Sign in maestro latest false Maestro Automation Cloud · latest - Collapse
- Introduction
- Overview
- What you get with Maestro
- Who should use Maestro
- How Maestro fits into UiPath
- Introduction to Maestro Case
- Maestro BPMN vs. Maestro Case: when to use case management
- The Maestro Case lifecycle: from event trigger to app experience
- Common business use cases
- Loan origination use case
- Purchase to pay use case
- Claims processing use case
- Supplier onboarding use case
- Maestro feature availability
- Getting started
- Licensing
- Unified Pricing
- Flex Plan
- Prerequisites
- Supported security standards
- Maestro landing page
- Home
- Process instances
- Process incidents
- Try Maestro in Playground
- Build your first case with Case Management
- Implementing a simple process
- Implementing a complex process
- Testing Maestro processes
- Keyboard shortcuts
- Process modeling with BPMN
- Understanding Process modeling
- BPMN primer
- Events in BPMN
- Tasks in BPMN modeling
- Gateways and flow logic
- Markers
- Subprocesses and modularity
- Data objects and data stores
- Participants
- Sequence flows
- BPMN-supported elements
- BPMN patterns and practices
- Flow and routing
- Looping
- Time and reminders
- Messages and updates
- Errors and recovery
- Advanced patterns
- Opening the modeling canvas
- Modeling your process
- Aligning and connecting BPMN elements
- Autopilot for Maestro (Preview)
- Process Repository
- Process modeling with Case Management
- Designing a persistent case entity schema
- Defining case keys (system vs. external)
- Establishing task I/O and write-back contracts
- Exit rules and early stage termination
- Modeling primary and secondary stages
- Triggering a case from Data Fabric
- Implementing stage-level personas and permissions
- Setting SLAs and automated escalation rules
- Configuring a rework loop (re-entry)
- Managing live case instances: pause, migrate, and retry
- Maestro case management component dictionary
- Process implementation
- Understanding Process implementation
- Configuring properties and data
- Configuring error handling
- Variables and Expression editor
- Events
- Tasks
- Service task
- User task
- Send task
- Receive task
- Business rule task (Preview)
- Script task
- Gateways
- Multi-instance implementation
- Subprocesses
- Event subprocess
- Solution-based projects: special settings
- Transitioning from C# to JavaScript expressions
- Integrating systems and data
- Working with files in Maestro processes
- Data Fabric operations
- Using agents in Maestro
- Business rules
- Process apps
- Debugging
- Simulating
- Publishing and upgrading agentic processes
- Common implementation scenarios
- Extracting and validating documents
- Process operations
- Understanding Process operations
- Working with instance management
- Custom instance ID
- Instance throttling
- Variables and element filtering
- Process monitoring
- Understanding Process monitoring
- Instance diagram view
- Monitoring dashboard
- Customizing dashboards
- Customizing alerts
- Creating a custom Maestro dashboard in Insights
- Alerts
- Notifications
- Process optimization
- Understanding Process optimization
- Optimization view
- Optimization dashboard
- Accessing the Process Optimization app
- Process Optimization app in Process Mining
- Enriching Process optimization with external data
- Reference information
- Maestro and ReFramework FAQ
- Downloads Home Open Dropdown to choose product Maestro ​ Automation Cloud latest Understanding Process implementation Maestro user guide

 Understanding Process implementation

 link In Maestro, implementation is the step where a modeled process (your BPMN diagram) becomes an executable, agentic workflow .

 On the UiPath® Studio Web canvas, you add runtime instructions (properties, variables/expressions, events, tasks, and gateways), bind them to automations, AI agents, and human steps, then test and publish to the process engine.

 This stage is distinct from Process modeling (designing the diagram) and from Process operations (monitoring/running instances).

 Why it matters : Maestro’s implementation stage is where the orchestration across robots, AI agents, and people is defined so the process can actually run end‑to‑end.

 A simple implementation example ​

 link
 Use case : Purchase request approval

 The example process contains the following elements:

- Variables — Amount:number and RequesterEmail:string (Expression editor) drive routing and outbound notifications.

- User task — Manager review , assigned to the Manager role, captures the approval decision.

- Exclusive gateway — evaluates Amount &gt; 5000 and routes to CFO approval if true, or directly to fulfillment otherwise.

- Service task — calls an external system or automation to create a purchase order.

- Send task — emails Request approved / rejected to RequesterEmail .

- Timer event — on Manager review , escalates after 24 hours via an alternate path.

- Test &amp; publish — the solution is validated with Simulate/Debug, then published to make the process available.

 This example provides you clear routing by amount, auditable approvals, automatic PO creation, and notifications—implemented once, reused safely.

 Start importing a BPMN model, or drawing new one, or using Autopilot for Maestro to help you along. See Process modeling for canvas features details.

 On this page
- A simple implementation example ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Maestro case management component dictionary NEXT Configuring properties and data Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated