import json
import boto3

# ============================================================
# AWS CLIENTS
# ============================================================

dynamodb = boto3.resource(
    "dynamodb",
    region_name="ap-south-1"
)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="ap-south-1"
)

ses = boto3.client(
    "ses",
    region_name="ap-south-1"
)

# ============================================================
# CONFIGURATION
# ============================================================

TABLE_NAME = "StudyPulseMemory"

MODEL_ID = "apac.amazon.nova-micro-v1:0"

EMAIL_ADDRESS = "disha.boston@gmail.com"

table = dynamodb.Table(TABLE_NAME)


# ============================================================
# CORS RESPONSE
# ============================================================

def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Methods": "POST,OPTIONS"
        },
        "body": json.dumps(body)
    }


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print("========================================")
    print("StudyPulse agent started.")
    print("========================================")

    # --------------------------------------------------------
    # 0. HANDLE OPTIONS / PREFLIGHT
    # --------------------------------------------------------

    if event.get("requestContext", {}).get("http", {}).get("method") == "OPTIONS":
        return response(200, {"message": "CORS OK"})

    # --------------------------------------------------------
    # 1. READ HUMAN INPUT
    # --------------------------------------------------------

    human_input = {}

    try:

        raw_body = event.get("body")

        if raw_body:

            if isinstance(raw_body, str):
                human_input = json.loads(raw_body)
            else:
                human_input = raw_body

    except Exception as e:

        print("Could not parse request body:", str(e))

    topic = human_input.get("topic", "").strip()
    time_available = human_input.get("time", "").strip()
    difficulty = human_input.get("difficulty", "").strip()
    goal = human_input.get("goal", "").strip()

    print("Human input:")
    print("Topic:", topic)
    print("Time:", time_available)
    print("Difficulty:", difficulty)
    print("Goal:", goal)

    # --------------------------------------------------------
    # 2. READ STUDENT MEMORY
    # --------------------------------------------------------

    response_data = table.get_item(
        Key={
            "studentId": "disha"
        }
    )

    student = response_data.get("Item")

    if not student:

        print("ERROR: Student memory not found.")

        return response(
            404,
            {
                "error": "Student memory not found"
            }
        )

    print("Student memory loaded successfully.")

    # --------------------------------------------------------
    # 3. GET STORED MEMORY
    # --------------------------------------------------------

    name = student.get(
        "name",
        "Student"
    )

    subjects = student.get(
        "subjects",
        "Not specified"
    )

    exam = student.get(
        "exam",
        "Not specified"
    )

    weak_topics = student.get(
        "weakTopics",
        "Not specified"
    )

    study_minutes = student.get(
        "studyMinutes",
        45
    )

    last_completed = student.get(
        "lastCompleted",
        "None"
    )

    previous_plan = student.get(
        "lastPlan",
        "None"
    )

    # --------------------------------------------------------
    # 4. BUILD HUMAN-CONTEXT SECTION
    # --------------------------------------------------------

    if topic or goal or time_available or difficulty:

        human_context = f"""
CURRENT STUDENT REQUEST
-----------------------

Topic / subject requested:
{topic if topic else "No specific topic — choose based on memory"}

Goal:
{goal if goal else "No specific goal provided"}

Available time:
{time_available if time_available else str(study_minutes) + " minutes"}

Difficulty:
{difficulty if difficulty else "Use the student's stored level/context"}
"""

    else:

        human_context = """
CURRENT STUDENT REQUEST
-----------------------

No manual request was provided.

Act autonomously using the student's stored memory.
"""

    # --------------------------------------------------------
    # 5. CREATE AI PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are StudyPulse, an autonomous AI study planning agent.

Your job is to create a personalized study plan by combining:

1. The student's persistent learning memory.
2. The student's current request, if one was provided.

IMPORTANT:
The current request should influence today's plan,
but persistent memory should still be considered.

Do not ignore the student's weaknesses, upcoming exam,
previous progress, or previous plan.

STUDENT MEMORY
--------------

Name:
{name}

Subjects:
{subjects}

Upcoming exam:
{exam}

Weak topics:
{weak_topics}

Stored available study time:
{study_minutes} minutes

Last completed topic:
{last_completed}

PREVIOUS STUDY PLAN
-------------------

{previous_plan}

{human_context}

YOUR TASK
---------

Reason about the student's situation and create a fresh,
practical study plan.

If the student provided a topic, prioritize that topic.

If the student provided a goal, design the plan around that goal.

If the student provided a time limit, keep the plan realistic
for that amount of time.

If no manual request was provided, act autonomously using
persistent memory.

Avoid repeating the exact same plan.

Connect today's plan to previous progress when appropriate.

Do not invent personal information.

Return the result in exactly this format:

TODAY'S PRIORITY:
<one topic>

WHY:
<one or two short sentences explaining the choice>

STUDY PLAN:
1. <task>
2. <task>
3. <task>

CHALLENGE:
<one useful question or practical challenge>

Keep the response concise and practical.
"""

    print("Sending request to Amazon Nova Micro.")

    # --------------------------------------------------------
    # 6. INVOKE BEDROCK
    # --------------------------------------------------------

    bedrock_response = bedrock.converse(

        modelId=MODEL_ID,

        messages=[
            {
                "role": "user",

                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],

        inferenceConfig={
            "maxTokens": 300,
            "temperature": 0.6
        }
    )

    # --------------------------------------------------------
    # 7. EXTRACT AI RESPONSE
    # --------------------------------------------------------

    study_plan = (
        bedrock_response
        ["output"]
        ["message"]
        ["content"][0]
        ["text"]
    )

    print("Study plan generated successfully.")
    print("----------------------------------------")
    print(study_plan)
    print("----------------------------------------")

    # --------------------------------------------------------
    # 8. SAVE PLAN TO DYNAMODB
    # --------------------------------------------------------

    table.update_item(

        Key={
            "studentId": "disha"
        },

        UpdateExpression="""
            SET lastPlan = :plan
        """,

        ExpressionAttributeValues={
            ":plan": study_plan
        }
    )

    print("Study plan saved to DynamoDB.")

    # --------------------------------------------------------
    # 9. CREATE EMAIL
    # --------------------------------------------------------

    email_subject = "Your StudyPulse Plan for Today"

    email_body = f"""
Hi {name},

Your StudyPulse personalized study plan is ready.

========================================

{study_plan}

========================================

StudyPulse combined your stored learning context
with your latest request to create this plan.

Keep the momentum going.

— StudyPulse AI
"""

    # --------------------------------------------------------
    # 10. SEND EMAIL
    # --------------------------------------------------------

    print("Sending study plan through Amazon SES...")

    ses_response = ses.send_email(

        Source=EMAIL_ADDRESS,

        Destination={
            "ToAddresses": [
                EMAIL_ADDRESS
            ]
        },

        Message={

            "Subject": {
                "Data": email_subject,
                "Charset": "UTF-8"
            },

            "Body": {
                "Text": {
                    "Data": email_body,
                    "Charset": "UTF-8"
                }
            }
        }
    )

    message_id = ses_response.get(
        "MessageId",
        "No MessageId returned"
    )

    print("========================================")
    print("EMAIL ACCEPTED BY AMAZON SES")
    print("SES Message ID:", message_id)
    print("========================================")

    # --------------------------------------------------------
    # 11. RETURN RESULT
    # --------------------------------------------------------

    return response(
        200,
        {
            "message":
                "StudyPulse generated and delivered today's plan!",

            "student":
                name,

            "studyPlan":
                study_plan,

            "sesMessageId":
                message_id,

            "personalization": {
                "topic": topic,
                "time": time_available,
                "difficulty": difficulty,
                "goal": goal
            }
        }
    )
