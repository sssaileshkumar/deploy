from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from pydantic import BaseModel, Field

from datetime import datetime

engine = create_engine("sqlite:///database.db")
LocalSession = sessionmaker(bind = engine)

class Base(DeclarativeBase):
   pass

def get_db() -> Session:
   db = LocalSession()
   
   try:
      yield db
   finally:
      db.close()

class Tweet(Base):
   __tablename__ = "tweets"

   id : int = Column(Integer, primary_key = True, index = True)
   username : str = Column(String)
   content : str = Column(String)
   created_at : datetime = Column(DateTime, default = datetime.now)

class CreateTweet(BaseModel):
   username : str = Field()
   content : str = Field()

class PublicTweet(BaseModel):
   id : int = Field()
   username : str = Field()
   content : str = Field()
   created_at : datetime = Field()

Base.metadata.create_all(bind = engine)

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins = ["*"],
   allow_methods = ["*"],
   allow_headers = ["*"],
   allow_credentials = True,
)

@app.post("/tweets")
def postTweet(data : CreateTweet, db : Session = Depends(get_db)):
   new_tweet = Tweet(username = data.username, content = data.content)

   try:
      db.add(new_tweet)
      db.commit()
      db.refresh(new_tweet)
      return {"message" : "tweeted"}
   except Exception as e:
      db.rollback()
      return {"message" : f"{e}"}

def tweet_to_dict(tweet : Tweet) -> dict:
   return {
		"id" : tweet.id,
		"username" : tweet.username,
		"content" : tweet.content,
		"create_at" : tweet.created_at
	}

@app.get("/tweets")
def getTweets(db : Session = Depends(get_db)):
   try:
      tweets = db.query(Tweet).order_by(Tweet.created_at.desc()).all()
      return [tweet_to_dict(tweet) for tweet in tweets]
   finally:
      db.close()