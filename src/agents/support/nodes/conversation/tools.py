
openai_vector_store_ids = [
  "vs_68f1a1e722508191ba51713db1cbf9a1",
]


file_search_tool = {
  "type": "file_search",
  "vector_store_ids": openai_vector_store_ids,
}

tools = [file_search_tool]