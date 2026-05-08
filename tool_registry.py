from tools import (
    find_documents,
    insert_document,
    update_document,
    delete_document,
    search_name_contains,
    search_name_startswith,
    filter_query,
    list_collections
)

TOOLS = {
    "find_documents": find_documents,
    "insert_document": insert_document,
    "update_document": update_document,
    "delete_document": delete_document,
    "search_name_contains": search_name_contains,
    "search_name_startswith": search_name_startswith,
    "filter_query": filter_query,
    "list_collections": list_collections
}