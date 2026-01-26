"""
Cognito Stack for Skillsnap

Creates Cognito User Pool and App Client for authentication:
- Email/password authentication
- Google OAuth integration
- Hosted UI configuration
- Lambda triggers for user management

Requirements: 1.1, 1.2, 1.3, 1.6
"""
from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    CfnOutput,
    aws_cognito as cognito,
    aws_lambda as lambda_,
    aws_iam as iam,
)
from constructs import Construct


class CognitoStack(Stack):
    """Stack containing Cognito authentication resources for Skillsnap."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_name: str = "skillsnap.me",
        google_client_id: str = "",
        google_client_secret: str = "",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.domain_name = domain_name

        # Create the User Pool
        self.user_pool = cognito.UserPool(
            self, "UserPool",
            user_pool_name="skillsnap-users",
            self_sign_up_enabled=True,
            sign_in_aliases=cognito.SignInAliases(
                email=True,
                username=True,
            ),
            auto_verify=cognito.AutoVerifiedAttrs(
                email=True,
            ),
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True,
                ),
                preferred_username=cognito.StandardAttribute(
                    required=False,
                    mutable=True,
                ),
            ),
            custom_attributes={
                "userid": cognito.StringAttribute(
                    mutable=False,
                    max_len=36,
                ),
                "userhandle": cognito.StringAttribute(
                    mutable=True,
                    max_len=100,
                ),
            },
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=False,
                temp_password_validity=Duration.days(7),
            ),
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # Add Google OAuth Identity Provider (if credentials provided)
        if google_client_id and google_client_secret:
            self.google_provider = cognito.UserPoolIdentityProviderGoogle(
                self, "GoogleProvider",
                user_pool=self.user_pool,
                client_id=google_client_id,
                client_secret=google_client_secret,
                scopes=["email", "profile", "openid"],
                attribute_mapping=cognito.AttributeMapping(
                    email=cognito.ProviderAttribute.GOOGLE_EMAIL,
                    preferred_username=cognito.ProviderAttribute.GOOGLE_NAME,
                    custom={
                        "userhandle": cognito.ProviderAttribute.GOOGLE_NAME,
                    },
                ),
            )

        # Create User Pool Domain for hosted UI
        self.user_pool_domain = cognito.UserPoolDomain(
            self, "UserPoolDomain",
            user_pool=self.user_pool,
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix="skillsnap-auth",
            ),
        )

        # Create App Client
        self.app_client = cognito.UserPoolClient(
            self, "AppClient",
            user_pool=self.user_pool,
            user_pool_client_name="skillsnap-webapp",
            generate_secret=False,
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
            ),
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=True,
                ),
                scopes=[
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.PROFILE,
                ],
                callback_urls=[
                    f"https://app.{domain_name}/callback",
                    "http://localhost:3000/callback",
                    "http://localhost:5173/callback",
                ],
                logout_urls=[
                    f"https://app.{domain_name}",
                    "http://localhost:3000",
                    "http://localhost:5173",
                ],
            ),
            supported_identity_providers=[
                cognito.UserPoolClientIdentityProvider.COGNITO,
            ],
            access_token_validity=Duration.hours(1),
            id_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            prevent_user_existence_errors=True,
        )

        # Outputs
        CfnOutput(self, "UserPoolId", value=self.user_pool.user_pool_id)
        CfnOutput(self, "UserPoolArn", value=self.user_pool.user_pool_arn)
        CfnOutput(self, "AppClientId", value=self.app_client.user_pool_client_id)
        CfnOutput(self, "UserPoolDomainUrl",
                  value=f"https://{self.user_pool_domain.domain_name}.auth.{self.region}.amazoncognito.com")
