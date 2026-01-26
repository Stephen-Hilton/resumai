"""
CloudFront Stack for Skillsnap

Creates CloudFront distributions for:
- skillsnap.me (landing page)
- app.skillsnap.me (webapp)
- *.skillsnap.me (custom resume URLs)

Also includes CloudFront Function for URL rewriting.

Requirements: 2.1, 3.1, 11.1, 11.2, 11.3, 11.4, 17.5
"""
from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
)
from constructs import Construct
from .s3_stack import S3Stack


# CloudFront Function code for URL rewriting
CLOUDFRONT_FUNCTION_CODE = """
function handler(event) {
  var request = event.request;
  var headers = request.headers;
  var host = headers.host && headers.host.value ? headers.host.value : "";
  host = host.split(":")[0].toLowerCase();

  var username = "www";
  var parts = host.split(".");
  if (parts.length >= 3) username = parts[0];

  var uri = request.uri || "/";
  if (uri === "") uri = "/";

  // Global assets: DO NOT rewrite
  if (
    uri.indexOf("/assets/") === 0 ||
    uri.indexOf("/_global/") === 0 ||
    uri === "/favicon.ico" ||
    uri === "/robots.txt" ||
    uri === "/sitemap.xml"
  ) {
    return request;
  }

  // User root -> user homepage
  if (uri === "/") {
    request.uri = "/" + username + "/index.html";
    return request;
  }

  // Normalize trailing slash
  if (uri.length > 1 && uri.charAt(uri.length - 1) === "/") {
    uri = uri.slice(0, -1);
  }

  var segs = uri.split("/").filter(Boolean);

  // "/company/job" -> "/username/company/job/index.html"
  if (segs.length === 2) {
    request.uri = "/" + username + "/" + segs[0] + "/" + segs[1] + "/index.html";
    return request;
  }

  // Anything deeper: prefix username
  request.uri = "/" + username + uri;
  return request;
}
"""


class CloudFrontStack(Stack):
    """Stack containing CloudFront distributions for Skillsnap."""

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        s3_stack: S3Stack,
        domain_name: str = "skillsnap.me",
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.domain_name = domain_name

        # Look up the hosted zone for the domain
        self.hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=domain_name,
        )

        # Create certificate in us-east-1 (required for CloudFront)
        # DnsValidatedCertificate handles cross-region certificate creation
        self.certificate = acm.DnsValidatedCertificate(
            self, "Certificate",
            domain_name=domain_name,
            subject_alternative_names=[f"*.{domain_name}"],
            hosted_zone=self.hosted_zone,
            region="us-east-1",  # CloudFront requires us-east-1
        )

        # Create Origin Access Identity for S3 access
        self.landing_oai = cloudfront.OriginAccessIdentity(
            self, "LandingOAI",
            comment="OAI for Skillsnap Landing Page"
        )

        self.webapp_oai = cloudfront.OriginAccessIdentity(
            self, "WebAppOAI",
            comment="OAI for Skillsnap WebApp"
        )

        self.resumes_oai = cloudfront.OriginAccessIdentity(
            self, "ResumesOAI",
            comment="OAI for Skillsnap Public Resumes"
        )

        # CloudFront Function for URL rewriting (resumes distribution)
        self.url_rewriter_function = cloudfront.Function(
            self, "UrlRewriterFunction",
            function_name="skillsnap-url-rewriter",
            code=cloudfront.FunctionCode.from_inline(CLOUDFRONT_FUNCTION_CODE),
            comment="Rewrites URLs for custom resume subdomains",
        )

        # Landing page distribution - skillsnap.me
        self.landing_distribution = cloudfront.Distribution(
            self, "LandingDistribution",
            comment="Skillsnap Landing Page",
            domain_names=[domain_name],
            certificate=self.certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_identity(
                    s3_stack.landing_bucket,
                    origin_access_identity=self.landing_oai,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
            ),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
            ],
        )

        # WebApp distribution - app.skillsnap.me
        self.webapp_distribution = cloudfront.Distribution(
            self, "WebAppDistribution",
            comment="Skillsnap WebApp",
            domain_names=[f"app.{domain_name}"],
            certificate=self.certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_identity(
                    s3_stack.webapp_bucket,
                    origin_access_identity=self.webapp_oai,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
            ),
            default_root_object="index.html",
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                    ttl=Duration.seconds(0),
                ),
            ],
        )

        # Resumes distribution - *.skillsnap.me with URL rewriting
        self.resumes_distribution = cloudfront.Distribution(
            self, "ResumesDistribution",
            comment="Skillsnap Public Resumes",
            domain_names=[f"*.{domain_name}"],
            certificate=self.certificate,
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_identity(
                    s3_stack.resumes_bucket,
                    origin_access_identity=self.resumes_oai,
                ),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD,
                function_associations=[
                    cloudfront.FunctionAssociation(
                        function=self.url_rewriter_function,
                        event_type=cloudfront.FunctionEventType.VIEWER_REQUEST,
                    )
                ],
            ),
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=404,
                    response_page_path="/404.html",
                    ttl=Duration.seconds(60),
                ),
            ],
        )

        # Route 53 DNS records
        # Landing page - skillsnap.me -> landing distribution
        route53.ARecord(
            self, "LandingARecord",
            zone=self.hosted_zone,
            record_name=domain_name,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.landing_distribution)
            ),
        )

        # WebApp - app.skillsnap.me -> webapp distribution
        route53.ARecord(
            self, "WebAppARecord",
            zone=self.hosted_zone,
            record_name=f"app.{domain_name}",
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.webapp_distribution)
            ),
        )

        # Wildcard for resumes - *.skillsnap.me -> resumes distribution
        route53.ARecord(
            self, "ResumesWildcardARecord",
            zone=self.hosted_zone,
            record_name=f"*.{domain_name}",
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.resumes_distribution)
            ),
        )

        # Outputs
        CfnOutput(self, "LandingDistributionDomain",
                  value=self.landing_distribution.distribution_domain_name)
        CfnOutput(self, "WebAppDistributionDomain",
                  value=self.webapp_distribution.distribution_domain_name)
        CfnOutput(self, "ResumesDistributionDomain",
                  value=self.resumes_distribution.distribution_domain_name)
        CfnOutput(self, "LandingDistributionId",
                  value=self.landing_distribution.distribution_id)
        CfnOutput(self, "WebAppDistributionId",
                  value=self.webapp_distribution.distribution_id)
        CfnOutput(self, "ResumesDistributionId",
                  value=self.resumes_distribution.distribution_id)
        CfnOutput(self, "LandingUrl",
                  value=f"https://{domain_name}")
        CfnOutput(self, "WebAppUrl",
                  value=f"https://app.{domain_name}")
