from flask_login import UserMixin
import math


class User(UserMixin):
    def __init__(self, user_id, username, password, account_type, course_id):
        self.user_id = int(user_id)
        self.username = str(username)
        self.password = str(password)
        self.account_type = str(account_type)
        self.course_id = int(course_id)

    # https://stackoverflow.com/questions/37472870/login-user-fails-to-get-user-id
    def get_id(self):
        return (self.user_id)

    def get_user(self):
        return self.user_id, self.username, self.username, self.password, self.account_type, self.course_id


class Users:
    def __init__(self, user_id, user_name, user_created_at, user_deleted_at, user_state):
        self.user_id = int(user_id)
        self.user_name = str(user_name)
        self.user_created_at = str(user_created_at)
        self.user_deleted_at = str(user_deleted_at)
        self.user_state = str(user_state)

    def get_user(self):
        return self.user_id, self.user_name, self.user_created_at, self.user_created_at, self.user_deleted_at, self.user_state


class Login:
    def __init__(self, user_id, user_login_id):
        self.user_id = int(user_id)
        self.user_login_id = str(user_login_id)

    def get_login(self):
        return self.user_id, self.user_login_id


class Enrollment:
    def __init__(self, user_id, course_id, enrollment_type, enrollment_state):
        self.user_id = int(user_id)
        self.course_id = int(course_id)
        self.enrollment_type = str(enrollment_type)
        self.enrollment_state = str(enrollment_state)

    def get_enrollment(self):
        return self.user_id, self.course_id, self.enrollment_type, self.enrollment_state


class Course:
    def __init__(self, course_id, semester, course_code, course_name, course_created_at):
        self.course_id = int(course_id)
        self.semester = str(semester)
        self.course_code = str(course_code)
        self.course_name = str(course_name)
        self.course_created_at = str(course_created_at)

    def get_course(self):
        return self.course_id, self.semester, self.course_code, self.course_name, self.course_created_at


class Topics:
    def __init__(self, topic_id, topic_title, topic_content, topic_created_at, topic_deleted_at, topic_state, course_id, topic_posted_by_user_id):
        self.topic_id = int(topic_id)
        self.topic_title = str(topic_title)
        self.topic_content = str(topic_content)
        self.topic_created_at = str(topic_created_at)
        self.topic_deleted_at = str(topic_deleted_at)
        self.topic_state = str(topic_state)
        self.course_id = int(course_id)
        self.topic_posted_by_user_id = int(topic_posted_by_user_id)

    def get_topic(self):
        return self.topic_id, self.topic_title, self.topic_content, self.topic_created_at, self.topic_deleted_at, self.topic_state, self.course_id, self.topic_posted_by_user_id


class Entries:
    def __init__(self, entry_id, entry_content, entry_created_at, entry_deleted_at, entry_state, entry_parent_id, entry_posted_by_user_id, topic_id):
        self.entry_id = int(entry_id)
        self.entry_content = str(entry_content)
        self.entry_created_at = str(entry_created_at)
        self.entry_deleted_at = str(entry_deleted_at)
        self.entry_state = str(entry_state)
        self.entry_parent_id = int(entry_parent_id) if not math.isnan(entry_parent_id) else -1
        self.entry_posted_by_user_id = int(entry_posted_by_user_id)
        self.topic_id = int(topic_id)

    def get_entry(self):
        return self.entry_id, self.entry_content, self.entry_created_at, self.entry_deleted_at, self.entry_state, self.entry_parent_id, self.entry_posted_by_user_id, self.topic_id
