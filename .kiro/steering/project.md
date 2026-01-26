# SkillSnap Project Guidelines

## Project Structure
- **Infrastructure**: AWS CDK in Python (`infrastructure/`)
- **Web App**: React + TypeScript + Vite (`webapp/`)
- **Lambdas**: Python handlers (`infrastructure/lambdas/`)

## Tech Stack
- AWS CDK (Python) for infrastructure
- React + TypeScript + Tailwind for frontend
- Python Lambda functions
- DynamoDB, S3, Cognito, API Gateway, CloudFront, SQS

## AWS Authentication
- This project does NOT user `aws sso login`, NEVER use that auth method.
- Instead, use the key stored in the `./.env` file:
    - AWS_SECRET_ACCESS_KEY
    - AWS_ACCESS_KEY


## Development Rules, ALL Requests: 
- Review `.kiro/specs/skillsnap-mvp/` before making changes
- Do not add features unless explicitly requested
- Do not remove / change functionality unless explicitly requested
- Do not change visual design or component location unless explicitly requested
- ALWAYS deploy changes to AWS immediately (still in dev)

## Rules for Change Requests (CR):
In addition to all "Development Rules":
- Attempt to follow the existing code style and patterns
- You MUST make changes as small as possible while still achieving the goal
- You MUST test all changes before notifying the user or marking it as Complete


## Rules for Bug Fixes (BF):
In addition to all "Development Rules":
- You MUST follow the existing code style and patterns
- If an existing style or pattern is causing the bug, generate a very short summary of the bug, and ask the user for confirmation
- You MUST NOT introduce any new technologies, design patterns, or dependencies unless explicitly asked
- Do not modify anything outside of the scope of the bug fix
- You MUST test all changes before notifying the user or marking it as Fixed 


# Short-Cut commands:
Below are short-cut commands that, if placed at the very beginning of a new request/prompt (only at the beginning), indicate special handling:
- `Q:` = what follows is a question only; answer the question, but do NOT modify code
- `CR:` = what follows is a change request, apply the rules found in "Rules for Change Requests (CR)" section
- `BF:` = what follows is a bug fix, apply the rules found in "Rules for Bug Fixes (BF)" section

