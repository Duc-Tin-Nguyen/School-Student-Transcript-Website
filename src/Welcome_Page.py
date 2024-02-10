import jaydebeapi
import matplotlib.pyplot as plt
import mpld3

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

connection: jaydebeapi.Connection = connect(path_to_h2_jar, url, user, password)
curs: jaydebeapi.Cursor = connection.cursor()

# Execute first query
curs.execute(
    'SELECT STUDENT_POPULATION_CODE_REF, COUNT(*) '
    'FROM STUDENTS s '
    'GROUP BY STUDENT_POPULATION_CODE_REF'
)

# Store results of first query in a list
data1: list[tuple] = curs.fetchall()

# Execute second query
curs.execute(
    'SELECT STUDENT_POPULATION_CODE_REF, sum(a.ATTENDANCE_PRESENCE) AS present_count, '
    'count(*)-sum(a.ATTENDANCE_PRESENCE) AS absent_count, count(*) AS total, '
    'sum(a.ATTENDANCE_PRESENCE)*100/count(*) AS percentage '
    'FROM STUDENTS s '
    'JOIN ATTENDANCE a ON s.STUDENT_EPITA_EMAIL = a.ATTENDANCE_STUDENT_REF '
    'GROUP BY STUDENT_POPULATION_CODE_REF'
)

# Store results of second query in a list
data2: list[tuple] = curs.fetchall()

# Close the cursor and connection
curs.close()
connection.close()

with open ("Welcome_Page.html", "r") as f: 
    html = f.read()
     
population_rows = ""
for i, tup in enumerate(data1):
    html = html.replace(f"Data {i*2+1}", str(tup[0]), 1)
    html = html.replace(f"Data {i*2+2}", str(tup[1]))


for i, tup in enumerate(data2):
    html = html.replace(f"Data {i*2+11}", str(tup[0]))
    html = html.replace(f"Data {i*2+12}", str(tup[4]))



with open ("Welcome_Page.html", "w") as f: 
    f.write(html)

import matplotlib.pyplot as plt

labels = [x[0] for x in data1]
values = [x[1] for x in data1]

plt.pie(values, labels=labels, autopct='%1.1f%%')

plt.title("Student Population")

plt.show()

labels = [x[0] for x in data2]
present_counts = [x[1] for x in data2]
absent_counts = [x[2] for x in data2]

bar_width = 0.35
r1 = range(len(present_counts))
r2 = [x + bar_width for x in r1]

plt.bar(r1, present_counts, color='b', width=bar_width, label='Present')
plt.bar(r2, absent_counts, color='r', width=bar_width, label='Absent')

plt.xlabel('Student Population')
plt.xticks([x + bar_width/2 for x in r1], labels)
plt.legend()

plt.show()









