from fastapi import FastAPI,Depends,HTTPException, Query
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas
from auth import create_token,verify_token


# print("DATABASE:", engine.url.database)
# print("HOST:", engine.url.host)
# print("PORT:", engine.url.port)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# db ependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# login api
@app.post("/login")
def login():
    return{
        "access_token": create_token({"user":"admin"}),
        "token_type":"bearer"
    }

@app.get("/")
def home():
    return {
        "message": "Blog API started"
    }

# create blog(protected)
@app.post("/blogs",response_model = schemas.BlogResponse)
def create_blog(blog :schemas.BlogCreate,db : Session = Depends(get_db),user = Depends(verify_token)):
    new_blog = models.Blog(
        title = blog.title,
        content = blog.content

    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


#Read All Blog
@app.get("/blogs")
def get_blogs(page: int =1,
              limit: int = 5,
              search:str = Query(default=""),
              db: Session = Depends(get_db)):
    query = db.query(models.Blog)
    if search:
        query = query.filter(models.Blog.title.ilike(f"%{search}%"))

    total = query.count()
    start = (page-1)*limit
    blogs = query.offset(start).limit(limit).all()

    return{
        "page": page,
        "limit": limit,
        "total": total,
        "data":blogs
    }   

@app.get("/blogs/{id}",response_model=schemas.BlogResponse)
def get_blog(id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404,detail="blog not found")
    return blog


@app.put("/blogs/{id}",response_model=schemas.BlogResponse)
def update(id:int ,blog :schemas.BlogCreate,db :Session=Depends(get_db),user = Depends(verify_token)):
    existing_blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not existing_blog:
        raise HTTPException(status_code=404,detail="blog not found")
    existing_blog .title = blog.title
    existing_blog.content = blog.content


    db.commit()

    return existing_blog

# delete blog
@app.delete("/blogs/{id}")
def delete(id:int,db:Session = Depends(get_db),user = Depends(verify_token)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=404,detail="blog not found")

    blog.delete()
    db.commit()

    return {
        "message":"blog deleted sucessfully"
    }