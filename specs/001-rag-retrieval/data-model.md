# Data Model: RAG Retrieval & Pipeline Testing

## Entity: Search Query
**Description**: User input text for similarity search with generated embedding
**Fields**:
- `query_text` (string): The original user query text
- `query_embedding` (array[float]): The embedding vector (1024 dimensions for Cohere)
- `created_at` (timestamp): When the query was processed
- `query_id` (string): Unique identifier for the query

**Validation Rules**:
- Query text must not exceed 1000 characters
- Query embedding must have exactly 1024 dimensions (for Cohere model)
- Query text must not be empty

## Entity: Search Result
**Description**: Retrieved content chunk with similarity score and metadata from Qdrant
**Fields**:
- `result_id` (string): Unique identifier for the search result
- `content_chunk` (string): The actual text content of the retrieved chunk
- `similarity_score` (float): The similarity score (0.0 to 1.0)
- `source_url` (string): URL of the original source document
- `document_title` (string): Title of the original document
- `chunk_position` (integer): Position of this chunk within the original document
- `chunk_metadata` (object): Additional metadata including headings, section info
- `retrieved_at` (timestamp): When the result was retrieved

**Validation Rules**:
- Similarity score must be between 0.0 and 1.0
- Content chunk must not be empty
- Source URL must be a valid URL
- Chunk position must be non-negative integer

## Entity: Validation Report
**Description**: Report of the validation results for retrieved content against source metadata
**Fields**:
- `query_id` (string): Reference to the original query
- `validation_results` (array): List of validation results for each retrieved chunk
- `overall_score` (float): Overall validation score (0.0 to 1.0)
- `metadata_accuracy` (float): Accuracy of metadata matching (0.0 to 1.0)
- `content_relevance` (float): Relevance of content to query (0.0 to 1.0)
- `validation_timestamp` (timestamp): When validation was performed
- `validation_details` (object): Detailed validation information

**Validation Rules**:
- Overall score must be between 0.0 and 1.0
- Metadata accuracy must be between 0.0 and 1.0
- Content relevance must be between 0.0 and 1.0
- Query_id must reference an existing Search Query

## Entity: Pipeline Test Result
**Description**: Result of end-to-end pipeline testing including query processing, retrieval, and validation
**Fields**:
- `test_id` (string): Unique identifier for the test
- `query_text` (string): The test query used
- `retrieval_success` (boolean): Whether retrieval was successful
- `validation_success` (boolean): Whether validation was successful
- `response_time` (float): Time taken for the entire pipeline (in seconds)
- `retrieved_chunks_count` (integer): Number of chunks retrieved
- `top_similarity_score` (float): Highest similarity score among results
- `test_timestamp` (timestamp): When the test was performed
- `error_message` (string): Error message if test failed

**Validation Rules**:
- Response time must be positive
- Retrieved chunks count must be non-negative
- Top similarity score must be between 0.0 and 1.0
- Test ID must be unique

## Relationships
- One Search Query generates many Search Results (1 to many)
- One Search Query maps to one Validation Report (1 to 1)
- One Search Query maps to one Pipeline Test Result (1 to 1)

## State Transitions
- Search Query: received → processed → embedding_generated → search_performed
- Search Result: retrieved → validated → returned
- Pipeline Test Result: started → completed → validated