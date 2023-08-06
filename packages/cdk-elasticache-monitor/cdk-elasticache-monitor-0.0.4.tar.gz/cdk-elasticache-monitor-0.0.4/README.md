# Welcome to `cdk-elasticache-monitor`

ElasticacheAutoMonitor allows you to send email, sms, slack, or trigger aws lambda when an alarm occurs.
You will get the following monitoring:

* Cpu Monitor: Should be less than 90%. (See below reference)
* SwapUsage Monitor: Should be less than 50M.
* Evictions Monitor: Should not have evictions value.
* CurrConnections Monitor: According to your business needs, default every 1 vcup is equal to 200 connections.
* FreeableMemory Monitor: Not less than 10%

Reference: https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/CacheMetrics.WhichShouldIMonitor.html

## Usage

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stack = cdk.Stack()

# sent with email
ElasticacheAutoMonitor.set_up_with_email(stack, "my-elasticache-id",
    emails=["jiale.chan@gmail.com"],
    node_type_class=NodeType.R4_16XLARGE
)

# or sent with sms
ElasticacheAutoMonitor.set_up_with_sms(stack, "my-elasticache-id",
    phones=["+15533728278"],
    node_type_class=NodeType.R4_16XLARGE
)

# or sent with slack
ElasticacheAutoMonitor.set_up_with_slack(stack, "my-elasticache-id",
    web_hook_url="http://xxx.xxx.xxx",
    node_type_class=NodeType.R4_16XLARGE
)

# or trigger lambda
fn = lambda.Function(stack, "MyFunction",
    runtime=lambda.Runtime.NODEJS_10_X,
    handler="index.handler",
    code=lambda.Code.from_inline("exports.handler = function(event, ctx, cb) { return cb(null, \"hi\"); }")
)
ElasticacheAutoMonitor.set_up_with_lambda(stack, "my-elasticache-id", fn,
    node_type_class=NodeType.R4_16XLARGE
)
```
