from fastapi import HTTPException, status


class ResourceNotFoundException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )


class UnauthorizedException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            # headers={"WWW-Authenticate": "Bearer"},
        )


class BadCredentialsException(UnauthorizedException):
    def __init__(self, message: str):
        super().__init__(message)


class AccessDeniedException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=message)


class InvalidDataException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=message)


class UnprocessableEntityException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message
        )
