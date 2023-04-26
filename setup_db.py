from sqlalchemy.ext.declarative import declarative_base
from my_db import User, Quote, FavoriteQuote, Session, engine, Base


def create_default_user():
    with Session() as session:
        user = User(username="default_user", email="default_user@example.com", password="password")
        session.add(user)
        session.commit()


def create_default_quotes():
    with Session() as session:
        with open("text/quotes_list.txt") as f:
            lines = f.readlines()
            quotes = []
            for line in lines:
                text, author = line.strip().split("-")
                quote = Quote(text=text, author=author)
                quotes.append(quote)
            session.add_all(quotes)
            session.commit()


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    create_default_user()
    create_default_quotes()
   