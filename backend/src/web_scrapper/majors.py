class Major:
    def __init__(self, name, total_credits, elective_credits, required_courses, critical_tracking):
        self.name = name

    def __str__(self):

        message = (
            f"======== {__class__.__name__} Object ========\n" +
            f"Name: {self.name}\n" +
            f"Total Credits Required: {self.total_credits}\n" +
            f"Elective Credits Required: {self.elective_credits}\n" +
            f"Required Courses: {self.required_courses}\n" +
            f"Critical Tracking Courses by Semester: {self.critical_tracking}\n"
            "==============================="
        )

        return message



def main():
    print("test")

if __name__ == "__main__":
    main()
