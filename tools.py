from registry import tool
from db import get_collection

users_collection = get_collection("users")


def build_query(filter=None):
    query = {}

    if not filter:
        return query

    if "name_starts_with" in filter:
        query["name"] = {
            "$regex": f"^{filter['name_starts_with']}",
            "$options": "i"
        }

    if "age_gt" in filter:
        query["age"] = {"$gt": filter["age_gt"]}

    if "age_gte" in filter:
        query["age"] = {"$gte": filter["age_gte"]}

    if "age_lt" in filter:
        query["age"] = {"$lt": filter["age_lt"]}

    if "age_lte" in filter:
        query["age"] = {"$lte": filter["age_lte"]}

    if "age_eq" in filter:
        query["age"] = filter["age_eq"]

    if "age_range" in filter:
        query["age"] = {
            "$gte": filter["age_range"][0],
            "$lte": filter["age_range"][1]
        }

    return query


# ---------------- INSERT SINGLE ----------------
@tool("insert_user", "Insert one user")
def insert_user(name: str, age: int):
    users_collection.insert_one({
        "name": name,
        "age": age
    })
    return {"status": "inserted", "name": name}


# ---------------- INSERT MULTIPLE ----------------
@tool("insert_users", "Insert multiple users")
def insert_users(users: list):
    users_collection.insert_many(users)
    return {
        "status": "bulk_inserted",
        "count": len(users)
    }


# ---------------- GET USERS ----------------
@tool("get_users", "Get users with filters")
def get_users(filter: dict = None):
    query = build_query(filter)
    users = list(users_collection.find(query, {"_id": 0}))

    return {
        "count": len(users),
        "users": users
    }


# ---------------- DELETE SINGLE ----------------
@tool("delete_user", "Delete one user")
def delete_user(name: str = None, names: list = None):
    """
    Supports both:
    delete_user(name="Ali")
    delete_user(names=["Ali"])   # planner mistake tolerance
    """
    if names and len(names) > 0:
        name = names[0]

    if not name:
        return {"error": "name is required"}

    res = users_collection.delete_one({"name": name})
    return {"deleted": res.deleted_count}


# ---------------- DELETE MULTIPLE ----------------
@tool("delete_users", "Delete multiple users")
def delete_users(names: list = None, filter: dict = None):
    """
    Supports:
    delete by names
    delete by filters
    """
    if names:
        res = users_collection.delete_many({
            "name": {"$in": names}
        })
        return {"deleted": res.deleted_count}

    if filter:
        query = build_query(filter)
        res = users_collection.delete_many(query)
        return {"deleted": res.deleted_count}

    return {"error": "Provide names or filter"}


# ---------------- UPDATE SINGLE ----------------
@tool("update_user", "Update one user")
def update_user(name: str, update: dict):
    res = users_collection.update_one(
        {"name": name},
        {"$set": update}
    )

    return {
        "matched": res.matched_count,
        "updated": res.modified_count
    }


# ---------------- UPDATE MULTIPLE ----------------
@tool("update_users", "Update multiple users")
def update_users(updates: list):
    count = 0

    for item in updates:
        res = users_collection.update_one(
            {"name": item["name"]},
            {"$set": item["update"]}
        )
        count += res.modified_count

    return {"updated": count}