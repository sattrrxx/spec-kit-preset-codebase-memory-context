---
schema_version: "2.0"
generator: "speckit.codebase-memory"
analysis_profiles:
  - generic
source_commit: "[SOURCE_COMMIT]"
working_tree: "[WORKING_TREE]"
evidence_tier: "verify"
---

# [PROJECT_NAME] Codebase Context

> Generated from current repository evidence. Inferred or unknown conclusions
> are marked explicitly. Repository paths are relative to the repository root.

## 1. Architecture Overview and Module Map

### System Purpose and Technology Stack
[Describe the system's core responsibilities and primary technology stack (languages, runtimes, primary frameworks, key libraries, and versions).]

### Module Layout and Boundaries
[List repository modules, packages, or directory structure in build/dependency order, describing verified dependency directions and major boundaries.]

### Entry Points
[List deployable web servers, CLI binaries, background jobs, event listeners, or public library exports.]

## 2. Core Flows and Interface Boundaries

### Request Pipeline and Middleware
[Describe the global request/execution pipeline: routing mechanism, filters, middlewares, interceptors, and exception/error handling conventions in verified execution order.]

### Security and Trust Boundaries
[Describe authentication mechanisms, token/session validation, authorization guards/RBAC, tenant/data isolation, credential boundaries, and public versus protected endpoint conventions without secret values.]

### Representative Traces
[Summarize one to five representative business flows with their entry point, major hops across layers, transaction boundary, side effects (cache, events, external calls), and failure path.]

### External Integrations
[List external databases, caches, message brokers, third-party APIs, and downstream services with verified usage status, consumer mechanism, and evidence.]

## 3. Data Persistence and Storage Model

### Storage and Entity Conventions
[Describe storage technologies, entity/model base classes, primary key/identifier strategies, auditing fields, logical deletion, and tenant/data scoping conventions.]

### Transactions and Schema Migrations
[Describe transaction demarcation patterns (declarative or programmatic boundaries, rollback rules) and database migration/schema management tooling.]

## 4. Development Conventions and Validation Commands

### Coding and Design Patterns
[Describe repository-specific patterns for organizing services, interfaces/implementations, dependency injection, validation, and error envelopes.]

### Testing Strategy
[Describe test frameworks in actual use, unit/integration boundaries, test data/fixture setup, mock conventions, and representative test files.]

### Operational Constraints and Packaging
[Describe required runtimes, profiles, containerization/packaging behavior (Docker, OCI, JAR, standalone binary), environment configuration, and port/network conventions.]

### Validation Commands

| Purpose | Command | Preconditions | Evidence |
|---|---|---|---|
| [Build / Test / Lint / Run / Package / Deploy] | `[Repository-declared command]` | [Required profile, runtime, or env] | [Config, CI, wrapper, or README path] |

## 5. Evidence and Coverage Limitations

[Record the codebase-memory project and index status, verified bounded scopes, excluded or stale paths inspected directly, unverified external dependencies, and any conclusion that remains inferred or unknown.]

<!-- PROJECT OVERRIDES START -->
## 6. Project Overrides

> Human-maintained and preserved verbatim. The generator does not validate this
> section or use it to raise the confidence of generated findings.

<!-- PROJECT OVERRIDES END -->
