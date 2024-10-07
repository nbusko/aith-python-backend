from typing import Iterable, List

from models import (
    Cart, 
    CartItem, 
    Item
)

from shop_api.app.item.contracts import (
    ItemRequest,
    PatchItemRequest
)

_item_db = dict[int, Item]
_cart_db = dict[int, Cart]

def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1

_cart_id_generator = int_id_generator()
_item_id_generator = int_id_generator()

def create_cart() -> int:
    _id = next(_cart_id_generator)
    cart = Cart(id=_id)
    _cart_db[_id] = cart
    return cart

def get_cart(id: int) -> Cart | None:
    return _cart_db.get(id)

# def get_carts_list(
#         min_price: float | None,
#         max_price: float | None,
#         min_quantity: int | None,
#         max_quantity: int | None,
#         offset: int = 0,
#         limit: int = 10
# ) -> List[Cart] | None:

#     filtered_carts = [
#         cart for cart in list(_cart_db.values())
#         if (min_price is None or cart.price >= min_price) and
#            (max_price is None or cart.price <= max_price)
#     ]
    
#     if min_quantity and filtered_carts:
#         if len(filtered_carts) < min_quantity:
#             return None
    
#     if filtered_carts and len(filtered_carts) >= (limit + offset):
#         filtered_carts = filtered_carts[offset : offset + limit]
        
#     if max_quantity and filtered_carts:
#         if len(filtered_carts) > max_quantity:
#             filtered_carts = filtered_carts[: max_quantity]

#     return filtered_carts or None

def get_carts_list(
    min_price: float | None,
    max_price: float | None,
    min_quantity: int | None,
    max_quantity: int | None,
    offset: int = 0,
    limit: int = 10
) -> List[Cart]:

    filtered_carts = [
        cart for cart in _cart_db.values()
        if (min_price is None or cart.price >= min_price) and
           (max_price is None or cart.price <= max_price)
    ]

    if min_quantity is not None and len(filtered_carts) < min_quantity:
        return []

    filtered_carts = filtered_carts[offset: offset + limit]

    if max_quantity is not None:
        filtered_carts = filtered_carts[:max_quantity]

    return filtered_carts

def add_item(
        cart_id : int,
        item_id : int
) -> Cart:
    
    cart = get_cart(cart_id)
    if cart is None:
        raise ValueError(f"Cart {cart_id} not found.")
        
    item = get_item(item_id)
    if item is None:
        raise ValueError(f"Item {item_id} not found.")

    item_dict = {item.id: item for item in cart.items}
    if item_id in item_dict:
        for in_item in cart.items:
            if in_item.id == item_id:
                in_item.quantity += 1
                break
    else:
        cart.items.append(
            CartItem(id=item.id, name=item.name, quantity=1, available=True)
        )
    cart.price += item.price

    return cart

def create_item(item_request: ItemRequest) -> Item:
    _id = next(_item_id_generator)
    item = Item(id=_id, 
                name=item_request.name, 
                price=item_request.price)
    _item_db[_id] = item
    return item

def get_item(id: int) -> Item | None:
    return _item_db.get(id)

# def get_items_list(
#         min_price: float | None,
#         max_price: float | None,
#         offset: int = 0,
#         limit: int = 10,
#         show_deleted: bool = False
# ) -> List[Item]:
    
#     filtered_items = [
#         item for item in list(_item_db.values())
#         if (min_price is None or item.price >= min_price) and
#            (max_price is None or item.price <= max_price) and
#            (show_deleted or (not item.deleted))
#     ]

#     if filtered_items and len(filtered_items) >= (limit + offset):
#         filtered_items = filtered_items[offset : offset + limit]
    
#     return filtered_items

def get_items_list(
        min_price: float | None = None,
        max_price: float | None = None,
        offset: int = 0,
        limit: int = 10,
        show_deleted: bool = False
) -> List[Item]:
    
    filtered_items = [
        item for item in _item_db.values()
        if (min_price is None or item.price >= min_price) and
           (max_price is None or item.price <= max_price) and
           (show_deleted or not item.deleted)
    ]
    
    return filtered_items[offset: offset + limit]

def change_item(id: int, item_request: ItemRequest) -> Item:

    item = get_item(id)
    if not item or item.deleted:
        return None
    item.name, item.price = item_request.name, item_request.price

    return item

def patch_item(
        id: int, 
        patch_item_request: PatchItemRequest
) -> Item:
    
    item = get_item(id)
    if not item or item.deleted:
        return None
    if patch_item_request.name:
        item.name = patch_item_request.name
    if patch_item_request.price:
        item.price = patch_item_request.price

    return item

def delete_item(id: int) -> Item | None:

    item = _item_db.get(id)
    if not item:
        return None
    item.deleted = True

    return item