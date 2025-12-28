---
id: 1
title: Create AI Book Constitution
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Alvina-Abdullah
command: /sp.constitution
labels: [constitution,spec-first,ai-book,rag-chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```text
/sp.constitution

Project: AI-Spec-Driven Technical Book with Embedded RAG Chatbot

Purpose:
Create a unified, production-grade technical book authored through AI-assisted workflows and specifications, published via Docusaurus and GitHub Pages, and enhanced with an embedded Retrieval-Augmented Generation (RAG) chatbot for interactive knowledge access.

Core principles:
- Spec-first development (all content, architecture, and integrations driven by explicit specifications)
- Accuracy through source-grounded and code-verifiable content
- Clarity for a technical audience (software engineers, AI practitioners, CS students)
- Reproducibility (all steps, configs, and pipelines documented)
- Practical rigor (real implementations over theoretical descriptions)

Key standards:

Content & Writing:
- All technical explanations must be correct, current, and implementation-aligned
- Concepts should progress from fundamentals to advanced topics
- Tone: instructional, precise, and developer-focused
- Writing clarity: Flesch-Kincaid grade 10–12
- Examples must be runnable or realistically implementable

Book Platform:
- Framework: Docusaurus
- Output: Static site deployed on GitHub Pages
- Structure: Versioned docs, sidebar navigation, search-enabled
- All configuration files must be included and documented
- Book must be fully usable without the chatbot

AI / Spec Tooling:
- Spec-Kit Plus used to define:
  - Book structure
  - Content sections
  - System architecture
  - Chatbot behavior
- Claude Code used for:
  - AI-assisted content generation
  - Code scaffolding
  - Refactoring and validation
- Specs must remain the source of truth

RAG Chatbot Requirements:
- Embedded directly within the Docusaurus site UI
- Capable of answering questions about:
  - Entire book content
  - User-selected text only (context-restricted answers)
- Architecture must include:
  - OpenAI Agents or ChatKit SDK
  - FastAPI backend
  - Neon Serverless Postgres (metadata, sessions, logs)
  - Qdrant Cloud Free Tier (vector storage)
- Retrieval must be citation-aware (responses grounded in book content)
- No hallucinated answers outside indexed material

Data & Retrieval Standards:
- All indexed content must originate from the book
- Chunking, embedding, and retrieval strategies must be documented
- Clear separation between:
  - System prompts
  - Retrieval context
  - User input
- Support future re-indexing and updates

Constraints:
- Book length: As required to fully cover topic (no filler content)
- All code must be production-ready and commented
- Free-tier compatible infrastructure only
- No proprietary or undisclosed dependencies
- Must work on GitHub Pages deployment constraints

Documentation & Transparency:
- Architecture diagrams (textual or visual)
- Clear setup instructions (local + production)
- Environment variable documentation
- Deployment workflow explained step-by-step
- Failure modes and limitations explicitly listed

Quality & Validation:
- All code paths must be logically sound
- Chatbot answers must be grounded in retrieved context
- Manual validation of:
  - Search relevance
  - Answer accuracy
  - UI integration
- No broken links or build errors

Success criteria:
- Book successfully builds and deploys on GitHub Pages
- RAG chatbot answers book-related questions accurately
- Selected-text-only queries are respected
- Specs fully align with final implementation
- Project is reproducible by a third-party developer
```

## Response snapshot

Created a comprehensive constitution file for the AI-Spec-Driven Technical Book with Embedded RAG Chatbot project. The constitution includes:

- Core Principles: Spec-first development, accuracy through source-grounded content, clarity for technical audience, reproducibility, Docusaurus-based platform, and RAG chatbot integration requirements
- Additional Constraints: Free-tier infrastructure compatibility, data and retrieval standards, documentation requirements
- Development Workflow: Content generation tooling, quality standards, and success criteria
- Governance: Rules for constitution compliance and amendment procedures

The constitution file (.specify/memory/constitution.md) has been created with version 1.0.0, ratified on 2025-12-27.

## Outcome

- ✅ Impact: Created foundational project constitution with 6 core principles and governance structure
- 🧪 Tests: none
- 📁 Files: Updated .specify/memory/constitution.md
- 🔁 Next prompts: Plan creation, spec definition, and task generation based on constitution
- 🧠 Reflection: Constitution provides clear guidance for all future development decisions

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - All specified principles included
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin spec creation based on constitution