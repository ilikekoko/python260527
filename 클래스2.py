class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}")


class Manager(Person):
    def __init__(self, id, name, title):
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Title: {self.title}")


class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        print(f"ID: {self.id}, Name: {self.name}, Skill: {self.skill}")


if __name__ == '__main__':
    people = [
        Manager(1, '��μ�', '����'),
        Manager(2, '�̿���', '������Ʈ �Ŵ���'),
        Manager(3, '��ö��', '����'),
        Employee(4, '������', 'Python'),
        Employee(5, '���켺', 'Java'),
        Employee(6, '�Ѽҿ�', 'JavaScript'),
        Employee(7, '�۴���', '������ �м�'),
        Employee(8, '������', 'UI/UX ������'),
        Employee(9, '������', 'DevOps'),
        Employee(10, 'Ȳ����', 'AI/ML'),
    ]

    for person in people:
        person.printInfo()
