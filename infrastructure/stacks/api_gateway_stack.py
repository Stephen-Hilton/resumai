"""
API Gateway Stack for Skillsnap

Creates REST API at api.skillsnap.me with:
- Cognito authorizer for all endpoints
- CORS configuration for app.skillsnap.me
- Lambda integrations for all API routes

Requirements: 14.1, 14.2
"""
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_apigateway as apigateway,
    aws_cognito as cognito,
)
from constructs import Construct
from .cognito_stack import CognitoStack
from .lambda_stack import LambdaStack


class ApiGatewayStack(Stack):
    """Stack containing API Gateway resources for Skillsnap."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        cognito_stack: CognitoStack,
        lambda_stack: LambdaStack,
        domain_name: str = "skillsnap.me",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create REST API
        self.api = apigateway.RestApi(
            self, "SkillsnapApi",
            rest_api_name="skillsnap-api",
            description="Skillsnap REST API",
            deploy_options=apigateway.StageOptions(
                stage_name="v1",
                throttling_rate_limit=1000,
                throttling_burst_limit=500,
            ),
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=[
                    f"https://app.{domain_name}",
                    "http://localhost:3000",
                    "http://localhost:5173",
                ],
                allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                allow_headers=[
                    "Content-Type",
                    "Authorization",
                    "X-Amz-Date",
                    "X-Api-Key",
                    "X-Amz-Security-Token",
                ],
                allow_credentials=True,
            ),
        )

        # Create Cognito authorizer
        self.authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer",
            cognito_user_pools=[cognito_stack.user_pool],
            authorizer_name="skillsnap-authorizer",
        )

        # Helper to create Lambda integration
        def lambda_integration(lambda_fn):
            return apigateway.LambdaIntegration(
                lambda_fn,
                proxy=True,
            )

        # Common method options with authorization
        auth_options = {
            'authorizer': self.authorizer,
            'authorization_type': apigateway.AuthorizationType.COGNITO,
        }

        # ==================== RESUME ENDPOINTS ====================
        resumes = self.api.root.add_resource("resumes")
        
        # GET /resumes - List resumes
        resumes.add_method(
            "GET",
            lambda_integration(lambda_stack.resume_list),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )
        
        # POST /resumes - Create resume
        resumes.add_method(
            "POST",
            lambda_integration(lambda_stack.resume_create),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # /resumes/{resumename}
        resume_by_name = resumes.add_resource("{resumename}")
        
        # GET /resumes/{resumename}
        resume_by_name.add_method(
            "GET",
            lambda_integration(lambda_stack.resume_get),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )
        
        # PUT /resumes/{resumename}
        resume_by_name.add_method(
            "PUT",
            lambda_integration(lambda_stack.resume_update),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )
        
        # DELETE /resumes/{resumename}
        resume_by_name.add_method(
            "DELETE",
            lambda_integration(lambda_stack.resume_delete),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # ==================== RESUME IMPORT ENDPOINTS ====================
        # /resumes/import
        resumes_import = resumes.add_resource("import")
        
        # POST /resumes/import/url - Get presigned URL for file upload
        import_url = resumes_import.add_resource("url")
        import_url.add_method(
            "POST",
            lambda_integration(lambda_stack.resume_import_url),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )
        
        # POST /resumes/import/process - Process uploaded file
        import_process = resumes_import.add_resource("process")
        import_process.add_method(
            "POST",
            lambda_integration(lambda_stack.resume_import_process),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # ==================== JOB ENDPOINTS ====================
        jobs = self.api.root.add_resource("jobs")
        
        # GET /jobs - List jobs
        jobs.add_method(
            "GET",
            lambda_integration(lambda_stack.job_list),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/manual - Create job manually
        jobs_manual = jobs.add_resource("manual")
        jobs_manual.add_method(
            "POST",
            lambda_integration(lambda_stack.job_create_manual),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/url - Create job from URL
        jobs_url = jobs.add_resource("url")
        jobs_url.add_method(
            "POST",
            lambda_integration(lambda_stack.job_create_url),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/gmail - Create jobs from Gmail
        jobs_gmail = jobs.add_resource("gmail")
        jobs_gmail.add_method(
            "POST",
            lambda_integration(lambda_stack.job_create_gmail),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # /jobs/{jobid}
        job_by_id = jobs.add_resource("{jobid}")
        
        # GET /jobs/{jobid}
        job_by_id.add_method(
            "GET",
            lambda_integration(lambda_stack.job_get),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )
        
        # DELETE /jobs/{jobid}
        job_by_id.add_method(
            "DELETE",
            lambda_integration(lambda_stack.job_delete),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # PUT /jobs/{jobid}/phase
        job_phase = job_by_id.add_resource("phase")
        job_phase.add_method(
            "PUT",
            lambda_integration(lambda_stack.job_update_phase),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # ==================== GENERATION ENDPOINTS ====================
        # POST /jobs/{jobid}/generate-all
        gen_all = job_by_id.add_resource("generate-all")
        gen_all.add_method(
            "POST",
            lambda_integration(lambda_stack.gen_all),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/{jobid}/generate/{component}
        gen_component = job_by_id.add_resource("generate")
        gen_single = gen_component.add_resource("{component}")
        gen_single.add_method(
            "POST",
            lambda_integration(lambda_stack.gen_single),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # GET /jobs/{jobid}/status
        job_status = job_by_id.add_resource("status")
        job_status.add_method(
            "GET",
            lambda_integration(lambda_stack.gen_status),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # PUT /jobs/{jobid}/type/{component}
        type_resource = job_by_id.add_resource("type")
        type_component = type_resource.add_resource("{component}")
        type_component.add_method(
            "PUT",
            lambda_integration(lambda_stack.gen_toggle_type),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # ==================== FINAL FILE ENDPOINTS ====================
        final = job_by_id.add_resource("final")
        
        # POST /jobs/{jobid}/final/resume-html
        final_resume_html = final.add_resource("resume-html")
        final_resume_html.add_method(
            "POST",
            lambda_integration(lambda_stack.gen_final_html),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/{jobid}/final/resume-pdf
        final_resume_pdf = final.add_resource("resume-pdf")
        final_resume_pdf.add_method(
            "POST",
            lambda_integration(lambda_stack.gen_final_pdf),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/{jobid}/final/cover-html
        final_cover_html = final.add_resource("cover-html")
        final_cover_html.add_method(
            "POST",
            lambda_integration(lambda_stack.gen_final_html),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # POST /jobs/{jobid}/final/cover-pdf
        final_cover_pdf = final.add_resource("cover-pdf")
        final_cover_pdf.add_method(
            "POST",
            lambda_integration(lambda_stack.gen_final_pdf),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # ==================== PREFERENCES ENDPOINTS ====================
        preferences = self.api.root.add_resource("preferences")
        
        # GET /preferences
        preferences.add_method(
            "GET",
            lambda_integration(lambda_stack.user_prefs_get),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )
        
        # PUT /preferences
        preferences.add_method(
            "PUT",
            lambda_integration(lambda_stack.user_prefs_update),
            authorizer=self.authorizer,
            authorization_type=apigateway.AuthorizationType.COGNITO,
        )

        # Outputs
        CfnOutput(self, "ApiUrl", value=self.api.url)
        CfnOutput(self, "ApiId", value=self.api.rest_api_id)
