from registry import tool
from db import get_collection, db


# ---------------- CREATE COLLECTION ----------------
@tool("create_collection", "Create collection")
async def create_collection(name: str):
    await db.create_collection(name)
    return {"status": "created", "collection": name}


# ---------------- DELETE COLLECTION ----------------
@tool("delete_collection", "Delete collection")
async def delete_collection(name: str):
    await db.drop_collection(name)
    return {"status": "deleted", "collection": name}


# ---------------- LIST COLLECTIONS ----------------
@tool("list_collections", "List collections")
async def list_collections():
    return await db.list_collection_names()


# ---------------- INSERT DOCUMENT ----------------
@tool("insert_document", "Insert document")
async def insert_document(collection_name: str, data: dict):
    col = get_collection(collection_name)
    result=await col.insert_one(data)
    
    data["_id"]=str(result.inserted_id)

    return {
        "status": "inserted",
        "collection": collection_name,
        "data": data,
        
    }


# ---------------- FIND DOCUMENTS ----------------
@tool("find_documents", "Find documents")
async def find_documents(collection_name: str, filter: dict = None):
    col = get_collection(collection_name)
    query = filter or {}

    docs = await col.find(query, {"_id": 0}).to_list(length=100)

    return {
        "collection": collection_name,
        "count": len(docs),
        "data": docs
    }