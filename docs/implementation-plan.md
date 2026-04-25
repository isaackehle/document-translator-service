# Implementation Plan: Hebrew Translation & AWS Infrastructure

## Overview

This plan covers the complete implementation of a bilingual (English ↔ Hebrew) document translation system with local LLM integration and AWS cloud capabilities. Each phase has checkboxes for tracking progress.

---

## Phase 1: Project Foundation

**Goal**: Define scope, requirements, and architecture

- ✅ Define project scope and requirements
- ✅ Establish architecture overview
- ✅ Document implementation phases

**Status**: ✅ Complete

---

## Phase 2: Local Development Environment

**Goal**: Set up local development with all required tools

### AWS Mocking Infrastructure
- ✅ Install and configure LocalStack for AWS service simulation
- ✅ Set up minio for S3-compatible local storage testing
- ✅ Configure moto library for boto3 mocking in tests
- ✅ Create Docker Compose setup for isolated local testing

### Core Development Tools
- ✅ Set up FastAPI backend with Python dependencies
- ✅ Initialize React/TypeScript frontend development environment
- ✅ Install Ollama and configure local LLM integration
- ✅ Configure Docker containers for local development

**Status**: ✅ Complete

---

## Phase 3: AWS Infrastructure - Storage & Messaging

**Goal**: Implement S3 storage and SQS queue services

### S3 Integration
- ✅ Create S3 client with LocalStack/minio configuration
- ⬜ Design bucket structure (source documents, translated documents)
- ⬜ Implement document upload operations
- ⬜ Implement document download/retrieval operations
- ⬜ Add error handling for S3 service failures

### SQS Queue Implementation
- ⬜ Create SQS queue with proper naming conventions
- ⬜ Define job message format and structure
- ⬜ Implement queue message publishing logic
- ⬜ Implement queue message consumption logic
- ⬜ Add retry logic and dead-letter queue handling
- ⬜ Test local SQS simulation using LocalStack

**Status**: ⬜ In Progress

---

## Phase 4: AWS Infrastructure - Compute Workers

**Goal**: Create Lambda workers for document translation processing

### Lambda Function Development
- ⬜ Design Lambda function architecture
- ⬜ Create Lambda handler for translation job processing
- ⬜ Implement job message parsing and validation
- ⬜ Add local Lambda simulation capability
- ⬜ Configure proper timeout handling
- ⬜ Implement idempotent processing logic

### Worker Integration
- ⬜ Connect Lambda to S3 for document retrieval
- ⬜ Implement translation API call (local Ollama or Bedrock)
- ⬜ Add result storage back to S3 with metadata
- ⬜ Implement error handling and retry mechanisms
- ⬜ Configure proper IAM roles and permissions

**Status**: ⬜ In Progress

---

## Phase 5: AWS Infrastructure - Database & Security

**Goal**: Implement RDS PostgreSQL and Secrets Manager

### PostgreSQL Database Setup
- ⬜ Design database schema for job tracking
- ⬜ Create jobs table with proper indexing
- ⬜ Implement status tracking and transition logic
- ⬜ Add constraints and data validation rules
- ⬜ Configure connection pooling
- ⬜ Set up RDS PostgreSQL instance (or local Docker alternative)

### Secrets Management
- ⬜ Design secrets structure for API keys and credentials
- ⬜ Configure AWS Secrets Manager integration
- ⬜ Implement secure credential loading in Lambda workers
- ⬜ Create SSM Parameter Store alternative for local development
- ⬜ Add environment variable fallbacks for local dev
- ⬜ Test secret rotation and access patterns

**Status**: ⬜ In Progress

---

## Phase 6: AWS Infrastructure - Observability

**Goal**: Add CloudWatch logging and monitoring capabilities

### Logging Framework
- ⬜ Implement structured CloudWatch logging
- ⬜ Add custom metrics for system health tracking
- ⬜ Configure log retention policies
- ⬜ Set up error tracking and exception handling
- ⬜ Define log levels for different environments

### Monitoring & Alerting
- ⬜ Create CloudWatch dashboard with key performance indicators
- ⬜ Set up metrics for job success/failure rates
- ⬜ Implement alerting for critical system failures
- ⬜ Configure alerts for system degradation scenarios
- ⬜ Test monitoring in both local and AWS environments

**Status**: ⬜ In Progress

---

## Phase 7: Core Backend - Translation Services

**Goal**: Build FastAPI backend with translation endpoint

### API Foundation
- ✅ Create `backend/app/main.py` with health endpoint
- ✅ Implement CORS middleware configuration
- ✅ Set up error handling and logging infrastructure
- ✅ Configure proper HTTP status codes for all responses

### Translation Service Integration
- ✅ Implement `/api/v1/translate` endpoint
- ✅ Create translation schemas (request/response models)
- ✅ Integrate Ollama LLM service for translations
- ✅ Add support for both language directions (en→he, he→en)
- ✅ Test endpoint via FastAPI docs interface

### API Response Schema Design
- ✅ Define basic segment response format with source/target pairs
```json
{
  "source_lang": "en",
  "target_lang": "he",
  "segments": [
    {
      "id": "seg-1",
      "source": "The report is due tomorrow.",
      "target": "הדוח אמור להימסר מחר."
    }
  ]
}
```
- ✅ Define future-friendly token link format with range support
```json
{
  "token_links": [
    {
      "sourceStart": 1,
      "sourceEnd": 2,
      "targetStart": 0,
      "targetEnd": 1
    }
  ]
}
```
- ✅ Document all response schemas in OpenAPI/Swagger specs

### Segmentation Service
- ✅ Build paragraph-based segmenter service
- ✅ Implement sentence-aware segmentation (NLTK Punkt)
- ✅ Handle markdown structure preservation (headings, lists)
- ✅ Add processing time metrics and structured logging
- ✅ Implement file size validation (>10MB rejection)

**Status**: ✅ Complete

---

## Phase 8: Core Frontend - Basic UI

**Goal**: Create React frontend for document upload and review

### Application Setup
- ✅ Initialize Vite + React + TypeScript project
- ✅ Set up API client for translation endpoint communication
- ✅ Configure routing and state management

### Upload Interface
- ✅ Implement file upload form with language selection
- ✅ Add validation for supported file types
- ✅ Display upload progress and status messages
- ✅ Handle error states gracefully

### Review Interface
- ✅ Build segment row component for side-by-side display
- ✅ Implement RTL support for Hebrew text rendering
- ✅ Connect frontend to backend API endpoints
- ✅ Add loading states and user feedback

**Status**: ✅ Complete

---

## Phase 9: Token-Level Processing

**Goal**: Add tokenization capabilities for granular segment analysis

### Backend Tokenization
- ⌛ Create tokenizer service (`backend/app/services/tokenizer.py`)
- ⌛ Implement basic whitespace/punctuation splitting
- ⌛ Add Hebrew-aware tokenizer with RTL support
- ⌛ Optional: Integrate NLTK for advanced tokenization
- ⌛ Build token alignment data structures (foundation for Phase 13)

### API Schema Extensions
- ⌛ Define `Token` model for response payloads
- ⌛ Define `TokenLink` model for source-target mappings
- ⌛ Extend `SegmentWithTokens` schema with token arrays
- ⌛ Create standalone tokenization request/response endpoints
- ⌛ Add confidence score support for token alignments

### Frontend Token Display
- ⌛ Create `TokenDisplay.tsx` component
- ⌛ Implement clickable token rendering
- ⌛ Add RTL direction support for Hebrew tokens
- ⌛ Build highlighting capabilities (foundation for Phase 13)
- ⌛ Style punctuation tokens distinctly
- ⌛ Wire component to segment review UI

### Component Architecture Recommendations
- ⌛ Use custom token-highlighting UI rather than generic diff viewers
- ⌛ Render each token as a clickable `<span>` element
- ⌛ Store active selection in component or page state (not external library)
- ⌛ Create `AlignedText.tsx` for bidirectional highlighting logic
- ⌛ Implement hover preview and click-to-lock functionality for Phase 13

**Status**: ⌛ Not Started

---

## Phase 10: Enhanced Review Interface

**Goal**: Implement improved side-by-side review interface

### Segment Navigation
- ⌛ Create scrollable container for long document reviews
- ⌛ Add segment ID display and row numbering
- ⌛ Build `SegmentList.tsx` component

### Status & Filtering
- ⌛ Design status badge system (draft/reviewed/approved)
- ⌛ Implement `StatusBadge.tsx` component
- ⌛ Create search/filter functionality for segments
- ⌛ Build `SearchFilter.tsx` component
- ⌛ Add keyboard navigation support

### State Management
- ⌛ Update frontend state to track segment status
- ⌛ Implement search/filter logic in component state
- ⌛ Add keyboard event handlers for navigation
- ⌛ Persist review progress across sessions

**Status**: ⌛ Not Started

---

## Phase 11: Token Highlighting & Alignment

**Goal**: Implement bidirectional token highlighting and alignment features

### Backend Token Mapping
- ⌛ Create token alignment service (`backend/app/services/token_alignment.py`)
- ⌛ Implement heuristic-based token mapping logic
- ⌛ Add support for missing tokens and length mismatches
- ⌛ Return token metadata in translation responses

### Frontend Interaction
- ⌛ Enhance `SegmentRow.tsx` with token-level click handlers
- ⌛ Create bidirectional highlighting component
- ⌛ Ensure RTL-compatible rendering for Hebrew
- ⌛ Add visual feedback for user interactions
- ⌛ Handle edge cases gracefully (different segment lengths)

**Status**: ⌛ Not Started

---

## Phase 12: Complete Reviewer Workflow

**Goal**: Build full reviewer workflow with editing and export capabilities

### Segment Editing
- ⌛ Create editable segment components in frontend
- ⌛ Implement split/merge functionality for segments
- ⌛ Add comment/annotation system for reviewer notes

### Backend Support
- ⌛ Extend translation service to handle edited content
- ⌛ Add database persistence for reviewer notes and edits
- ⌛ Implement version control for segment changes
- ⌛ Create API endpoints for save/retrieve operations

### Export System
- ⌛ Design export format structure (JSON, DOCX, PDF)
- ⌛ Implement multiple format export functionality
- ⌛ Ensure proper document formatting in exports
- ⌛ Add download progress and error handling

### Production Polish
- ⌛ Finalize all UI components for production
- ⌛ Add comprehensive error handling and user feedback
- ⌛ Conduct end-to-end workflow testing
- ⌛ Gather and incorporate user feedback

**Status**: ⌛ Not Started

---

## Phase 13: AWS Migration & Production Deployment

**Goal**: Complete migration to production AWS services with full pipeline validation

### Infrastructure-as-Code Setup
- ⌛ Choose deployment framework (Terraform or CloudFormation)
- ⌛ Define infrastructure modules for all AWS services
- ⌛ Create environment-specific configurations (dev/staging/prod)
- ⌛ Set up CI/CD pipeline for automated deployments

### Production Migration
- ⌛ Deploy Lambda functions to AWS
- ⌛ Migrate database to production RDS instance
- ⌛ Configure proper IAM roles and permissions
- ⌛ Set up CloudWatch logging and monitoring in production
- ⌛ Deploy secrets to AWS Secrets Manager

### End-to-End Validation
- ⌛ Test complete document translation pipeline end-to-end
- ⌛ Validate error handling and recovery scenarios
- ⌛ Perform load testing with realistic workloads
- ⌛ Document system behavior under various conditions
- ⌛ Create runbook for common operational issues

**Status**: ⌛ Not Started

---

## Testing Strategy

### Automated Tests by Phase

| Phase               | Test File                         | Command                                       |
| ------------------- | --------------------------------- | --------------------------------------------- |
| Local Environment   | `tests/test_env_setup.py`         | `pytest tests/test_env_setup.py -v`           |
| AWS Mocking         | `tests/test_aws_mock.py`          | `pytest tests/test_aws_mock.py -v --aws-mock` |
| Backend API         | `backend/tests/test_api.py`       | `cd backend && pytest tests/ -v`              |
| Frontend Components | `frontend/tests/components/*.tsx` | `cd frontend && npm test`                     |

### Manual Testing Checklist

- [ ] Local development environment configured and working
- [ ] AWS services mocked successfully in local environment
- [ ] S3 storage works for document uploads/downloads
- [ ] SQS queue processing functions correctly (publish/consume)
- [ ] Lambda workers process jobs successfully locally
- [ ] PostgreSQL database stores job metadata correctly
- [ ] Secrets manager loads credentials properly in all environments
- [ ] CloudWatch logging captures events in local and AWS
- [ ] End-to-end translation pipeline works end-to-end
- [ ] Production deployment completes without errors

---

## Deployment Commands Reference

### Local Development
```bash
# Start local AWS services for testing
docker-compose up -d localstack minio

# Run tests with mocked AWS services
pytest tests/ --aws-mock --verbose

# Verify local setup
curl http://localhost:4566/_localstack/health
```

### Production Deployment
```bash
# Initialize Terraform infrastructure
terraform init
terraform apply -auto-approve

# Validate production environment
aws cloudformation describe-stacks --stack-name translation-pipeline

# Test API endpoint
curl https://api.example.com/translate \
  -H "Content-Type: application/json" \
  -d '{"source_lang": "en", "target_lang": "he", "text": "Hello"}'
```

---

## Success Criteria Summary

**Infrastructure (Phases 3-6)**
- [ ] All AWS services functional in local environment with mocking
- [ ] Lambda workers process jobs successfully
- [ ] Database stores and retrieves job metadata reliably
- [ ] Secrets management secures all credentials properly
- [ ] Observability captures system events and metrics

**Application (Phases 7-12)**
- [ ] Translation endpoint works for both language directions
- [ ] Segmentation handles complex document structures correctly
- [ ] Frontend displays Hebrew text with proper RTL direction
- [ ] Token-level highlighting enables bidirectional alignment
- [ ] Reviewer workflow supports full editing and export cycle

**Production (Phase 13)**
- [ ] Complete migration to production AWS services successful
- [ ] End-to-end pipeline validated under realistic workloads
- [ ] All automated tests pass in production environment
- [ ] Documentation complete for operations team

---

## Current Progress Summary

| Phase | Title                 | Status        | Completion |
| ----- | --------------------- | ------------- | ---------- |
| 1     | Project Foundation    | ✅ Complete    | 100%       |
| 2     | Local Dev Environment | ✅ Complete    | 100%       |
| 3-6   | AWS Infrastructure    | 🟡 In Progress | ~40%       |
| 7-8   | Core Backend/Frontend | ✅ Complete    | 100%       |
| 9     | Token Processing      | 🔴 Not Started | 0%         |
| 10    | Enhanced Review UI    | 🔴 Not Started | 0%         |
| 11    | Token Highlighting    | 🔴 Not Started | 0%         |
| 12    | Complete Workflow     | 🔴 Not Started | 0%         |
| 13    | AWS Migration         | 🔴 Not Started | 0%         |

**Overall Progress**: ~45% complete (Phases 1-8 partially done)

---

## Resume & Interview Framing

### Portfolio Summary Statement

Use this framing when discussing the project in interviews or on your resume:

> "Built a bilingual English ↔ Hebrew translation-review workflow with FastAPI backend and React frontend. The system ingests text/Markdown files, segments content intelligently, and translates using a local LLM (Ollama). Features include side-by-side review interface with RTL support for complex scripts, interactive token-level highlighting for bidirectional alignment, and AWS infrastructure patterns (S3, SQS, Lambda, RDS) demonstrating production-ready cloud architecture."

### Key Skills Demonstrated

- **Backend**: FastAPI design patterns, service layer architecture, API schema design
- **AI/ML**: Local LLM integration via Ollama, prompt engineering for translation tasks
- **Frontend**: React with TypeScript, RTL layout handling, custom interaction components
- **Cloud Architecture**: AWS services (S3, SQS, Lambda, RDS, Secrets Manager), infrastructure patterns
- **DevOps**: Docker containerization, local service mocking, CI/CD pipeline design

### Public vs. Commercial Extension Path

**Public Repository (Portfolio-Ready)**:
- Core translation workflow with basic token highlighting
- Clean FastAPI + React architecture demo
- README with screenshots and usage examples

**Commercial/Private Extensions**:
- Advanced alignment algorithms with ML-based matching
- Team review and approval workflows with permissions
- Glossary/terminology enforcement for brand consistency
- Customer-specific translation memory integration
- Analytics dashboard and audit trail reporting
- Hosted deployment with multi-tenant architecture

---

## Notes

- **Phase Ordering**: AWS infrastructure phases (3-6) come first as they provide foundational services for the compute workers
- **AI Integration**: Ollama LLM integration happens in Phase 7 alongside core backend development
- **Sequential Dependencies**: Later phases build on earlier work; do not skip phases
- **Testing**: Automated tests should be written during each phase, not after
- **Documentation**: Update this plan as implementation details change or new requirements emerge