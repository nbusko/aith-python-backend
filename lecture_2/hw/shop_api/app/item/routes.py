from http import HTTPStatus
from typing import List, Optional
from starlette.responses import Response
from fastapi import APIRouter, HTTPException, Query

from lecture_2.hw.shop_api.app.item.contracts import Item, ItemRequest, PatchItemRequest
from lecture_2.hw.shop_api.store import queries

router = APIRouter()

@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully created new item",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to create new item",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=Item,
)
async def create_item(item_request: ItemRequest, response: Response) -> Item:
    try:
        item = queries.create_item(item_request)
        response.headers["location"] = f"/item/{item.id}"
        return item
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))

@router.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def get_item(id: int) -> Item:
    item = queries.get_item(id)
    if item is None or item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return item

@router.get(
    "/",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned list of items",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return any items for these parameters",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[Item],
)
async def get_items_list(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    show_deleted: bool = False,
):
    try:
        items = queries.get_items_list(offset, limit, min_price, max_price, show_deleted)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=f"Error retrieving items: {str(e)}")
    if items is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Items not found")
    return items
    
@router.put(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully changed item",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to change item",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def change_item(id: int, item_request: ItemRequest) -> Item:
    try:
        updated_item = queries.change_item(id, item_request)
        if updated_item is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return updated_item

@router.patch(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully modified item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=Item,
)
async def patch_item(id: int, patch_item_request: PatchItemRequest) -> Item:
    try:
        patched_item = queries.patch_item(id, patch_item_request)
        if patched_item is None:
            raise HTTPException(HTTPStatus.NOT_FOUND, "Item not found")
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail=str(e))
    return patched_item

@router.delete(
    "/{id}",
    responses={
        HTTPStatus.OK: {"description": "Successfully deleted item"},
        HTTPStatus.NOT_FOUND: {"description": "Failed to delete item"},
    },
    status_code=HTTPStatus.OK,
)
async def delete_item(id: int):
    try:
        item = queries.delete_item(id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    return item