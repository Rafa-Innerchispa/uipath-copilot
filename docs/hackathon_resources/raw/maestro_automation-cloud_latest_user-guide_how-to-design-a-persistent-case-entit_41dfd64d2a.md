# Maestro - Designing a persistent case entity schema

- **URL:** https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/how-to-design-a-persistent-case-entity-schema
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

Maestro - Designing a persistent case entity schema
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
- Downloads Home Open Dropdown to choose product Maestro ​ Automation Cloud latest Designing a persistent case entity schema Maestro user guide

 Designing a persistent case entity schema

 link Overview ​

 link
 The case entity [Coming Soon] is the central, persistent data model that every stage, task, and rule reads from and writes to throughout a case&#x27;s lifetime. A well-designed entity schema separates input fields (data provided at case creation) from computed fields (data produced by tasks during processing) and assigns clear field ownership so that no two tasks write to the same field. Follow this guide to define a schema that prevents data collisions during write-back and supports reliable stage rules.

 Prerequisites ​

 link

- Access to Studio Web .

- A defined business process with identified stages and tasks.

- Familiarity with the core concepts of Maestro Case .

- A Data Fabric instance available in your UiPath environment (recommended for native entity creation).

 Step 1: understanding the out-of-the-box data objects ​

 link
 Every case project automatically creates three data objects:

 Object Purpose Case Entity [Coming Soon] Holds all structured business data that stages, tasks, and rules read from and write to. Case Documents Stores attachments and files associated with the case (receipts, photos, contracts). Case Comments Stores notes, annotations, and communications added by case workers throughout the lifecycle.
 All three share an immutable caseID system field that is auto-generated at case creation. This field ties all case data together and cannot be changed.

 Focus your schema design effort on the Case Entity — it is the single source of truth for all case processing logic.

 Step 2: choosing where the entity lives ​

 link
 Before defining fields, decide how to source the entity. Select the option that best fits your data ownership model:

 Source Description When to Use Native in Data Fabric (recommended) Create the entity as a native business entity in Data Fabric and link it to your case. New processes where you own the data model. Virtual Data Object (VDO) in Data Fabric Register an external source as a VDO in Data Fabric and link the VDO to the case. Entity data lives in an external system (CRM, ERP) and you want to reference it without duplicating. Case trigger payload Pass existing data in the case creation trigger (for example, an API connector). The payload fields become case fields available across all stages. Lightweight integrations where you hydrate the case at creation time.
 Step 3: identifying and categorize your fields ​

 link
 Mapping out the full case lifecycle ​

 List every stage and every task in your case plan. For each task, identify:

- What data it needs to read (inputs).

- What data it produces (outputs).

 Classifying fields into two categories ​

 Separate every field in your schema into one of two groups:

 Category Definition Characteristics Examples Input fields Data provided when the case is created, either by a trigger payload, a form submission, or an external system. Populated at creation. Typically read-only after hydration. Required for initial routing and task execution. policyNumber , claimantName , dateOfLoss , lossDescription Computed fields Data produced by tasks during case processing. These fields start empty and are written back as tasks complete. Empty at creation. Written by a specific task. Consumed by downstream tasks and rules. validationResult , damageEstimate , adjusterDecision , paymentReference
 Marking input fields as read-only ​

 Input fields such as employeeId , policyNumber , or reportId should never be overwritten by tasks. Document these fields as read-only in your schema to prevent accidental modification during processing.

 Step 4: establishing field ownership ​

 link
 Field ownership is the most critical principle for preventing data collisions. Each computed field in the entity must be written by exactly one task .

 Assigning one writer per field ​

 For every computed field, designate the single task responsible for writing to it. If two tasks write to the same field, the last writer wins and previous data is lost.

 Annotating ownership in your schema ​

 Use a writtenBy annotation (or equivalent comment) to document which task owns each computed field. While the platform does not enforce this annotation at runtime, it serves as a design contract that prevents collisions during development.

 Using namespaced fields to avoid ambiguity ​

 When multiple tasks produce similar types of output, namespace your fields to keep them distinct. For example:

- Use photoAnalysis for the output of an image analysis agent task.

- Use fieldInspection for the output of a human field inspection task.

- Avoid a generic analysisResult field that multiple tasks might contend for.

 Step 5: defining the schema ​

 link
 Creating the entity in your chosen source ​

 Navigate to the Case Entity designer in Studio Web. Create a new entity with a descriptive name that matches your business domain (for example, AutoInsuranceClaim or ExpenseReport ).

 Adding input fields first ​

 Define all input fields with their types, required flags, and any default values. Set required: true for fields that must be present at case creation.

 Adding computed fields with ownership annotations ​

 Define all computed fields with their types, set required: false (these fields are empty at creation), and annotate each with the task that writes to it.

 Reviewing a reference schema ​

 The following example demonstrates the input-versus-computed pattern with field ownership for an auto insurance claims case:

 assignment {
 &quot;entityName&quot; : &quot;AutoInsuranceClaim&quot; ,
 &quot;fields&quot; : {
 // --- Input fields (populated by trigger, read-only after creation) ---
 &quot;claimId&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true , &quot;generated&quot; : true } ,
 &quot;policyNumber&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;claimantName&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;claimantEmail&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;dateOfLoss&quot; : { &quot;type&quot; : &quot;date&quot; , &quot;required&quot; : true } ,
 &quot;lossDescription&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;vehicleInfo&quot; : { &quot;type&quot; : &quot;object&quot; , &quot;required&quot; : true } ,
 &quot;photos&quot; : { &quot;type&quot; : &quot;array&quot; , &quot;items&quot; : &quot;url&quot; } ,
 &quot;policeReportNumber&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : false } ,

 // --- Computed fields (written by tasks during processing) ---
 &quot;policyValid&quot; : { &quot;type&quot; : &quot;boolean&quot; , &quot;writtenBy&quot; : &quot;Validate Policy&quot; } ,
 &quot;extractedDetails&quot; : { &quot;type&quot; : &quot;object&quot; , &quot;writtenBy&quot; : &quot;Extract Details&quot; } ,
 &quot;photoAnalysis&quot; : { &quot;type&quot; : &quot;object&quot; , &quot;writtenBy&quot; : &quot;Analyze Photos&quot; } ,
 &quot;fieldInspection&quot; : { &quot;type&quot; : &quot;object&quot; , &quot;writtenBy&quot; : &quot;Field Inspection&quot; } ,
 &quot;policeReport&quot; : { &quot;type&quot; : &quot;object&quot; , &quot;writtenBy&quot; : &quot;Retrieve Police Report&quot; } ,
 &quot;damageEstimate&quot; : { &quot;type&quot; : &quot;decimal&quot; , &quot;writtenBy&quot; : &quot;Estimate Damage&quot; } ,
 &quot;adjusterDecision&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;enum&quot; : [ &quot;approve&quot; , &quot;deny&quot; , &quot;investigate_more&quot; ] } ,
 &quot;payoutAmount&quot; : { &quot;type&quot; : &quot;decimal&quot; , &quot;writtenBy&quot; : &quot;Calculate Payout&quot; } ,
 &quot;paymentReference&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;writtenBy&quot; : &quot;Issue Payment&quot; }
 }
 }
 {
 &quot;entityName&quot;: &quot;AutoInsuranceClaim&quot;,
 &quot;fields&quot;: {
 // --- Input fields (populated by trigger, read-only after creation) ---
 &quot;claimId&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true, &quot;generated&quot;: true },
 &quot;policyNumber&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;claimantName&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;claimantEmail&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;dateOfLoss&quot;: { &quot;type&quot;: &quot;date&quot;, &quot;required&quot;: true },
 &quot;lossDescription&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;vehicleInfo&quot;: { &quot;type&quot;: &quot;object&quot;, &quot;required&quot;: true },
 &quot;photos&quot;: { &quot;type&quot;: &quot;array&quot;, &quot;items&quot;: &quot;url&quot; },
 &quot;policeReportNumber&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: false },

 // --- Computed fields (written by tasks during processing) ---
 &quot;policyValid&quot;: { &quot;type&quot;: &quot;boolean&quot;, &quot;writtenBy&quot;: &quot;Validate Policy&quot; },
 &quot;extractedDetails&quot;: { &quot;type&quot;: &quot;object&quot;, &quot;writtenBy&quot;: &quot;Extract Details&quot; },
 &quot;photoAnalysis&quot;: { &quot;type&quot;: &quot;object&quot;, &quot;writtenBy&quot;: &quot;Analyze Photos&quot; },
 &quot;fieldInspection&quot;: { &quot;type&quot;: &quot;object&quot;, &quot;writtenBy&quot;: &quot;Field Inspection&quot; },
 &quot;policeReport&quot;: { &quot;type&quot;: &quot;object&quot;, &quot;writtenBy&quot;: &quot;Retrieve Police Report&quot; },
 &quot;damageEstimate&quot;: { &quot;type&quot;: &quot;decimal&quot;, &quot;writtenBy&quot;: &quot;Estimate Damage&quot; },
 &quot;adjusterDecision&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;approve&quot;, &quot;deny&quot;, &quot;investigate_more&quot;] },
 &quot;payoutAmount&quot;: { &quot;type&quot;: &quot;decimal&quot;, &quot;writtenBy&quot;: &quot;Calculate Payout&quot; },
 &quot;paymentReference&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;writtenBy&quot;: &quot;Issue Payment&quot; }
 }
}

 Step 6: wiring input and output mappings to tasks ​

 link
 After defining the schema, connect it to tasks through input and output mappings.

 Configuring input mappings ​

 For each task, select only the Case Entity fields the task needs to read. This controls what data the task can see.

 Example — Validate Policy task input mapping:

 assignment &quot;input&quot; : {
 &quot;policyNumber&quot; : &quot;caseEntity.policyNumber&quot;
 }
 &quot;input&quot;: {
 &quot;policyNumber&quot;: &quot;caseEntity.policyNumber&quot;
}

 Configuring output mappings ​

 For each task, map the task&#x27;s result to the specific Case Entity field that the task owns. This is the write-back mechanism.

 Example — Validate Policy task output mapping:

 assignment &quot;output&quot; : {
 &quot;caseEntity.policyValid&quot; : &quot;taskOutput.policyValid&quot;
 }
 &quot;output&quot;: {
 &quot;caseEntity.policyValid&quot;: &quot;taskOutput.policyValid&quot;
}

 Verifying that output mappings respect field ownership ​

 Cross-check every task&#x27;s output mapping against your schema annotations. Confirm that no two tasks write to the same Case Entity field.

 Step 7: validating the schema against rules ​

 link
 Stage rules (entry, complete, exit, re-entry) evaluate against Case Entity fields. Verify that:

- Every field referenced in a rule&#x27;s IF clause is present in the schema.

- The field is written by a task that completes before the rule evaluates.

- The field type matches the operator used in the rule (for example, do not use a string comparison on a decimal field).

 Example — an Exit rule on an Intake stage depends on the policyValid field:

 assignment WHEN PolicyCheckCompleted event arrives
 IF caseEntity . policyValid == false
 WHEN PolicyCheckCompleted event arrives
 IF caseEntity.policyValid == false

 Confirm that the Validate Policy task writes policyValid and completes within the Intake stage before this Exit rule evaluates.

 Expected outcome ​

 link
 After completing these steps, you have a case entity schema that:

- Clearly separates input fields (populated at case creation) from computed fields (written by tasks during processing).

- Assigns explicit field ownership so that exactly one task writes to each computed field.

- Uses namespaced field names to prevent ambiguity and collisions.

- Supports reliable write-back from tasks to the entity, ensuring downstream rules and tasks consume accurate, non-conflicting data.

- Documents the data contract between the case plan and its tasks through writtenBy annotations.

 Code snippet ​

 link
 The following is a second reference schema for an expense report use case, demonstrating the same input-versus-computed pattern:

 assignment {
 &quot;entityName&quot; : &quot;ExpenseReport&quot; ,
 &quot;fields&quot; : {
 // --- Input fields (populated at case creation) ---
 &quot;reportId&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true , &quot;generated&quot; : true } ,
 &quot;employeeId&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;employeeName&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;department&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : true } ,
 &quot;totalAmount&quot; : { &quot;type&quot; : &quot;decimal&quot; , &quot;required&quot; : true } ,
 &quot;currency&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;default&quot; : &quot;USD&quot; } ,
 &quot;lineItems&quot; : { &quot;type&quot; : &quot;array&quot; , &quot;items&quot; : &quot;ExpenseLineItem&quot; } ,

 // --- Computed fields (written by tasks during processing) ---
 &quot;validationResult&quot; : { &quot;type&quot; : &quot;object&quot; , &quot;required&quot; : false , &quot;writtenBy&quot; : &quot;Validate Receipts&quot; } ,
 &quot;categories&quot; : { &quot;type&quot; : &quot;array&quot; , &quot;required&quot; : false , &quot;writtenBy&quot; : &quot;Categorize Expenses&quot; } ,
 &quot;anomalyFlags&quot; : { &quot;type&quot; : &quot;array&quot; , &quot;required&quot; : false , &quot;writtenBy&quot; : &quot;Flag Anomalies&quot; } ,
 &quot;managerDecision&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;enum&quot; : [ &quot;approved&quot; , &quot;rejected&quot; , &quot;needs_info&quot; ] } ,
 &quot;financeDecision&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;enum&quot; : [ &quot;approved&quot; , &quot;rejected&quot; , &quot;hold&quot; ] } ,
 &quot;paymentRef&quot; : { &quot;type&quot; : &quot;string&quot; , &quot;required&quot; : false , &quot;writtenBy&quot; : &quot;Process Payment&quot; }
 }
 }
 {
 &quot;entityName&quot;: &quot;ExpenseReport&quot;,
 &quot;fields&quot;: {
 // --- Input fields (populated at case creation) ---
 &quot;reportId&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true, &quot;generated&quot;: true },
 &quot;employeeId&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;employeeName&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;department&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: true },
 &quot;totalAmount&quot;: { &quot;type&quot;: &quot;decimal&quot;, &quot;required&quot;: true },
 &quot;currency&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;default&quot;: &quot;USD&quot; },
 &quot;lineItems&quot;: { &quot;type&quot;: &quot;array&quot;, &quot;items&quot;: &quot;ExpenseLineItem&quot; },

 // --- Computed fields (written by tasks during processing) ---
 &quot;validationResult&quot;: { &quot;type&quot;: &quot;object&quot;, &quot;required&quot;: false, &quot;writtenBy&quot;: &quot;Validate Receipts&quot; },
 &quot;categories&quot;: { &quot;type&quot;: &quot;array&quot;, &quot;required&quot;: false, &quot;writtenBy&quot;: &quot;Categorize Expenses&quot; },
 &quot;anomalyFlags&quot;: { &quot;type&quot;: &quot;array&quot;, &quot;required&quot;: false, &quot;writtenBy&quot;: &quot;Flag Anomalies&quot; },
 &quot;managerDecision&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;approved&quot;, &quot;rejected&quot;, &quot;needs_info&quot;] },
 &quot;financeDecision&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;enum&quot;: [&quot;approved&quot;, &quot;rejected&quot;, &quot;hold&quot;] },
 &quot;paymentRef&quot;: { &quot;type&quot;: &quot;string&quot;, &quot;required&quot;: false, &quot;writtenBy&quot;: &quot;Process Payment&quot; }
 }
}

 Troubleshooting ​

 link

 Problem Cause Resolution A computed field contains unexpected or stale data. Multiple tasks write to the same field. The last writer overwrites the previous value. Audit your output mappings. Assign each field to exactly one task and use namespaced field names. A rule never evaluates to true . The field referenced in the rule&#x27;s IF clause is not yet written by the time the rule evaluates. Verify that the task responsible for writing the field completes within the current or a preceding stage. A variable does not appear in the entity selector. The field is not defined in the deployed version of the case entity schema. Add the field to the schema, republish, and redeploy the case plan. Input fields are being overwritten during processing. A task output mapping targets an input field. Remove the output mapping that targets the input field. Document input fields as read-only in your schema.
 Limitations ​

 link

- Native case-entity support in Data Fabric is not yet available. Use one of the three sourcing options described in Step 2 .

- The writtenBy annotation is a design-time documentation convention. The platform does not enforce single-writer constraints at runtime. Developers must verify field ownership through review.

- Case user roles and access support (restricting which personas can edit specific entity fields) is not yet available.

 Next steps ​

 link

- How to model primary and secondary stages — Learn how to configure stage rules that consume your entity fields.

- Input and output mapping reference — Detailed reference for wiring entity fields to task parameters.

- Maestro Case tutorial: Property insurance claims — End-to-end tutorial that applies these schema design principles to a complete case plan.
 On this page
- Overview ​
- Prerequisites ​
- Step 1: understanding the out-of-the-box data objects ​
- Step 2: choosing where the entity lives ​
- Step 3: identifying and categorize your fields ​
- Mapping out the full case lifecycle ​
- Classifying fields into two categories ​
- Marking input fields as read-only ​
- Step 4: establishing field ownership ​
- Assigning one writer per field ​
- Annotating ownership in your schema ​
- Using namespaced fields to avoid ambiguity ​
- Step 5: defining the schema ​
- Creating the entity in your chosen source ​
- Adding input fields first ​
- Adding computed fields with ownership annotations ​
- Reviewing a reference schema ​
- Step 6: wiring input and output mappings to tasks ​
- Configuring input mappings ​
- Configuring output mappings ​
- Verifying that output mappings respect field ownership ​
- Step 7: validating the schema against rules ​
- Expected outcome ​
- Code snippet ​
- Troubleshooting ​
- Limitations ​
- Next steps ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No PREVIOUS Process Repository NEXT Defining case keys (system vs. external) Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated