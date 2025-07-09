import pandas as pd
from .models import User, Enrollment, Course, Entries, Topics, Users


def load_users_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create a dictionary to store users with their ID as the key
    users = {}
    for _, row in df.iterrows():
        user = User(user_id=row['user_id'], username=row['username'], password=row['password'], account_type=row['account_type'], course_id=row['course_id'])
        users[user.user_id] = user

    return users


def load_users_from_excel_v2(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create a dictionary to store users with their ID as the key
    users = {}
    for _, row in df.iterrows():
        user = Users(user_id=row['user_id'], user_name=row['user_name'], user_created_at=row['user_created_at'], user_deleted_at=row['user_deleted_at'], user_state=row['user_state'])
        users[user.user_id] = user

    return users


def load_enrollment_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create a dictionary to store enrollment with their ID as the key
    enrollment = {}
    for _, row in df.iterrows():
        enroll = Enrollment(user_id=row['user_id'], course_id=row['course_id'], enrollment_type=row['enrollment_type'], enrollment_state=row['enrollment_state'])
        enrollment[enroll.user_id] = enroll

    return enrollment


def load_courses_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create a dictionary to store courses with their ID as the key
    courses = {}
    for _, row in df.iterrows():
        course = Course(course_id=row['course_id'], semester=row['semester'], course_code=row['course_code'], course_name=row['course_name'], course_created_at=['course_created_at'])
        courses[course.course_id] = course

    return courses


def load_topics_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create a dictionary to store topics with their ID as the key
    topics = {}
    for _, row in df.iterrows():
        topic = Topics(topic_id=row['topic_id'], topic_title=row['topic_title'], topic_content=row['topic_content'], topic_created_at=row['topic_created_at'], topic_deleted_at=row['topic_deleted_at'], topic_state=row['topic_state'], course_id=row['course_id'], topic_posted_by_user_id=row['topic_posted_by_user_id'])
        topics[topic.topic_id] = topic

    return topics


def load_entries_from_excel(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path)

    # Create a dictionary to store entries with their ID as the key
    entries = {}
    for _, row in df.iterrows():
        entry = Entries(entry_id=row['entry_id'], entry_content=row['entry_content'], entry_created_at=row['entry_created_at'], entry_deleted_at=row['entry_deleted_at'], entry_state=row['entry_state'], entry_parent_id=row['entry_parent_id'], entry_posted_by_user_id=row['entry_posted_by_user_id'], topic_id=row['topic_id'])
        entries[entry.entry_id] = entry

    return entries
