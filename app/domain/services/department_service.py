from app.domain.entities.department import Department
import app.database.database as db

if __name__ == "__main__":
    db.create_department_table()