# 🧠 StudyPulse

### An Autonomous AI Study Agent That Remembers, Adapts & Acts

> **StudyPulse** is a serverless AI study companion that uses persistent student memory and generative AI to create personalized study plans based on what you want to study, how much time you have, your difficulty level, and your learning history.

**Built with AWS · Amazon Bedrock · Amazon Nova Micro · AWS Lambda · DynamoDB · API Gateway · Amazon SES · Amazon S3 · EventBridge Scheduler**

---

## 🌐 Live Demo

🚀 **Try StudyPulse:**
http://studypulse-showcase-disha-2026.s3-website.ap-south-1.amazonaws.com/#live

The live application lets you provide your current study context and request a fresh personalized plan from the StudyPulse agent.

---

## ✨ Why StudyPulse?

Planning what to study can sometimes take almost as much effort as studying itself.

Traditional planners usually follow a fixed schedule, while generic AI assistants often forget previous context.

**StudyPulse takes a different approach.**

It combines:

* 🧠 Persistent learning memory
* 🤖 Generative AI
* ⏱️ Available study time
* 🎯 Current learning goals
* 📚 Weak topics
* 🔄 Previous study plans
* ⚡ Serverless AWS infrastructure
* 📧 Proactive email delivery

The goal is simple:

> **Less time planning. More time learning.**

---

# 🚀 Features

### 🎯 Personalized Study Plans

StudyPulse generates a focused plan based on the student's current context rather than returning a generic study routine.

### 🧠 Persistent Memory

Student information and previous plans are stored in **Amazon DynamoDB**, allowing future agent runs to use historical context.

### 🤖 AI-Powered Planning

**Amazon Nova Micro through Amazon Bedrock** analyzes the student's context and generates a structured study plan.

### 🔄 Adaptive Planning

The agent receives information about previous activity and is instructed to avoid simply repeating the exact same plan.

### ⏱️ Time-Aware Recommendations

The student can specify how much time they have available, allowing the generated plan to remain realistic.

### 🧩 Interactive Input

The showcase version allows the learner to provide:

* What they want to study
* Available study time
* Difficulty level
* Current goal

### 📧 Proactive Delivery

Generated plans can also be delivered through **Amazon SES**, allowing StudyPulse to reach the learner through email.

### ⚡ Serverless Architecture

The backend runs using AWS managed/serverless services, eliminating the need to maintain a traditional application server.

---

# 🏗️ Architecture

```text
                     ┌──────────────────────┐
                     │      Student         │
                     │                      │
                     │ Topic / Time / Goal  │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    Amazon S3         │
                     │   Static Web App     │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │    API Gateway       │
                     │    HTTP Endpoint    │
                     └──────────┬───────────┘
                                │
                                ▼
                     ┌──────────────────────┐
                     │     AWS Lambda       │
                     │ Agent Orchestrator   │
                     └──────┬───────┬───────┘
                            │       │
              ┌─────────────┘       └──────────────┐
              ▼                                    ▼
     ┌──────────────────┐                 ┌──────────────────┐
     │   DynamoDB       │                 │ Amazon Bedrock   │
     │                  │                 │                  │
     │ Student Memory   │◄───────────────►│   Nova Micro     │
     │ Previous Plans   │                 │                  │
     └──────────────────┘                 └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌──────────────────┐
                                          │   Amazon SES     │
                                          │                  │
                                          │ Email Delivery   │
                                          └──────────────────┘

                    ┌──────────────────────────────┐
                    │ EventBridge Scheduler        │
                    │                              │
                    │ Scheduled Agent Execution    │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                              AWS Lambda
```

---

# ☁️ AWS Services

| AWS Service                      | Purpose                                |
| -------------------------------- | -------------------------------------- |
| **Amazon S3**                    | Hosts the StudyPulse frontend          |
| **Amazon API Gateway**           | Provides the backend HTTP API          |
| **AWS Lambda**                   | Runs the StudyPulse agent workflow     |
| **Amazon DynamoDB**              | Stores persistent student memory       |
| **Amazon Bedrock**               | Provides access to generative AI       |
| **Amazon Nova Micro**            | Generates personalized study plans     |
| **Amazon SES**                   | Delivers study plans through email     |
| **Amazon EventBridge Scheduler** | Enables scheduled autonomous execution |
| **AWS IAM**                      | Controls access between AWS services   |

---

# 🧠 How the Agent Works

StudyPulse follows a simple agent workflow.

### 1. Student provides context

The learner tells StudyPulse what they want to study and provides information such as available time, difficulty, and goal.

### 2. Lambda receives the request

API Gateway forwards the request to the AWS Lambda backend.

### 3. StudyPulse retrieves memory

Lambda retrieves the student's stored information from DynamoDB.

This can include:

```text
Student
Subjects
Upcoming exam
Weak topics
Available study time
Last completed topic
Previous study plan
```

### 4. The agent builds its context

The current request and stored memory are combined into a structured prompt.

### 5. Amazon Nova Micro generates the plan

The prompt is sent to Amazon Nova Micro through Amazon Bedrock.

The model generates:

```text
TODAY'S PRIORITY

WHY

STUDY PLAN

1. Task
2. Task
3. Task

CHALLENGE
```

### 6. Memory is updated

The newly generated plan is stored in DynamoDB.

This means the next agent run doesn't have to start from scratch.

### 7. The result is delivered

The plan is returned to the web application and can also be delivered through Amazon SES.

---

# 🔐 Example Student Memory

A simplified DynamoDB record can look like:

```json
{
  "studentId": "student-001",
  "name": "Student",
  "subjects": "Cybersecurity, Cloud Computing",
  "exam": "Cloud Security Assessment",
  "weakTopics": "IAM and networking",
  "studyMinutes": 60,
  "lastCompleted": "IAM fundamentals",
  "lastPlan": "Review IAM policies and solve practice questions"
}
```

This memory becomes part of the agent's decision-making context.

---

# 🧪 Example Output

A StudyPulse response might look like:

```text
TODAY'S PRIORITY:
AWS IAM Policy Evaluation

WHY:
IAM is currently one of your weaker areas and builds directly
on the topic you completed previously.

STUDY PLAN:
1. Review IAM policy structure for 15 minutes.
2. Work through 3 policy evaluation examples for 25 minutes.
3. Complete a short self-test for 10 minutes.

CHALLENGE:
Why can an explicit Deny override an Allow in an IAM policy?
```

The important part is that the recommendation is based on **context**, rather than being a completely random study list.

---

# 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Responsive UI
* Fetch API

### Backend

* Python
* AWS Lambda
* API Gateway

### AI

* Amazon Bedrock
* Amazon Nova Micro

### Data & Automation

* Amazon DynamoDB
* Amazon SES
* Amazon EventBridge Scheduler
* AWS IAM
* Amazon S3

---

# 💥 Challenges & What I Learned

Building StudyPulse wasn't a straight line.

Several things broke before the complete workflow worked.

## 1. Amazon Bedrock Model Invocation

The initial Bedrock implementation produced errors related to model invocation and inference profiles.

I encountered errors such as:

```text
ValidationException:
The provided model identifier is invalid.
```

The issue required understanding how Amazon Bedrock handles regional inference profiles and model identifiers.

The solution was to use the appropriate Amazon Nova Micro inference profile for the region.

---

## 2. DynamoDB Permissions

The Lambda function successfully generated the study plan, but failed when attempting to save the result.

The error was:

```text
AccessDeniedException
when calling the UpdateItem operation
```

The problem was not the database itself.

The Lambda execution role simply didn't have the required DynamoDB permission.

Updating the IAM policy resolved the issue.

This was an important lesson:

> **An AI application is only as reliable as the infrastructure surrounding the model.**

---

## 3. Frontend → API Integration

Another challenge was connecting the static frontend hosted on S3 with the API Gateway endpoint.

The application needed to correctly send the user's input through the API and handle the Lambda response.

This required testing the endpoint independently before connecting the final frontend experience.

---

## 4. Making the Agent Context-Aware

A simple implementation could generate the same type of plan repeatedly.

To improve this, StudyPulse stores the previous plan and learning context in DynamoDB and provides that information to the model.

The prompt explicitly instructs the agent to consider previous activity and avoid repeating the exact same plan.

This transforms the application from a simple AI generator into a more context-aware system.

---

# 📈 What Makes StudyPulse Different?

A traditional study planner might say:

> Study Chapter 3.

A generic AI assistant might say:

> Here are five things you could study today.

StudyPulse aims to answer a more useful question:

> **Given what I know about this learner, what should they do next?**

That distinction is the foundation of the project.

The long-term vision is to evolve StudyPulse into an increasingly personalized learning agent that can track progress, identify knowledge gaps, adapt recommendations, and proactively support learners.

---

# 🔮 Future Improvements

StudyPulse is still a work in progress.

Potential future improvements include:

* 📊 Progress dashboards
* 🧠 More detailed learner profiles
* 📈 Learning analytics
* 📝 Automatic quiz generation
* 🔁 Feedback-based plan adaptation
* 🏆 Streaks and achievement tracking
* 📅 Calendar integration
* 💬 Conversational study assistant
* 🎯 Automatic weak-topic detection
* 📚 Integration with learning resources
* 🔐 Stronger authentication and per-user data isolation

The ultimate goal is to move from:

**AI-generated study plans**

to:

**an AI agent that continuously understands and supports a learner's progress.**

---

# 🚀 Running the Project

## Frontend

The frontend consists of static HTML, CSS, and JavaScript files and can be hosted using Amazon S3 static website hosting.

Update the API endpoint in the frontend JavaScript:

```javascript
const API_URL =
    "YOUR_API_GATEWAY_ENDPOINT";
```

Then deploy the frontend files to your S3 bucket.

---

## Backend

The Lambda function requires access to:

* DynamoDB
* Amazon Bedrock
* Amazon SES

The Lambda execution role should have the appropriate least-privilege permissions for these services.

Configure the required environment/configuration values before deployment.

---

# ⚠️ Security Notes

This repository is intended as a showcase project.

Do **not** commit:

* AWS access keys
* Secret keys
* API credentials
* `.env` files containing secrets
* SES credentials
* Private student information

Use AWS IAM roles and appropriate secret-management mechanisms instead of hardcoding credentials.

---

# 🏆 Built for the AWS Summer Builds Showcase

StudyPulse was created and refined as part of the **AWS Summer Builds Showcase Weekend Challenge**.

The project represents the evolution of an earlier creative AI idea into a more complete autonomous application using persistent memory, generative AI, serverless infrastructure, and automated delivery.

---

# 👩‍💻 Author

**Disha Pure**

B.Tech Computer Science & IT — Cybersecurity

AWS Student Builder · Cloud & Cybersecurity Enthusiast

---

## ⭐ If you like StudyPulse

Give the repository a ⭐ and try the live application.

If you have an idea for what an AI study agent should remember about a learner, feel free to open an issue or start a discussion.

---

### Built with ☁️ AWS

**Amazon Bedrock · Amazon Nova Micro · AWS Lambda · Amazon DynamoDB · Amazon API Gateway · Amazon S3 · Amazon SES · Amazon EventBridge Scheduler**
