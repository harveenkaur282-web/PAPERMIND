from frontend.gradio_app import handle_query


def test_handle_query_returns_string():
    response = handle_query("What is RAG?")

    assert isinstance(response, str)


def test_query_is_present_in_response():
    query = "What is RAG?"

    response = handle_query(query)

    assert query in response
