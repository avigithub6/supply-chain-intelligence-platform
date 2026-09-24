from uuid import uuid4


def generate_request_id() -> str:
    """Generate a unique request ID for tracing a request."""
    return str(uuid4())