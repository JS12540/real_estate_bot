from src.rag.retriever import Retriever

def test_retrieval_runs():
    r = Retriever()
    res = r.search("4 bedroom type B with pool", k=3)
    assert isinstance(res, list)
    if res:
        assert "page" in res[0] and isinstance(res[0]["page"], int)
