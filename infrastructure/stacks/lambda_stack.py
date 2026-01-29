"""
Lambda Stack for Skillsnap

Creates all Lambda functions for the application:
- Auth Lambdas (post-confirmation, pre-token)
- Resume Lambdas (CRUD operations)
- Job Lambdas (CRUD operations, scraping, cleanup)
- Generation Lambdas (subcomponent, final files)
- User Lambdas (preferences)

Requirements: 17.3
"""
from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as lambda_,
    aws_iam as iam,
    aws_lambda_event_sources as lambda_events,
    aws_events as events,
    aws_events_targets as targets,
)
from constructs import Construct
from .dynamodb_stack import DynamoDBStack
from .sqs_stack import SQSStack


class LambdaStack(Stack):
    """Stack containing all Lambda functions for Skillsnap."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        dynamodb_stack: DynamoDBStack,
        sqs_stack: SQSStack,
        resumes_bucket_name: str = "skillsnap-public-resumes",
        imports_bucket_name: str = "skillsnap-imports-temp",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Common environment variables for all Lambdas
        common_env = {
            'USER_TABLE': dynamodb_stack.user_table.table_name,
            'USER_EMAIL_TABLE': dynamodb_stack.user_email_table.table_name,
            'USER_USERNAME_TABLE': dynamodb_stack.user_username_table.table_name,
            'USER_PREF_TABLE': dynamodb_stack.user_pref_table.table_name,
            'JOB_TABLE': dynamodb_stack.job_table.table_name,
            'USER_JOB_TABLE': dynamodb_stack.user_job_table.table_name,
            'RESUME_TABLE': dynamodb_stack.resume_table.table_name,
            'RESUME_URL_TABLE': dynamodb_stack.resume_url_table.table_name,
            'GENERATION_QUEUE_URL': sqs_stack.generation_queue.queue_url,
            'RESUMES_BUCKET': resumes_bucket_name,
            'IMPORTS_BUCKET': imports_bucket_name,
        }

        # Create Lambda layer for shared code
        import os
        lambdas_path = os.path.join(os.path.dirname(__file__), '..', 'lambdas')
        
        self.shared_layer = lambda_.LayerVersion(
            self, "SharedLayer",
            layer_version_name="skillsnap-shared",
            code=lambda_.Code.from_asset(lambdas_path),
            compatible_runtimes=[lambda_.Runtime.PYTHON_3_12],
            description="Shared utilities for Skillsnap Lambdas",
        )

        # IAM role for Lambdas
        lambda_role = iam.Role(
            self, "LambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"),
            ],
        )

        # Grant DynamoDB permissions
        dynamodb_stack.user_table.grant_read_write_data(lambda_role)
        dynamodb_stack.user_email_table.grant_read_write_data(lambda_role)
        dynamodb_stack.user_username_table.grant_read_write_data(lambda_role)
        dynamodb_stack.user_pref_table.grant_read_write_data(lambda_role)
        dynamodb_stack.job_table.grant_read_write_data(lambda_role)
        dynamodb_stack.user_job_table.grant_read_write_data(lambda_role)
        dynamodb_stack.resume_table.grant_read_write_data(lambda_role)
        dynamodb_stack.resume_url_table.grant_read_write_data(lambda_role)

        # Grant SQS permissions
        sqs_stack.generation_queue.grant_send_messages(lambda_role)
        sqs_stack.generation_queue.grant_consume_messages(lambda_role)

        # Grant S3 permissions for resumes bucket
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
            resources=[f"arn:aws:s3:::{resumes_bucket_name}/*"],
        ))

        # Grant S3 permissions for imports temp bucket
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["s3:PutObject", "s3:GetObject", "s3:DeleteObject"],
            resources=[f"arn:aws:s3:::{imports_bucket_name}/*"],
        ))

        # Grant Bedrock permissions
        lambda_role.add_to_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel"],
            resources=["*"],
        ))

        # Helper function to create Lambda
        def create_lambda(name: str, handler: str, timeout: int = 30) -> lambda_.Function:
            return lambda_.Function(
                self, name,
                function_name=f"skillsnap-{name.lower()}",
                runtime=lambda_.Runtime.PYTHON_3_12,
                handler=handler,
                code=lambda_.Code.from_asset(lambdas_path),
                environment=common_env,
                role=lambda_role,
                timeout=Duration.seconds(timeout),
                memory_size=256,
            )

        # Auth Lambdas
        self.auth_post_confirmation = create_lambda(
            "AuthPostConfirmation",
            "auth.post_confirmation.handler"
        )

        # Resume Lambdas
        self.resume_create = create_lambda("ResumeCreate", "resume.create.handler")
        self.resume_get = create_lambda("ResumeGet", "resume.get.handler")
        self.resume_list = create_lambda("ResumeList", "resume.list.handler")
        self.resume_update = create_lambda("ResumeUpdate", "resume.update.handler")
        self.resume_delete = create_lambda("ResumeDelete", "resume.delete.handler")

        # Resume Import Lambdas (Requirements: 4.4)
        self.resume_import_url = create_lambda("ResumeImportUrl", "resume.import_url.handler")
        self.resume_import_process = create_lambda(
            "ResumeImportProcess",
            "resume.import_process.handler",
            timeout=60  # Allow time for AI processing
        )

        # Job Lambdas
        self.job_create_manual = create_lambda("JobCreateManual", "job.create_manual.handler")
        self.job_create_url = create_lambda("JobCreateUrl", "job.create_url.handler", timeout=60)
        self.job_create_gmail = create_lambda("JobCreateGmail", "job.create_gmail.handler", timeout=60)
        self.job_get = create_lambda("JobGet", "job.get.handler")
        self.job_list = create_lambda("JobList", "job.list.handler")
        self.job_update_phase = create_lambda("JobUpdatePhase", "job.update_phase.handler")
        self.job_delete = create_lambda("JobDelete", "job.delete.handler")
        self.job_cleanup_trash = create_lambda("JobCleanupTrash", "job.cleanup_trash.handler", timeout=300)

        # Add daily EventBridge schedule for trash cleanup (runs at 3 AM UTC)
        cleanup_rule = events.Rule(
            self, "TrashCleanupRule",
            rule_name="skillsnap-trash-cleanup-daily",
            schedule=events.Schedule.cron(minute="0", hour="3"),
            description="Daily cleanup of jobs in Trash phase older than 7 days",
        )
        cleanup_rule.add_target(targets.LambdaFunction(self.job_cleanup_trash))

        # User Lambdas
        self.user_prefs_get = create_lambda("UserPrefsGet", "user.prefs_get.handler")
        self.user_prefs_update = create_lambda("UserPrefsUpdate", "user.prefs_update.handler")

        # Generation Lambdas
        self.gen_subcomponent = create_lambda(
            "GenSubcomponent",
            "generation.subcomponent.handler",
            timeout=300  # 5 minutes for AI generation
        )
        self.gen_all = create_lambda("GenAll", "generation.generate_all.handler")
        self.gen_single = create_lambda("GenSingle", "generation.generate_single.handler")
        self.gen_status = create_lambda("GenStatus", "generation.status.handler")
        self.gen_toggle_type = create_lambda("GenToggleType", "generation.toggle_type.handler")
        self.gen_final_html = create_lambda("GenFinalHtml", "generation.final_html.handler", timeout=60)
        self.gen_final_pdf = create_lambda("GenFinalPdf", "generation.final_pdf.handler", timeout=120)

        # Add SQS trigger to subcomponent generator
        self.gen_subcomponent.add_event_source(
            lambda_events.SqsEventSource(
                sqs_stack.generation_queue,
                batch_size=1,
            )
        )

        # Store references for API Gateway
        self.lambdas = {
            'resume_create': self.resume_create,
            'resume_get': self.resume_get,
            'resume_list': self.resume_list,
            'resume_update': self.resume_update,
            'resume_delete': self.resume_delete,
            'resume_import_url': self.resume_import_url,
            'resume_import_process': self.resume_import_process,
            'job_create_manual': self.job_create_manual,
            'job_create_url': self.job_create_url,
            'job_create_gmail': self.job_create_gmail,
            'job_get': self.job_get,
            'job_list': self.job_list,
            'job_update_phase': self.job_update_phase,
            'job_delete': self.job_delete,
            'user_prefs_get': self.user_prefs_get,
            'user_prefs_update': self.user_prefs_update,
            'gen_all': self.gen_all,
            'gen_single': self.gen_single,
            'gen_status': self.gen_status,
            'gen_toggle_type': self.gen_toggle_type,
            'gen_final_html': self.gen_final_html,
            'gen_final_pdf': self.gen_final_pdf,
        }
