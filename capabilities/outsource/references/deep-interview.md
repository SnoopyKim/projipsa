# Deep Interview

Use this reference to discover enough intent and context to make a responsible delivery proposal without asking the Maker to design the implementation.

## Contents

1. Interview objective
2. Interview sequence
3. Discovery domains
4. Question policy
5. Readiness and output

## 1. Interview objective

A Deep Interview is an adaptive discovery process, not a fixed questionnaire. Its output is a project model that Outsource can translate into a Delivery Contract.

The interview should reduce **consequential uncertainty**: unknowns that could change the desired outcome, scope, risk, user experience, operating model, or acceptance decision.

Do not try to eliminate every unknown. Classify remaining unknowns as:

- a Maker decision;
- an inspectable fact Outsource can discover;
- an assumption that can be documented;
- a hypothesis requiring a small experiment;
- a later reversible decision.

## 2. Interview sequence

### A. Context sweep

Before asking, inspect:

- the Maker's request and prior answers;
- repository or product documentation;
- current code, data shape, tests, deployment, or workflow when in scope;
- known Maker preferences and confirmed project state;
- applicable permissions and irreversible actions.

Create a private gap map. Do not turn it into a long questionnaire for the Maker.

### B. Highest-impact question

Ask the smallest coherent set of questions that resolves the most consequential gap. Prefer questions about desired change, trade-offs, failure impact, and real usage over implementation trivia.

When useful, offer a recommendation with alternatives:

```text
I recommend A because of X. B would optimize Y but adds Z.
Which trade-off better matches your goal?
```

### C. Synthesis

Periodically summarize:

- what Outsource believes the Maker wants;
- what evidence supports it;
- decisions already made;
- assumptions Outsource proposes;
- material unknowns still blocking a responsible proposal.

Invite correction without forcing confirmation of every detail.

### D. Stop or continue

Stop when the readiness conditions are met. Continue only for gaps that materially affect the contract.

## 3. Discovery domains

Use the domains selectively.

### Purpose and outcome

- Why is this worth doing now?
- What observable change should result?
- What would make the project feel unsuccessful even if it technically works?

### Current state

- How is the problem handled today?
- What existing product, workflow, code, data, or behavior must be preserved?
- What prior attempts or constraints matter?

### Users and usage

- Who experiences the problem or uses the result?
- In what situation and frequency?
- Which journey or moment matters most?

### Scope and non-goals

- What must be true in this delivery?
- What can be deferred without undermining the outcome?
- What should Outsource explicitly avoid?

### Constraints and preferences

- Time, cost, platform, technology, compliance, brand, accessibility, or operational constraints
- Maker preferences that influence a meaningful trade-off
- Required integrations and unavailable resources

### Quality and risk

- Most damaging failure modes
- Required confidence, reliability, performance, privacy, and security
- Reversible versus hard-to-reverse decisions

### Operations and handoff

- Who will operate, maintain, support, or market the result?
- Required deployment, observability, rollback, documentation, and ownership
- What should happen after release?

### Unknowns and evidence

- What can Outsource inspect directly?
- Which assumptions need experiments?
- Which criteria can be tested mechanically, and which require Maker review?

## 4. Question policy

- Never repeat information already supplied or safely discoverable.
- Do not ask “How should I implement this?” when Outsource can make a recommendation.
- Ask about preferences only when plausible choices have materially different outcomes.
- Explain why a sensitive or consequential question matters.
- Separate facts from Maker preferences and Outsource recommendations.
- Prefer concrete scenarios over abstract adjectives such as “fast,” “simple,” or “professional.”
- Avoid presenting every possible option. Curate the meaningful choices.
- Ask progressively; do not front-load a comprehensive survey.
- Match interview depth to engagement mode.
- If the Maker wants speed, propose explicit assumptions and a reversible first milestone instead of silently skipping discovery.

## 5. Readiness and output

The interview is ready for `PROPOSE` when Outsource can responsibly state:

- the intended outcome and why it matters;
- current context and affected users;
- scope and non-goals;
- material constraints and authority boundaries;
- recommended approach and meaningful alternative, if any;
- deliverables and review points;
- acceptance criteria and feasible evidence;
- assumptions, risks, and remaining Maker decisions.

Produce this synthesis:

```markdown
## Interview synthesis

### Intended outcome

### Current context and users

### Confirmed decisions

### Outsource recommendations

### Proposed assumptions

### Risks and unknowns

### Remaining material decisions

### Ready for Delivery Contract?
Yes | No — reason
```

The synthesis is an input to the Delivery Contract, not the final contract itself.
