from uclacatalog.model.course import Course
import base64
import json

'''
Model for objects that start and end in the space-time continuum

meet_days       (List[string])  A list containing the days the event takes place (Abbreviations are M: Monday, T: Tuesday, W: Wednesday, R: Thursday, F: Friday)
start_time      (int)           Unix timestamp containing the start time (If only a time, such as for a section rather than a final, disregard date portion when parsing)
end_time        (int)           Unix timestamp containing the end time
location        (string)        Location of the event
'''

class Event:
    def __init__(self):
        self.meet_days = []
        self.start_time = ''
        self.end_time = ''
        self.location = ''

class Final(Event):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

'''
Model for course sections (lectures, discussions, and labs). A subclass of the Event type.

course:         (Course)        The course that this section is for
id:             (int)           Section ID (Note that courses are not provided ID's by the UCLA Registrar)
sec_no:         (string)        Course number zero-padded such that sec_no is 3 characters long plus a whitespace at the front
term:           (string)        Academic term course information is accurate for
type:           (string)        Section type (lecture, discussion, lab)
enrollable:     (boolean)       Convenience field to see if enrolled < enrolled_max
waitlistable:   (boolean)       Convenience field to see if waitlisted < waitlisted_max
enrolled:       (int)           Number of students enrolled in the section
enrolled_max:   (int)           Maximum capacity of section
waitlisted:     (int)           Number of students that are on the section's waitlist
waitlisted_max: (int)           Maximum capacity of waitlist
instructors:    (List[string])  List of instructors for the section
final:          (Final)         An object containing information about the final for the section
restrictions:   (string)        Any restrictions needed to be fulfilled to enroll (Not prerequisites)
webpage:        (string)        A URL to the section's website
grade_type:     (string)        Whether the class is P/NP, Letter Graded, or Not Graded
notes:          (List[string])        Notes specified by the department or registrar
children:       (List[Section]) Children sections (e.g Discussion or lab sections for lectures)
last_updated:   (int)           Unix timestamp for which enrolled and waitlisted was accurate
'''
class Section(Event):
    def __init__(self):
        super().__init__()
        self.course = None
        self.id = 0
        self.sec_no = 0
        self.term = ''
        self.type = ''
        self.enrollable = False
        self.waitlistable = False
        self.enrolled = 0
        self.enrolled_max = 0
        self.waitlisted = 0
        self.waitlisted_max = 0
        self.instructors = []
        self.final = None
        self.restrictions = ''
        self.webpage = ''
        self.grade_type = ''
        self.notes = []
        self.children = []
        self.last_updated = 0

    def to_jsons(self):
        json_obj = json.loads(self.course.to_jsons(self.term))
        json_obj['IsRoot'] = False
        json_obj['SessionGroup'] = None
        json_obj['ClassNumber'] = self.sec_no
        json_obj['SequenceNumber'] = '1'
        json_obj['Path'] = self._get_path()
        json_obj['Token'] = self.get_token()

        return json.dumps(json_obj)

    '''
    See course.py for full documentation on how the UCLA Registrar formats its tokens

    For course sections, tokens are used to fetch child sections. They follow mostly the same format as their course
    counterparts, with one difference:

    XXXXAABBID_DEPTXXXXABB
    
    Where ID is the section ID
    '''
    def get_token(self):
        if self.course.subj_area == '' or self.course.ctlg_no == '':
            raise ValueError
        else:
            unencoded_token = self.course.get_full_ctlg_no() + self._get_path()
            unencoded_token_bytes = unencoded_token.encode('utf-8')
            base64_token = base64.standard_b64encode(unencoded_token_bytes)
            return base64_token.decode('utf-8')

    def _get_path(self):
        # This feels so dirty
        return self.id + "_" + self.course.get_path()

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
