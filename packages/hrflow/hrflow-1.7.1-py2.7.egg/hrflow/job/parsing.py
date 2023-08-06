from .validator import validate_job_id, validate_job_reference


class JobParsing():
    """Manage parsing related job calls."""

    def __init__(self, api):
        """Init."""
        self.client = api

    def get(self, job_id=None, job_reference=None):
        return
