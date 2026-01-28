from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated , Optional
from database import SessionLocal
from models.post import Post
from models.comment import Comment
from schemas.post import PostCreate, PostOut , PostUpdate
from schemas.comment import CommentCreate, CommentOut

router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# ------------------ POSTS ------------------

@router.post("/posts", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, db: db_dependency):
    new_post = Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/posts", response_model=list[PostOut]) # get all posts
def get_all_posts(db: db_dependency):
    posts = db.query(Post).all()
    return posts

@router.get("/posts/{post_id}", response_model=PostOut) # get post by id
def get_post(post_id: int, db: db_dependency):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# @router.put("/posts/{post_id}", response_model=PostOut)
# def update_post(post_id: int,
#                 post : PostCreate,
#                 db: db_dependency , 
#                 newTitle : Optional[str] = None ,
#                 newContent : Optional[str] = None 
#                 ):
#     post = db.query(Post).filter(Post.id == post_id).first()
#     if not post:
#         raise HTTPException(status_code=404, detail="Post not found")
    
#     if newTitle is not None and newTitle.strip():
#         post.title = newTitle
#     if newContent is not None and newContent.strip():
#         post.content = newContent


#     db.commit()
#     db.refresh(post)
#     return post

@router.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, update_data: PostUpdate, db: db_dependency):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if update_data.title and update_data.title.strip():
        post.title = update_data.title
    if update_data.content and update_data.content.strip():
        post.content = update_data.content

    db.commit()
    db.refresh(post)
    return post


@router.delete("/posts/{post_id}", status_code=status.HTTP_200_OK)
def delete_post(post_id: int, db: db_dependency):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}

# ------------------ COMMENTS ------------------

@router.post("/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def create_comment(comment: CommentCreate, db: db_dependency):
    new_comment = Comment(**comment.model_dump())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/comments", response_model=list[CommentOut])
def get_all_comments(db: db_dependency):
    comments = db.query(Comment).all()
    return comments

@router.get("/comments/{comment_id}", response_model=CommentOut)
def get_comment(comment_id: int, db: db_dependency):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, updated_comment: CommentCreate, db: db_dependency):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment.content = updated_comment.content
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
def delete_comment(comment_id: int, db: db_dependency):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}
