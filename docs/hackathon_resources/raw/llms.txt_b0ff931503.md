# https://docs.uipath.com/llms.txt

- **URL:** https://docs.uipath.com/llms.txt
- **Content-Type:** text/plain; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

# UiPath Documentation

> Complete reference documentation for UiPath products.

## How to interpret this index

This index explains how UiPath docs URLs map to product, delivery model, version, and guide type, so answers are grounded in the correct source scope. Platform-level guide locations are defined in the platform-pair sections below.

- Coverage scope:
 - Public production documentation only.
 - Included versions: 2023.10 and newer.
 - Versions older than 2023.10 are excluded.

- URL pattern:
 - https://docs.uipath.com/[product]/[delivery-model]/[version]/[guide-type]/[page-slug]
 - Add `.md` to retrieve the Markdown version.
 - Example:
 - https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-capabilities-in-the-uipath-platform.md
 - product = agents
 - delivery-model = automation-cloud
 - version = latest
 - guide-type = user-guide
 - page-slug = agent-capabilities-in-the-uipath-platform

- Delivery models:
 - automation-cloud: canonical cloud documentation.
 - automation-suite: on-premises platform documentation.
 - standalone:
 - desktop: Robot, Assistant, Studio, StudioX
 - web-based: all other standalone products
 - other: hybrid or special deployment models.

- Versioning:
 - Automation Cloud uses latest.
 - Automation Suite uses:
 - calendar format for 2024.10 and older
 - product format for 2.2510 and newer
 - Web-based standalone uses versioned calendar-format releases (for example, 2025.10).
 - Desktop standalone provides:
 - latest (version used for forward development)
 - stable versioned calendar-based releases (for example, 2025.10)

- Automation Cloud and Test Cloud:
 - Both use the same delivery option in URLs: automation-cloud.
 - They are different platform contexts under that same delivery option.
 - FPS docs are shared.
 - Platform docs are separate:
 - Automation Cloud: https://docs.uipath.com/automation-cloud/automation-cloud/latest
 - Test Cloud: https://docs.uipath.com/test-cloud/automation-cloud/latest
 - Flavors: Commercial, Public Sector, Dedicated.
 - Non-release-notes guides are shared across all flavors; flavor differences are tracked in `[product]-feature-availability`.
 - Release notes are flavor-specific, with page slug patterns:
 - Commercial: `[month]-[year]`
 - Public Sector: `public-sector-[month]-[year]`
 - Dedicated: `dedicated-[month]-[year]`

- Automation Suite and Private Test Cloud:
 - Both use the same delivery option in URLs: automation-suite.
 - They are different platform contexts under that same delivery option.
 - FPS docs are shared.
 - Platform docs are separate:
 - Automation Suite: https://docs.uipath.com/automation-suite/automation-suite/[version]
 - Private Test Cloud: https://docs.uipath.com/private-test-cloud/automation-suite/[version]
 - Flavors: Linux, EKS/AKS, OpenShift.
 - FPS docs are shared across all flavors.
 - Installation guides and release notes are flavor-specific.
 - Release note page slug families:
 - `automation-suite-[version]`
 - `automation-suite-on-eks-aks-[version]`
 - `automation-suite-on-openshift-[version]`
 - `private-test-cloud-on-linux-[version]`
 - `private-test-cloud-on-eks-aks-[version]`
 - `private-test-cloud-on-openshift-[version]`

- Cross-product platform guides:
 - Release notes: https://docs.uipath.com/release-notes/other/latest/release-notes/
 - Overview: https://docs.uipath.com/overview/other/latest/overview/
 - These provide cross-product context and do not replace product-level procedural docs.

- Language:
 - Multiple localized versions are available.
 - If no language segment is present, default to English.

- Scope and compatibility rules:
 - automation-cloud, automation-suite, and web-based standalone are mutually exclusive contexts and are not combined in one answer.
 - desktop standalone content can be combined with any of those contexts when relevant.
 - Content is not interchangeable across delivery models or versions.

- Source precedence:
 - Prefer sources that match the exact delivery model and version.
 - If matching sources conflict, prefer the newer release notes entry.

- Answer resolution:
 - Resolve one scope per answer: product + delivery model + version.
 - If scope is ambiguous, request clarification before answering.

- Current version anchors: These values are the default version anchors used when a query asks for “latest” or does not explicitly specify a version.
 - Automation Cloud: latest
 - Automation Suite: latest public version = 2.2510
 - Desktop standalone: latest (version used for forward development), 2025.10 (latest stable)
 - Web-based standalone: latest public version = 2025.10

- [Action Center](https://docs.uipath.com/llms-action-center.txt)
- [Activities](https://docs.uipath.com/llms-activities.txt)
- [Add-ins](https://docs.uipath.com/llms-add-ins.txt)
- [Agents](https://docs.uipath.com/llms-agents.txt)
- [AI Center](https://docs.uipath.com/llms-ai-center.txt)
- [AI Computer Vision](https://docs.uipath.com/llms-ai-computer-vision.txt)
- [Apps](https://docs.uipath.com/llms-apps.txt)
- [Assistant](https://docs.uipath.com/llms-assistant.txt)
- [Assistant Web](https://docs.uipath.com/llms-assistant-web.txt)
- [Automation Cloud](https://docs.uipath.com/llms-automation-cloud.txt)
- [Automation Hub](https://docs.uipath.com/llms-automation-hub.txt)
- [Automation Ops](https://docs.uipath.com/llms-automation-ops.txt)
- [Automation Suite](https://docs.uipath.com/llms-automation-suite.txt)
- [Autopilot](https://docs.uipath.com/llms-autopilot.txt)
- [CICD Integrations](https://docs.uipath.com/llms-cicd-integrations.txt)
- [Clipboard AI](https://docs.uipath.com/llms-clipboard-ai.txt)
- [Customer Portal](https://docs.uipath.com/llms-customer-portal.txt)
- [Data Service](https://docs.uipath.com/llms-data-service.txt)
- [UiPath Platform Installer](https://docs.uipath.com/llms-uipath-platform-installer.txt)
- [Document Understanding](https://docs.uipath.com/llms-document-understanding.txt)
- [Functions](https://docs.uipath.com/llms-functions.txt)
- [High Availability Add-on](https://docs.uipath.com/llms-high-availability-add-on.txt)
- [Industry & Department Solutions](https://docs.uipath.com/llms-industry-department-solutions.txt)
- [Insights](https://docs.uipath.com/llms-insights.txt)
- [Integration Service](https://docs.uipath.com/llms-integration-service.txt)
- [IXP](https://docs.uipath.com/llms-ixp.txt)
- [Maestro](https://docs.uipath.com/llms-maestro.txt)
- [Marketplace](https://docs.uipath.com/llms-marketplace.txt)
- [Orchestrator](https://docs.uipath.com/llms-orchestrator.txt)
- [Overview](https://docs.uipath.com/llms-overview.txt)
- [Private Test Cloud](https://docs.uipath.com/llms-private-test-cloud.txt)
- [Process Mining](https://docs.uipath.com/llms-process-mining.txt)
- [Release notes](https://docs.uipath.com/llms-release-notes.txt)
- [Robot](https://docs.uipath.com/llms-robot.txt)
- [SDK](https://docs.uipath.com/llms-sdk.txt)
- [Solutions Management](https://docs.uipath.com/llms-solutions-management.txt)
- [Studio](https://docs.uipath.com/llms-studio.txt)
- [StudioX](https://docs.uipath.com/llms-studiox.txt)
- [Studio Web](https://docs.uipath.com/llms-studio-web.txt)
- [Task Mining](https://docs.uipath.com/llms-task-mining.txt)
- [Test Manager](https://docs.uipath.com/llms-test-manager.txt)
- [Test Cloud](https://docs.uipath.com/llms-test-cloud.txt)
- [UiPath CLI](https://docs.uipath.com/llms-uipath-cli.txt)