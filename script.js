const API_URL =
    "https://4q53mq3v81.execute-api.ap-south-1.amazonaws.com/generate";


function setTopic(topic) {

    document.getElementById("topic-input").value = topic;

    document.getElementById("topic-input").focus();

}


async function generateStudyPlan() {

    const button =
        document.getElementById("generate-btn");

    const result =
        document.getElementById("study-result");

    const thinking =
        document.getElementById("agent-thinking");


    const topic =
        document.getElementById("topic-input").value.trim();

    const time =
        document.getElementById("time-input").value;

    const difficulty =
        document.getElementById("difficulty-input").value;

    const goal =
        document.getElementById("goal-input").value.trim();


    button.disabled = true;

    button.innerHTML =
        "<span>◌</span> StudyPulse is thinking...";


    thinking.classList.remove("hidden");


    result.innerHTML = "";


    try {

        const response = await fetch(
            API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    student: "disha",

                    topic: topic,

                    time: time,

                    difficulty: difficulty,

                    goal: goal

                })
            }
        );


        if (!response.ok) {

            throw new Error(
                "API request failed: " +
                response.status
            );

        }


        const data = await response.json();


        let body = data;


        if (data.body) {

            body =
                typeof data.body === "string"
                    ? JSON.parse(data.body)
                    : data.body;

        }


        const plan =
            body.studyPlan;


        if (!plan) {

            throw new Error(
                "Study plan was not returned."
            );

        }


        result.innerHTML = `

            <div class="live-result">

                <div class="result-top">

                    <div>

                        <span class="result-kicker">
                            PERSONALIZED AGENT OUTPUT
                        </span>

                        <h3>
                            Your plan is ready.
                        </h3>

                    </div>

                    <div class="result-live">
                        ● LIVE
                    </div>

                </div>


                <div class="memory-used">

                    <span>✦</span>

                    StudyPulse combined your
                    current request with persistent memory.

                </div>


                <div class="plan-output">

                    ${formatPlan(plan)}

                </div>


                <div class="email-confirmation">

                    <span>✓</span>

                    Plan generated and delivered through
                    Amazon SES.

                </div>

            </div>

        `;


        result.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });


    } catch (error) {

        console.error(error);


        result.innerHTML = `

            <div class="error-message">

                <strong>
                    ✕ Agent request failed
                </strong>

                <p>
                    Check API Gateway / Lambda configuration
                    and try again.
                </p>

            </div>

        `;

    }


    finally {

        thinking.classList.add("hidden");

        button.disabled = false;

        button.innerHTML =
            "<span>⚡</span> Generate My Personalized Plan";

    }

}


function formatPlan(text) {

    const safe = escapeHtml(text);

    return safe

        .replace(
            /TODAY'S PRIORITY:/g,
            '<div class="plan-heading">🎯 TODAY\'S PRIORITY</div>'
        )

        .replace(
            /WHY:/g,
            '<div class="plan-heading">💡 WHY</div>'
        )

        .replace(
            /STUDY PLAN:/g,
            '<div class="plan-heading">📚 STUDY PLAN</div>'
        )

        .replace(
            /CHALLENGE:/g,
            '<div class="plan-heading">⚡ CHALLENGE</div>'
        )

        .replace(
            /\n/g,
            "<br>"
        );

}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}