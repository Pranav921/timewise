import asyncio
import asyncpg
import sys
# sys.path.append('my/path/to/module/folder')
print(sys.path)
sys.path.append("/Users/hieu/dev/timewise/backend/src")
from web_scrapers.degrees_web_scraper import get_all_data, split_dict, get_minor_data, get_certificate_data, get_major_data
from web_scrapers.courses_web_scraper import runner

catalog_url = "https://catalog.ufl.edu/UGRD/programs/#filter=.filter_24"
all_data = get_all_data(catalog_url) # Get links for all majors, minors, and certificates
split_data = split_dict(all_data) # Split data into three dictionaries
minors = split_data[0]
certificates = split_data[1]
majors = split_data[2]
all_minors = get_minor_data(minors)
all_certificates = get_certificate_data(certificates)
all_majors = get_major_data(majors)
all_courses = runner()

def format_array(lst):
    return "{" + ",".join(f'"{item}"' for item in lst) + "}" if lst else None

async def main():
    # Establish a connection to an existing database named "test"
    # as a "postgres" user.
    conn = await asyncpg.connect('postgresql://postgres:root@localhost/testdb')
    await conn.execute('''
        DROP TABLE IF EXISTS Minors;
        DROP TABLE IF EXISTS Majors;
        DROP TABLE IF EXISTS Certificates;
        DROP TABLE IF EXISTS Courses;
    ''')

    # Execute a statement to create a new table.
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS Minors (
             id SERIAL PRIMARY KEY,
             name TEXT NOT NULL,
             credit INT NOT NULL,
             description TEXT,
             college_under TEXT,
             admission_requirements TEXT,
             non_eligible_majors TEXT,
             lvl VARCHAR(50),
             required_courses TEXT[],
             electives TEXT[]
         );

        CREATE TABLE IF NOT EXISTS Majors (
             id SERIAL PRIMARY KEY,
             name TEXT NOT NULL,
             credit INT NOT NULL,
             description TEXT,
             college_under TEXT,
             admission_requirements TEXT,
             lvl VARCHAR(50),
             required_courses TEXT[],
             electives TEXT[],
             electives_desc TEXT
        );

        CREATE TABLE IF NOT EXISTS Certificates (
             id SERIAL PRIMARY KEY,
             name TEXT NOT NULL,
             credit INT NOT NULL,
             description TEXT,
             college_under TEXT,
             admission_requirements TEXT,
             lvl VARCHAR(50),
             required_courses TEXT[],
             electives TEXT[]
         );
         
         CREATE TABLE IF NOT EXISTS Courses (
             id SERIAL PRIMARY KEY,
             code TEXT NOT NULL,
             credit TEXT NOT NULL,
             name TEXT,
             subject TEXT,
             description TEXT,
             prereq_description TEXT,
             prereq_codes TEXT[],
             coreq_description TEXT,
             coreq_codes TEXT[],
             attribute TEXT,
             lvl VARCHAR(50)
         );
    ''')

    for major in all_majors:
        await conn.execute('''
            INSERT INTO Majors (name, credit, description, college_under, admission_requirements, lvl, required_courses, electives, electives_desc)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);
        ''', major.name, major.credit, major.description, major.college_under,
                           major.admission_requirements, major.level,
                           major.required_courses, major.electives, major.electives_desc)

    for certificate in all_certificates:
        await conn.execute('''
            INSERT INTO Certificates (name, credit, description, college_under, admission_requirements, lvl, required_courses, electives)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
        ''', certificate.name, certificate.credit, certificate.description, certificate.college_under,
                           certificate.admission_requirements, certificate.level,
                           certificate.required_courses, certificate.electives)

    for minor in all_minors:
        await conn.execute('''
            INSERT INTO Minors (name, credit, description, college_under, admission_requirements, non_eligible_majors, lvl, required_courses, electives)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);
        ''', minor.name, minor.credit, minor.description, minor.college_under,
                           minor.admission_requirements, minor.non_eligible_majors, minor.level,
                           minor.required_courses, minor.electives)

    for course in all_courses:
        await conn.execute('''
            INSERT INTO Courses (code, credit, name, subject, description, prereq_description, prereq_codes, coreq_description, coreq_codes, attribute, lvl)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
        ''', course.code, course.credit, course.name, course.subject,
                           course.description, course.prereq_description, course.prereq_codes, course.coreq_description,
                           course.coreq_codes, course.attribute, course.level)

    # Close the connection.
    await conn.close()

asyncio.run(main())