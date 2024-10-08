from fastapi import FastAPI
from lecture_2.hw.shop_api.app.cart.routes import router as cart_router
from lecture_2.hw.shop_api.app.item.routes import router as item_router

app = FastAPI(title="Shop API", version="1.0.0")

app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(item_router, prefix="/item", tags=["Item"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Shop API"}
