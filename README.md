# StudyPulse

> An autonomous AI study agent that remembers a student's learning context, generates a personalized study plan, and delivers it automatically every day.

## Overview

StudyPulse is a serverless AI study agent built with Amazon Bedrock and AWS services.

Instead of requiring a student to open an AI chatbot every day and ask what they should study, StudyPulse runs automatically on a schedule. It retrieves the student's stored learning context from DynamoDB, uses Amazon Nova Micro to determine an appropriate study focus, saves the generated plan, and delivers it through Amazon SES.

The goal is simple:

**Remember → Reason → Plan → Deliver → Repeat**

## Why StudyPulse?

Students often know what they need to learn but struggle with deciding what to focus on next.

StudyPulse turns that decision into an automated workflow.

A student's profile can contain:

* Subjects
* Upcoming exam
* Weak topics
* Available study time
* Previous study plan

The agent uses this context when generating the next study plan.

## Architecture

```text
                EventBridge Scheduler
                       │
                       │ scheduled trigger
                       ▼
                 AWS Lambda
                StudyPulse Agent
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
          DynamoDB          Amazon Bedrock
           Memory           Amazon Nova Micro
              │                 │
              └────────┬────────┘
                       ▼
                 Study Plan
                       │
                       ▼
                  Amazon SES
                       │
                       ▼
                    Student
```

## AWS Services

| Service                      | Purpose                                  |
| ---------------------------- | ---------------------------------------- |
| Amazon EventBridge Scheduler | Automatically triggers the agent         |
| AWS Lambda                   | Runs the StudyPulse workflow             |
| Amazon Bedrock               | Provides generative AI reasoning         |
| Amazon Nova Micro            | Generates the personalized study plan    |
| Amazon DynamoDB              | Stores student memory and previous plans |
| Amazon SES                   | Delivers the generated plan by email     |
| AWS IAM                      | Controls service permissions             |

## Agent Workflow

1. EventBridge Scheduler triggers the Lambda function.
2. Lambda retrieves the student's memory from DynamoDB.
3. Lambda constructs a context-aware prompt.
4. Amazon Nova Micro analyzes the context.
5. Nova Micro generates today's study recommendation.
6. Lambda saves the generated plan back to DynamoDB.
7. Amazon SES sends the study plan to the student.
8. The process repeats automatically on the next scheduled run.

## Example Output

```text
TODAY'S PRIORITY:
Networking

WHY:
Networking remains a weak topic and is important for the student's upcoming exam.

STUDY PLAN:
1. Review advanced networking concepts.
2. Study VPC security best practices.
3. Complete a short networking quiz.

CHALLENGE:
Explain how to configure a VPC containing both public and private subnets.
```

## What I Learned

Building StudyPulse gave me hands-on experience with serverless AWS architecture, Amazon Bedrock inference, DynamoDB-based application memory, EventBridge scheduling, Amazon SES, and IAM permissions.

One of the most useful lessons was that integrating several managed AWS services requires understanding how permissions, regions, and service-specific configurations interact.

I also learned that an AI agent is not simply a model generating text. The useful part comes from connecting the model to memory, triggers, and actions so that it can participate in an automated workflow.

## Challenges

During development, I initially attempted to invoke Nova Micro directly using its base model identifier. The request failed because on-demand invocation was not supported for the selected regional setup. I investigated the error and switched to the appropriate APAC inference profile.

I also encountered an IAM permission error when Lambda attempted to save the generated plan to DynamoDB. The Lambda execution role initially had read access but not the required `dynamodb:UpdateItem` permission. Updating the role resolved the problem.

These issues helped me understand the importance of AWS regional availability, inference profiles, and IAM permissions when building serverless AI applications.

## Future Improvements

Future versions could allow students to provide feedback on each study plan, track completed topics, adapt difficulty based on performance, and support multiple students.

A future dashboard could also visualize learning progress and upcoming exams.

## Project Status

StudyPulse is deployed using AWS services and runs as an automated serverless workflow.

Built for the **AWS Weekend Creative Agent Challenge — Dear Tomorrow**.
