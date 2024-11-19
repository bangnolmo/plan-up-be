from app.domain.entities.department import Department
import app.database.database as db

db.create_department_table()
db.insert_department()