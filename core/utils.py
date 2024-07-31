from fastapi.responses import JSONResponse


async def responses(message: str = None, status_code: int = None, error=None, data=None):
    """
    Create a JSON response with a custom message, error, and data.

    - **message**: Optional message to include in the response.
    - **status_code**: HTTP status code for the response.
    - **error**: Optional error detail to include in the response.
    - **data**: Optional data to include in the response.

    Returns:
    - A JSONResponse object with the specified content and status code.
    """
    if message and not data:
        # If a message is provided and no data, return a response with the message
        return JSONResponse(status_code = status_code, content = { "message": message })

    if error:
        # If an error is provided, return a response with the error
        return JSONResponse(status_code = status_code, content = { "error": error })

    if message and data:
        # If both a message and data are provided, return a response with both
        return JSONResponse(status_code = status_code, content = { "message": message, "data": data })

    # Default case: return a response with no content if no message, error, or data are provided
    return JSONResponse(status_code = 200)
