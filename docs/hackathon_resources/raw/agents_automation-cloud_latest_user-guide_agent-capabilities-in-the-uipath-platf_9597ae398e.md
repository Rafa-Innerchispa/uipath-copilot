# https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-capabilities-in-the-uipath-platform.md

- **URL:** https://docs.uipath.com/agents/automation-cloud/latest/user-guide/agent-capabilities-in-the-uipath-platform.md
- **Content-Type:** text/markdown; charset=utf-8
- **Scraped:** scripts/scrape_hackathon_resources.py
## Contenido extraído

# Agent capabilities in the UiPath Platform™

> Agent orchestration and management capabilities in the UiPath Platform, supporting agents of any origin or runtime environment.

UiPath® offers a comprehensive platform for orchestrating and managing a wide range of agents, regardless of their origin or runtime environment. This flexibility lets you leverage the best agent for each specific task, optimizing your automation processes.

In the UiPath Platform™, you can interact with the following types of agents:

Figure 1. Agent types

![The types of agents you can interact with in the UiPath Platform](https://dev-assets.cms.uipath.com/assets/images/agents/agents-docs-image-5-31bc8e3c.webp)

## UiPath system agents

UiPath system agents are built-in, platform-managed tools like [Autopilot](https://docs.uipath.com/autopilot/other/latest/overview/about-autopilot) and [Healing Agent](https://docs.uipath.com/agents/automation-cloud/latest/user-guide-ha/what-is-healing-agent), designed to enhance the overall automation experience.

## UiPath-built agents

UiPath-built agents are created using the Agent designer canvas in Studio Web. The UiPath low-code development application enables business users and citizen developers to create powerful agents with minimal traditional coding expertise.

UiPath-built agents benefit from:

* Speed and ease of development: Enabling quick agent creation.
* UiPath Platform integration: Integration with Orchestrator for management, scheduling, and monitoring, and leveraging the full spectrum of UiPath resources, including: activities, other agents, apps, tasks, and Maestro for business process orchestration.

For details, refer to [Building an agent in Studio Web](https://docs.uipath.com/agents/automation-cloud/latest/user-guide/building-an-agent-in-studio-web#building-an-agent-in-studio-web).

## UiPath coded agents

UiPath coded agents are developed by coding experts using UiPath SDKs within their preferred integrated development environment (IDE). Developers can then package and publish these coded agents to the UiPath ecosystem, where they run on Automation Cloud Robots – Serverless infrastructure.

Coded agents benefit from:

* Flexibility and power of custom code: Allowing for highly tailored automations with complex logic.
* UiPath Platform integration: Integration with Orchestrator for management, scheduling, and monitoring, and leveraging the full spectrum of UiPath resources, including: activities, other agents, apps, tasks, and Maestro for business process orchestration.

Coded agents can also be connected to Studio Web, which acts as a control plane for debugging, evaluation, and publishing without leaving the UiPath platform. Alternatively, existing low-code agents built in Studio Web can be cloned as coded agents, letting developers take full ownership of the implementation in their IDE while retaining access to the same platform capabilities.

For details, refer to [About coded agents](https://docs.uipath.com/agents/automation-cloud/latest/user-guide/about-coded-agents).

## External agents

UiPath capabilities extend to incorporating and managing agents built outside UiPath. You can invoke coded or low-code agents from other platforms, integrating pre-existing agents in UiPath for end-to-end, cross-platform business processes orchestration via UiPath [Maestro™](https://docs.uipath.com/maestro/automation-cloud/latest/user-guide/introduction-to-maestro).