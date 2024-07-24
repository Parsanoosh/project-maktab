from enum import Enum

class JobAndUserError(Exception):
    """Base class for exceptions in this module."""

class InvalidNameError(JobAndUserError):
    """Exception raised for invalid names."""
    def __init__(self, message="Invalid name"):
        super().__init__(message)

class InvalidAgeError(JobAndUserError):
    """Exception raised for invalid age."""
    def __init__(self, message="Invalid age"):
        super().__init__(message)

class InvalidTimeConditionError(JobAndUserError):
    """Exception raised for invalid time conditions."""
    def __init__(self, message="Invalid time condition"):
        super().__init__(message)

class InvalidSalaryError(JobAndUserError):
    """Exception raised for invalid salary."""
    def __init__(self, message="Invalid salary"):
        super().__init__(message)

class TimeCondition(Enum):
    FULLTIME = 'FULLTIME'
    PARTTIME = 'PARTTIME'
    PROJECT = 'PROJECT'

class Job:
    """Job Class"""
    _id_counter = 1
    job_list = {}

    def __init__(self, name, min_age, max_age, time_condition, salary):
        self.id = Job._id_counter
        Job._id_counter += 1
        self.name = name
        self.min_age = min_age
        self.max_age = max_age
        self.time_condition = time_condition
        self.salary = salary
        self.views = 0
        self.skill_views = {}

    def __str__(self):
        return f'Job {self.id}: {self.name}, Age Range: {self.min_age}-{self.max_age}, Time: {self.time_condition}, Salary: {self.salary}'

    def validate(self):
        if not self.is_valid_name(self.name):
            raise InvalidNameError()
        if not self.is_valid_age(self.min_age, self.max_age):
            raise InvalidAgeError()
        if not self.is_valid_time_condition(self.time_condition):
            raise InvalidTimeConditionError()
        if not self.is_valid_salary(self.salary):
            raise InvalidSalaryError()

    def increment_view(self, skill):
        self.views += 1
        self.skill_views[skill] = self.skill_views.get(skill, 0) + 1

    @staticmethod
    def is_valid_name(name):
        return 1 <= len(name) <= 10 and name.isalpha()

    @staticmethod
    def is_valid_age(min_age, max_age):
        return 0 <= min_age <= 200 and 0 <= max_age <= 200 and min_age <= max_age

    @staticmethod
    def is_valid_time_condition(condition):
        return condition in TimeCondition

    @staticmethod
    def is_valid_salary(salary):
        return 0 <= salary < 1_000_000_000 and salary % 1000 == 0

class User:
    """User Class"""
    _id_counter = 1
    user_list = {}

    def __init__(self, name, age, time_condition, salary):
        self.id = User._id_counter
        User._id_counter += 1
        self.name = name
        self.age = age
        self.time_condition = time_condition
        self.salary = salary
        self.total_views = 0
        self.skill_views = {}

    def __str__(self):
        return f'User {self.id}: {self.name}, Age: {self.age}, Time: {self.time_condition}, Salary: {self.salary}'

    def validate(self):
        if not self.is_valid_name(self.name):
            raise InvalidNameError()
        if not self.is_valid_age(self.age):
            raise InvalidAgeError()
        if not self.is_valid_time_condition(self.time_condition):
            raise InvalidTimeConditionError()
        if not self.is_valid_salary(self.salary):
            raise InvalidSalaryError()

    def view_job(self, job_id, job_dict):
        if job_id not in job_dict:
            print("Invalid job ID")
            return
        
        job = job_dict[job_id]
        if not self.skill_views:
            print("User has no skills to view the job")
            return

        for skill in self.skill_views.keys():
            job.increment_view(skill)
            self.total_views += 1

        print("Job viewed successfully")

    @staticmethod
    def is_valid_name(name):
        return 1 <= len(name) <= 10 and name.isalpha()

    @staticmethod
    def is_valid_age(age):
        return 0 <= age <= 200

    @staticmethod
    def is_valid_time_condition(condition):
        return condition in TimeCondition

    @staticmethod
    def is_valid_salary(salary):
        return 0 <= salary < 1_000_000_000 and salary % 1000 == 0

def display_job_status(job_id, job_dict):
    if job_id not in job_dict:
        print("Invalid job ID")
        return

    job = job_dict[job_id]
    skill_views_output = ", ".join(f"{skill},{count}" for skill, count in job.skill_views.items())
    print(f"{job.name}-{job.views}-({skill_views_output})" if job.skill_views else f"{job.name}-{job.views}-")

def display_user_status(user_id, user_dict):
    if user_id not in user_dict:
        print("Invalid user ID")
        return

    user = user_dict[user_id]
    skill_views_output = ", ".join(f"{skill},{count}" for skill, count in user.skill_views.items())
    print(f"{user.name}-({skill_views_output})" if user.skill_views else f"{user.name}-")

def add_skill_to_job(job_id, skill, job_dict):
    if job_id not in job_dict:
        raise JobAndUserError("Invalid job ID")

    job = job_dict[job_id]
    if skill in job.skill_views:
        raise JobAndUserError("Skill already exists in job")

    job.skill_views[skill] = 0
    print("Skill added to job")

def add_skill_to_user(user_id, skill, user_dict):
    if user_id not in user_dict:
        raise JobAndUserError("Invalid user ID")

    user = user_dict[user_id]
    if skill in user.skill_views:
        raise JobAndUserError("Skill already exists for user")

    user.skill_views[skill] = 0
    print("Skill added to user")

users = {}
jobs = {}

num_skills = int(input())
global_skills = set(input().split()[:num_skills])

n = int(input())
for _ in range(n):
    command, *data = input().split()

    try:
        if command == "ADD-JOB":
            job = Job(data[0], int(data[1]), int(data[2]), data[3], int(data[4]))
            job.validate()
            jobs[job.id] = job
            print(f"Job ID is {job.id}")

        elif command == "ADD-USER":
            user = User(data[0], int(data[1]), data[2], int(data[3]))
            user.validate()
            users[user.id] = user
            print(f"User ID is {user.id}")

        elif command == "ADD-JOB-SKILL":
            add_skill_to_job(int(data[0]), data[1], jobs)

        elif command == "ADD-USER-SKILL":
            add_skill_to_user(int(data[0]), data[1], users)

        elif command == "VIEW":
            user_id = int(data[0])
            job_id = int(data[1])
            if user_id in users:
                users[user_id].view_job(job_id, jobs)
            else:
                print("Invalid user ID")

        elif command == "JOB-STATUS":
            job_id = int(data[0])
            display_job_status(job_id, jobs)

        elif command == "USER-STATUS":
            user_id = int(data[0])
            display_user_status(user_id, users)

    except JobAndUserError as e:
        print(e)
