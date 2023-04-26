from fastapi import FastAPI, HTTPException, status, Header
from my_db import Session, User, Quote, FavoriteQuote
from models import CreateUser, LoginUser, LoginResponse
from sqlalchemy import exists, func
from sqlalchemy.exc import IntegrityError
from key import generate_api_key, check_api_key, hash_password
app = FastAPI()


@app.post("/login")
async def login(user: LoginUser):
    """
    Log in a user with provided email or username and password.

    Args:
        user (LoginUser): The login credentials of the user, containing either email or username and password.

    Returns:
        LoginResponse: A response containing a message, the username of the logged-in user, and an access token.

    Raises:
        HTTPException: If neither email nor username is provided, or if the provided credentials are invalid.
    """
    with Session() as session:
        if user.email:
            user_data = session.query(User).filter_by(email=user.email, password=hash_password(user.password)).one_or_none()
        elif user.username:
            user_data = session.query(User).filter_by(username=user.username, password=hash_password(user.password)).one_or_none()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either email or username must be provided",
            )
        if user_data:
            return LoginResponse(message="You have successfully logged in", username=user_data.username, access_token=user_data.api_key)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid email or password for {user.email or user.username}",
            )
        

@app.post("/register")
async def register(user: CreateUser):
    """
    Register a new user with a unique email and username.

    Args:
        user (CreateUser): The registration information of the user, containing a unique email, username, and password.

    Returns:
        dict: A response containing a success message and an API key for the registered user.

    Raises:
        HTTPException: If the provided email or username already exists in the database.
    """
    # Check if the username or email are exists before you register someone!
    with Session() as session:
        try:
            # Create a new user and add it to the session
            api_key = generate_api_key(user.email, user.username)
            user = User(username=user.username, email=user.email, password=hash_password(user.password),api_key=api_key)
            session.add(user)
            session.commit()
            
            return {"message": "Account has been registered successfully!","api_key":api_key}
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username or email already exists")
        
@app.get("/quotes")
async def get_quotes(api_key:str = Header(...)):
    """
    Get a list of all quotes in the database.

    Args:
        api_key (str): The API key of the user making the request.

    Returns:
        dict: A response containing the username of the user and a list of all quotes in the database.

    Raises:
        HTTPException: If the provided API key is invalid.
    """
    if user := check_api_key(api_key):
        with Session() as session:
                quotes = session.query(Quote).all()
                return {"user":user.username, "quotes":quotes}
    raise HTTPException(status_code=409, detail="Invalid api key")

@app.get("/qoute/random")
async def get_random_quote(api_key: str = Header(...)):
    """
    Get a random quote from the database.

    Args:
        api_key (str): The API key of the user making the request.

    Returns:
        dict: A response containing the text and author of the random quote.

    Raises:
        HTTPException: If the provided API key is invalid.
    """
    with Session() as session:
        if check_api_key(api_key):
            random_qoute = session.query(Quote).order_by(func.random()).first()
    return {"quote":random_qoute.text, "author": random_qoute.author}

@app.get("/quote/{quote_id}")
async def get_quote_by_id(quote_id: int, api_key: str = Header(...)):
    """
    Get a specific quote from the database by ID.

    Args:
        quote_id (int): The ID of the quote to retrieve.
        api_key (str): The API key of the user making the request.

    Returns:
        dict: A response containing the requested quote and the username of the user.

    Raises:
        HTTPException: If the provided API key is invalid or if the requested quote does not exist.
    """
    if user := check_api_key(api_key):
        with Session() as session:
            quote = session.query(Quote).filter_by(id=quote_id).one_or_none()
            if quote:
                return {"quote": quote, "user": user}
            else:
                raise HTTPException(status_code=404, detail="Quote not found")
    raise HTTPException(status_code=409, detail="Invalid api key")

# favorite a specific quote
@app.put("/quote/{quote_id}/favorite")
async def favorite_quote(quote_id: int, api_key: str = Header(...)):
    """
    Favorite a specific quote for the user with the provided API key.

    Args:
        quote_id (int): The ID of the quote to favorite.
        api_key (str): The API key of the user making the request.

    Returns:
        dict: A response containing a success message.

    Raises:
        HTTPException: If the provided API key is invalid, if the requested quote does not exist, or if the quote is already favorited by the user.
    """
    with Session() as session:
        if not session.query(exists().where(Quote.id == quote_id)).scalar():
            raise HTTPException(status_code=409, detail="Qoute is not found")
        elif not session.query(exists().where(User.api_key == api_key)).scalar():
            raise HTTPException(status_code=409, detail="Invalid api key")
        try:
            user = session.query(User).filter_by(api_key=api_key).one()
            quote = session.query(Quote).filter_by(id=quote_id).one()
            favorite = FavoriteQuote(user_id=user.id, quote_id=quote_id)
            session.add(favorite)
            session.commit()
            return {"message":f"{quote.text} by {quote.author} has been favorited successfully!"}
        except IntegrityError:
            session.rollback()
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The qoute already favorited")

@app.get("/quote/favorited")
async def get_favorited_quotes(api_key: str = Header(...)):
    """
    Get a list of all quotes favorited by the user with the provided API key.

    Args:
        api_key (str): The API key of the user making the request.

    Returns:
        dict: A response containing the username of the user and the list of qoutes favorited by the user.
    """
    if user := check_api_key(api_key):
        with Session() as session:
            favorites = session.query(FavoriteQuote).filter_by(user_id=user.id).all()
            qoutes_list = [x.quote_id for x in favorites]
            
            return {"user":user.username, "favorites":[session.query(Quote).filter_by(id=x).one() for x in qoutes_list]}
    raise HTTPException(status_code=409, detail="Invalid api key")

