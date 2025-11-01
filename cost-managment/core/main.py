from fastapi import FastAPI, HTTPException, status
from typing import Optional
from contextlib import asynccontextmanager
import random

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Server started")

    yield
    print("Server shot down")

app = FastAPI(lifespan=lifespan)

COSTS_MANAGEMENT = [
    {"id":1, "description":"this is my first cost", "amount":20}
]

@app.post("/add-cost", status_code=status.HTTP_201_CREATED)
async def make_cost(info: str, amount: int):
    random_id = random.randint(1, 100)
    for item in COSTS_MANAGEMENT:
        if item["id"] == random_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Try again" )
    
    datas = {"id": random_id,
              "descrption": info,
              "amount": amount}
    COSTS_MANAGEMENT.append(datas)
    print(COSTS_MANAGEMENT)
    return {"message": "Cost Added", "detail": datas}

@app.get("/all-costs")
async def get_cost():
    return COSTS_MANAGEMENT

@app.get("/get-costs/")
async def get_cost(costID: int):
    for item in COSTS_MANAGEMENT:
        if item["id"] == costID:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.put("/update-cost")
async def edit_cost(costID: int, info: Optional[str] = None, amount: Optional[float] = None):
    for item in COSTS_MANAGEMENT:
        if item["id"] == costID:
            if info:
                item["description"] = info
            if amount is not None:
                item["amount"] = amount
            return {"message": "Cost updated", "detail": item}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")

@app.delete("/delete-cost", status_code=status.HTTP_204_NO_CONTENT)
async def delete_cost(costID: int):
    for i, item in enumerate(COSTS_MANAGEMENT):
        if item["id"] == costID:
            del COSTS_MANAGEMENT[i]
            print(f"Cost with ID {costID} deleted")
            return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cost not found")

@app.get("/")
def root():
    return {"message:": "salam azizam"}
