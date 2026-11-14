"""
Safe application dispatcher.

This deliberately does not submit generic web forms. Add one employer/ATS-specific
adapter at a time after checking that automation is permitted. Each adapter must:
- verify the exact job and candidate identity;
- prevent duplicate applications;
- use only candidate-confirmed profile answers;
- stop for CAPTCHA, OTP, assessments, legal attestations, or unknown questions;
- record 'applied' only after the employer confirms successful submission.
"""
class ManualInterventionRequired(Exception):
    pass

def apply_to_job(job, profile):
    raise ManualInterventionRequired(
        "No verified employer-specific adapter is configured. "
        "Open the job URL and complete the application manually."
    )
