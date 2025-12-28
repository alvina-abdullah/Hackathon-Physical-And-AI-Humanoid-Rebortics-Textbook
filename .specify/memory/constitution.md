<!--
Sync Impact Report:
Version change: N/A → 1.0.0
Modified principles: N/A (new constitution)
Added sections: All principles and sections for AI-Spec-Driven Technical Book
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ updated
  - .specify/templates/spec-template.md ✅ updated
  - .specify/templates/tasks-template.md ✅ updated
  - .specify/templates/commands/*.md ✅ updated
Follow-up TODOs: None
-->
# AI-Spec-Driven Technical Book with Embedded RAG Chatbot Constitution

## Core Principles

### I. Spec-First Development
All content, architecture, and integrations must be driven by explicit specifications. No implementation should proceed without a clear, documented specification that defines scope, requirements, and acceptance criteria.

### II. Accuracy Through Source-Grounded Content
All technical explanations must be correct, current, and implementation-aligned. Content must be verifiable against actual implementations, with examples that are runnable or realistically implementable.

### III. Clarity for Technical Audience
Content must be instructional, precise, and developer-focused with Flesch-Kincaid grade 10–12 readability. Concepts should progress from fundamentals to advanced topics in a logical sequence.

### IV. Reproducibility and Practical Rigor
All steps, configurations, and pipelines must be fully documented and reproducible. The book must demonstrate real implementations over theoretical descriptions, with production-ready code that is properly commented.

### V. Docusaurus-Based Book Platform
The book platform must use Docusaurus framework for static site generation, deployed on GitHub Pages with versioned docs, sidebar navigation, and search-enabled content. The book must remain fully usable without the chatbot component.

### VI. RAG Chatbot Integration Requirements
The embedded RAG chatbot must be capable of answering questions about the entire book content and support user-selected text queries. Architecture must include OpenAI Agents or ChatKit SDK, FastAPI backend, Neon Serverless Postgres for metadata, and Qdrant Cloud Free Tier for vector storage.

## Additional Constraints and Standards

### Free-Tier Infrastructure Compatibility
All infrastructure components must be compatible with free-tier services only. No proprietary or undisclosed dependencies are allowed. The solution must work within GitHub Pages deployment constraints.

### Data and Retrieval Standards
All indexed content must originate from the book. Chunking, embedding, and retrieval strategies must be documented with clear separation between system prompts, retrieval context, and user input. Retrieval must be citation-aware with responses grounded in book content and no hallucinated answers.

### Documentation and Transparency Requirements
Architecture diagrams must be provided (textual or visual). Clear setup instructions for local and production environments must be included. Environment variables must be documented with deployment workflows explained step-by-step. Failure modes and limitations must be explicitly listed.

## Development Workflow and Quality Standards

### Content Generation and Tooling
Spec-Kit Plus must be used to define book structure, content sections, system architecture, and chatbot behavior. Claude Code must be used for AI-assisted content generation, code scaffolding, refactoring, and validation. Specifications must remain the source of truth.

### Quality and Validation Requirements
All code paths must be logically sound. Chatbot answers must be grounded in retrieved context. Manual validation must occur for search relevance, answer accuracy, and UI integration. No broken links or build errors are acceptable.

### Success Criteria
The book must successfully build and deploy on GitHub Pages. The RAG chatbot must accurately answer book-related questions. Selected-text-only queries must be respected. Specifications must fully align with final implementation. The project must be reproducible by a third-party developer.

## Governance

This constitution supersedes all other development practices for this project. All changes must comply with these principles. Amendments require explicit documentation, approval, and migration planning. All pull requests and reviews must verify constitution compliance. The project must maintain adherence to the spec-first methodology throughout its lifecycle.

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
