import audit_agent


def test_system_prompt_defines_auditor_role_and_guardrails():
    prompt = audit_agent.SYSTEM_PROMPT
    assert "Senior Financial Auditor" in prompt
    assert "Shree Manufacturing" in prompt
    assert "refuse" in prompt.lower()


def test_agent_builder_passes_domain_prompt(monkeypatch):
    calls = {}

    def fake_create_deep_agent(**kwargs):
        calls.update(kwargs)
        return "agent"

    monkeypatch.setattr(audit_agent, "create_deep_agent", fake_create_deep_agent)
    agent = audit_agent.build_agent("test-model")

    assert agent == "agent"
    assert calls["model"] == "test-model"
    assert calls["system_prompt"] == audit_agent.SYSTEM_PROMPT
