from registry import tool
from db import get_collection

users = get_collection("users")


# ---------------- SINGLE INSERT ----------------
@tool("insert_user", "Insert one user")
def insert_user(name: str, age: int):
    users.insert_one({"name": name, "age": age})
    return {"status": "inserted", "name": name}


# ---------------- MULTI INSERT ----------------
@tool("insert_users", "Insert multiple users")
def insert_users(users: list):
    users.insert_many(users)
    return {"status": "bulk_inserted", "count": len(users)}


# ---------------- GET WITH FILTER ----------------
@tool("get_users", "Get users with optional filters")
def get_users(filter: dict = None):
    query = {}

    if filter and filter.get("name_starts_with"):
        query["name"] = {
            "$regex": f"^{filter['name_starts_with']}",
            "$options": "i"
        }

    return list(users.find(query, {"_id": 0}))


# ---------------- DELETE ONE ----------------
@tool("delete_user", "Delete single user")
def delete_user(name: str):
    res = users.delete_one({"name": name})
    return {"deleted": res.deleted_count}


# ---------------- DELETE MANY ----------------
@tool("delete_users", "Delete multiple users")
def delete_users(names: list):
    res = users.delete_many({"name": {"$in": names}})
    return {"deleted": res.deleted_count}

# 🔄 UPDATE SINGLE USER
@tool("update_user", "Update a user by name")
def update_user(name: str, update: dict):
    result = users.update_one(
        {"name": name},
        {"$set": update}
    )

    return {
        "matched": result.matched_count,
        "updated": result.modified_count
    }
    
    
@tool("update_users", "Update multiple users by names")
def update_users(names: list, update: dict):
    result = users.update_many(
        {"name": {"$in": names}},
        {"$set": update}
    )

    return {
        "matched": result.matched_count,
        "updated": result.modified_count
    }