
[![Docker Pulls](https://img.shields.io/docker/pulls/artursmet/docker-route53-discovery.svg)](https://hub.docker.com/r/artursmet/docker-route53-discovery/)

## Simple service discovery for docker-based environment

### Problem to solve
Let's imagine an ECS cluster that hosts web application and a database.
In pure ECS setup, those two separate services don't know anything about eachother. So app container requires static db address in configuration.

### Solution
This package runs as a short living sidecar container, after core service is started - this container checks local ip address of underlying EC2 instance (using EC2 metadata endpoint) and updates selected Route53 record with correct ip address.


### Example

Example ECS task definition that starts redis with a service discovery

```json
{
    "executionRoleArn": null,
    "containerDefinitions": [
        {
            "dnsSearchDomains": null,
            "logConfiguration": null,
            "entryPoint": null,
            "portMappings": [
                {
                    "hostPort": 6379,
                    "protocol": "tcp",
                    "containerPort": 6379
                }
            ],
            "name": "redis"
        },
        {
            "name": "service-discovery",
            "image": "artursmet/docker-route53-discovery:latest",
            "memory": "64",
            "essential": false,
            "portMappings": [],
            "environment": [
                {
                    "name": "DNS_ZONE_ID",
                    "value": "your-zone-id"
                },
                {
                    "name": "DNS_RECORD_NAME",
                    "value": "my-redis.somewhere.internal"
                }
            ]
        }
    ],
    "memory": "128",
    "taskRoleArn": null,
    "family": "redis",
    "requiresCompatibilities": null,
    "networkMode": "bridge",
    "cpu": null,
    "volumes": [],
    "placementConstraints": []
}
```

After service is started, redis container should run and service discovery container should end after updating proper DNS records.
Selected domain entry will point to **local ip address** of EC2 instance where this service was started.


### Requirements
This container requires `Route53:ChangeResourceRecordSets` IAM permission to be available through ECS instance role.

Example IAM policy:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AllowUpdateInternalDNS",
            "Effect": "Allow",
            "Action": "route53:ChangeResourceRecordSets",
            "Resource": "arn:aws:route53:::hostedzone/YOURZONEID"
        }
    ]
}
```
