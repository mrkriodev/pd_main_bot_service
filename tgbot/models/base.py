from sqlalchemy import (
    BigInteger,   
    MetaData,
    text,
)

from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
)

#from dexlotdb.config import settings
from .case_converter import camel_case_to_snake_case

naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Base(DeclarativeBase):
    created_at: Mapped[int | None] = mapped_column(
        BigInteger,
        server_default=text("(EXTRACT(EPOCH FROM NOW())::BIGINT * 1000)"),
    )
    updated_at: Mapped[int | None] = mapped_column(
        BigInteger,
        server_default=text("(EXTRACT(EPOCH FROM NOW())::BIGINT * 1000)"),
    )

    metadata = MetaData(
        naming_convention=naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
