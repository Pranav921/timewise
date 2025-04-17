from itertools import product
from itertools import combinations
from data_templates.semester_course import SemesterCourse


class SemesterScheduler:
    def __init__(self, semester_class_codes):
        self.semester_class_codes = semester_class_codes  # give it a list of
        # course codes that the user wants to take for the semester
        self.semester_class_data = {}
        self.semester_courses_grouped_by_code = []
        self.valid_semester_schedules = []
        self.have_valid_semester_schedules = False

    def get_semester_class_data(self):
        pass
        # self.semester_class_data = func() # call webscrapper function that
        # (using the semester_course class as a data holder/template)
        # returns the data in dictionary form with the keys being the course
        # code and the values being a list of the semester_course objects
        # associated with said course code

    def get_all_valid_semester_schedules(self):
        self.semester_courses_grouped_by_code = list(
            self.semester_class_data.values())

        all_class_combos = list(product(*self.semester_courses_grouped_by_code))

        for class_combo in all_class_combos:
            valid_class_combo = True
            all_class_pairs = list(combinations(class_combo, 2))

            for class_pair in all_class_pairs:
                if not class_pair[0].is_compatible(class_pair[1]):
                    valid_class_combo = False
                    break

            if valid_class_combo:
                self.valid_semester_schedules.append(list(class_combo))

        if len(self.valid_semester_schedules) != 0:
            self.have_valid_semester_schedules = True

    def print_valid_semester_schedules(self):
        if self.have_valid_semester_schedules:
            for i, valid_semester_schedule in (
                    enumerate(self.valid_semester_schedules)):
                print(f"***************** Valid Schedule #{i+1} "
                      f"*****************")
                for j, course in enumerate(valid_semester_schedule):
                    print(f" --------------- Course #{j+1} ---------------")
                    print(course)
                print("*****************************************************")
        else:
            print("No valid semester schedule found.")
