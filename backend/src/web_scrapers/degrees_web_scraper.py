import requests
from bs4 import BeautifulSoup
import re
import json
from pathlib import Path
import sys
from data_templates.certificate_template import Certificate
from data_templates.major_template import Major
from data_templates.minor_template import Minor

def print_semester_courses(courses_dict):
    for semester, courses in courses_dict.items():
        print(f"{semester}:")
        for course in courses:
            print(f"  - {course}")
        print()  # Add a blank line between semesters

def save_courses_to_json(courses_dict, filename):
    try:
        filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
        data_path = Path(__file__).resolve().parents[2] / 'data'
        data_path.mkdir(parents=True, exist_ok=True)  # Create it if it doesn't exist
        full_path = data_path / filename

        with open(full_path, 'w') as f:
            json.dump(courses_dict, f, indent=4)
        print(f"✅ Courses successfully saved to '{full_path}'")
    except Exception as e:
        print(f"❌ Failed to save courses: {e}")
        sys.exit(1)

# Get links on all majors, minors, and certificates offered at UF
def get_all_data(catalog_url):
    response = requests.get(catalog_url)
    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.find_all("li", id=lambda x: x and x.startswith("isotope-item"))

    all_data = {}
    for item in items:
        link = item.find("a")
        if link:
            name = link.get_text(strip=True)
            href = link.get("href")
            if name.lower() != "learn more":  # Filter out unwanted links
                all_data[name] = href

    return all_data

def split_dict(input_dict):
    minor = {}
    certificates = {}
    major = {}

    for key, value in input_dict.items():
        lowered_key = key.lower()
        if "minor" in lowered_key:
            minor[key] = value
        elif "certificate" in lowered_key:
            certificates[key] = value
        else:
            major[key] = value

    return minor, certificates, major

# Some formatting issues like in
# https://catalog.ufl.edu/UGRD/colleges-schools/UGART/ART_UCT06/
# College name structured differently so difficult to get name
# Credits don't display sometimes
# Sometimes required courses don't show up
# Possibly more issues as I have checked each individiual certificate
def get_certificate_data(dict):
    all_certificates = []
    max_val = 0
    base_url = "https://catalog.ufl.edu"
    counter = 0
    for name, value in dict.items():
        url = f"{base_url}{value}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        list_items = soup.find_all('li')
        p_elements = soup.find_all('p')
        print("Certificate URL: " + url)
        description = ' '.join([p.get_text() for p in soup.find_all('p') if 'certificate' in p.get_text().lower()])
        prerequisite_courses = []
        required_courses = []
        # Extract courses from Prerequisite Courses
        prerequisite_section = soup.find('h2', string='Prerequisite Courses')
        if prerequisite_section:
            prerequisite_table = prerequisite_section.find_next('table')
            if prerequisite_table:
                prerequisite_links = prerequisite_table.find_all('a', class_='bubblelink code')
                prerequisite_courses = [link.text.strip().replace('\xa0', '') for link in prerequisite_links]
        else:
            prerequisite_courses = []  # No prerequisite courses found

        # Extract courses from Required Courses
        required_section = soup.find('h2', string='Required Courses')
        if required_section:
            required_table = required_section.find_next('table')
            if required_table:
                required_links = required_table.find_all('a', class_='bubblelink code')
                required_courses = [link.text.strip().replace('\xa0', '') for link in required_links]
        credits = -1
        college_name = "-1"
        # Get all the College Names
        for li in list_items:
            if li.find('strong') and 'College:' in li.find('strong').text:
                college_name = li.find('a').text.strip()
            if li.find('strong') and 'Credits:' in li.find('strong').text:
                credits_text = li.text.strip()
                credits = re.search(r'\d+', credits_text.lstrip()).group()
        # scrape the admissions criteria (ex: https://catalog.ufl.edu/UGRD/colleges-schools/UGENG/ENG_UCT12/)
        # Add the electives
        certificate = Certificate(name, int(credits), description, college_name, "Work in Progress", "Undergraduate", required_courses, [])
        all_certificates.append(certificate)
        if len(description) > max_val:
            max_val = len(description)
        counter += 1
    return all_certificates

def get_minor_data(dict):
    all_minors = []
    base_url = "https://catalog.ufl.edu"
    for name, value in dict.items():
        url = f"{base_url}{value}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Minor URL: " + url)
        list_items = soup.find_all('li')
        p_elements = soup.find_all('p')
        description = ' '.join([p.get_text() for p in soup.find_all('p') if 'minor' in p.get_text().lower()])
        prerequisite_courses = []
        required_courses = []
        # Extract courses from Prerequisite Courses
        prerequisite_section = soup.find('h2', string='Prerequisite Courses')
        if prerequisite_section:
            prerequisite_table = prerequisite_section.find_next('table')
            if prerequisite_table:
                prerequisite_links = prerequisite_table.find_all('a', class_='bubblelink code')
                prerequisite_courses = [link.text.strip().replace('\xa0', '') for link in prerequisite_links]

        else:
            prerequisite_courses = []  # No prerequisite courses found

        # Extract courses from Required Courses
        required_section = soup.find('h2', string='Required Courses')
        if required_section:
            required_table = required_section.find_next('table')
            if required_table:
                required_links = required_table.find_all('a', class_='bubblelink code')
                required_courses = [link.text.strip().replace('\xa0', '') for link in required_links]
                or_cols = soup.find_all('td', class_='codecol orclass')
                for course in or_cols:
                    course_code = course.find('a').text
        college_name = "-1"
        credits = -1
        # Get all the College Names
        for li in list_items:
            if li.find('strong') and 'College:' in li.find('strong').text:
                college_name = li.text.strip()
                college_name = college_name.replace('College: ', '')
            if li.find('strong') and 'Credits:' in li.find('strong').text:
                credits_text = li.text.strip()
                credits = re.search(r'\d+', credits_text.lstrip())
                if credits:
                    credits = credits.group().strip()
                else:
                    credits = -1
        # Add non-eligible majors (ex:https://catalog.ufl.edu/UGRD/colleges-schools/UGENG/CIE_UMN/)
        minor = Minor(name, int(credits), description, college_name, "Work in Progress", "", "Undergraduate", required_courses, [])
        all_minors.append(minor)
    return all_minors

def get_major_data(majors_dict):
    base_url = "https://catalog.ufl.edu"
    all_majors = []

    for name, value in majors_dict.items():
        url = f"{base_url}{value}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        intro_text_div = soup.find('div', id='intro-text')
        description = str(intro_text_div.find_all('p')[0]) if intro_text_div else ''
        description = description.replace('<p>', '').replace('</p>', '')

        prerequisite_courses = []
        required_courses = []

        prerequisite_section = soup.find('h2', string='Prerequisite Courses')
        if prerequisite_section:
            prerequisite_table = prerequisite_section.find_next('table')
            if prerequisite_table:
                prerequisite_links = prerequisite_table.find_all('a', class_='bubblelink code')
                prerequisite_courses = [link.text.strip().replace('\xa0', '') for link in prerequisite_links]

        list_items = soup.find_all('li')
        credits = -1
        college_name = "-1"
        for li in list_items:
            if li.find('strong') and 'College:' in li.find('strong').text:
                college_name = li.text.strip().replace('College: ', '')
            if li.find('strong') and 'Credits for Degree:' in li.find('strong').text:
                credits_text = li.text.strip()
                match = re.search(r'\d+', credits_text)
                credits = match.group() if match else -1

        semester_url = f"{url}#modelsemesterplantext"
        sem_response = requests.get(semester_url)
        sem_soup = BeautifulSoup(sem_response.text, 'html.parser')
        required_courses = [link.text.strip().replace('\xa0', '') for link in
                            sem_soup.find_all('a', class_='bubblelink code')]
        credits = credits if credits is not None else "-1"

        major = Major(name, int(credits), description, college_name, "Work in Progress", "Undergraduate",
                      required_courses, [], "Elective Description Needed")
        print(major)
        all_majors.append(major)

    return all_majors

def four_year_plans(majors_dict):
    base_url = "https://catalog.ufl.edu"
    for name, value in majors_dict.items():
        url = f"{base_url}{value}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Major URL: " + url)

        semester_url = f"{url}#modelsemesterplantext"
        sem_response = requests.get(semester_url)
        sem_soup = BeautifulSoup(sem_response.text, 'html.parser')
        table = sem_soup.find('table', class_='sc_plangrid')

        semester_courses = {}
        course_credits = {}
        current_semester = None
        semester_count = 1

        if table:
            for tr in table.find_all('tr'):
                if 'plangridterm' in tr.get('class', []):
                    current_semester = f"Semester {semester_count}"
                    semester_courses[current_semester] = []
                    semester_count += 1
                elif current_semester and (codecell := tr.find(class_='codecol')):
                    course = codecell.get_text(strip=True).replace('\xa0', ' ')
                    course = f"{course} (CT)" if 'Critical Tracking' in tr.get_text() else course
                    course = course.replace('&', ' & ')
                    credit_cell = tr.find(class_='hourscol')
                    credits = credit_cell.get_text(strip=True) if credit_cell and credit_cell.get_text(
                        strip=True).isdigit() else None
                    course_credits[course] = credits
                    semester_courses[current_semester].append(course)

            for semester, courses in semester_courses.items():
                i = 0
                while i < len(courses):
                    if courses[i] == "Select one:" and i + 2 < len(courses):
                        combined = f"Select one: {courses[i + 1]} OR {courses[i + 2]}"
                        if "(CT)" in combined and courses[i + 1].endswith("(CT)") and courses[i + 2].endswith("(CT)"):
                            combined = combined.replace(" (CT)", "", 1)
                        courses[i] = combined
                        del courses[i + 1:i + 3]
                    else:
                        i += 1

            for semester, courses in semester_courses.items():
                for i, course in enumerate(courses):
                    if not course.startswith("Select one:"):
                        course_code = course.split(' (')[0].strip()
                        credits = course_credits.get(course, None)
                        if (not bool(re.search(r'\d{4}', course_code)) or '3000' in course_code) and credits:
                            courses[i] = f"{course} ({credits} credits)"

        print("Major Name: " + str(name))
        print_semester_courses(semester_courses)
        save_courses_to_json(semester_courses, str(name) + '.json')

# Code to run four_year plans to generate json files
# catalog_url = "https://catalog.ufl.edu/UGRD/programs/#filter=.filter_24"
# all_data = get_all_data(catalog_url) # Get links for all majors, minors, and certificates
# split_data = split_dict(all_data) # Split data into three dictionaries
# majors = split_data[2]
# four_year_plans(majors)
