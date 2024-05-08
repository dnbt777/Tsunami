import base64
import os
import json
import logging
from .logger import log
from Tsunami.Metrics.CostTracker import CostTracker

import boto3
from botocore.exceptions import ClientError

class ModelInterface():
    def __init__(self, client=None, cost_tracker=None):
        if client:
            self.client = client
        else:
            # Make a client
            self.client = boto3.client(
                service_name="bedrock-runtime",
                region_name=os.environ.get("AWS_REGION"),
                aws_access_key_id=os.environ.get("ACCESS_KEY"),
                aws_secret_access_key=os.environ.get("SECRET_KEY"),
                aws_session_token=os.environ.get("SESSION_TOKEN"),
            )
            self.model_interface = ModelInterface(self.client)
        
        if cost_tracker:
            self.cost_tracker = cost_tracker
        else:
            self.cost_tracker = CostTracker()

    
    def invoke_claude_3_with_text(self, prompt, model="sonnet", max_tokens=1000):
        """
        Invokes Anthropic Claude 3 Sonnet to run an inference using the input
        provided in the request body.

        :param prompt: The prompt that you want Claude 3 to complete.
        :return: Inference response from the model.
        """

        # Initialize the Amazon Bedrock runtime client
        client = self.client or boto3.client(
            service_name="bedrock-runtime", region_name="us-west-2"
        )

        # Invoke Claude 3 with the text prompt
        model_id = {
            "haiku"     : "anthropic.claude-3-haiku-20240307-v1:0",
            "sonnet"    : "anthropic.claude-3-sonnet-20240229-v1:0",
            "opus"      : "anthropic.claude-3-opus-20240229-v1:0",
        }[model]

        try:
            response = client.invoke_model(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": max_tokens,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )

            # Process and print the response
            result = json.loads(response.get("body").read())
            result_text = result["content"][0]["text"]
            
            input_tokens = result["usage"]["input_tokens"]
            output_tokens = result["usage"]["output_tokens"]

            metrics = {
                "inputTokenCount" : input_tokens,
                "outputTokenCount": output_tokens
            } # Same keys as AZ metrics for compat w other methods/functions that take metrics as an input

            return result_text, metrics

        except ClientError as err:
            log(
                "Couldn't invoke Claude 3. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise


    def invoke_claude_3_with_stream(self, prompt, model="sonnet", max_tokens=1000):
        """
        Invokes Anthropic Claude 3 Sonnet to run an inference using the input
        provided in the request body.

        :param prompt: The prompt that you want Claude 3 to complete.
        :return: Inference response from the model.
        """

        # Initialize the Amazon Bedrock runtime client
        client = self.client or boto3.client(
            service_name="bedrock-runtime", region_name="us-west-2"
        )

        # Invoke Claude 3 with the text prompt
        model_id = {
            "haiku"     : "anthropic.claude-3-haiku-20240307-v1:0",
            "sonnet"    : "anthropic.claude-3-sonnet-20240229-v1:0",
            "opus"      : "anthropic.claude-3-opus-20240229-v1:0",
        }[model]

        try:
            response_stream = client.invoke_model_with_response_stream(
                modelId=model_id,
                body=json.dumps(
                    {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": max_tokens,
                        "messages": [
                            {
                                "role": "user",
                                "content": [{"type": "text", "text": prompt}],
                            }
                        ],
                    }
                ),
            )

            result_text = ""
            metrics = {}
            #print(response_stream)
            for event in response_stream["body"]:
                chunk = json.loads(event["chunk"]["bytes"])
                if chunk["type"] == "content_block_start":
                    print(chunk["content_block"]["text"], end="")
                    result_text += chunk["content_block"]["text"]
                if chunk["type"] == "content_block_delta":
                    print(chunk["delta"]["text"], end="")
                    result_text += chunk["delta"]["text"]
                if chunk["type"] == "content_block_stop":
                    continue
                if chunk["type"] == "message_delta":
                    continue
                if chunk["type"] == "message_stop":
                    metrics = chunk["amazon-bedrock-invocationMetrics"] # TODO add cost in here
                    continue
            
            metrics.update({
                "model" : model,
            })

            # input_tokens = result["usage"]["input_tokens"]
            # output_tokens = result["usage"]["output_tokens"]
            # output_list = result.get("content", [])

            # print("Invocation details:")
            # print(f"- The input length is {input_tokens} tokens.")
            # print(f"- The output length is {output_tokens} tokens.")

            # print(f"- The model returned {len(output_list)} response(s):")
            # for output in output_list:
            #     print(output["text"])

            return result_text, metrics

        except ClientError as err:
            log(
                "Couldn't invoke Claude 3. Here's why: %s: %s",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
    


    def send_to_ai(self, prompt, model, max_tokens=1000, stream=True):
        log(f"Sending to {model}")
        log("SENDING PROMPT, LENGTH =", len(prompt))
        log("Estimated tokens:", len(prompt)//5)
        
        if stream == False:
            result_text, metrics = self.model_interface.invoke_claude_3_with_text(prompt, model=model, max_tokens=max_tokens)
        else:
            result_text, metrics = self.model_interface.invoke_claude_3_with_stream(prompt, model=model, max_tokens=max_tokens)
        
        # Update cost data
        self.cost_tracker.add_request_metrics_to_cost_data(metrics)
        self.cost_tracker.show_cost_data()
        print('\n\n\n')

        return result_text, metrics