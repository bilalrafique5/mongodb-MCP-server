from registry import tool
from db import get_collection, db


# ---------------- CREATE COLLECTION ----------------
@tool("create_collection", "Create a new MongoDB collection")
async def create_collection(name: str):
    try:
        await db.create_collection(name)
        return {"status": "created", "collection": name}
    except Exception as e:
        return {"error": str(e)}


# ---------------- DELETE COLLECTION ----------------
@tool("delete_collection", "Delete a MongoDB collection")
async def delete_collection(name: str):
    try:
        await db.drop_collection(name)
        return {"status": "deleted", "collection": name}
    except Exception as e:
        return {"error": str(e)}


# ---------------- LIST COLLECTIONS ----------------
@tool("list_collections", "List all collections")
async def list_collections():
    return await db.list_collection_names()


# ---------------- INSERT SINGLE ----------------
@tool("insert_document", "Insert document into any collection")
async def insert_document(collection_name: str, data: dict):
    collection = get_collection(collection_name)
    await collection.insert_one(data)

    return {
        "status": "inserted",
        "collection": collection_name,
        "data": data
    }


# ---------------- INSERT MULTIPLE ----------------
@tool("insert_documents", "Insert multiple documents")
async def insert_documents(collection_name: str, documents: list):
    collection = get_collection(collection_name)
    await collection.insert_many(documents)

    return {
        "status": "bulk_inserted",
        "collection": collection_name,
        "count": len(documents)
    }


# ---------------- DELETE DOCUMENTS ----------------
@tool("delete_documents", "Delete documents from any collection")
async def delete_documents(collection_name: str, filter: dict):
    collection = get_collection(collection_name)
    result = await collection.delete_many(filter)

    return {
        "deleted": result.deleted_count,
        "collection": collection_name
    }


# ---------------- UPDATE DOCUMENTS ----------------
@tool("update_documents", "Update documents in any collection")
async def update_documents(collection_name: str, filter: dict, update: dict):
    collection = get_collection(collection_name)

    result = await collection.update_many(
        filter,
        {"$set": update}
    )

    return {
        "matched": result.matched_count,
        "updated": result.modified_count,
        "collection": collection_name
    }


# ---------------- FIND DOCUMENTS ----------------
@tool("find_documents", "Get documents from any collection with filters")
async def find_documents(collection_name: str, filter: dict = None):
    collection = get_collection(collection_name)

    query = filter or {}

    docs = await collection.find(query, {"_id": 0}).to_list(length=100)

    return {
        "collection": collection_name,
        "count": len(docs),
        "data": docs
    }


# ---------------- FILTERED USERS (OPTIONAL LEGACY SUPPORT) ----------------
@tool("get_users", "Backward compatibility user query tool")
async def get_users(filter: dict = None):
    collection = get_collection("users")

    query = {}

    if filter:
        if "name_starts_with" in filter:
            query["name"] = {
                "$regex": f"^{filter['name_starts_with']}",
                "$options": "i"
            }

        if "age_gt" in filter:
            query["age"] = {"$gt": filter["age_gt"]}

        if "age_lt" in filter:
            query["age"] = {"$lt": filter["age_lt"]}

    users = await collection.find(query, {"_id": 0}).to_list(length=100)

    return {
        "count": len(users),
        "users": users
    }


# ---------------- COLLECTION SCHEMA ----------------
@tool("get_collection_schema", "Get schema of any collection")
async def get_collection_schema(collection_name: str):
    collection = get_collection(collection_name)

    sample = await collection.find_one()

    if not sample:
        return {
            "collection": collection_name,
            "schema": {},
            "message": "empty collection"
        }

    schema = {}

    for k, v in sample.items():
        if k != "_id":
            schema[k] = {
                "type": type(v).__name__,
                "example": v
            }

    return {
        "collection": collection_name,
        "schema": schema
    }