from fastapi import FastAPI, Depends, status, HTTPException, Response
from app.database import Database
from typing import Tuple, List
from dicttoxml import dicttoxml
from json import loads
import json
import requests
from app.database import get_database, sqlalchemy_engine
from app.models import metadata, PostDB, PostCreate, PostBase, posts

app = FastAPI()


@app.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


async def call_api():
    request_url = f'https://jsonplaceholder.typicode.com/posts'
    resp = requests.get(request_url)
    data = resp.content
    response_data = json.loads(data.decode('utf-8').replace('\n', ''))
    print(resp.content.strip())
    return response_data


async def get_post_or_404(
    id: int, database: Database = Depends(get_database)
) -> PostDB:
    select_query = posts.select().where(posts.c.id == id)
    raw_post = await database.fetch_one(select_query)

    if raw_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return PostDB(**raw_post)


@app.get("/posts")
async def list_posts(
    database: Database = Depends(get_database),
) -> List[PostDB]:
    select_query = posts.select()
    rows = await database.fetch_all(select_query)
    results = [PostDB(**row) for row in rows]
    return results


@app.get("/postsjson/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)) -> PostDB:
    return post


@app.get("/postsxml/{id}", response_model=PostDB)
async def get_post(post: PostDB = Depends(get_post_or_404)):
    json_data = post.json()
    xml_data = dicttoxml(loads(json_data))
    print(xml_data)
    return Response(content=xml_data, media_type="application/xml")


@app.post("/posts", response_model=PostDB, status_code=status.HTTP_201_CREATED)
async def create_post(
    post: PostCreate, database: Database = Depends(get_database)
) -> PostDB:
    insert_query = posts.insert().values(post.dict())
    post_id = await database.execute(insert_query)
    post_db = await get_post_or_404(post_id, database)

    return post_db


@app.get("/postsupdate/{id}")
async def load_post(id: int, database: Database = Depends(get_database)):
    request_url = f'https://jsonplaceholder.typicode.com/posts/{id}'
    resp = requests.get(request_url)
    data = resp.content
    response_data = json.loads(data.decode('utf-8').replace('\n', ''))
    post_id = response_data['id']
    select_query = posts.select().where(posts.c.id == post_id)
    raw_post = await database.fetch_one(select_query)
    if raw_post is not None:
        return {"message":"Data found in Database, cannot insert"}
    else:
        post_id = response_data['id']
        post_title = response_data['title']
        post_body = response_data['body']
        post_dict = {"id":post_id, "title":post_title, "body":post_body}
        insert_query = posts.insert().values(post_dict)
        post_insert = await database.execute(insert_query)
    print(raw_post)
    return post_insert


@app.get("/")
async def root():
    result_1 = await call_api()
    return result_1



