---
icon: fas fa-file-alt
order: 6
---

<p class="resume-actions"><a class="resume-download" href="{{ '/assets/resume/srinivasan-nanduri-resume.pdf' | relative_url }}" download>Download PDF</a><span>Two pages</span></p>

**Principal Engineer** · Cloud Infrastructure & Platform Engineering · Observability & AIOps · Distributed Systems

Bengaluru, India · [LinkedIn](https://www.linkedin.com/in/srinivasannanduri) · [X](https://x.com/snanduri_)

## Summary

I’m a principal engineer who builds the layers entire organizations depend on, from zero to one, then to scale. Across a 22+ year career, that has meant integration middleware connecting enterprise systems, 4 revenue-generating IBM Cloud services, the base platform for IBM Cloud Paks and, today, IBM Cloud IaaS’s observability stack and its platform foundation. I own their multi-year technical strategy; they serve 4 organizations and ~400 SREs, and AI agents now query their operational data directly. Different layers, one thread: making complex distributed systems dependable, secure and understandable.

I set direction through 7 lead architects and 4 engineering managers and represent observability on IBM Cloud’s architecture review boards, with sign-off before production. I stay hands-on at every level, from production Go and Python and code reviews to strategy and architecture documents and roadmaps. I mentor engineers on both craft and career and hold 8 US patents.

## Signature impact

- **Observability, cost and reliability:** Cut observability cost ~10x and MTTR ~60% by consolidating ~20 teams across 4 organizations onto one self-hosted stack with AI-assisted investigation, replacing third-party tooling and ending tool sprawl.
- **AI and operational data:** Built a streaming data lake on Kafka and Flink, orchestrated with Airflow, joining telemetry and incidents, and an MCP server that opens metrics and logs to AI agents. All ~400 SREs use them in incident response.
- **Teams and talent:** Built the teams that own the observability stack and platform foundation, partnering with engineering managers from hiring to delivery, and grew technical leads across the organization into senior architects.
- **Platform engineering:** Architected IBM Automation Foundation, the hybrid multi-cloud base platform for 4 IBM Cloud Paks.
- **Cloud-native services:** Took Event Notifications, App Configuration and Privileged Access Gateway (a managed bastion host that closed audit gaps for regulated workloads) from first design to general availability, and modernized Mobile Foundation.
- **Enterprise integration:** Led and built the SAP adapter that, in its original design, has moved through IBM’s WebSphere integration products for 15+ years and still serves thousands of enterprise customers via IBM App Connect.

## Experience

### IBM · Bengaluru, India · Jul 2008 – Present

India Software Lab (2008–2021) · India Systems Development Lab (2021–present)

Staff Software Engineer → Senior Staff → Advisory → Architect → STSM (Principal level)

#### Senior Technical Staff Member (STSM), IBM Cloud IaaS · Nov 2023 – Present

Chief Architect, Observability Stack & Platform Foundation

Conceived, architected and took to production the multi-tenant observability platforms for all 300+ IaaS services (34 data centers, 14 regions), the OpenShift-on-VPC platform foundation beneath them, and the operational data lake and AI-assisted incident investigation above them.

- **Build vs. buy:** Chose and defended a self-hosted Grafana OSS stack (Mimir, Loki, Alloy) on object storage after evaluating Thanos, VictoriaMetrics, Grafana Cloud, Coralogix, New Relic and IBM’s own Instana. Much of the undercloud can’t reach public SaaS, and self-hosting traded vendor convenience for architectural control and freedom from ingest-priced licensing.
- **Consolidation:** Moved teams in Compute, Network, Storage and Platform Integration off per-team stacks onto shared metrics, logs, events, alerting and visualization, across three generations of IBM Cloud infrastructure. Ran the stack as an internal product, shaping the roadmap around each team’s adoption patterns.
- **Alerting at scale:** Built one alerting system for every signal: ~20,000 rules in ~250 groups, with high-severity alerts evaluated first under load. Alert-quality standards give every alert an owner, a runbook and less noise.
- **Multi-tenant at scale:** Scaled to ~400M active time series (up to 100M in the largest region) and 2–10 TB of logs a day per regional instance, absorbing ~25% growth in IBM Cloud VPC, with tenant isolation, automated certificate lifecycle and GitOps delivery to every region. Designed Kafka-based ingestion that decouples durable ingest from query for independent scaling, replay and availability-zone resilience.
- **Data and AIOps:** Architected and built AI-assisted incident investigation on the operational data lake: a governed gateway over logs, metrics, Git and ServiceNow, and LLM agents that query telemetry through MCP and run operational tools in controlled sandboxes. Data governance controls what reaches the model; tool governance controls what agents may do.
- **Platform foundation:** Built the common foundation every platform in the portfolio runs on, writing its first implementation in Go and Python with operators, service mesh, and Terraform, Ansible, Helm and GitOps delivery. Moving from managed Kubernetes to self-hosted OpenShift cut cluster costs 30%.
- **Governance:** Own observability on the IaaS Systems Review Board, reviewing ~20 services in two years for failure modes and readiness. Established the portfolio’s architecture process: reference architectures, RFCs, ADRs and conformance checks.

#### Architect, Privileged Access Gateway, IBM Cloud · Jun 2021 – Nov 2023

- Took it from inception to general availability for customers, including ISVs, and to internal adoption across IBM Cloud, replacing third-party access tooling in core services and data centers.
- Designed policy-driven authorization, approval workflows and full session recording for audit and compliance.
- Led technology selection and proofs of concept, guided leads through delivery, and advised financial-services customers.

#### Architect, IBM Automation Foundation · Aug 2020 – Jun 2021

- Led architecture and development of operator-driven install, upgrade and lifecycle on Red Hat OpenShift, with shared base services and control planes used across IBM Cloud Paks.
- Delivered it as a service on AWS and IBM Cloud, and aligned product teams on packaging and operational contracts.

#### Technical Lead, IBM Cloud Platform Services · Feb 2013 – Aug 2020

- **IBM Event Notifications:** Built the multi-channel notification platform (originally IBM Push Notifications) and migrated it from monolith to microservices with zero downtime.
- **IBM Cloud App Configuration:** Designed and launched feature flags, audience targeting and progressive rollouts.
- **IBM Mobile Foundation:** Modernized it from on-premises to Cloud Foundry to Kubernetes and OpenShift.
- Partnered directly with global enterprise customers building on these services.

#### Technical Lead, Enterprise Middleware & Integration · Jul 2008 – Jan 2013

- Lead developer of the WebSphere Adapter for SAP, built on SAP JCo 3 (BAPI, IDoc, RFC).
- Designed MQ service discovery and change notification for WebSphere Service Registry, and owned 24×7 escalations.

### Software AG India · Pune, India · 2005 – 2008

Developer → Senior Developer → Team Lead

- Led the UDDI, JAXR and XQJ implementations and built Java middleware for Tamino XML Server and CentraSite.

### Tessera Systems · Hyderabad, India · 2003 – 2005

Associate Software Developer

- Built automated test suites for the company’s web services tooling (Java, SOAP, WSDL).

## Skills

- **Cloud & Platform:** IBM Cloud · AWS · Linux · Docker · Kubernetes · Red Hat OpenShift · Cloud Foundry · Operators · Service mesh (Istio) · Multi-tenancy · Multi-region architecture · Fleet management (Red Hat ACM) · Terraform · Ansible · Helm · Argo CD · Tekton · Jenkins · GitOps
- **Architecture:** Distributed systems · Fault tolerance · Replication & consistency · Partitioning & sharding · Stream processing · Microservices · Event-driven architecture · REST API design · gRPC · High availability & disaster recovery · Performance engineering · SAP & MQ integration
- **Observability & SRE:** Grafana OSS · Prometheus · OpenTelemetry · Fluent Bit · eBPF · Telemetry pipelines · Monitoring · SLI/SLO · Error budgets · Root cause analysis (RCA) · Capacity planning · Cardinality & cost control
- **Data & Applied AI:** Apache Kafka · Apache Flink · Airflow · PostgreSQL · Db2 · Cloudant (CouchDB) · Redis · Elasticsearch · AIOps · LLM agents · Model Context Protocol (MCP) · Agent & tool orchestration · AI governance
- **Security:** Zero trust · PKI · mTLS · Privileged access management · Policy-driven authorization · Audit & compliance
- **Languages & SDKs:** Go · Python · Java · Server & client SDKs · Mobile SDKs (Android, hybrid)
- **Technical Leadership:** Technical strategy & roadmaps · Architecture governance · Technology & vendor evaluation · FinOps · Cross-org alignment · Hiring & team building · Mentoring · Customer engagement

## Patents

8 granted US patents · IBM Invention Plateau, 2nd level (IBM recognition for sustained invention output)

- Assistant for cloud architectures, US 12,591,458 (2026)
- Intelligent attribute value substitution in infrastructure as code (IAC) generation, US 12,730,614 (2026)

## Recognition & thought leadership

- **Awards:** IBM Outstanding Technical Achievement Awards: 2025 (scalable, cost-efficient observability), 2018, 2016
- **Speaking:** Bangalore SRE Meetup · Cloud Foundry Days · IBM Think · IBM Cloud Technical University
- **Writing:** Handbook for Engineers: 7 Best Practices for Hybrid Cloud Innovation and Trust in Regulated Industries, Express Computer, 2024 · Feature Flags: The Hidden Gem to Agility, CIO Advisor, 2019 · Five IBM Developer articles, 2016–2018
- **Developing Leaders:** Co-facilitator, IBM Leadership Academy · Mentor via IBM JumpStart and Extreme Blue

## Education

- Master of Computer Applications (MCA) · M.S. University, Tirunelveli
- B.Sc. (Computer Science) · Andhra University, Visakhapatnam
