from agents.intake_agent import IntakeAgent
from agents.resolution_agent import ResolutionAgent
from agents.escalation_agent import EscalationAgent

def handle_query(query: str, faq_df):
    intake_agent = IntakeAgent()
    resolution_agent = ResolutionAgent(faq_df)
    escalation_agent = EscalationAgent()

    intent = intake_agent.detect_intent(query)
    
    if intent == "resolve":
        return resolution_agent.query_faq_and_llm(query)
    else:
        escalation_agent.escalate(query)
        return "Query escalated to support team."
