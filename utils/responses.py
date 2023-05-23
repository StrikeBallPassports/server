from enum import Enum

from fastapi.responses import FileResponse


class ResponseDescription(Enum):
    BAD_REQUEST = 'Bad Request'
    UNAUTHORIZED = 'Unauthorized'
    FORBIDDEN = 'Forbidden, not admin user'
    NOT_FOUND = 'Not Found'
    ALREADY_EXISTS = 'Already exists'

    SUCCESSFUL_RESPONSE = 'Successful Response'


class ResponseDetail(Enum):
    BAD_REQUEST = 'Bad Request'
    UNAUTHORIZED = 'Incorrect username or password'
    FORBIDDEN = 'For admin only'
    NOT_FOUND = 'Not Found'
    ALREADY_EXISTS = 'Object already exists'


error_responses = {
    400: {
        'description': ResponseDescription.BAD_REQUEST.value,
        'content': {'application/json': {'example': {'detail': ResponseDetail.BAD_REQUEST.value}}}
    },
    401: {
        "description": ResponseDescription.UNAUTHORIZED.value,
        'content': {'application/json': {'example': {'detail': ResponseDetail.UNAUTHORIZED.value}}}
    },
    403: {
        'description': ResponseDescription.FORBIDDEN.value,
        'content': {
            'application/json': {
                'example': {'detail': ResponseDetail.FORBIDDEN.value}
            }
        }
    },
    404: {
        'description': ResponseDescription.NOT_FOUND.value,
        'content': {
            'application/json': {
                'example': {'detail': ResponseDetail.NOT_FOUND.value}
            }
        }
    },
    409: {
        'description': ResponseDescription.ALREADY_EXISTS.value,
        'content': {
            'application/json': {
                'example': {'detail': ResponseDetail.ALREADY_EXISTS.value}
            }
        }
    }
}

responses = {
    'user_images': {
        'description': ResponseDescription.SUCCESSFUL_RESPONSE.value,
        'content': {
            'application/json': {
                'example': {
                    'data': {
                        '1': 'FileResponse',
                    }
                }
            }
        }
    },
}
