import datetime
import uuid

from sqlalchemy import Integer, String, Column, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

CONN_STR = 'postgres://xxx:xxx@127.0.0.1:5432/xxx'


class DbBase(object):
    def as_dict(self):
        d = {}
        for c in self.__table__.columns:
            d[c.name] = getattr(self, c.name)
        return d


Base = declarative_base(cls=DbBase)


class TestTable(Base):
    __tablename__ = 'test_table'

    id = Column(Integer, primary_key=True, unique=True)
    uuid = Column(String(64), default=str(uuid.uuid4()), unique=True)
    name = Column(String(64), nullable=False)
    time_test_without_tz = Column(DateTime)
    time_test_with_tz = Column(DateTime(timezone=True))

    created_time = Column(DateTime, default=datetime.datetime.utcnow)
    updated_time = Column(DateTime, onupdate=datetime.datetime.utcnow)


class UTC(datetime.tzinfo):
    def __init__(self, offset=0):
        self._offset = offset

    def utcoffset(self, dt):
        return datetime.timedelta(hours=self._offset)

    def tzname(self, dt):
        return "UTC +%s" % self._offset

    def dst(self, dt):
        return datetime.timedelta(hours=self._offset)


if __name__ == '__main__':
    # engine = create_engine(CONN_STR, connect_args={"options": "-c timezone=utc"})
    engine = create_engine(CONN_STR, connect_args={"options": "-c timezone=Asia/Shanghai"})
    Base.metadata.create_all(engine, Base.metadata.tables.values(), checkfirst=True)

    session_factory = sessionmaker(bind=engine)
    db_session = scoped_session(session_factory)
    sess = db_session()

    print(datetime.datetime.now())
    print(datetime.datetime.now().timestamp())
    print(datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp(), tz=datetime.timezone.utc))
    print(datetime.datetime.now().tzname())

    print(datetime.datetime.now(tz=datetime.timezone.utc))
    print(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
    print(datetime.datetime.fromtimestamp(datetime.datetime.now(tz=datetime.timezone.utc).timestamp(),
                                          tz=datetime.timezone.utc))
    print(datetime.datetime.now(tz=datetime.timezone.utc).tzname())

    print(datetime.datetime.now(tz=UTC(8)))
    print(datetime.datetime.now(tz=UTC(8)).timestamp())
    print(datetime.datetime.fromtimestamp(datetime.datetime.now(tz=UTC(8)).timestamp(), tz=datetime.timezone.utc))
    print(datetime.datetime.now(tz=UTC(8)).tzname())

    tt01 = TestTable(**{
        "name": "AAA",
        "time_test_without_tz": datetime.datetime.now(),
        "time_test_with_tz": datetime.datetime.now()
    })
    try:
        sess.add(tt01)
        sess.commit()
    except Exception as e:
        print(e)
        sess.rollback()
    finally:
        sess.close()

    tts = []
    query = sess.query(TestTable)
    try:
        tts = query.all()
    except Exception as e:
        print(e)
        sess.rollback()
    finally:
        sess.close()
    for t in tts:
        print("{}, {}, {}, {}, {}, {}, {}".format(
            t.id,
            t.time_test_without_tz,
            t.time_test_without_tz.tzname(),
            datetime.datetime.fromtimestamp(t.time_test_without_tz.timestamp(), tz=datetime.timezone.utc),
            t.time_test_with_tz,
            t.time_test_with_tz.tzname(),
            datetime.datetime.fromtimestamp(t.time_test_with_tz.timestamp(), tz=datetime.timezone.utc)
        ))
