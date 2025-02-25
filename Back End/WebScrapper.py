import requests
from bs4 import BeautifulSoup
from Course import Course

def get_subjects(catalog_url):
    response = requests.get(catalog_url)
    soup = BeautifulSoup(response.text, "html.parser")
    get_subjects = soup.find("div", class_="az_sitemap")
    subjects_dict = {}
    links_dict = {}
    for header in get_subjects.find_all("h2", class_="letternav-head"):
        letter = header.text.strip()
        subjects_dict[f"{letter}_subjects"] = []
        links_dict[f"{letter}_links"] = []

        ul = header.find_next_sibling("ul")  # Find the next <ul> after <h2>
        if ul:
            subjects_dict[f"{letter}_subjects"] = [li.text.strip() for li in ul.find_all("li")]
            links_dict[f"{letter}_links"] = [a["href"] for a in ul.find_all("a")]
    return subjects_dict, links_dict

def get_courses(subject_url):
    response_2 = requests.get(subject_url)
    soup2 = BeautifulSoup(response_2.text, "html.parser")
    courses = []

    course_blocks = soup2.find_all("div", class_="courseblock courseblocktoggle")
    for block in course_blocks:
        try:
            title_tag = block.find("p", class_="courseblocktitle")
            description_tag = block.find("p", class_="courseblockdesc")
            prerequisite_tags = block.find_all("p", class_="courseblockextra noindent")

            if title_tag:
                title_text = title_tag.get_text(" ", strip=True)
                parts = title_text.split()
                code = " ".join(parts[:2])  # First two parts are the course code
                credits = parts[-2] if "Credits" or "Credit" in parts[-1] else ""
                name = " ".join(parts[2:-2] if credits else parts[2:])

                description = description_tag.get_text(" ", strip=True) if description_tag else ""
                if len(prerequisite_tags) > 1:
                    prerequisite = prerequisite_tags[1].get_text(" ", strip=True).replace("Prerequisite: ", "")
                    prerequisite = prerequisite.replace(" .", ".")
                    prerequisite = prerequisite.replace("( ", "(")
                    prerequisite = prerequisite.replace(" )", ")")
                else:
                    prerequisite = "None"

                courses.append(Course(code, credits, name, description, prerequisite))
        except Exception as e:
            print(f"Error parsing course: {e}")
            continue
    return courses

def main():
    base_url = "https://catalog.ufl.edu"
    catalog_url = f"{base_url}/UGRD/courses"
    dicts = get_subjects(catalog_url)

    subj_dict = dicts[0]
    links_dict = dicts[1]

    for value in links_dict.values():
        for links in value:
            subject_url = f"{base_url}{links}"
            courses = get_courses(subject_url)
            print(links)
            for course in courses:
                print(course)

if __name__ == "__main__":
    main()
