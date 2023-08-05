import time
from sync.classroom import ClassroomSync
from sync.course import CourseSync
from sync.meeting_room import MeetingRoomSync
from sync.schedule import ScheduleSync
from sync.section import SectionSync
from sync.subject import SubjectSync
from sync.student import StudentSync
from sync.teacher import TeacherSync
from utils.loggerutils import logging

logger = logging.getLogger(__name__)


def start_all_sync():
    teacher_sync = TeacherSync()
    teacher_sync.start()
    section_sync = SectionSync()
    section_sync.start()
    student_sync = StudentSync()
    student_sync.start()
    subject_sync = SubjectSync()
    subject_sync.start()
    schedule_sync = ScheduleSync()
    schedule_sync.start()
    classroom_sync = ClassroomSync()
    classroom_sync.start()
    course_sync = CourseSync()
    course_sync.slot_map = schedule_sync.slot_map
    course_sync.semester = schedule_sync.semester
    course_sync.rest_table = schedule_sync.rest_table
    course_sync.student_map = student_sync.student_map
    course_sync.teacher_map = teacher_sync.teacher_map
    course_sync.classroom_map = classroom_sync.classroom_map
    course_sync.class_name_num = section_sync.name_num
    course_sync.start()
    meeting_room_sync = MeetingRoomSync()
    meeting_room_sync.start()


if __name__ == '__main__':
    start_all_sync()
