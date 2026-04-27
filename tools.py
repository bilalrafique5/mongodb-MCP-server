from registry import tool
from db import get_collection

users = get_collection("users")


# ---------------- INSERT SINGLE ----------------
@tool("insert_user", "Insert one user")
def insert_user(name: str, age: int):
    users.insert_one({"name": name, "age": age})
    return {"status": "inserted", "name": name}


# ---------------- INSERT MULTIPLE ----------------
@tool("insert_users", "Insert multiple users")
def insert_users(users_list: list):
    users.insert_many(users_list)
    return {"status": "bulk_inserted", "count": len(users_list)}


# ---------------- GET WITH FILTERS ----------------
@tool("get_users", "Get users with filters")
def get_users(filter: dict = None):
    query = {}

    if filter:
        # name filter
        if "name_starts_with" in filter:
            query["name"] = {
                "$regex": f"^{filter['name_starts_with']}",
                "$options": "i"
            }

        # age filters
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

    return list(users.find(query, {"_id": 0}))


# ---------------- DELETE SINGLE ----------------
@tool("delete_user", "Delete one user")
def delete_user(name: str):
    res = users.delete_one({"name": name})
    return {"deleted": res.deleted_count}


# ---------------- DELETE MULTIPLE ----------------
@tool("delete_users", "Delete multiple users")
def delete_users(names: list):
    res = users.delete_many({"name": {"$in": names}})
    return {"deleted": res.deleted_count}


# ---------------- UPDATE SINGLE ----------------
@tool("update_user", "Update one user")
def update_user(name: str, update: dict):
    res = users.update_one({"name": name}, {"$set": update})
    return {"matched": res.matched_count, "updated": res.modified_count}


# ---------------- UPDATE MULTIPLE ----------------
@tool("update_users", "Update multiple users")
def update_users(names: list, update: dict):
    res = users.update_many({"name": {"$in": names}}, {"$set": update})
    return {"matched": res.matched_count, "updated": res.modified_count}