import enum


class ResponseDetail(enum.Enum):
    UNAUTHORIZED = 'Incorrect username or password'
    ALREADY_EXISTS = 'Username already registered'
    FORBIDDEN = 'For admin only'
