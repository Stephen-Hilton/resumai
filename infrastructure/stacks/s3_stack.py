"""
S3 Stack for Skillsnap

Creates S3 buckets for:
- skillsnap-landing: Static landing page
- skillsnap-webapp: React application
- skillsnap-public-resumes: Generated resume files

Requirements: 2.1, 3.1, 10.6
"""
from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_s3 as s3,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class S3Stack(Stack):
    """Stack containing all S3 buckets for Skillsnap."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Landing page bucket - skillsnap.me
        # Note: CloudFront OAI access is granted in cloudfront_stack.py
        self.landing_bucket = s3.Bucket(
            self, "LandingBucket",
            bucket_name="skillsnap-landing",
            website_index_document="index.html",
            website_error_document="index.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=False,  # Allow bucket policy for OAI
                ignore_public_acls=True,
                restrict_public_buckets=False,  # Allow OAI access
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )
            ],
        )

        # WebApp bucket - app.skillsnap.me
        self.webapp_bucket = s3.Bucket(
            self, "WebAppBucket",
            bucket_name="skillsnap-webapp",
            website_index_document="index.html",
            website_error_document="index.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=False,
                ignore_public_acls=True,
                restrict_public_buckets=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )
            ],
        )

        # Public resumes bucket - *.skillsnap.me
        self.resumes_bucket = s3.Bucket(
            self, "ResumesBucket",
            bucket_name="skillsnap-public-resumes",
            website_index_document="index.html",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=False,
                ignore_public_acls=True,
                restrict_public_buckets=False,
            ),
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.GET, s3.HttpMethods.HEAD],
                    allowed_origins=["*"],
                    allowed_headers=["*"],
                )
            ],
        )

        # Temp imports bucket - for file upload processing
        # Requirements: 4.1, 4.3
        self.imports_temp_bucket = s3.Bucket(
            self, "ImportsTempBucket",
            bucket_name="skillsnap-imports-temp",
            public_read_access=False,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            lifecycle_rules=[
                s3.LifecycleRule(
                    id="delete-temp-imports",
                    enabled=True,
                    expiration=Duration.days(1),
                    prefix="temp-imports/",
                )
            ],
            cors=[
                s3.CorsRule(
                    allowed_methods=[s3.HttpMethods.PUT, s3.HttpMethods.GET],
                    allowed_origins=[
                        "https://app.skillsnap.me",
                        "http://localhost:3000",
                        "http://localhost:5173",
                    ],
                    allowed_headers=["*"],
                    max_age=60,
                )
            ],
        )

        # Outputs for reference
        CfnOutput(self, "LandingBucketName", value=self.landing_bucket.bucket_name)
        CfnOutput(self, "WebAppBucketName", value=self.webapp_bucket.bucket_name)
        CfnOutput(self, "ResumesBucketName", value=self.resumes_bucket.bucket_name)
        CfnOutput(self, "ImportsTempBucketName", value=self.imports_temp_bucket.bucket_name)
