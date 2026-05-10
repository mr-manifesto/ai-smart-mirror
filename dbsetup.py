import sqlite3 as sq

con = sq.connect("smartMirror.db")
cursor = con.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS studentInfo(
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    year INTEGER,
    branch TEXT,
    section TEXT,
    attendence INTEGER
)
""")

cursor.execute("""
INSERT OR REPLACE INTO studentInfo(id, name, year, branch, section, attendence)
VALUES ("22L31A0433", "Ch.Dhanush" , 4 , "ECE" , "A", 100)
""")

cursor.execute("""
INSERT OR REPLACE INTO studentInfo(id, name, year, branch, section, attendence)
VALUES ("22L31A0431", "Ch.Hemanth Kumar" , 4 , "ECE" , "A", 100)
""")

cursor.execute("""
INSERT OR REPLACE INTO studentInfo(id, name, year, branch, section, attendence)
VALUES ("23L35A0404", "Ch.Dhanasree" , 4 , "ECE" , "A", 100)
""")

cursor.execute("""
INSERT OR REPLACE INTO studentInfo(id, name, year, branch, section, attendence)
VALUES ("22L31A0414", "B.Grace" , 4 , "ECE" , "A", 100)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS lecturerInfo (
    id TEXT PRIMARY KEY,
    name TEXT,
    department TEXT,
    subject TEXT,
    experience TEXT
)
""")

cursor.execute("""
INSERT OR REPLACE INTO lecturerInfo(id, name, department, subject, experience)
VALUES ("001", "DR.sumadeep", "ECE", "Computer Vision", "10 years")
""")

cursor.execute("""
INSERT OR REPLACE INTO lecturerInfo(id, name, department, subject, experience)
VALUES ("002", "DR.A.Naga Jyoti", "ECE", "MWOC", "8 years")
""")

cursor.execute("""
INSERT OR REPLACE INTO lecturerInfo(id, name, department, subject, experience)
VALUES ("003", "Mrs.B.Maha lakshmi", "ECE", "Machine Learning", "12 years")
""")


con.commit()
con.close()

print("Database created successfully💥")