class ErrorCode:
    INVALID_CREDENTIALS = 40001
    RATE_LIMIT_EXCEEDED = 40002
    INVALID_PARAMS = 40003


unauthenticated = {
    'status_code': 401,
    'error_code': ErrorCode.INVALID_CREDENTIALS,
    'error_message': 'Invalid credentials'
}

rate_limit_exceeded = {
    'status_code': 429,
    'error_code': ErrorCode.RATE_LIMIT_EXCEEDED,
    'error_message': 'Rate limit exceeded'
}

invalid_parameters = {
    'status_code': 400,
    'error_code': ErrorCode.INVALID_PARAMS,
    'error_message': 'Invalid parameters',
    'invalid_params': []
}
