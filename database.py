from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://michelleCheng:<PASSWORD>@cluster0.4yijmgs.mongodb.net/masterdatabase?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Create an AsyncIO client for asynchronous operations
async_client = AsyncIOMotorClient(uri)
database = async_client.get_database()
resumes_collection = database.get_collection("resumes")
job_descriptions_collection = database.get_collection("job_descriptions")