from fastapi import HTTPException
from consistentpeer.constants.consistentpeer import driver

def add_vector_indexes():
    try:
        with driver.session() as session:
            review_embed_result = session.run(
                """
                CREATE VECTOR INDEX reviewEmbeddings IF NOT EXISTS
                FOR (r:Review)
                ON r.reviewEmbeddings
                OPTIONS {indexConfig: {
                `vector.similarity_function`: 'cosine'
                }}
                """
            )
            review_fulltext_result = session.run(
                """
                CREATE FULLTEXT INDEX reviewFullText IF NOT EXISTS
                FOR (r:Review)
                ON EACH [r.review]
                """
            )
        review_result = {
            "reviewEmbeddings": review_embed_result,
            "reviewFullText": review_fulltext_result
        }
        return review_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))