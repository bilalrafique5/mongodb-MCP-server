from registry import tool
from db import get_collection, db


# ---------------- CREATE COLLECTION ----------------
@tool("create_collection", "Create collection")
async def create_collection(name: str):
    await db.create_collection(name)
    return {"status": "created", "collection": name}


# ---------------- DELETE DOCUMENT ----------------
@tool("delete_document", "Delete document(s) by filter")
async def delete_document(collection_name: str, filter: dict):
    col = get_collection(collection_name)

    result = await col.delete_many(filter or {})

    return {
        "status": "deleted",
        "deleted_count": result.deleted_count
    }


# ---------------- LIST COLLECTIONS ----------------
@tool("list_collections", "List collections")
async def list_collections():
    return await db.list_collection_names()


# ---------------- INSERT DOCUMENT ----------------
@tool("insert_document", "Insert document")
async def insert_document(collection_name: str, data: dict):
    col = get_collection(collection_name)

    result = await col.insert_one(data)

    data["_id"] = str(result.inserted_id)

    return {
        "status": "inserted",
        "collection": collection_name,
        "data": data
    }


# ---------------- FILTER NORMALIZER ----------------
def normalize_filter(filter: dict):
    if not filter:
        return {}

    def fix(obj):
        if isinstance(obj, dict):
            new = {}
            for k, v in obj.items():

                # fix common LLM mistakes
                if k in ["gt", "lt", "gte", "lte", "eq"]:
                    k = f"${k}"

                new[k] = fix(v)
            return new
        return obj

    return fix(filter)


# ---------------- FIND DOCUMENTS ----------------
@tool("find_documents", "Find documents")
async def find_documents(collection_name: str, filter: dict = None):
    col = get_collection(collection_name)

    query = normalize_filter(filter or {})

    docs = await col.find(query).to_list(length=100)

    for d in docs:
        if "_id" in d:
            d["_id"] = str(d["_id"])

    return {
        "collection": collection_name,
        "count": len(docs),
        "data": docs
    }


# ---------------- UPDATE DOCUMENTS ----------------
@tool("update_document", "Update document(s)")
async def update_document(collection_name: str, filter: dict, update: dict):
    col = get_collection(collection_name)

    query = normalize_filter(filter or {})

    result = await col.update_many(
        query,
        {"$set": update}
    )

    return {
        "status": "updated",
        "matched": result.matched_count,
        "modified": result.modified_count
    }


# ---------------- SEARCH: NAME STARTS WITH ----------------
@tool("search_name_startswith", "Search names starting with text")
async def search_name_startswith(collection_name: str, text: str):
    col = get_collection(collection_name)

    query = {"name": {"$regex": f"^{text}", "$options": "i"}}

    docs = await col.find(query).to_list(length=100)

    for d in docs:
        d["_id"] = str(d["_id"])

    return {"count": len(docs), "data": docs}


# ---------------- SEARCH: NAME CONTAINS ----------------
@tool("search_name_contains", "Search names containing text")
async def search_name_contains(collection_name: str, text: str):
    col = get_collection(collection_name)

    query = {"name": {"$regex": text, "$options": "i"}}

    docs = await col.find(query).to_list(length=100)

    for d in docs:
        d["_id"] = str(d["_id"])

    return {"count": len(docs), "data": docs}


# ---------------- ADVANCED FILTER QUERY ----------------
@tool("filter_query", "Advanced filter query helper")
async def filter_query(collection_name: str, filter: dict):
    col = get_collection(collection_name)

    query = normalize_filter(filter or {})

    docs = await col.find(query).to_list(length=100)

    for d in docs:
        d["_id"] = str(d["_id"])

    return {"count": len(docs), "data": docs}