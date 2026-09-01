from fastapi import HTTPException


def validate_pagination(page: int, page_size: int) -> None:
    if page < 1:
        raise HTTPException(
            status_code=400,
            detail="page must be greater than or equal to 1",
        )

    if page_size < 1:
        raise HTTPException(
            status_code=400,
            detail="page_size must be greater than or equal to 1",
        )

    if page_size > 100:
        raise HTTPException(
            status_code=400,
            detail="page_size must not be greater than 100",
        )