import requests
from bs4 import BeautifulSoup
# Run as modules to prevent errors
from data_templates.course_template import Course
from web_scrapers.web_scrapers_util import remove_html_entities

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
            subjects_dict[f"{letter}"] = [
                li.text.strip() for li in ul.find_all("li")
            ]
            links_dict[f"{letter}"] = [
                a["href"] for a in ul.find_all("a")
            ]

    return subjects_dict, links_dict

def get_courses(subject_url, subject):
    response_2 = requests.get(subject_url)
    soup2 = BeautifulSoup(response_2.text, "html.parser")
    courses = []

    course_blocks = soup2.find_all("div",
                                   class_="courseblock courseblocktoggle")
    for block in course_blocks:
        try:
            title_tag = block.find("p", class_="courseblocktitle")
            description_tag = block.find("p", class_="courseblockdesc")
            prerequisite_tags = block.find_all(
                "p", class_="courseblockextra noindent"
            )

            if title_tag:
                title_text = title_tag.get_text(" ", strip=True)
                parts = title_text.split()
                code = " ".join(parts[:2])  # 1st two parts are the course code
                credits = parts[-2] if "Credit" in parts[-1] else ""
                name = " ".join(parts[2:-2] if credits else parts[2:])
                description = description_tag.get_text(" ", strip=True) if (
                    description_tag) else ""

                if len(prerequisite_tags) > 1:
                    prerequisite = prerequisite_tags[1].get_text(
                        " ", strip=True).replace("Prerequisite: ", "")
                    prerequisite = prerequisite.replace(" .", ".")
                    prerequisite = prerequisite.replace("( ", "(")
                    prerequisite = prerequisite.replace(" )", ")")
                    prerequisite = prerequisite.replace(" ,", ",")
                else:
                    prerequisite = "None"

                courses.append(
                    Course(
                        remove_html_entities(code),
                        remove_html_entities(credits),
                        remove_html_entities(name),
                        remove_html_entities(subject),
                        remove_html_entities(description),
                        remove_html_entities(prerequisite)
                    )
                )

        except Exception as e:
            print(f"Error parsing course: {e}")
            continue

    return courses


def runner():
    base_url = "https://catalog.ufl.edu"
    catalog_url = f"{base_url}/UGRD/courses"
    dicts = get_subjects(catalog_url)


    subj_dict = dicts[0]
    links_dict = dicts[1]
    all_courses = []
    for key, value in links_dict.items():
        for index, links in enumerate(value):
            subject_url = f"{base_url}{links}"
            print("Subject URL: " + subject_url)
            subj_courses = get_courses(subject_url, subj_dict[key][index])
            for subj in subj_courses:
                all_courses.append(subj)

    return all_courses


if __name__ == "__main__":
    runner()
