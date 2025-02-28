import re

class Course:
    def __init__(self, course_code, course_credit, course_name, course_description="", prereq_description=""):
        self.course_code = self.set_course_code(course_code)
        self.course_credit = course_credit
        self.course_name = course_name
        self.course_description = course_description
        self.prereq_description = prereq_description
        self.prereq_codes = self.get_prereq_codes()
        self.level = self.set_level()

    def __eq__(self, other):
        return (
                self.course_code == other.course_code and
                self.course_credit == other.course_credit and
                self.course_name == other.course_name and
                self.course_description == other.course_description and
                self.prereq_description == other.prereq_description and
                self.prereq_codes == other.prereq_codes and
                self.level == other.level
        )

    def __str__(self):
        prerequisites_desc_message = self.prereq_description if self.prereq_description else "No prerequisites"
        course_desc_message = self.course_description if self.course_description else "No description"

        message = (
            f"======== {__class__.__name__} Object ========\n" +
            f"Course Code: {self.course_code}\n" +
            f"Course Credit: {self.course_credit}\n" +
            f"Course Name: {self.course_name}\n" +
            f"Course Description: {course_desc_message}\n" +
            f"Prerequisites: {prerequisites_desc_message}\n" +
            f"Level: {self.level}\n" +
            "==============================="
        )

        return message

    def set_course_code(self, course_code):
        pattern = r"^([A-Za-z]{1,3}) ?(\d{4})([A-Za-z]?)$"
        match = re.fullmatch(pattern, course_code)

        if match:
            groups = match.groups()

            return groups[0].upper() + " " + groups[1] + groups[2].upper()
        else:
            return "INVALID"

    def set_level(self):
        highest_undergrad_first_digit = 4
        highest_grad_first_digit = 6
        invalid_level_name = "INVALID"

        for char in self.course_code:
            if char.isdigit():
                first_digit = int(char)

                if highest_undergrad_first_digit < first_digit <= highest_grad_first_digit:
                    level = "Graduate"
                elif 0 < first_digit <= highest_undergrad_first_digit:
                    level = "Undergraduate"
                else:
                    level = invalid_level_name

                return level

        return invalid_level_name

    def get_prereq_codes(self):
        return []


def test():
    # Area to test new features added to the class in this file.
    p1 = Course("cal1201", 3, "Calc 1")
    p2 = Course("cal1202", 3, "Calc 2")
    p3 = Course("cal1201", 3, "Calc 1")
    c1 = Course("maP3202", 3, "Diff Eq")

    print(c1)
    c1.prereqs = [p1, p2]
    c2 = Course("MAP 3202", 3, "Diff Eq")
    c2.prereqs = [p3, p2]

    print(c1)
    print(c2)
    print(c1==c2)

if __name__ == "__main__":
    test()
