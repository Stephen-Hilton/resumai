#!/bin/bash
# Deploy Infrastructure Script
# Requirements: 17.1

set -e

echo "🚀 Deploying Skillsnap Infrastructure..."

# Navigate to infrastructure directory
cd "$(dirname "$0")/../infrastructure"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt -q

# Run tests first
echo "🧪 Running tests..."
python -m pytest tests/ -v --tb=short

# Synthesize CDK
echo "🔧 Synthesizing CDK..."
cdk synth

# Deploy all stacks
echo "☁️ Deploying to AWS..."
cdk deploy --all --require-approval never

echo "✅ Infrastructure deployment complete!"
