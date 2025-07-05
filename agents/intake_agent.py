from crewai import Agent

class IntakeAgent(Agent):
    def __init__(self):
        super().__init__(
            role="First Point of Contact Agent",
            goal="Understand user intent and route the query to the correct agent.",
            backstory=(
                "Tools: Basic intent detection.\n"
                "Guardrails: Never attempt to resolve complex queries directly.\n"
                "Memory: Remember past query intents in current session."
            )
        )

    def detect_intent(self, query: str) -> str:
        """Always resolve for demo (can be improved later)."""
        return "resolve"
