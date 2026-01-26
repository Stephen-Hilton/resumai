"""
SQS Stack for Skillsnap

Creates SQS queues for asynchronous processing:
- Generation queue for subcomponent tasks
- Dead letter queue for failed messages

Requirements: 16.1, 16.5
"""
from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_sqs as sqs,
)
from constructs import Construct


class SQSStack(Stack):
    """Stack containing SQS queues for Skillsnap."""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Dead Letter Queue for failed generation messages
        self.generation_dlq = sqs.Queue(
            self, "GenerationDLQ",
            queue_name="skillsnap-generation-dlq",
            retention_period=Duration.days(14),
            visibility_timeout=Duration.seconds(300),
        )

        # Main Generation Queue for subcomponent tasks
        self.generation_queue = sqs.Queue(
            self, "GenerationQueue",
            queue_name="skillsnap-generation-queue",
            visibility_timeout=Duration.seconds(300),  # 5 minutes for Lambda processing
            retention_period=Duration.days(4),
            receive_message_wait_time=Duration.seconds(20),  # Long polling
            dead_letter_queue=sqs.DeadLetterQueue(
                queue=self.generation_dlq,
                max_receive_count=3,  # Retry 3 times before DLQ
            ),
        )

        # Outputs
        CfnOutput(self, "GenerationQueueUrl", value=self.generation_queue.queue_url)
        CfnOutput(self, "GenerationQueueArn", value=self.generation_queue.queue_arn)
        CfnOutput(self, "GenerationDLQUrl", value=self.generation_dlq.queue_url)
        CfnOutput(self, "GenerationDLQArn", value=self.generation_dlq.queue_arn)
