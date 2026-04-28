---
description: Deep analysis through first-principles reasoning, abstraction decomposition, and multi-dimensional evaluation
argument-hint: [problem or question to analyze deeply]
allowed-tools: Read, Grep, Glob
---

# Ultra Think - Abstraction-First Deep Analysis

Analyze the following with systematic rigor: $ARGUMENTS

## Phase 1: Decompose to First Principles

Strip away assumptions. Identify:

- The **invariants** - what must always be true regardless of implementation
- The **boundaries** - where does this system begin and end
- The **contracts** - what interfaces exist between components
- The **unknowns** - what information is missing or assumed

## Phase 2: Abstraction Layer Analysis

Map the problem through abstraction layers (inside-out):

### Domain Core (innermost - zero dependencies)

- Pure types, traits, protocols, interfaces
- Business rules as functions over domain types
- No I/O, no frameworks, no external knowledge
- Complexity: what are the Big-O implications of the domain model?

### Application Layer (orchestration)

- Use cases / command handlers / query handlers
- Depends only on domain abstractions (ports)
- CQRS consideration: are reads and writes fundamentally different here?
- What data structures (hash maps, trees, queues) best model the workflow?

### Adapter Layer (outermost - all I/O lives here)

- Concrete implementations of ports
- DB connections, HTTP handlers, message queues, 3rd party integrations
- These are the ONLY places external libraries are justified:
  - DB drivers (sqlx, database/sql, pg)
  - IAM providers (Zitadel, Keycloak via OIDC)
  - Payment gateways (Stripe Connect, PayPal)
  - Auth protocols (OAuth2, OIDC)

## Phase 3: Multi-Perspective Evaluation

### Technical Lens

- Which language (Rust > Python > Go > TypeScript) fits this problem's constraints?
- Can we leverage zero-cost abstractions (Rust traits, Go interfaces)?
- What are the performance characteristics? Analyze with Big-O notation.
- Where does the data flow? What data structures optimize for the access patterns?

### Architectural Lens

- Does this follow Dependency Inversion? High-level modules must not import low-level modules.
- Single Responsibility: does each component have exactly one reason to change?
- Open/Closed: can we extend without modifying existing code?
- Interface Segregation: are interfaces minimal and focused?
- Which design pattern applies? (Strategy, Adapter, Factory, Observer, Command)

### Pragmatic Lens

- What is the simplest abstraction that solves this?
- YAGNI: are we building for actual requirements or hypothetical ones?
- KISS: is the abstraction earning its complexity?
- DRY: is there genuine duplication, or just superficial similarity?

## Phase 4: Generate Solutions (minimum 3)

For each solution:

1. **Name** - concise label
2. **Abstraction model** - what are the core interfaces/traits/protocols?
3. **Language fit** - which supported language is strongest here and why
4. **Dependency count** - how many external libs are required?
5. **Big-O profile** - time and space complexity of critical paths
6. **Trade-offs** - what do you gain vs what do you lose?
7. **Implementation sketch** - pseudocode or type signatures showing the abstraction boundaries

## Phase 5: Recommend

Present as:

```
RECOMMENDATION
==============
Approach: [name]
Language: [primary language]
Core abstractions: [list of traits/interfaces/protocols]
External deps: [only inevitable ones]
Complexity: [Big-O of hot paths]
Confidence: [high/medium/low with reasoning]

WHY NOT THE OTHERS
==================
[brief reasoning for each rejected option]

IMPLEMENTATION ORDER
====================
1. Define domain types and traits/interfaces (zero deps)
2. Implement use cases against abstractions
3. Build adapters for external systems
4. Wire everything at the composition root

RISKS AND MITIGATIONS
======================
[specific risks with specific mitigations]
```

## Phase 6: Meta-Analysis

- What biases might be affecting this analysis?
- What would change if the constraints changed?
- Where is the analysis weakest?
- What expertise or information would improve confidence?
