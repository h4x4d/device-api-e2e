import json
from typing import List

import allure
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from framework.sql.act_device_api_models import DevicesEvent
from sqlalchemy.dialects import postgresql


json_serializable = [str, int, bool, dict, list]


def log_sql(sql):
    query = sql.statement.compile(dialect=postgresql.dialect())

    results = sql.all()

    allure.attach(str(query), "SQL Query", allure.attachment_type.TEXT)
    allure.attach(json.dumps([obj.serialize() for obj in results]), "SQL Result", allure.attachment_type.JSON)


class Alchemy:
    def __init__(self, dsn: str):
        engine = create_engine(dsn)
        self.session_factory = sessionmaker(bind=engine)

    def entries_by_id(self, device_id: int) -> List[DevicesEvent]:
        session = self.session_factory()

        sql = session.query(DevicesEvent).filter_by(device_id=device_id)

        log_sql(sql)

        return sql.all()

    def first_edit_event(self) -> DevicesEvent:
        session = self.session_factory()

        sql = session.query(DevicesEvent).filter_by(type=2)
        log_sql(sql)

        return sql.first()
