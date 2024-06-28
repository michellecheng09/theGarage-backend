from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

json = {
  "similarity_score": 0.8463
}

class ResumeJobPair(BaseModel):
    resume: str
    job_description: str


@app.post("/match")
def match_resumes(pair: ResumeJobPair):
    resume = pair.resume
    job_description = pair.job_description

    documents = [resume, job_description]

    # Vectorize the documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compute the cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    similarity_score = similarity_matrix[0][1]

    return {"similarity_score": similarity_score}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
