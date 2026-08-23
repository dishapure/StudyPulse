import json
import boto3

# ============================================================
# AWS CLIENTS
# ============================================================

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")
ses = boto3.client("ses", region_name="ap-south-1")

# ============================================================
# CONFIGURATION
# ============================================================

TABLE_NAME = "StudyPulseMemory"

# Amazon Nova Micro APAC inference profile
MODEL_ID = "apac.amazon.nova-micro-v1:0"

# IMPORTANT:
# Replace this with the EXACT email address you verified in SES.
EMAIL_ADDRESS = "disha.boston@gmail.com"

# ============================================================
# DYNAMODB TABLE
# ============================================================

table = dynamodb.Table(TABLE_NAME)


# ============================================================
# LAMBDA HANDLER
# ============================================================

def lambda_handler(event, context):

    print("StudyPulse agent started.")

    # --------------------------------------------------------
    # 1. READ STUDENT MEMORY FROM DYNAMODB
    # --------------------------------------------------------

    response = table.get_item(
        Key={
            "studentId": "disha"
        }
    )

    student = response.get("Item")

    if not student:
        print("Student memory not found.")

        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "Student memory not found"
            })
        }

    print("Student memory loaded successfully.")

    # --------------------------------------------------------
    # 2. EXTRACT STUDENT INFORMATION
    # --------------------------------------------------------

    name = student.get("name", "Student")
    subjects = student.get("subjects", "Not specified")
    exam = student.get("exam", "Not specified")
    weak_topics = student.get("weakTopics", "Not specified")
    study_minutes = student.get("studyMinutes", 45)
    last_completed = student.get("lastCompleted", "None")
    previous_plan = student.get("lastPlan", "None")

    # --------------------------------------------------------
    # 3. BUILD THE AGENT PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are StudyPulse, an autonomous AI study planning agent.

Your job is to decide what this student should focus on today.

You have access to the student's stored learning memory.

STUDENT INFORMATION
-------------------
Name: {name}
Subjects: {subjects}
Upcoming exam: {exam}
Weak topics: {weak_topics}
Available study time: {study_minutes} minutes
Last completed topic: {last_completed}

PREVIOUS STUDY PLAN
-------------------
{previous_plan}

YOUR TASK
---------
Analyze the student's current information and create a focused,
realistic study plan for today.

Prioritize weak topics when appropriate.

Avoid repeating the exact same plan every day.

The plan must fit within the student's available study time.

Do not invent information about the student.

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
<one useful question the student should answer>

Keep the response concise and practical.
"""

    print("Sending request to Amazon Nova Micro.")

    # --------------------------------------------------------
    # 4. INVOKE AMAZON NOVA MICRO
    # --------------------------------------------------------

    response = bedrock.converse(
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
            "temperature": 0.4
        }
    )

    # --------------------------------------------------------
    # 5. EXTRACT AI RESPONSE
    # --------------------------------------------------------

    study_plan = (
        response["output"]
        ["message"]
        ["content"][0]
        ["text"]
    )

    print("Study plan generated successfully.")
    print(study_plan)

    # --------------------------------------------------------
    # 6. SAVE NEW MEMORY TO DYNAMODB
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
    # 7. SEND STUDY PLAN THROUGH AMAZON SES
    # --------------------------------------------------------

    email_subject = "☀️ Your StudyPulse for Today"

    email_body = f"""
Hi {name},

Your StudyPulse for today is ready.

----------------------------------------
{study_plan}
----------------------------------------

Keep the momentum going. Small progress every day compounds.

— StudyPulse 🤖
"""

    ses.send_email(

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

    print("Study plan email sent successfully.")

    # --------------------------------------------------------
    # 8. RETURN SUCCESS
    # --------------------------------------------------------

    return {
        "statusCode": 200,

        "body": json.dumps({

            "message": "StudyPulse generated and delivered today's plan!",

            "student": name,

            "studyPlan": study_plan

        })
    }
