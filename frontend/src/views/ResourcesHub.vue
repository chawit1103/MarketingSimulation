<template>
  <div class="resources-page">
    <nav class="navbar">
      <div class="nav-brand">3C SIMULATOR</div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/proof-of-value" class="nav-link">Proof of Value</router-link>
        <router-link to="/strategic-command" class="nav-link">Strategic Command</router-link>
        <router-link to="/campaigns" class="nav-link">Campaigns</router-link>
        <router-link to="/settings" class="nav-link">Settings</router-link>
      </div>
    </nav>

    <main class="resources-shell">
      <header class="resources-header">
        <div>
          <span class="page-kicker">Operator and Sales Resources</span>
          <h1>Proof-of-Value Resource Hub</h1>
          <p>
            Curated links for running a customer proof-of-value session, preparing sales material,
            checking data boundaries, and assembling safe customer-facing demo artifacts.
          </p>
        </div>
        <a class="primary-link" :href="githubDocsRoot" target="_blank" rel="noreferrer">
          Open docs folder
        </a>
      </header>

      <section class="boundary-panel" aria-label="Pilot readiness boundary">
        <div class="panel-heading">
          <h2>Readiness Boundary</h2>
          <p>Use these boundaries when positioning a proof-of-value session or controlled private pilot.</p>
        </div>
        <dl class="readiness-grid">
          <div v-for="item in readinessBoundary" :key="item.label" :class="['readiness-item', item.status]">
            <dt>{{ item.label }}</dt>
            <dd>{{ item.value }}</dd>
          </div>
        </dl>
      </section>

      <section class="guardrail-panel" aria-label="Proof-of-value guardrails">
        <h2>Guardrails</h2>
        <ul>
          <li v-for="guardrail in guardrails" :key="guardrail">{{ guardrail }}</li>
        </ul>
      </section>

      <section class="resource-sections" aria-label="Proof-of-value documentation links">
        <article v-for="section in resourceSections" :key="section.title" class="resource-section">
          <div class="section-heading">
            <span>{{ section.eyebrow }}</span>
            <h2>{{ section.title }}</h2>
            <p>{{ section.description }}</p>
          </div>
          <div class="doc-list">
            <a
              v-for="doc in section.docs"
              :key="doc.path"
              class="doc-card"
              :href="doc.route || docUrl(doc.path)"
              :target="doc.route ? undefined : '_blank'"
              :rel="doc.route ? undefined : 'noreferrer'"
            >
              <span class="doc-path">{{ doc.path }}</span>
              <strong>{{ doc.title }}</strong>
              <p>{{ doc.description }}</p>
            </a>
          </div>
        </article>
      </section>
    </main>
  </div>
</template>

<script setup>
const githubDocsRoot = 'https://github.com/chawit1103/MarketingSimulation/tree/multilang-v0.3/docs'
const githubBlobRoot = 'https://github.com/chawit1103/MarketingSimulation/blob/multilang-v0.3/'

const docUrl = (path) => `${githubBlobRoot}${path}`

const readinessBoundary = [
  { label: 'Local demo', value: 'ready', status: 'ready' },
  { label: 'Controlled private pilot', value: 'conditional candidate', status: 'conditional' },
  { label: 'Public pilot', value: 'blocked', status: 'blocked' },
  { label: 'Public internet exposure', value: 'blocked', status: 'blocked' },
  { label: 'Production customer deployment', value: 'blocked', status: 'blocked' },
]

const guardrails = [
  'No PII',
  'No raw CRM records',
  'No customer lists',
  'No secrets',
  'No live integrations',
  'Decision-support estimate only',
]

const resourceSections = [
  {
    eyebrow: 'Start Here',
    title: 'Start Here: First Customer',
    description: 'Recommended founder-led execution order for selling, running, and closing the first customer proof-of-value session.',
    docs: [
      {
        title: 'Proof-of-Value Outreach Message Pack',
        path: 'docs/PROOF_OF_VALUE_OUTREACH_PACK.md',
        description: 'Founder-led outreach, follow-up, brief request, and objection-response copy.',
      },
      {
        title: 'Founder First Customer Close Pack',
        path: 'docs/FOUNDER_FIRST_CUSTOMER_CLOSE_PACK.md',
        description: 'Founder-led qualification, default offer, close sequence, and paid-pilot proposal skeleton for the first customer.',
      },
      {
        title: 'Proof-of-Value One-Page Copy',
        path: 'docs/PROOF_OF_VALUE_ONE_PAGE_COPY.md',
        description: 'Customer-facing one-page overview for landing page, PDF, email, or sales message use.',
      },
      {
        title: 'Customer Brief Intake Template',
        path: 'docs/CUSTOMER_BRIEF_INTAKE_TEMPLATE.md',
        description: 'Approved brief fields, A/B/C route requirement, and safety confirmations before intake.',
      },
      {
        title: '/proof-of-value route',
        path: 'proof-of-value',
        route: '/proof-of-value',
        description: 'Operator intake workflow for validating the approved brief before output assembly.',
      },
      {
        title: 'Proof-of-Value Customer Output Template',
        path: 'docs/PROOF_OF_VALUE_CUSTOMER_OUTPUT_TEMPLATE.md',
        description: 'Customer-facing package template with provenance footer placeholders.',
      },
      {
        title: 'Proof-of-Value Output Package',
        path: 'docs/PROOF_OF_VALUE_OUTPUT_PACKAGE.md',
        description: 'Operator sequence for assembling and reviewing customer-facing outputs.',
      },
      {
        title: 'Proof-of-Value Sales Offer',
        path: 'docs/PROOF_OF_VALUE_SALES_OFFER.md',
        description: 'Offer framing, buyer fit, deliverables, exclusions, and next-step language.',
      },
      {
        title: 'Proof-of-Value Pricing Options',
        path: 'docs/PROOF_OF_VALUE_PRICING_OPTIONS.md',
        description: 'Placeholder pricing and the recommended first-customer default offer.',
      },
    ],
  },
  {
    eyebrow: 'Public Policy',
    title: 'Public Policy / Strategic Command',
    description: 'Thai-first resources for government communication, policy risk review, crisis-information simulation, and executive decision support.',
    docs: [
      {
        title: '/strategic-command route',
        path: 'strategic-command',
        route: '/strategic-command',
        description: 'Thai-first demo page for public policy and government communication stakeholders.',
      },
      {
        title: 'Strategic Command Overview',
        path: 'docs/STRATEGIC_COMMAND_TH.md',
        description: 'Positioning, use cases, four pillars, output package, demo offer, and safety boundaries.',
      },
      {
        title: 'Public Policy PoV Intake Template',
        path: 'docs/PUBLIC_POLICY_POV_INTAKE_TEMPLATE_TH.md',
        description: 'Approved intake fields, review checklist, and prohibited data boundaries for policy scenarios.',
      },
      {
        title: 'Strategic Command Demo Script',
        path: 'docs/STRATEGIC_COMMAND_DEMO_SCRIPT_TH.md',
        description: '15-minute demo flow, 30-minute workshop flow, presenter questions, screen sequence, and next step.',
      },
      {
        title: 'Strategic Command Safety Boundaries',
        path: 'docs/STRATEGIC_COMMAND_SAFETY_BOUNDARIES_TH.md',
        description: 'Allowed use, disallowed use, data boundary, output boundary, and political-risk exclusions.',
      },
      {
        title: 'PM2.5 Demo Package Input',
        path: 'docs/strategic-command/PM25_DUST_FREE_ROOM_INPUT_TH.md',
        description: 'User-provided PM2.5 dust-free room scenario, synthetic personas, watchouts, and response inputs.',
      },
      {
        title: 'PM2.5 Executive Strategy Pack',
        path: 'docs/strategic-command/PM25_EXECUTIVE_STRATEGY_PACK_TH.md',
        description: 'Ready-to-present PM2.5 Health Resilience Strategy Pack with provenance and validation notes.',
      },
      {
        title: 'PM2.5 Demo Script',
        path: 'docs/strategic-command/PM25_DEMO_SCRIPT_TH.md',
        description: '5-minute and 15-minute presenter script for political/government strategy team demos.',
      },
      {
        title: 'PM2.5 Screenshot Guide',
        path: 'docs/strategic-command/PM25_SCREENSHOT_GUIDE_TH.md',
        description: 'Capture checklist, filenames, storage path, and required visible safety/provenance labels.',
      },
    ],
  },
  {
    eyebrow: 'Customer Proof-of-Value',
    title: 'Customer Proof-of-Value',
    description: 'Start here when a prospect wants to evaluate value using one approved campaign brief.',
    docs: [
      {
        title: 'Proof-of-Value One-Page Copy',
        path: 'docs/PROOF_OF_VALUE_ONE_PAGE_COPY.md',
        description: 'Concise customer-facing copy for a landing page, PDF, email attachment, or sales message.',
      },
      {
        title: 'Proof-of-Value Sales Offer',
        path: 'docs/PROOF_OF_VALUE_SALES_OFFER.md',
        description: 'Offer framing, customer inputs, deliverables, session format, success criteria, and next step.',
      },
      {
        title: 'Customer Brief Intake Template',
        path: 'docs/CUSTOMER_BRIEF_INTAKE_TEMPLATE.md',
        description: 'Approved campaign brief fields and safety confirmations before a proof-of-value session.',
      },
      {
        title: 'Proof-of-Value Deliverables',
        path: 'docs/PROOF_OF_VALUE_DELIVERABLES.md',
        description: 'Defines what the customer receives, provenance labels, limitations, and validation step.',
      },
    ],
  },
  {
    eyebrow: 'AI Preparation',
    title: 'Prepare Brief with AI',
    description: 'Thai-first prompt packs for turning a loose customer question into safe intake fields before operator review.',
    docs: [
      {
        title: 'AI Research Prompt Pack',
        path: 'docs/AI_RESEARCH_PROMPT_PACK.md',
        description: 'Thai-first prompts for brief structuring, market context, A/B/C routes, risk watchouts, KPIs, and final formatting.',
      },
      {
        title: 'PoV Intake Import Template',
        path: 'docs/POV_INTAKE_IMPORT_TEMPLATE.md',
        description: 'Markdown and JSON templates for preparing reviewed intake data before pasting into /proof-of-value.',
      },
      {
        title: 'Raw Brief to PoV Example',
        path: 'docs/RAW_BRIEF_TO_POV_EXAMPLE.md',
        description: 'Synthetic Thai example showing a raw business question converted into structured proof-of-value intake.',
      },
      {
        title: '/proof-of-value route',
        path: 'proof-of-value',
        route: '/proof-of-value',
        description: 'Operator intake workflow for validating approved, reviewed, and safety-checked brief data.',
      },
    ],
  },
  {
    eyebrow: 'Sales Materials',
    title: 'Sales Materials',
    description: 'Use these when preparing a sales conversation or showing a synthetic example package.',
    docs: [
      {
        title: 'Proof-of-Value Pricing Options',
        path: 'docs/PROOF_OF_VALUE_PRICING_OPTIONS.md',
        description: 'Placeholder pricing ranges and packaging options for planning conversations.',
      },
      {
        title: 'Sample Proof-of-Value Package',
        path: 'docs/SAMPLE_PROOF_OF_VALUE_PACKAGE.md',
        description: 'Synthetic sample package that demonstrates expected customer-facing outputs.',
      },
      {
        title: 'Sales Demo Walkthrough',
        path: 'docs/SALES_DEMO_WALKTHROUGH.md',
        description: '15-minute and 30-minute demo flows for brand and agency sales conversations.',
      },
    ],
  },
  {
    eyebrow: 'Operator Checklist',
    title: 'Operator Checklist',
    description: 'Follow these before assembling or sharing any customer-facing proof-of-value artifacts.',
    docs: [
      {
        title: 'Proof-of-Value Operator Checklist',
        path: 'docs/PROOF_OF_VALUE_OPERATOR_CHECKLIST.md',
        description: 'Step-by-step operator checklist from intake validation through customer package review.',
      },
      {
        title: 'Proof-of-Value Output Package',
        path: 'docs/PROOF_OF_VALUE_OUTPUT_PACKAGE.md',
        description: 'Operator sequence for turning approved intake into customer-facing outputs.',
      },
      {
        title: 'Demo Artifact Checklist',
        path: 'docs/DEMO_ARTIFACT_CHECKLIST.md',
        description: 'Safety review before sharing screenshots, decks, exports, or demo recordings.',
      },
    ],
  },
  {
    eyebrow: 'Data Safety and Guardrails',
    title: 'Data Safety and Guardrails',
    description: 'Use these docs to keep pilot handling, retention, deployment, and sharing boundaries clear.',
    docs: [
      {
        title: 'Customer Data Handling',
        path: 'docs/CUSTOMER_DATA_HANDLING.md',
        description: 'Rules for approved briefs, prohibited data, source labels, audit metadata, and operator handling.',
      },
      {
        title: 'Data Retention and Deletion',
        path: 'docs/DATA_RETENTION_AND_DELETION.md',
        description: 'Retention boundaries, deletion workflow, audit log handling, and dry-run expectations.',
      },
      {
        title: 'Pilot Deployment Checklist',
        path: 'docs/PILOT_DEPLOYMENT_CHECKLIST.md',
        description: 'Deployment gates for a controlled private pilot environment before external use.',
      },
    ],
  },
  {
    eyebrow: 'Sample Packages',
    title: 'Sample Packages',
    description: 'Safe synthetic examples for showing format and workflow without customer data.',
    docs: [
      {
        title: 'Sample Proof-of-Value Package',
        path: 'docs/SAMPLE_PROOF_OF_VALUE_PACKAGE.md',
        description: 'Synthetic proof-of-value package with visible provenance labels and limitations.',
      },
      {
        title: 'Sample Strategy Pack Exports',
        path: 'docs/SAMPLE_STRATEGY_PACK_EXPORTS.md',
        description: 'Recommended Strategy Pack slide sequences and provenance footer guidance.',
      },
      {
        title: 'Sample Demo Briefs',
        path: 'docs/SAMPLE_DEMO_BRIEFS.md',
        description: 'Synthetic demo-only briefs for Premium Water, InsurTech, energy, EV, and agency scenarios.',
      },
    ],
  },
]
</script>

<style scoped>
.resources-page {
  min-height: 100vh;
  color: var(--text-secondary);
}

.navbar {
  position: sticky;
  top: 0;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-8);
  background: var(--bg-glass);
  border-bottom: 1px solid var(--border-subtle);
  backdrop-filter: blur(18px);
}

.nav-brand {
  color: var(--text-primary);
  font-family: var(--font-mono);
  font-weight: 900;
  letter-spacing: 0;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.nav-link,
.primary-link {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  text-decoration: none;
  font-size: var(--text-sm);
  font-weight: 800;
}

.nav-link:hover,
.nav-link.router-link-active,
.primary-link:hover {
  color: var(--text-primary);
  background: var(--bg-muted);
}

.resources-shell {
  width: min(1280px, calc(100% - 32px));
  margin: 0 auto;
  padding: var(--space-8) 0 var(--space-16);
}

.resources-header {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: var(--space-6);
  align-items: end;
  margin-bottom: var(--space-6);
}

.resources-header h1 {
  margin-bottom: var(--space-4);
}

.resources-header p,
.panel-heading p,
.section-heading p,
.doc-card p {
  max-width: 820px;
  color: var(--text-secondary);
}

.page-kicker,
.section-heading span,
.doc-path {
  display: block;
  color: var(--teal);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  letter-spacing: 0;
  text-transform: uppercase;
}

.page-kicker {
  margin-bottom: var(--space-2);
}

.boundary-panel,
.guardrail-panel,
.resource-section {
  margin-bottom: var(--space-8);
  padding: var(--space-6);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-lg);
  background: var(--bg-glass);
  box-shadow: var(--shadow-card);
}

.readiness-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: var(--space-3);
  margin: var(--space-5) 0 0;
}

.readiness-item {
  min-width: 0;
  margin: 0;
  padding: var(--space-4);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
}

.readiness-item dt {
  margin-bottom: var(--space-2);
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 900;
}

.readiness-item dd {
  margin: 0;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: 900;
  text-transform: uppercase;
}

.readiness-item.ready {
  border-color: color-mix(in srgb, var(--green) 44%, var(--border-default));
}

.readiness-item.conditional {
  border-color: color-mix(in srgb, var(--yellow) 48%, var(--border-default));
}

.readiness-item.blocked {
  border-color: color-mix(in srgb, var(--red) 48%, var(--border-default));
}

.guardrail-panel ul {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  padding: 0;
  margin: var(--space-4) 0 0;
  list-style: none;
}

.guardrail-panel li {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-pill);
  background: var(--bg-surface);
  color: var(--text-primary);
  font-size: var(--text-sm);
  font-weight: 800;
}

.section-heading {
  margin-bottom: var(--space-5);
}

.section-heading h2 {
  margin: var(--space-2) 0 var(--space-3);
}

.doc-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--space-4);
}

.doc-card {
  display: flex;
  min-height: 188px;
  flex-direction: column;
  padding: var(--space-5);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-md);
  background: var(--bg-surface);
  color: inherit;
  text-decoration: none;
  transition:
    border-color var(--transition-fast),
    transform var(--transition-fast),
    box-shadow var(--transition-fast);
}

.doc-card:hover {
  transform: translateY(-2px);
  border-color: var(--border-accent);
  box-shadow: var(--shadow-md);
}

.doc-path {
  margin-bottom: var(--space-4);
  color: var(--text-tertiary);
  overflow-wrap: anywhere;
  text-transform: none;
}

.doc-card strong {
  margin-bottom: var(--space-3);
  color: var(--text-primary);
  font-size: var(--text-lg);
  line-height: 1.25;
}

.doc-card p {
  margin: 0;
  font-size: var(--text-sm);
}

@media (max-width: 980px) {
  .resources-header,
  .readiness-grid,
  .doc-list {
    grid-template-columns: 1fr;
  }

  .resources-header {
    align-items: start;
  }
}

@media (max-width: 640px) {
  .navbar {
    align-items: flex-start;
    padding: var(--space-4);
  }

  .nav-links {
    justify-content: flex-end;
  }

  .resources-shell {
    width: min(100% - 24px, 1280px);
    padding-top: var(--space-6);
  }

  .boundary-panel,
  .guardrail-panel,
  .resource-section {
    padding: var(--space-4);
  }
}
</style>
