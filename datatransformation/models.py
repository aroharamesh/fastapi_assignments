from datetime import datetime
from typing import Optional

import sqlalchemy
from pydantic import BaseModel, Field


metadata = sqlalchemy.MetaData()


courses = sqlalchemy.Table(
    "courses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=False),
)


employees = sqlalchemy.Table(
    "employees",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("name", sqlalchemy.String(length=255), nullable=False),
    sqlalchemy.Column("employee_id", sqlalchemy.String(length=255), nullable=False),
)

employees_courses = sqlalchemy.Table(
    "employees_courses",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column(
        "employee_id", sqlalchemy.ForeignKey("employees.id", ondelete="CASCADE"), nullable=False
    ),
    sqlalchemy.Column(
        "course_id", sqlalchemy.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    ),
)