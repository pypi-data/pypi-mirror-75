import datetime
import uuid
from sync.base import BaseSync
from utils.loggerutils import logging
from utils.code import get_md5_hash
from classcard_dataclient.models.course import CourseV2, CourseTableManagerV2, TableCategory, WalkingModeSet

logger = logging.getLogger(__name__)


class CourseSync(BaseSync):
    def __init__(self):
        super(CourseSync, self).__init__()
        self.offset = 300
        self.course_map = {}
        self.space_map = {}
        self.slot_map = {}
        self.student_map = {}
        self.teacher_map = {}
        self.classroom_map = {}
        self.class_set = set()
        self.class_name_num = {}
        self.rest_table = None
        self.semester = None
        self.course_name_list = []

    def create_unique_course_name(self, subject_name, class_name):
        course_name = "{}_{}".format(subject_name, class_name) if class_name else subject_name
        new_course_name = course_name
        while True:
            if new_course_name not in self.course_name_list:
                break
            new_course_name = "{}_{}".format(course_name, str(uuid.uuid4())[:3])
        self.course_name_list.append(new_course_name)
        return new_course_name

    def extract_course(self):
        today, last_day = self.get_date_range()
        sql = "SELECT id, coursename, sectionid, classroomid, coursedate, weekday, userid, isteacher, deptname " \
              "FROM mid_attendschedule " \
              "WHERE coursedate > '{}' and coursedate <= '{}' ORDER BY weekday".format(today, last_day)
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        for row in rows:
            category = TableCategory.ALL
            attend_id, subject_name, slot_id = row[0], row[1], row[2]
            classroom_id, course_date, week = row[3], row[4], row[5]
            user_id, is_teacher, class_name = row[6], row[7], row[8]
            unique_key = "{}_{}_{}".format(subject_name, classroom_id, class_name)
            # unique_key = "{}_{}".format(subject_name, classroom_id)
            course_number = get_md5_hash(unique_key)
            subject_number = get_md5_hash(subject_name)
            num = self.slot_map.get(slot_id, None)
            classroom_number = self.classroom_map.get(str(classroom_id))
            if not num:
                print("Can't Find SlotID {}".format(slot_id))
                continue
            if unique_key not in self.course_map:
                course_name = self.create_unique_course_name(subject_name, class_name=class_name)
                course_data = {'name': course_name, 'number': course_number, 'subject_number': subject_number,
                               "subject_name": subject_name, 'classroom_number': classroom_number, 'is_walking': False,
                               "teacher_number": None, "begin_week": 1, "end_week": 8, 'student_list': []}
                course = CourseV2(**course_data)
                course.class_name = class_name
                course.required_student = False
                self.course_map[unique_key] = course
                if class_name and class_name in self.class_name_num:
                    self.class_set.add(self.class_name_num[class_name])
            else:
                course = self.course_map[unique_key]
            if is_teacher:
                if str(user_id) in ["1", "4"]:
                    continue
                teacher_number = self.teacher_map.get(user_id)
                if teacher_number:
                    course.teacher_number = teacher_number
            else:
                student_number = self.student_map.get(user_id)
                if student_number:
                    course.add_student(student_number)
            course.add_position(num, week, category, classroom_number)

    def sync(self):
        self.extract_course()
        if not self.course_map:
            logger.info("没有课程信息")
            return
        begin_date, end_date = self.get_date_range(days=60)
        course_table_name = "{}课表_{}".format(self.semester.name, str(uuid.uuid4())[:4])
        course_table_number = get_md5_hash(course_table_name)[:20]
        course_table = CourseTableManagerV2(name=course_table_name, number=course_table_number,
                                            rest_name=self.rest_table.name, walking_mode=WalkingModeSet.WALKING,
                                            begin_date=begin_date, end_date=end_date, semester_name=self.semester.name)
        course_table.classrooms_num = list(self.classroom_map.values())
        course_table.sections_num = list(self.class_set)
        course_table.courses = list(self.course_map.values())
        print(">>> CREATE_COURSE_TABLE")
        logger.info(">>> CREATE_COURSE_TABLE")
        self.client.create_course_table(self.school_id, course_table, is_active=True)
        self.client.active_semester(self.school_id, self.semester, delete_other=True)
        self.close_db()
