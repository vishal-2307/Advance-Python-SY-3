def uppercase(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper


def bold(func):
    def wrapper(*args, **kwargs):
        return "**" + func(*args, **kwargs) + "**"
    return wrapper


def add_border(func):
    def wrapper(*args, **kwargs):
        border = "-" * 40
        return border + "\n" + func(*args, **kwargs) + "\n" + border
    return wrapper


class Report:
    templates = {}

    def __init__(self, title, author="Unknown"):
        self.title = title
        self.author = author
        self.sections = []

    @classmethod
    def add_template(cls, name, section_list):
        cls.templates[name] = section_list
        print(f"Template '{name}' saved with sections: {section_list}")

    @classmethod
    def create_from_template(cls, template_name, title, author="Unknown"):
        new_report = cls(title, author)
        for heading in cls.templates[template_name]:
            new_report.add_section(heading, "content not filled yet")
        return new_report

    def add_section(self, heading, content):
        self.sections.append((heading, content))

    def fill_section(self, heading, content):
        for i in range(len(self.sections)):
            if self.sections[i][0] == heading:
                self.sections[i] = (heading, content)
                return True
        return False

    @bold
    @add_border
    def summary(self):
        return f"Report: {self.title} | Author: {self.author} | Sections: {len(self.sections)}"

    def __str__(self):
        text = f"REPORT: {self.title} (by {self.author})\n"
        for heading, content in self.sections:
            text += f" - {heading}: {content}\n"
        return text

    def __len__(self):
        return len(self.sections)

    def __getitem__(self, index):
        return self.sections[index]

    def __add__(self, other):
        combined = Report(self.title + " + " + other.title, self.author)
        combined.sections = self.sections + other.sections
        return combined

    def __eq__(self, other):
        return self.title == other.title and self.sections == other.sections


if __name__ == "__main__":
    Report.add_template("project_report", ["Introduction", "Result", "Conclusion"])

    r1 = Report.create_from_template("project_report", "My Mini Project", "Rahul")
    r1.fill_section("Introduction", "This project shows OOP concepts in Python.")
    r1.fill_section("Result", "The program worked correctly.")
    r1.fill_section("Conclusion", "Decorators and magic methods make code flexible.")

    r2 = Report("Attendance Report", "Rahul")
    r2.add_section("Summary", "92% attendance this month.")

    print(r1)
    print(len(r1))
    print(r1[0])

    combined = r1 + r2
    print(combined)

    print(r1 == r1)
    print(r1.summary())