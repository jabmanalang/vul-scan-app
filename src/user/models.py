from sqlalchemy.orm import Mapped, mapped_column

from src.database.session import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
