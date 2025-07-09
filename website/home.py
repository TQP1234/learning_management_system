from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .utils import load_enrollment_from_excel, load_courses_from_excel, load_topics_from_excel, load_entries_from_excel, load_users_from_excel_v2
from collections import Counter


home = Blueprint('home', __name__)

enrollment_data = './data_tables/enrollment.xlsx'
courses_data = './data_tables/courses.xlsx'
entries_data = './data_tables/entries.xlsx'
topics_data = './data_tables/topics.xlsx'
users_data = './data_tables/users.xlsx'


def filter_data_by_conditions(data, conditions):
    # Filter data records based on multiple conditions, including handling multiple values for a single field
    filtered_data = {
        data_id: data
        for data_id, data in data.items()
        if all(
            (getattr(data, key) in value if isinstance(value, (list, set)) else getattr(data, key) == value)
            for key, value in conditions.items()
        )
    }
    return filtered_data


def get_unique_records(data, unique_keys):
    unique_records = {}

    for _, data in data.items():
        # Create a tuple of values from the unique keys for comparison
        unique_key_values = tuple(getattr(data, key) for key in unique_keys)

        if unique_key_values not in unique_records:
            unique_records[unique_key_values] = data

    return unique_records


def get_most_frequent_attribute_value(data, attribute):
    # Collect all attribute values
    attribute_values = [
        getattr(data, attribute, None) for data_id, data in data.items() if getattr(data, attribute, None) is not None
    ]

    # Use Counter to find the most common attribute value
    value_counts = Counter(attribute_values)

    # Get the value with the highest count
    most_frequent_value, count = value_counts.most_common(1)[0] if value_counts else (None, 0)

    return most_frequent_value, count


def count_attribute_value(data, attribute, value):
    count = 0

    for item in data.values():
        if getattr(item, attribute, None) == value:
            count += 1

    return count


def get_instructor_based_on_name(users, instructor_name):
    for _, v in users.items():
        if v.user_name.lower() == instructor_name.lower():
            return v

    return None


def get_course_based_on_name(courses, course_name):
    for _, v in courses.items():
        if v.course_name.lower() == course_name.lower():
            return v

    return None


# home page
@home.route('/', methods=['GET', 'POST'])
@login_required
def home_page():
    # Load data from Excel files
    enrollment = load_enrollment_from_excel(enrollment_data)
    courses = load_courses_from_excel(courses_data)
    topics = load_topics_from_excel(topics_data)
    entries = load_entries_from_excel(entries_data)
    users = load_users_from_excel_v2(users_data)

    if current_user.account_type == 'admin':
        instructor_data = filter_data_by_conditions(enrollment, {'enrollment_type': 'teacher', 'enrollment_state': 'active'})

        instructors_list = []
        for k, v in instructor_data.items():
            instructors_list.append((users[k].user_name, courses[v.course_id].course_name.title()))

        instructors_list = sorted(instructors_list, key=lambda x: x[1])

        if request.method == 'POST':
            selected_username, selected_course = request.form.get('course').split(';')
            instructor = get_instructor_based_on_name(users, selected_username)
            instructor = filter_data_by_conditions(
                enrollment, {'user_id': instructor.user_id, 'enrollment_type': 'teacher'}
            )[instructor.user_id]
            user_course = get_course_based_on_name(courses, selected_course)

        else:
            instructor = get_instructor_based_on_name(users, instructors_list[0][0])
            instructor = filter_data_by_conditions(
                enrollment, {'user_id': instructor.user_id, 'enrollment_type': 'teacher'}
            )[instructor.user_id]
            user_course = get_course_based_on_name(courses, instructors_list[0][1])

        students = filter_data_by_conditions(enrollment, {'course_id': instructor.course_id, 'enrollment_type': 'student', 'enrollment_state': 'active'})
        topics = filter_data_by_conditions(topics, {'topic_posted_by_user_id': instructor.user_id, 'topic_state': 'active', 'course_id': instructor.course_id})
        entries = filter_data_by_conditions(entries, {'topic_id': [topic_id for topic_id in topics]})

        hottest_topic = get_most_frequent_attribute_value(entries, 'topic_id')
        hottest_topic_title = topics[hottest_topic[0]].topic_title

        students_posting = get_unique_records(entries, ['entry_posted_by_user_id'])
        participation_rate = (len(students_posting) / len(students)) * 100

        topic_table = []
        for k, v in topics.items():
            topic_table.append(
                {
                    'topic_id': k,
                    'topic_title': v.topic_title,
                    'topic_content': v.topic_content,
                    'topic_created_at': v.topic_created_at,
                    'number_of_entries': count_attribute_value(entries, 'topic_id', k)
                }
            )

        entries_table = []
        for k, v in students_posting.items():
            entries_table.append(
                {
                    'student': users[v.entry_posted_by_user_id].user_name,
                    'entries': count_attribute_value(entries, 'entry_posted_by_user_id', users[v.entry_posted_by_user_id].user_id)
                }
            )

        # length_menu = [len(topic_table)] if len(topic_table) <= len(entries_table) else [len(entries_table)]

        return render_template(
            'admin.html',
            courses=instructors_list,
            username=current_user.username,
            course_name=user_course.course_name.title(),
            instructor_name=users[instructor.user_id].user_name,
            num_of_students=len(students),
            num_of_topics=len(topics),
            num_of_entries=len(entries),
            hottest_topic=hottest_topic_title,
            num_of_students_posting=len(students_posting),
            participation_rate=f'{participation_rate:.2f} %',
            topic_table=topic_table,
            entries_table=entries_table,
            length_menu=5,
        )

    elif current_user.account_type == 'instructor':
        user_data = next((e for e in enrollment.values() if e.user_id == current_user.user_id), None)
        user_course = next((c for c in courses.values() if c.course_id == user_data.course_id), None)

        students = filter_data_by_conditions(enrollment, {'course_id': user_data.course_id, 'enrollment_type': 'student', 'enrollment_state': 'active'})
        topics = filter_data_by_conditions(topics, {'topic_posted_by_user_id': current_user.user_id, 'topic_state': 'active', 'course_id': user_data.course_id})
        entries = filter_data_by_conditions(entries, {'topic_id': [topic_id for topic_id in topics]})

        hottest_topic = get_most_frequent_attribute_value(entries, 'topic_id')
        hottest_topic_title = topics[hottest_topic[0]].topic_title

        students_posting = get_unique_records(entries, ['entry_posted_by_user_id'])
        participation_rate = (len(students_posting) / len(students)) * 100

        topic_table = []
        for k, v in topics.items():
            topic_table.append(
                {
                    'topic_id': k,
                    'topic_title': v.topic_title,
                    'topic_content': v.topic_content,
                    'topic_created_at': v.topic_created_at,
                    'number_of_entries': count_attribute_value(entries, 'topic_id', k)
                }
            )

        entries_table = []
        for k, v in students_posting.items():
            entries_table.append(
                {
                    'student': users[v.entry_posted_by_user_id].user_name,
                    'entries': count_attribute_value(entries, 'entry_posted_by_user_id', users[v.entry_posted_by_user_id].user_id)
                }
            )

        # length_menu = [len(topic_table)] if len(topic_table) <= len(entries_table) else [len(entries_table)]

        return render_template(
            'instructor.html',
            username=current_user.username,
            course_name=user_course.course_name.title(),
            num_of_students=len(students),
            num_of_topics=len(topics),
            num_of_entries=len(entries),
            hottest_topic=hottest_topic_title,
            num_of_students_posting=len(students_posting),
            participation_rate=f'{participation_rate:.2f} %',
            topic_table=topic_table,
            entries_table=entries_table,
            length_menu=5,
        )
