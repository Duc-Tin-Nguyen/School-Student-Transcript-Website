import jaydebeapi

emails = ['albina.glick@epita.fr','ammie.corrio@epita.fr','bernardo.figeroa@epita.fr','bette.nicka@epita.fr','blondell.pugh@epita.fr','cammy.albares@epita.fr','carmelina.lindall@epita.fr','cecily.hollack@epita.fr','danica.bruschke@epita.fr','delmy.ahle@epita.fr','dominque.dickerson@epita.fr','donette.foller@epita.fr','elza.lipke@epita.fr','emerson.bowley@epita.fr','erick.ferencz@epita.fr','ernie.stenseth@epita.fr','francine.vocelka@epita.fr','gladys.rim@epita.fr','jamal.vanausdal@epita.fr','jina.briddick@epita.fr','kallie.blackwood@epita.fr','kanisha.waycott@epita.fr','kati.rulapaugh@epita.fr','kiley.caldarera@epita.fr','kris.marrier@epita.fr','lai.gato@epita.fr','laurel.reitler@epita.fr','lavera.perin@epita.fr','leota.dilliard@epita.fr','lettie.isenhower@epita.fr','malinda.hochard@epita.fr','marjory.mastella@epita.fr','maryann.royster@epita.fr','minna.amigon@epita.fr','moon.parlato@epita.fr','myra.munns@epita.fr','natalie.fern@epita.fr','rozella.ostrosky@epita.fr','sage.wieser@epita.fr','simona.morasca@epita.fr','solange.shinko@epita.fr','tamar.hoogland@epita.fr','tawna.buvens@epita.fr','timothy.mulqueen@epita.fr','tonette.wenner@epita.fr','tyra.shields@epita.fr','veronika.inouye@epita.fr','viva.toelkes@epita.fr','wilda.giguere@epita.fr','yuki.whobrey@epita.fr']
original_file = 'Grade.html'


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
for email in emails:
    new_file = f'{email}_GRADE.html'

    connection: jaydebeapi.Connection = jaydebeapi.connect("org.h2.Driver", url, [user, password], path_to_h2_jar)
    curs: jaydebeapi.Cursor = connection.cursor()

    # Execute last query
    curs.execute(
        f"SELECT s.STUDENT_EPITA_EMAIL, c.CONTACT_FIRST_NAME, c.CONTACT_LAST_NAME, g.GRADE_COURSE_CODE_REF, g.GRADE_SCORE "
        f"FROM STUDENTS s "
        f"JOIN CONTACTS c ON s.STUDENT_CONTACT_REF = c.CONTACT_EMAIL "
        f"JOIN GRADES g ON s.STUDENT_EPITA_EMAIL = g.GRADE_STUDENT_EPITA_EMAIL_REF "
        f"WHERE s.STUDENT_EPITA_EMAIL LIKE '{email}%' "
    )
 
    results = curs.fetchall()

    data: list[tuple] = results

    # Create file name based on major
    new_file = f'{email}_grade.html'
    
    # Read HTML file
    with open(original_file, 'r') as f:
        html = f.read()
    
    with open('./grade_row_fragment.html', 'r') as file:
        grade_rows_template = file.read() 

    grade_row_html = ''
    for i, tup in enumerate(data):
        temp = grade_rows_template.replace(r'%student_email%', tup[0])
        temp = temp.replace(r'%student_fname%', tup[1])
        temp = temp.replace(r'%student_lname%', tup[2])
        temp = temp.replace(r'%course_id%',tup[3])
        temp = temp.replace(r'%grade%', str(tup[4]))
        grade_row_html += temp
        
    html = html.replace("%grade_rows%", grade_row_html)  
    with open(new_file, 'w') as f: 
        f.write(html)

    print(f'Created {new_file}')