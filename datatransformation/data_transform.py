from fastapi import FastAPI, Depends, status, HTTPException, Response
from app.database import get_database, sqlalchemy_engine
from app.models import employees, courses, employees_courses, metadata
from app.database import Database

app = FastAPI()


@app.on_event("startup")
async def startup():
    await get_database().connect()
    metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await get_database().disconnect()


@app.get('/courses')
async def get_courses(database: Database = Depends(get_database)):
    # return {"name": "ramesh"}
    select_query = courses.select()
    rows = await database.fetch_all(select_query)
    return rows


@app.get('/employees')
async def get_courses(database: Database = Depends(get_database)):
    # return {"name": "ramesh"}
    select_query = employees.select()
    rows = await database.fetch_all(select_query)
    return rows


@app.get('/employeecourses')
async def get_courses(database: Database = Depends(get_database)):
    # return {"name": "ramesh"}
    select_query = employees_courses.select()
    rows = await database.fetch_all(select_query)
    return rows


@app.post('/{emp_array}')
async def post_all_data(employee_array: list, database: Database = Depends(get_database)):
    for i in employee_array:
        # print(i)
        employee_name = i['name']
        employee_id = i['employee_id']
        #print(employee_id, employee_name)
        employee_dict = {"employee_id": employee_id, "name":employee_name}
        select_query = employees.select().where(employees.c.employee_id == employee_id)
        raw_employee = await database.fetch_one(select_query)
        #print(raw_employee)
        if raw_employee is None:
            #print("no employee id")
            insert_query = employees.insert().values(employee_dict)
            employee_insert = await database.execute(insert_query)
            print(employee_insert)
        for j in i['courses']:
            #print(j)
            course_name = j['name']
            course_dict = {"name": course_name}
            select_query = courses.select().where(courses.c.name == course_name)
            raw_course = await database.fetch_one(select_query)
            if raw_course is None:
                insert_query = courses.insert().values(course_dict)
                course_insert = await database.execute(insert_query)
                print(course_insert)
            emp_course_dict = {"employee_id": employee_insert, "course_id": course_insert}
            insert_query = employees_courses.insert().values(emp_course_dict)
            employee_course_insert = await database.execute(insert_query)
    return {"array": employee_array}
