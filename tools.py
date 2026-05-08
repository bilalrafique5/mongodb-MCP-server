from fastmcp import FastMCP
from db import get_collection, db

mcp = FastMCP("mongodb-mcp")


# ---------------- FILTER NORMALIZER ----------------
def normalize_filter(f):
    if not f:
        return {}

    def fix(obj):
        if isinstance(obj, dict):
            new = {}
            for k, v in obj.items():
                if k in ["gt", "lt", "gte", "lte", "eq"]:
                    k = f"${k}"
                new[k] = fix(v)
            return new
        return obj

    return fix(f)


# ---------------- COLLECTIONS ----------------
@mcp.tool()
async def create_collection(name):
    # 🔥 MULTI COLLECTION SUPPORT
    if isinstance(name, list):
        results = []

        for n in name:
            if n in await db.list_collection_names():
                results.append({"name": n, "status": "exists"})
            else:
                await db.create_collection(n)
                results.append({"name": n, "status": "created"})

        return {"collections": results}

    # SINGLE COLLECTION
    if name in await db.list_collection_names():
        return {"status": "exists"}

    await db.create_collection(name)
    return {"status": "created"}


@mcp.tool()
async def list_collections():
    return await db.list_collection_names()


# ---------------- CRUD ----------------
@mcp.tool()
async def insert_document(collection_name: str, data):
    col = get_collection(collection_name)

    # 🔥 BULK INSERT SUPPORT
    if isinstance(data, list):
        result = await col.insert_many(data)

        for i, d in enumerate(data):
            d["_id"] = str(result.inserted_ids[i])

        return {
            "inserted_count": len(result.inserted_ids),
            "data": data
        }

    # ❌ BLOCK EMPTY INSERTS
    if not data or len(data.keys()) == 0:
        return {"error": "Empty document not allowed"}

    result = await col.insert_one(data)
    data["_id"] = str(result.inserted_id)

    return data


@mcp.tool()
async def delete_document(collection_name: str, filter: dict):
    col = get_collection(collection_name)

    result = await col.delete_many(filter or {})
    return {"deleted": result.deleted_count}


@mcp.tool()
async def update_document(collection_name: str, filter: dict, update: dict):
    col = get_collection(collection_name)

    result = await col.update_many(filter, {"$set": update})
    return {"matched": result.matched_count, "modified": result.modified_count}


# ---------------- FIND ----------------
@mcp.tool()
async def find_documents(
    collection_name: str,
    filter: dict = None,
    sort: dict = None,
    limit: int = 100
):
    col = get_collection(collection_name)

    query = normalize_filter(filter or {})

    cursor = col.find(query)

    if sort:
        cursor = cursor.sort(list(sort.items()))

    cursor = cursor.limit(limit)

    docs = await cursor.to_list(length=limit)

    for d in docs:
        d["_id"] = str(d["_id"])

    return {
        "count": len(docs),
        "data": docs
    }


# ---------------- SEARCH ----------------
@mcp.tool()
async def search_name_startswith(collection_name: str, text: str):
    col = get_collection(collection_name)

    query = {"name": {"$regex": f"^{text}", "$options": "i"}}

    docs = await col.find(query).to_list(100)

    for d in docs:
        d["_id"] = str(d["_id"])

    return docs


@mcp.tool()
async def search_name_contains(collection_name: str, text: str):
    col = get_collection(collection_name)

    query = {"name": {"$regex": text, "$options": "i"}}

    docs = await col.find(query).to_list(100)

    for d in docs:
        d["_id"] = str(d["_id"])

    return docs


@mcp.tool()
async def filter_query(collection_name: str, filter: dict):
    col = get_collection(collection_name)

    query = normalize_filter(filter or {})

    docs = await col.find(query).to_list(200)

    for d in docs:
        d["_id"] = str(d["_id"])

    return docs


# ---------------- LATEST ----------------
@mcp.tool()
async def get_latest_document(collection_name: str, limit: int = 1):
    col = get_collection(collection_name)

    cursor = col.find().sort("_id", -1).limit(limit)

    docs = await cursor.to_list(length=limit)

    for d in docs:
        d["_id"] = str(d["_id"])

    return {
        "count": len(docs),
        "data": docs
    }