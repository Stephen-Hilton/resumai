"""
DynamoDB Stack for Skillsnap

Creates all DynamoDB tables for the application:
- USER: User profiles
- USER_EMAIL: Email uniqueness enforcement
- USER_USERNAME: Username uniqueness enforcement
- USER_PREF: User preferences
- JOB: Job postings
- USER_JOB: User-job relationships and generation data
- RESUME: User resumes
- RESUME_URL: Resume URL uniqueness

Requirements: 15.1, 15.2, 15.3, 15.4, 15.5
"""
from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class DynamoDBStack(Stack):
    """Stack containing all DynamoDB tables for Skillsnap."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # USER table - User profiles
        # PK: userid (uuid7)
        self.user_table = dynamodb.Table(
            self, "UserTable",
            table_name="skillsnap-user",
            partition_key=dynamodb.Attribute(
                name="userid",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            point_in_time_recovery=True,
        )

        # USER_EMAIL table - Email uniqueness enforcement
        # PK: useremail
        self.user_email_table = dynamodb.Table(
            self, "UserEmailTable",
            table_name="skillsnap-user-email",
            partition_key=dynamodb.Attribute(
                name="useremail",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # USER_USERNAME table - Username uniqueness enforcement
        # PK: username
        self.user_username_table = dynamodb.Table(
            self, "UserUsernameTable",
            table_name="skillsnap-user-username",
            partition_key=dynamodb.Attribute(
                name="username",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # USER_PREF table - User preferences
        # PK: userid, SK: prefname
        self.user_pref_table = dynamodb.Table(
            self, "UserPrefTable",
            table_name="skillsnap-user-pref",
            partition_key=dynamodb.Attribute(
                name="userid",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="prefname",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # JOB table - Job postings
        # PK: jobid (uuid7)
        self.job_table = dynamodb.Table(
            self, "JobTable",
            table_name="skillsnap-job",
            partition_key=dynamodb.Attribute(
                name="jobid",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            point_in_time_recovery=True,
        )

        # USER_JOB table - User-job relationships and generation data
        # PK: userid, SK: jobid
        self.user_job_table = dynamodb.Table(
            self, "UserJobTable",
            table_name="skillsnap-user-job",
            partition_key=dynamodb.Attribute(
                name="userid",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="jobid",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            point_in_time_recovery=True,
        )

        # Add GSI for querying jobs by phase
        self.user_job_table.add_global_secondary_index(
            index_name="phase-index",
            partition_key=dynamodb.Attribute(
                name="userid",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="jobphase",
                type=dynamodb.AttributeType.STRING
            ),
            projection_type=dynamodb.ProjectionType.ALL,
        )

        # RESUME table - User resumes
        # PK: userid, SK: resumename
        self.resume_table = dynamodb.Table(
            self, "ResumeTable",
            table_name="skillsnap-resume",
            partition_key=dynamodb.Attribute(
                name="userid",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="resumename",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
            point_in_time_recovery=True,
        )

        # RESUME_URL table - Resume URL uniqueness
        # PK: resumeurl
        self.resume_url_table = dynamodb.Table(
            self, "ResumeUrlTable",
            table_name="skillsnap-resume-url",
            partition_key=dynamodb.Attribute(
                name="resumeurl",
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
