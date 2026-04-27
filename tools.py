from registry import tool
from db import get_collection

# ✅ clear naming (no conflict)
users_collection = get_collection("users")


@tool("insert_user", "Insert user into MongoDB")
def insert_user(name: str, age: int):
    users_collection.insert_one({"name": name, "age": age})
    return {"status": "inserted", "name": name}


@tool("get_users", "Fetch all users")
def get_users():
    return list(users_collection.find({}, {"_id": 0}))


@tool("delete_user", "Delete user by name")
def delete_user(name: str):
    return {"deleted": users_collection.delete_one({"name": name}).deleted_count}


# ✅ FIXED (matches AI schema)
@tool("insert_users", "Insert multiple users")
def insert_users(users: list):
    for user in users:
        users_collection.insert_one(user)

    return {
        "status": "multiple users inserted",
        "count": len(users)
    }
    
@tool("get_users", "Fetch users with optional filtering")
def get_users(filter: dict = None):
    query = {}

    if filter and "name_starts_with" in filter:
        prefix = filter["name_starts_with"]
        query["name"] = {"$regex": f"^{prefix}", "$options": "i"}

    return list(users_collection.find(query, {"_id": 0}))


@tool("delete_users", "Delete multiple users by names")
def delete_users(names: list):
    result = users_collection.delete_many({"name": {"$in": names}})
    return {"deleted_count": result.deleted_count}