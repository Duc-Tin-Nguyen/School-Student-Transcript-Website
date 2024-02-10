import os
import jaydebeapi

majors = ['AIs', 'CS', 'DSA', 'ISM', 'SE']

original_file = 'Population.html'

def connect(db_driver_path: str, db_url: str, db_user: str, db_password: str) -> jaydebeapi.Connection:
    """
    connects to the h2 database
    :return:f
    """
    conn = jaydebeapi.connect('org.h2.Driver', db_url, [db_user, db_password], db_driver_path)
    return conn

# TODO read those configuration entries from a configuration file
path_to_h2_jar: str = r'h2-2.1.214.jar'
url: str = 'jdbc:h2:tcp://localhost:9092/./DATABASEMIDTERMTESTPREP'
user: str = 'Tin'
password: str = ''

for major in majors:
    # Create file name based on major
    new_file = f'{major}_Population.html'

    connection: jaydebeapi.Connection = connect(path_to_h2_jar, url, user, password)
    curs: jaydebeapi.Cursor = connection.cursor()

    # Execute third query
    curs.execute(
        f"SELECT sub.STUDENT_EPITA_EMAIL, sub.CONTACT_FIRST_NAME, sub.CONTACT_LAST_NAME, "
        f"SUM(sub.COURSE_PASSED) AS PASSED, COUNT(sub.COURSE_PASSED) AS TOTAL "
        f"FROM (SELECT s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, g.GRADE_COURSE_CODE_REF, "
        f"CASE WHEN ROUND(SUM(g.GRADE_SCORE*e.EXAM_WEIGHT)/SUM(e.EXAM_WEIGHT)) >= 10 "
        f"THEN 1 ELSE 0 END AS COURSE_PASSED "
        f"FROM STUDENTS s "
        f"INNER JOIN CONTACTS c ON s.STUDENT_CONTACT_REF = c.CONTACT_EMAIL "
        f"INNER JOIN GRADES g ON s.STUDENT_EPITA_EMAIL = g.GRADE_STUDENT_EPITA_EMAIL_REF "
        f"INNER JOIN EXAMS e ON g.GRADE_COURSE_CODE_REF = e.EXAM_COURSE_CODE "
        f"WHERE s.STUDENT_POPULATION_CODE_REF LIKE '{major}%' "
        f"GROUP BY s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, g.GRADE_COURSE_CODE_REF) AS sub "
        f"GROUP BY sub.STUDENT_EPITA_EMAIL, sub.CONTACT_FIRST_NAME, sub.CONTACT_LAST_NAME"
    )

    # Store results of third query in a list
    data: list[tuple] = curs.fetchall()

    # Execute fourth query
    curs.execute(
       f"SELECT c.COURSE_CODE, c.COURSE_NAME, COUNT(*) AS session_count "
        f"FROM COURSES c "
        f"JOIN SESSIONS s ON c.COURSE_CODE = s.SESSION_COURSE_REF "
        f"JOIN PROGRAMS p ON c.COURSE_CODE = p.PROGRAM_COURSE_CODE_REF "
        f"WHERE p.PROGRAM_ASSIGNMENT LIKE '{major}%' "
        f"GROUP BY c.COURSE_CODE, c.COURSE_NAME"
    )

    # Store results of fourth query in a list
    value: list[tuple] = curs.fetchall()

    # Close the cursor and connection
    curs.close()
    connection.close()

    # Loop over majors and create a new HTML file for each one
for major in majors:
    # Create file name based on major
    new_file = f'{major}_Population.html'
    
    # Read HTML file
    with open(original_file, 'r') as f:
        html = f.read()
    
    # Replace population code placeholder with major
    html = html.replace('Population_Code', major)
    
    with open('./students_row_fragment.html', 'r') as file:
        students_rows_template = file.read() 

    students_rows_html = ''
    for i, tup in enumerate(data):
        student_grade_href = f"./{tup[0]}_GRADE.html"
        temp = students_rows_template.replace(r'%student_email%', tup[0])
        temp = temp.replace(r'%student_fname%', tup[1])
        temp = temp.replace(r'%student_lname%', tup[2])
        temp = temp.replace(r'%pass_count%', f'{tup[3]} / {tup[4]}')
        temp = temp.replace(r'%grades_href%', student_grade_href)
        students_rows_html += temp

    with open('./courses_row_fragments.html', 'r') as file:
        courses_row_template = file.read()
        
    courses_row_html = ''    
    for i, tup in enumerate(value):
        temp = courses_row_template.replace("%course_id%", tup[0])
        temp = temp.replace("%course_name%", str(tup[1]))
        temp = temp.replace("%sessions_count%", str(tup[2]))
        courses_row_html += temp
         
    html = html.replace("%student_rows%", students_rows_html)
    html = html.replace("%courses_rows%", courses_row_html)   
    with open(new_file, 'w') as f: 
        f.write(html)

    print(f'Created {new_file}')
