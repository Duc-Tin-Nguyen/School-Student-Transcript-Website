# Student Population Management System

## Overview
This project is designed to manage and display student population data, grades, and course information using a web interface. It connects to an H2 database to fetch and display relevant data dynamically. The system allows users to view student populations by major, their grades, and course information.

## Project Structure
The project consists of the following main components:

- **HTML Files**: 
  - `Welcome_Page.html`: The landing page that displays welcome messages and student population statistics.
  - `Population.html`: Displays student and course information.
  - `Grade.html`: Shows individual student grades.
  - `students_row_fragment.html`: Template for rendering student rows in the population table.
  - `grade_row_fragment.html`: Template for rendering grade rows in the grade table.
  - `courses_row_fragments.html`: Template for rendering course rows in the population table.

- **Python Scripts**:
  - `Welcome_Page.py`: Connects to the H2 database, retrieves student population data, and generates the welcome page.
  - `Population.py`: Connects to the H2 database, retrieves student and course data, and generates population HTML files for each major.
  - `Grade.py`: Connects to the H2 database, retrieves grades for each student, and generates individual grade HTML files.

## Installation
1. Ensure you have Python installed on your machine.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the H2 database and place the `h2-2.1.214.jar` file in the project directory (not visible now due to data privacy)

## Usage
1. Start the H2 database server.
2. Run the `Welcome_Page.py` script to generate the welcome page:
   ```bash
   python src/Welcome_Page.py
   ```
3. Run the `Population.py` script to generate population HTML files for each major:
   ```bash
   python src/Population.py
   ```
4. Run the `Grade.py` script to generate grade HTML files for each student:
   ```bash
   python src/Grade.py
   ```
5. Open the generated HTML files in a web browser to view the data.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Thanks to the contributors and libraries that made this project possible.
