from http import HTTPStatus
from typing import List, Optional
from starlette.responses import Response
from fastapi import APIRouter, HTTPException, Query

from lecture_2.hw.shop_api.app.cart.contracts import CartResponse
from lecture_2.hw.shop_api.store import queries

router = APIRouter()

@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully created new cart",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to create new cart",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=CartResponse,
)
async def create_cart(response: Response) -> CartResponse:
    try:
        cart = queries.create_cart()
        response.headers["location"] = f"/cart/{cart.id}"
        return cart
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))

@router.get(
    "/{cart_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=CartResponse,
)
async def get_cart(id: int) -> CartResponse:
    try:
        cart = queries.get_cart(id)
        if cart is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Cart not found"
            )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart

@router.get(
    "/",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned the cart list",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "No carts match the query parameters",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Unable to process the request",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[CartResponse],
)
async def get_carts_list(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_quantity: Optional[int] = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
) -> List[CartResponse]:
    try:
        carts = queries.get_carts_list(
            min_price, max_price, min_quantity, max_quantity, offset, limit
        )
        if not carts:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="No matching carts found"
            )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"Invalid input: {e}")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal error occurred")
    
    return carts

@router.post(
    "/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully added item to cart",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to add item to cart",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=CartResponse,
)
async def add_item(cart_id: int, item_id: int) -> CartResponse:
    try:
        cart = queries.add_item(cart_id, item_id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart