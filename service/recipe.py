from fastapi import HTTPException, status
from bson import ObjectId
import pymongo

from scheme.scheme import Recipe

class PostSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = pymongo.MongoClient(*args, **kwargs)
            cls._instance.db = cls._instance.client.get_database("blog")
            cls._instance.collection = cls._instance.db.get_collection("posts")
        return cls._instance

    def get_posts(self):
        data = [{**post, '_id': str(post['_id'])} for post in self.collection.find()]
        if data:
            return dict(zip(range(1, len(data) + 1), data))
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        
    def get_post(self, post_id: str):
        if data:= self.collection.find_one({"_id": ObjectId(post_id)}):
            return data
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

    def add_post(self, post_data: Recipe):
        result=self.collection.insert_one(post_data.dict())
        if not result.acknowledged:
            raise HTTPException(status.HTTP_409_CONFLICT)
        return {"id": str(result.inserted_id)}

    def delete_post(self, post_id: str):
        result = self.collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    def delete_all_posts(self):
        result = self.collection.delete_many({})
        if result.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    def update_post(self, post_id: str, new_data: Recipe):
        result = self.collection.update_one({"_id": ObjectId(post_id)}, {"$set": new_data.dict()})
        if result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")