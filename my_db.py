from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    api_key = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=func.now())

    favorite_quotes = relationship("FavoriteQuote", back_populates="user")


class Quote(Base):
    __tablename__ = "quote"
    id = Column(Integer, primary_key=True)
    author = Column(String(50), nullable=False)
    text = Column(String(255), nullable=False)

    favorite_quotes = relationship("FavoriteQuote", back_populates="quote")


class FavoriteQuote(Base):
    __tablename__ = "favorite_quote"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    quote_id = Column(Integer, ForeignKey("quote.id"), nullable=False)

    user = relationship("User", back_populates="favorite_quotes")
    quote = relationship("Quote", back_populates="favorite_quotes")

    __table_args__ = (UniqueConstraint("user_id", "quote_id"),)




        