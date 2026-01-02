# Research: RAG Knowledge Ingestion & Vector Indexing

## Decision: URL Crawling Strategy
**Rationale**: For the Docusaurus book at https://hackathon-physical-and-ai-humanoid.vercel.app/, we'll implement a breadth-first crawler that starts from the base URL and follows internal links to discover all book pages.
**Alternatives considered**:
- Sitemap parsing: May not exist or be complete
- Manual URL list: Not scalable for large books
- RSS feed: Not typically available for Docusaurus sites

## Decision: Text Extraction Method
**Rationale**: Using BeautifulSoup with specific CSS selectors to extract main content from Docusaurus pages, focusing on elements with class names like 'markdown' or 'container' that typically contain the main content.
**Alternatives considered**:
- Selenium: More complex and slower, unnecessary for static content
- Regular expressions: Less reliable for HTML parsing
- Newspaper3k: Not optimized for documentation sites like Docusaurus

## Decision: Content Chunking Strategy
**Rationale**: Implement recursive text splitting that respects document structure (headings, paragraphs) with chunk sizes of 500-1000 words as specified in the requirements. Will include overlap to maintain context.
**Alternatives considered**:
- Fixed-size token splitting: May break document context
- Sentence-based splitting: May create chunks that are too small
- Semantic splitting: More complex and may not be necessary for documentation

## Decision: Cohere Embedding Model
**Rationale**: Using Cohere's embed-english-v3.0 model which is optimized for English text and provides good balance of quality and cost. Will use "search_document" type for stored chunks and "search_query" type for search queries.
**Alternatives considered**:
- OpenAI embeddings: Would violate constraint of using Cohere API
- Hugging Face models: Would require self-hosting, violating free-tier constraint
- Other Cohere models: v3.0 is the latest and most efficient

## Decision: Qdrant Collection Structure
**Rationale**: Creating a collection named "rag_embedding" with appropriate vector dimensions for Cohere embeddings (1024 dimensions), and storing metadata including source URL, document title, and chunk position.
**Alternatives considered**:
- Different vector dimensions: Cohere models output 1024-dim vectors
- Different collection names: Following user's specific requirement
- Alternative vector databases: Must use Qdrant Cloud as specified

## Decision: Error Handling Strategy
**Rationale**: Implement graceful error handling for network issues, API rate limits, and content extraction failures. Include retry logic with exponential backoff for transient failures.
**Alternatives considered**:
- Fail-fast approach: Would not meet 95% success rate requirement
- No error handling: Would make system unreliable

## Decision: Rate Limiting Implementation
**Rationale**: Implement token bucket or sliding window rate limiting to stay within Cohere API limits and avoid being blocked. Will use standard library approaches to avoid additional dependencies.
**Alternatives considered**:
- No rate limiting: Would likely exceed API limits
- External rate limiting libraries: Would add unnecessary complexity