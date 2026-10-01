"""End-to-end walkthrough of the support management system.

Runs the path a real case takes: a customer calls, the case is routed, worked,
resolved from a knowledge-base article, closed and surveyed. Useful as a smoke
test and as a readable description of how the modules fit together.

    python demo.py
"""
from support_system import (assignment, attachments, audit, cases, contacts, csat, customers,
                            dashboard, escalation, intake_phone, kb_articles, kb_linking,
                            notifications, priority, rbac, routing, sla_policy, sla_timer,
                            worklog, workflow)


def main() -> None:
    customers.create_customer("ACME-1", "Acme Industries")
    contact = contacts.add_contact("ACME-1", "Dana Reed", "dana@acme.test", "+1 555 0142")

    case = intake_phone.log_call("ACME-1", contact.contact_id, "Terminal will not boot",
                                 "Caller reports a black screen after a power cut.",
                                 category="outage")
    print(f"opened {case.reference} on the {case.channel} channel")

    print("routed to queue:", routing.route(case.reference))
    assignment.assign(case.reference, "amara", assigned_by="chi")
    priority.apply_priority(case.reference, impact="high", urgency="high", actor="amara")
    print("priority:", case.priority)

    workflow.move(case.reference, "In Progress", actor="amara")
    worklog.add_comment(case.reference, "amara", "Walked the caller through a power cycle.")
    worklog.add_comment(case.reference, "amara", "Suspect the PSU.", internal=True)
    worklog.log_time(case.reference, "amara", 25, "Diagnosis")
    attachments.attach(case.reference, "screen.png", 120_000, "amara")
    print(f"customer sees {len(worklog.customer_visible(case.reference))} of "
          f"{len(worklog.comments_for(case.reference))} comments; "
          f"{worklog.total_minutes(case.reference)} minutes logged")

    sla_policy.create_policy("standard",
                             {"Critical": 15, "High": 30, "Medium": 120, "Low": 480},
                             {"Critical": 240, "High": 480, "Medium": 1440, "Low": 2880})
    sla_policy.activate("standard")
    sla_timer.start(case.reference)
    print("SLA minutes remaining:", sla_timer.remaining_minutes(case.reference),
          "| breached:", escalation.evaluate(case.reference).breached)

    article = kb_articles.create_article("Terminal will not boot",
                                         "Check the power supply unit and reseat the cable.",
                                         ["boot", "terminal", "outage"])
    kb_articles.publish(article.article_id)
    print("suggested:", [(a.title, round(s, 2)) for a, s in kb_linking.suggest(case.reference)])
    kb_linking.link_as_resolution(case.reference, article.article_id, actor="amara")

    workflow.move(case.reference, "Closed", actor="amara")
    csat.send_survey(case.reference)
    csat.record_response(case.reference, 5, "Sorted quickly.")

    print("audit entries:", len(audit.trail(case.reference)))
    print("satisfaction by agent:", csat.by_agent())
    print("dashboard:", dashboard.summary())
    print("notifications sent:", len(notifications.sent_for(case.reference)))

    try:
        rbac.require_view("customer", "SOMEONE-ELSE", case.reference)
    except rbac.AccessDenied as exc:
        print("access control holds:", exc)


if __name__ == "__main__":
    main()
