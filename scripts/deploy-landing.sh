#!/bin/bash
# Deploy Landing Page Script
# Requirements: 17.1

set -e

echo "🚀 Deploying Skillsnap Landing Page..."

# Navigate to webapp directory
cd "$(dirname "$0")/../webapp"

# Deploy landing page to S3
echo "☁️ Uploading to S3..."
aws s3 sync public/landing/ s3://skillsnap-landing --delete

# Deploy CSS assets to public resumes bucket
echo "📄 Uploading CSS assets..."
aws s3 cp public/assets/resume-base.css s3://skillsnap-public-resumes/assets/resume-base.css --cache-control "max-age=31536000"
aws s3 cp public/assets/cover-base.css s3://skillsnap-public-resumes/assets/cover-base.css --cache-control "max-age=31536000"

# Invalidate CloudFront cache for landing page
echo "🔄 Invalidating CloudFront cache..."
DISTRIBUTION_ID=$(aws cloudfront list-distributions --query "DistributionList.Items[?Aliases.Items[?contains(@, 'skillsnap.me') && !contains(@, 'app.')]].Id" --output text)
if [ -n "$DISTRIBUTION_ID" ]; then
    aws cloudfront create-invalidation --distribution-id "$DISTRIBUTION_ID" --paths "/*"
fi

echo "✅ Landing page deployment complete!"
