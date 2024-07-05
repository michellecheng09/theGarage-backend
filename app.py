from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from database import resumes_collection, job_descriptions_collection

app = FastAPI()

class JobDescription(BaseModel):
    id: str = Field(..., example="12345")
    department: str = Field(..., example="R&D")
    job: str = Field(..., example="Software Engineer")
    content: str = Field(..., example="We are looking for a software developer proficient in Python, JavaScript, and SQL...")

class Resume(BaseModel):
    id: str = Field(..., example="12345")
    name: str = Field(..., example="John Doe")
    age: int = Field(..., example=30)
    job: str = Field(..., example="Software Engineer")
    content: str = Field(..., example="Experienced software developer with expertise in Python, JavaScript, and SQL...")


@app.post("/match")
async def match_resumes(resume:Resume, job_description:JobDescription):
    resume_id=resume.id
    resume_name=resume.name
    resume_age=resume.age
    resume_job=resume.job
    resume_content = resume.content
    
    job_description_id=job_description.id
    job_description_department=job_description.department
    job_description_job=job_description.job
    job_description_content = job_description.content

    # Store the resume in the database
    resume_result = await resumes_collection.insert_one({"id":resume_id,"name":resume_name,"age":resume_age,"job title":resume_job,"content": resume_content})
    resume_id = str(resume_result.inserted_id)

    # Store the job description in the database
    job_description_result = await job_descriptions_collection.insert_one({"id":job_description_id,"department":job_description_department,"job title":job_description_job,"content": job_description_content})
    job_description_id = str(job_description_result.inserted_id)

    documents = [resume_content, job_description_content]

    # Vectorize the documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Compute the cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    similarity_score = similarity_matrix[0][1]

    return {"similarity_score": similarity_score, "resume_id": resume_id, "job_description_id": job_description_id}

@app.get("/resumes/{resume_id}")
async def read_resume(resume_id: str):
    resume = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume

@app.get("/job_descriptions/{job_description_id}")
async def read_job_description(job_description_id: str):
    job_description = await job_descriptions_collection.find_one({"_id": ObjectId(job_description_id)})
    if job_description is None:
        raise HTTPException(status_code=404, detail="Job description not found")
    return job_description

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
