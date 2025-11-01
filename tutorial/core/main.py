from fastapi import FastAPI, Query, status, HTTPException, Body
from typing import Optional, Annotated
import uvicorn
import random
 
app = FastAPI()

name_list = [
    {"id":1, "name": "amir"},
    {"id":2, "name": "erfan"},
    {"id":3, "name": "ali"},
    {"id":4, "name": "mohamad"},
]

@app.get("/home")
def root():
    return {"message:": "salam azizam"}

@app.post("/names", status_code=status.HTTP_201_CREATED)
def create_name(name: str = Body(embed=True)):
    name_obj = {"id": random.randint(6, 100), "name": name}
    name_list.append(name_obj)
    return {"result": name_obj}

@app.get("/names")
def show_name_list():
    return name_list

@app.get("/names/{name_id}")
def show_name_id(name_id: int,
                min_item=1,
                max_item=5
                ):

    print(name_id)
    for name in name_list:
        if name["id"] == name_id:
            return {"User": name}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")    

@app.put("/names/{name_id}")
def update_name(name_id: int, new_name:str):
    for item in name_list:
        if item["id"] == name_id:
            item["name"] = new_name
            return {"message": "succefully changed the name"}, {"User": item}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")  

@app.delete("/names/{name_id}")
def update_name(name_id: int):
    for item in name_list:
        if item["id"] == name_id:
            name_list.remove(item)
            return HTTPException(content={"Message": "Object removed successfully"}, status_code=status.HTTP_202_ACCEPTED)
    return {"message": f"Not Found id No.{name_id}"}, {"message": f"bia inam bara khodet ---({name_id})"}

@app.get("/show-names", status_code=status.HTTP_200_OK)
def search_user(q: Annotated[str | None, Query(max_length=25)]):
    # [operation, iteration, condition]
    return [item for item in name_list if item["name"] == q]

# if __name__ == "__main__":
#     uvicorn.run("main:app",host="0.0.0.0", port=8000, reload=True)
