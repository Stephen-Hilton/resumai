# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SkillSnap** is a serverless web application that automates bespoke resume generation for job seekers. The system uses an event-driven architecture on AWS with a React frontend.

## Tech Stack

- **Infrastructure**: AWS CDK in Python (`infrastructure/`)
- **Frontend**: React + TypeScript + Vite + Tailwind (`webapp/`)
- **Backend**: Python Lambda functions (`infrastructure/lambdas/`)
- **AWS Services**: DynamoDB, S3, Cognito, API Gateway, CloudFront, SQS, Bedrock Nova Micro

## Development Commands

### Infrastructure (Python/CDK)
```bash
cd infrastructure

# Setup virtual environment (first time)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Development workflow
cdk synth                    # Synthesize CloudFormation
cdk diff                     # Compare with deployed
cdk deploy --all             # Deploy all stacks
pytest tests/                # Run tests
pytest tests/ -v --tb=short  # Run tests with details

# Full deployment (includes tests)
../scripts/deploy-infrastructure.sh
```

### WebApp (React/TypeScript)
```bash
cd webapp

npm install          # Install dependencies
npm run dev          # Start dev server
npm run build        # Build for production
npm run lint         # Lint code
npm run test         # Run tests once
npm run test:watch   # Run tests in watch mode

# Full deployment (includes tests and S3 sync)
../scripts/deploy-webapp.sh
```

## Architecture Overview

### Infrastructure Stack Dependencies
The CDK stacks must be deployed in this order due to dependencies:
1. **DynamoDBStack** - Data persistence (8 tables for multi-table design)
2. **S3Stack** - Static assets and file storage
3. **CloudFrontStack** - CDN distributions (depends on S3)
4. **CognitoStack** - User authentication with Google OAuth
5. **SQSStack** - Async processing queues for generation tasks
6. **LambdaStack** - All Lambda functions (depends on DynamoDB, SQS)
7. **ApiGatewayStack** - REST API (depends on Cognito, Lambda)

The `app.py` entry point orchestrates these stacks and configures cross-stack references.

### Lambda Organization
Lambdas are organized by domain in `infrastructure/lambdas/`:
- `auth/` - Cognito triggers (post-confirmation)
- `resume/` - CRUD operations for resumes
- `job/` - CRUD, scraping, cleanup, expiration
- `generation/` - Subcomponent and final file generation (HTML/PDF)
- `user/` - User preferences
- `shared/` - Common utilities (response, dynamodb, validation)

All Lambdas use Python 3.12 runtime and share a Lambda Layer for common code.

### Frontend Architecture
- **SPA Router**: React Router at `webapp/src/App.tsx`
- **API Service**: Centralized API client at `webapp/src/services/api.ts` with Cognito JWT token injection
- **Auth**: AWS Amplify for Cognito integration
- **Types**: TypeScript definitions in `webapp/src/types/index.ts` mirror backend data models

### Data Model Key Concepts
- **Multi-Table Design**: Separate DynamoDB tables enforce uniqueness constraints (userid, email, username, resume URLs)
- **Job Phases**: Jobs progress through phases: Queued → Generating → Ready → Applied → Follow-Up → Negotiation → Accepted (or Skipped/Expired/Trash)
- **Subcomponents**: Resumes have 9 subcomponents (contact, summary, skills, highlights, experience, education, awards, keynotes, coverletter)
- **Generation Types**: Each subcomponent can be 'manual' (from resume JSON), 'ai' (Bedrock generation), or 'omit' (excluded)
- **Generation Flow**: User triggers generation → Lambda queues work to SQS → Workers generate subcomponents → Final files (HTML/PDF) aggregated and uploaded to S3

## AWS Configuration

**IMPORTANT**: This project does NOT use `aws sso login`. Authentication uses static keys from `.env`:
- `AWS_ACCESS_KEY`
- `AWS_SECRET_ACCESS_KEY`

All infrastructure is deployed to **us-west-2** region.

## Development Workflow Rules

### ALL Development Tasks
- Review `.kiro/specs/skillsnap-mvp/` before making changes
- Do NOT add features unless explicitly requested
- Do NOT remove/change functionality unless explicitly requested
- Do NOT change visual design or component locations unless explicitly requested
- ALWAYS deploy changes to AWS immediately after making them (project is still in active development)

### Change Requests (CR:)
When user prefixes request with `CR:`:
- Follow existing code style and patterns
- Make changes as small as possible while achieving the goal
- MUST test all changes before notifying user or marking Complete

### Bug Fixes (BF:)
When user prefixes request with `BF:`:
- MUST follow existing code style and patterns exactly
- If existing pattern is causing the bug, summarize the issue and ask user for confirmation before changing patterns
- Do NOT introduce new technologies, design patterns, or dependencies unless explicitly asked
- Do NOT modify anything outside the scope of the bug fix
- MUST test all changes before notifying user or marking Fixed

### Questions Only (Q:)
When user prefixes request with `Q:`:
- Answer the question but do NOT modify any code

## Important File Locations

- **Specs**: `.kiro/specs/` - Requirements and design documents
- **Deploy Scripts**: `scripts/deploy-*.sh` - Deployment automation
- **CDK Entry**: `infrastructure/app.py` - Infrastructure definition
- **API Service**: `webapp/src/services/api.ts` - Frontend API client
- **Shared Lambda Utils**: `infrastructure/lambdas/shared/` - DynamoDB client, response helpers, validation
- **Type Definitions**: `webapp/src/types/index.ts` - TypeScript types matching backend models
