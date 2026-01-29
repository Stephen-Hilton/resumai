#!/bin/bash
# Deploy WebApp Script
# Requirements: 17.1

set -e

echo "🚀 Deploying Skillsnap WebApp..."

# Navigate to webapp directory
cd "$(dirname "$0")/../webapp"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Run tests
echo "🧪 Running tests..."
npm run test

# Build the app
echo "🔨 Building webapp..."
npm run build

# Deploy to S3
echo "☁️ Uploading to S3..."
aws s3 sync dist/ s3://skillsnap-webapp --delete

# Invalidate CloudFront cache
echo "🔄 Invalidating CloudFront cache..."
DISTRIBUTION_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Aliases.Items[?contains(@, 'app.skillsnap.me')]].Id" --output text)
if [ -n "$DISTRIBUTION_ID" ]; then
    aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths "/*"
fi

echo "✅ WebApp deployment complete!"
