from sqlalchemy import *
from sqlalchemy import orm
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from feeder.settings import DATABASE_URL
from datetime import datetime
from sqlalchemy.dialects import postgresql
from psycopg2.extensions import register_adapter, AsIs, adapt, register_type
from sqlalchemy.dialects.postgresql import UUID
import arrow
import uuid
from feeder.settings import U3_ENV
from sqlalchemy.ext.compiler import compiles
import psycopg2.extras
import sqlalchemy.dialects.postgresql
from sqlalchemy.types import TypeEngine
from sqlalchemy.types import String
from sqlalchemy.types import TypeDecorator
import uuid

Base = declarative_base()


def adapt_arrow(arrow_date):
    return AsIs("'%s'::timestamptz" % str(arrow_date))


def adapt_dict(some_dict):
    return AsIs("'problem'")


register_adapter(arrow.Arrow, adapt_arrow)


class ArrayLike(TypeDecorator):
    """This works with PG and also with SQLite3."""
    impl = String

    def process_bind_param(self, value, dialect):
        if dialect.name is 'sqlite':
            return '||'.join(value)
        else:
            return value

    def process_result_value(self, value, dialect):
        if dialect.name is 'sqlite':
            return value.split('||')
        else:
            return value


def db_connect():
    return create_engine(DATABASE_URL, echo=False)


@compiles(UUID, 'sqlite')
def compile_UUID(element, compiler, **kw):
    return "varchar(36)"


@compiles(ArrayLike, 'sqlite')
def compile_Array(element, compiler, **kw):
    return "text"


@compiles(ArrayLike, 'postgresql')
def compile_Array_x(element, compiler, **kw):
    return "text[]"


class DBSource(Base):
    __tablename__ = 'sources_test' if 'test' in U3_ENV else 'sources'
    id = Column(UUID, primary_key=True, default=lambda: str(uuid.uuid4()))
    domain = Column(Unicode(100), nullable=False)
    scraped_at = Column(DateTime(timezone=True), default=datetime.utcnow(), nullable=False)
    scraped_url = Column(Unicode(400), nullable=False, unique=True)
    files = Column(ArrayLike(), nullable=True)
    file_urls = Column(ArrayLike(), nullable=True)
