from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Transfer = Table('Transfer', pre_meta,
    Column('transferid', VARCHAR(length=16), primary_key=True, nullable=False),
    Column('date', DATETIME),
    Column('sourceid', VARCHAR(length=16)),
    Column('destid', VARCHAR(length=16)),
    Column('amount', INTEGER),
)

User = Table('User', pre_meta,
    Column('userid', VARCHAR(length=16), primary_key=True, nullable=False),
    Column('password', VARCHAR(length=16)),
    Column('balance', INTEGER),
)

transfers = Table('transfers', post_meta,
    Column('transferid', String(length=16), primary_key=True, nullable=False),
    Column('date', DateTime),
    Column('sourceid', String(length=16)),
    Column('destid', String(length=16)),
    Column('amount', Integer),
)

users = Table('users', post_meta,
    Column('userid', String(length=16), primary_key=True, nullable=False),
    Column('password', String(length=16)),
    Column('balance', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Transfer'].drop()
    pre_meta.tables['User'].drop()
    post_meta.tables['transfers'].create()
    post_meta.tables['users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Transfer'].create()
    pre_meta.tables['User'].create()
    post_meta.tables['transfers'].drop()
    post_meta.tables['users'].drop()
