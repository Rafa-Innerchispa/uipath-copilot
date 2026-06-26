# UiPath CLI - About UiPath CLI

- **URL:** https://docs.uipath.com/uipath-cli/standalone/latest/user-guide/coding-agent
- **Content-Type:** text/html; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

UiPath CLI - About UiPath CLI
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
- search Search ​ Language translate English expand_more ​ Sign in uipath-cli latest false UiPath CLI Standalone · latest - Collapse
- Overview
- About UiPath CLI
- What&#x27;s new
- Versioning and stability
- Get started
- Installing UiPath CLI
- First commands (quickstart)
- Your first pipeline
- Concepts
- Overview
- How UiPath CLI is organized
- Tools (plugins)
- Skills
- Sessions and credentials
- Using UiPath CLI
- Overview
- Authentication
- Configuration (uipath.config.json)
- Output formats (table, JSON, YAML)
- Scripting patterns
- Managing tools and skills
- UiPath for Coding Agents
- Using UiPath CLI with Coding Agents
- Operate with UiPath for Coding Agents
- Troubleshoot with UiPath for Coding Agents
- How-to guides
- Overview
- Pack and publish a solution
- Deploy to Orchestrator from CI
- Run tests in a pipeline
- Deploy an Agent
- Manage Orchestrator assets and queues
- CI/CD recipes
- Azure DevOps
- GitHub Actions
- Jenkins
- GitLab CI
- Command reference
- Overview
- Exit codes
- Global options
- uip
- uip login
- uip logout
- uip login status
- uip tools
- uip skills
- uip mcp
- uip completion
- uip agent
- init
- config
- pack
- publish
- deploy
- run
- validate
- push / pull
- list / share
- file
- context-manage
- io-manage
- tool-manage
- escalation-manage
- eval
- uip api-workflow
- pack
- build
- run
- uip codedagent
- uip codedapp
- push
- pull
- pack
- publish
- deploy
- uip df
- entities
- records
- files
- uip docsai
- uip flow
- init
- pack
- debug
- validate
- node / edge
- process / processes
- instances
- incidents
- job
- registry
- uip insights
- jobs
- uip is
- connectors
- connections
- activities
- resources
- triggers
- uip maestro
- init
- pack
- debug
- process / processes
- instances
- incidents
- job
- registry
- uip or
- jobs
- folders
- processes
- packages
- machines
- users
- roles
- licenses
- feeds
- attachments
- sessions
- calendars
- credential-stores
- audit-logs
- settings
- uip platform
- tenants
- users
- groups
- licenses
- uip resource
- assets
- buckets
- bucket-files
- libraries
- queues
- queue-items
- triggers
- webhooks
- uip rpa
- add-test-data-entity
- add-test-data-queue
- add-test-data-variation
- analyze
- build
- create-project
- diff
- find-activities
- get-analyzer-rules
- get-default-activity-xaml
- get-errors
- get-manual-test-cases
- get-manual-test-steps
- get-versions
- get-workflow-example
- indicate-application
- indicate-element
- inspect-package
- install-data-fabric-entities
- install-or-update-packages
- list-data-fabric-entities
- list-workflow-examples
- pack
- restore
- run-file
- search-templates
- start-studio
- stop-execution
- uia
- uip rpa-legacy
- debug
- find-activities
- find-package
- package
- type-definition
- validate
- uip solution
- new
- pack
- publish
- upload
- bundle
- project
- packages
- deploy
- resource
- uip tm
- attachment
- customfield
- executions
- objectlabel
- project
- report
- requirements
- result
- testcases
- testsets
- teststeplog
- user
- wait
- uip traces
- uip vss
- init
- scaffold
- sync
- add
- generate
- Migration
- Overview
- Migrating from the legacy .NET CLI
- Command map (legacy to uip)
- Flag renames
- Breaking changes
- Reference &amp; support
- Troubleshooting Home Open Dropdown to choose product UiPath CLI ​ Standalone latest About UiPath CLI UiPath CLI user guide

 About UiPath CLI

 link Note: UiPath CLI is currently in Public preview . All releases prior to version 1.0.0 are preview releases and may include breaking changes between versions. Version 1.0.0 will mark the first stable release.

 UiPath Command-Line Interface ( UiPath CLI , invoked as uip ) is the cross-platform command-line tool for the UiPath platform. It lets developers, RPA engineers, and DevOps teams build, manage, operate, and deploy UiPath automations — Orchestrator jobs and resources, Solutions, Agents, Flows, Maestro processes, Test Manager assets, and more — from a terminal or a CI/CD pipeline.

 UiPath CLI is distributed on npm and follows semantic versioning ( MAJOR.MINOR.PATCH ). This replaces the calendar-based scheme used up to 2025.10 and the legacy .NET CLI ( uipcli.exe ).

 Note: This is the documentation for UiPath CLI (the TypeScript-based uip command). For the legacy .NET CLI ( uipcli.exe / dotnet uipcli.dll ), see the CI/CD integrations 2025.10 docs . A migration guide is available.

 For the Azure DevOps extension , Jenkins plugin , and other pipeline integrations, see CI/CD integrations .

 More than a CI/CD tool ​

 link
 Earlier UiPath command-line tooling focused on CI/CD tasks — pack, analyze, deploy, run tests. UiPath CLI 1.x keeps all of that and adds the full platform surface. You can use uip to:

- Build — scaffold projects ( uip solution new , uip agent init , uip flow init , uip maestro init ), pack ( uip rpa pack , uip solution pack , uip agent pack ), and analyze ( uip rpa analyze with governance policies).

- Manage — work with Orchestrator folders, users, roles, and licenses; create and update assets, queues, storage buckets, libraries, triggers, and webhooks; administer Test Manager projects, test sets, and results; manage Integration Service connectors and connections.

- Operate — start, stop, and inspect Orchestrator jobs; monitor Flow and Maestro instances and incidents; run Agents and evaluate them against datasets; execute test sets and read results.

- Deploy — upload packages, create and update processes, publish Solutions and Agents, activate or uninstall Solution deployments.

 This is the same tool whether you are a developer exploring the platform from a laptop or a pipeline doing unattended deployments. The verbs, flags, output formats, and exit codes are the same in both contexts.

 Designed for humans and coding agents ​

 link
 UiPath CLI is designed to be consumed equally well by two audiences:

- Humans — a terminal-first experience with interactive uip login , shell tab completion ( uip completion ), colored --output table view, and help embedded on every command ( uip &lt;cmd&gt; --help ).

- Coding agents — the uip skills system installs UiPath skills into coding agents so they know how to build, deploy, and operate UiPath automations with uip — not just which commands exist. Supported agents: Claude Code , Cursor , GitHub Copilot , Gemini CLI , Codex , and OpenCode .

 uip skills install fetches the full UiPath skill catalog from GitHub and installs it into one or more coding agents. You pick the target agents (not individual skills — the agent itself decides which skill applies to a given task) either by passing --agent &lt;name&gt; or interactively from a checkbox prompt when the flag is omitted. By default the install is global; add --local to scope skills to the current project (where the agent supports it — Claude Code is global-only, for example).

 assignment uip skills install # prompts you to pick one or more agents
uip skills install -- agent claude # non - interactive , skills installed globally for Claude Code
uip skills install -- agent cursor -- local # non - interactive , skills installed into the current project for Cursor
uip skills update -- agent claude # re - fetch and reinstall to pick up new skills
uip skills uninstall -- agent claude # remove skills for Claude Code
 uip skills install # prompts you to pick one or more agents
uip skills install --agent claude # non-interactive, skills installed globally for Claude Code
uip skills install --agent cursor --local # non-interactive, skills installed into the current project for Cursor
uip skills update --agent claude # re-fetch and reinstall to pick up new skills
uip skills uninstall --agent claude # remove skills for Claude Code

 The same commands work either way. A uip invocation that a developer types by hand is the exact same call an agent makes — which means your team can build an automation interactively, pipe the exact sequence into a script, and hand it to an AI agent to iterate further.

 Output is JSON by default — the same on a developer laptop and in a pipeline, so scripts do not need to branch on whether they are running interactively. Add --output table for the reading-friendly view, --output yaml for YAML, or --output plain for key=value lines. JMESPath filtering is available via --output-filter &quot;Data[*].Name&quot; .

 How UiPath CLI is organized ​

 link
 uip is a small host with a plugin system. The host handles authentication, session management, configuration, and tool lifecycle. Everything else — Orchestrator, Solution, Agent, Flow, Maestro, RPA, Test Manager, and so on — ships as an installable tool on npm.

 assignment uip &lt; tool &gt; &lt; resource - or - command &gt; [ subcommand ] [ options ]
 uip &lt;tool&gt; &lt;resource-or-command&gt; [subcommand] [options]

 Examples:

 assignment uip login # core command
uip or jobs list # orchestrator jobs ( manage + operate )
uip solution pack . / MySolution . / dist # solution packing ( build )
uip rpa analyze . / MyProject # workflow analyzer ( build )
uip agent deploy my - agent # agent deploy ( deploy )
 uip login # core command
uip or jobs list # orchestrator jobs (manage + operate)
uip solution pack ./MySolution ./dist # solution packing (build)
uip rpa analyze ./MyProject # workflow analyzer (build)
uip agent deploy my-agent # agent deploy (deploy)

 A fresh npm install -g @uipath/cli contains only the host and core commands — no tools are preinstalled . The first time you invoke a command whose prefix matches a tool on the whitelist, the host installs that tool from npm automatically. You can also install tools explicitly with uip tools install &lt;name&gt; — useful for offline preparation and CI runners. See Tools (plugins) for details.

 Built-in tools ​

 link
 All tools below are on the auto-install whitelist — typing the prefix is enough. Prefixes shown are the canonical names as defined in the host:

 Tool Prefix Purpose Orchestrator or Jobs, folders, processes, packages, machines, users, roles, licenses, feeds Solution solution Scaffold, pack, publish, upload, deploy UiPath Solutions Resource resource Assets, queues, storage buckets, libraries, triggers, webhooks RPA rpa Studio-project packaging, workflow analyzer, dependency restore Agent agent Low-code Agent authoring, packaging, deployment, execution Coded Agent codedagent Python-based Coded Agents Coded App codedapp Coded web application projects Maestro maestro Maestro project authoring, packaging, runtime operations Test Manager tm Test cases, test sets, executions, results, reports Integration Service is Connectors and connections Vertical Solutions vss Vertical Solution scaffolding and generation API Workflow api-workflow Local execution of UiPath API Workflows Data Fabric df Data Fabric operations Insights insights Insights dashboards and reporting Traces traces Execution traces and diagnostics DocsAI docsai AI-powered UiPath documentation search
 Tip: Run uip --help to see the exact prefixes in your installation, and uip tools list to see which tools are currently installed. Only the whitelisted @uipath/ tools above are supported in UiPath CLI 1.x; third-party extension is not available yet. The Flow tool ( @uipath/flow-tool ) is published but not on the auto-install whitelist — install it explicitly with uip tools install @uipath/flow-tool before using uip flow commands.

 Authentication at a glance ​

 link
 UiPath CLI supports three authentication flows. The interactive flow is new in 1.x; the other two have analogs in the legacy .NET CLI.

 Flow When to use it How to use it Interactive OAuth2 user login (new in 1.x) Developers working from a terminal. Binds the session to your personal account and its permissions. uip login opens a browser for sign-in and selects a tenant. Session tokens are stored and refreshed automatically. External App (client credentials) CI/CD pipelines, servers, any non-interactive context. Binds the session to an External App you create in UiPath, with explicit scopes. uip login --client-id env.UIPATH_CLIENT_ID --client-secret env.UIPATH_CLIENT_SECRET --tenant &lt;name&gt; — the env.VAR prefix reads the secret from an environment variable without exposing it on the command line. Environment-variable auth Containers and ephemeral runners that already hold a UiPath access token. No browser, no External App round-trip, no on-disk state. Set UIPATH_CLI_ENABLE_ENV_AUTH=true and supply UIPATH_CLI_AUTH_TOKEN + organization / tenant variables. Every uip command authenticates from the env vars; there is no refresh.
 See Authentication for the full flow, tenant selection, credential folder layout, and how to pre-configure External Apps for CI.

 UiPath CLI versus the legacy .NET CLI ​

 link

 Aspect UiPath CLI ( uip , 1.x) Legacy .NET CLI ( uipcli , 2025.10 and earlier) Runtime Node.js (cross-platform) .NET 8 (Windows-first) Distribution npm install -g @uipath/cli .nupkg on MyGet / NuGet feed Versioning Semantic versioning ( 1.0.0 , 1.1.0 , …) Calendar versioning ( 2023.10 , 2024.10 , 2025.10 ) Scope Build, manage, operate, deploy across the full platform CI/CD focused — pack, analyze, deploy, run tests Authentication Interactive OAuth2 ( uip login ) and External App (client credentials) External App (client credentials), plus deprecated basic/token auth Architecture Modular tools, auto-installed on first use from npm Monolithic executable Output formats table , json , yaml , plain with JMESPath filtering Text / JSON (limited) AI integration Skills system for coding agents Not available Workflow Analyzer Preserved as uip rpa analyze , with governance-file policy support Bundled with CLI ( uipcli package analyze ) Dependency restore Preserved as uip rpa restore , with air-gapped and NuGet-config support Bundled with CLI ( uipcli package restore )
 If you are starting a new pipeline today, use UiPath CLI 1.x. If you are maintaining existing Azure DevOps or Jenkins pipelines built on uipcli.exe , see the migration guide for the command map, flag renames, and breaking changes.

 UiPath CLI versus the CI/CD plugins ​

 link
 UiPath CLI ( uip ) is the tool . The Azure DevOps extension, the Jenkins plugin, and similar pipeline integrations are wrappers around that tool — they package uip invocations behind UI-driven task forms, secure variable injection, and pipeline-native logging. Going forward, newer versions of those plugins will call uip internally.

 Use the plugin when you want the pipeline UI and variable management. Use uip directly (via a bash or pwsh step) when you want the latest CLI capabilities without waiting for a plugin release, or when you need a command the plugin does not expose.

 See CI/CD integrations for the plugin documentation.

 Supported platforms ​

 link
 UiPath CLI 1.x runs on any platform that supports Node.js 18 or later:

- Windows (x64, ARM64)

- macOS (x64, ARM64)

- Linux (x64, ARM64)

 Stability and release cadence ​

 link
 UiPath CLI follows semantic versioning:

- MAJOR — breaking changes to command names, flag semantics, or the JSON envelope. A deprecation cycle precedes any MAJOR release.

- MINOR — new commands, new flags, new tools; additive only. Note that the shape of Data in JSON output is command-specific and may change in MINOR releases; pipelines should pin @uipath/cli .

- PATCH — bug fixes; no documented behavior change.

 Individual commands and tools are labeled GA , Preview , or Deprecated . Preview commands may change without a major version bump; deprecated commands keep working for at least one MAJOR cycle. See Versioning and stability for the full contract.

 Next steps ​

 link

- Install UiPath CLI — set up uip on Windows, macOS, or Linux.

- Quickstart — log in, list Orchestrator folders, and run a job in five minutes.

- Your first pipeline — pack a project and deploy it from a CI pipeline.

- Using UiPath CLI with Coding Agents — install skills into Claude Code, Cursor, GitHub Copilot, or Gemini CLI and let them build UiPath automations with uip .

- Command reference — full reference for every command.

- Migrating from the legacy .NET CLI — if you are coming from uipcli.exe .
 On this page
- More than a CI/CD tool ​
- Designed for humans and coding agents ​
- How UiPath CLI is organized ​
- Built-in tools ​
- Authentication at a glance ​
- UiPath CLI versus the legacy .NET CLI ​
- UiPath CLI versus the CI/CD plugins ​
- Supported platforms ​
- Stability and release cadence ​
- Next steps ​ Help improve this page Was this page helpful?

 thumb_up Yes thumb_down No NEXT What&#x27;s new Connect

 Need help? Support

 Want to learn? UiPath Academy

 Have questions? UiPath Forum

 Stay updated