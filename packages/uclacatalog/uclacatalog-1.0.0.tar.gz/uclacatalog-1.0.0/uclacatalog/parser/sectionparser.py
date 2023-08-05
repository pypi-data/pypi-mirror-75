from uclacatalog.model.course import Course
from uclacatalog.model.section import Section, Final
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from typing import List
import requests as req
import uclacatalog.requesthandler as requesthandler
import re
import time

'''
Parser for responses from https://sa.ucla.edu/ro/public/soc
'''

def parse_sections(resp, course, term) -> List[Section]:
    out = []
    out.extend(_parse_root_sections(resp, course, term))
    for section in out:
        section.children = _parse_leaf_sections(requesthandler.fetch_leaf_sections(section, None, term), section)
    return out

def _parse_root_sections(resp, course, term):
    out = []
    sections_soup = BeautifulSoup(resp.text, 'lxml').find('div', {'id': re.compile('\\d*-children')})
    if sections_soup is not None:
        sections_arr = sections_soup.find_all("div", class_="class-info")
        for i in range(len(sections_arr)):
            section_soup = sections_arr[i]
            section = _populate_section(section_soup, course, term)
            # Why IT decided to format the section number like this and actually strictly enforce its format on the backend, I have no idea. 
            # The interface is full of bad design decisions like these.
            section.sec_no = ' ' + str(i + 1).zfill(3)
            _parse_section_details(section)
            out.append(section)
    return out

# Leaf sections can be both labs or discussions, or just may not exist
def _parse_leaf_sections(resp, parent):
    out = []
    sections_soup = BeautifulSoup(resp.text, 'lxml').find('div', {'id': re.compile('\\d*-children')})
    sections_arr = sections_soup.find_all("div", class_="class-info")
    for section_soup in sections_arr:
        section = _populate_section(section_soup, parent.course, parent.term)
        section.sec_no = parent.sec_no
        _parse_section_details(section)
        out.append(section)
    return out

def _populate_section(section_soup, course, term):
    section = Section()
    section.id = _parse_id(section_soup)
    section.term = term
    section.type = _parse_type(section_soup)
    section.waitlistable = _parse_waitlistable(section_soup)
    section.enrollable = _parse_enrollable(section_soup)
    section.enrolled = _parse_enrollment(section_soup)
    section.enrolled_max = _parse_enrollment_max(section_soup)
    section.waitlisted = _parse_waitlisted(section_soup)
    section.waitlisted_max = _parse_waitlisted_max(section_soup)
    section.meet_days = _parse_days(section_soup)
    section.start_time = time.mktime(_parse_start(section_soup).timetuple())
    section.end_time = time.mktime(_parse_end(section_soup).timetuple())
    section.location = _parse_location(section_soup)
    section.instructors = _parse_instructors(section_soup)
    section.last_updated = int(time.time())
    section.course = course
    return section

def _parse_section_details(section):
    detail_resp = requesthandler.fetch_section_detail(section)
    detail_soup = BeautifulSoup(detail_resp.text, 'lxml')

    section.restrictions = _parse_detail_restrictions(detail_soup)
    section.webpage = _parse_detail_webpage(detail_soup)
    section.grade_type = _parse_detail_gradetype(detail_soup)
    section.final = _parse_detail_final(detail_soup)
    section.notes = _parse_detail_notes(detail_soup)

def _parse_id(section_soup):
    # ID Attribute is in format of ID_subjAreaCLASSNUM; we want to split at '_' and take the first element
    return section_soup.div['id'].split("_")[0]

def _match_status(section_soup):
    status = section_soup.find("div", class_="statusColumn")

    # Use regex match groups to seperate openness from class capacity
    return re.findall("(Open|Closed|Waitlist)\\D*((\\d+ of \\d+ Enrolled)|(Class Full \\(\\d+\\))?)", status.text)[0]

def _parse_type(section_soup):
    type_soup = section_soup.find('div', class_='sectionColumn')
    sec_type = type_soup.text
    if 'Lec' in sec_type:
        return 'lecture'
    elif 'Dis' in sec_type:
        return 'discussion'
    elif 'Lab' in sec_type:
        return 'lab'
    else:
        raise ValueError

def _parse_enrollable(section_soup):
    status = _match_status(section_soup)[0]
    return status == "Open"

def _parse_waitlistable(section_soup):
    status = _match_status(section_soup)[0]
    return status == "Waitlist"

''' 
For matching enrollment and waitlist, we only care about the numbers for matching. 

The result will always either come in a tuple containing (current_num, max_num) or an empty tuple if the course was closed by the department
'''
def _match_enrollment(section_soup):
    enrollment = _match_status(section_soup)[1]
    return re.findall('\\d+', enrollment)

def _parse_enrollment(section_soup):
    groups = _match_enrollment(section_soup)
    if len(groups) > 0: 
        return groups[0]
    else:
        return 0

def _parse_enrollment_max(section_soup):
    groups = _match_enrollment(section_soup)
    if len(groups) > 1:
        return groups[1]
    elif len(groups) == 0:
        return 0
    else: 
        return groups[0]

def _match_waitlisted(section_soup):
    waitlist = section_soup.find("div", class_="waitlistColumn")
    return re.findall("\\d+", waitlist.text)

def _parse_waitlisted(section_soup):
    groups = _match_waitlisted(section_soup)
    if len(groups) > 0:
        return groups[0]
    else:
        return 0

def _parse_waitlisted_max(section_soup):
    groups = _match_waitlisted(section_soup)
    if len(groups) > 1:
        return groups[1]
    elif len(groups) == 0:
        return 0
    else:
        return groups[0]

def _parse_time(section_soup):
    time_soup = section_soup.find("div", class_="timeColumn")

    # Text comes in the format DAYS \n TIME, so we split it to give an array of [DAYS, TIME]
    return time_soup.text.split()

def _parse_days(section_soup):
    days = _parse_time(section_soup)[0]
    groups = re.findall("(M+)?(T+)?(W+)?(R+)?(F+)?", days)[0]
    
    # Filter for elements that aren't empty strings
    return list(filter(lambda e: e != '', groups))

def _parse_start_end(section_soup):
    time = _parse_time(section_soup)[1]
    return time.split('-') # time_arr is in format of [start_time, end_time]

def _parse_start(section_soup):
    start_str = _parse_start_end(section_soup)[0]
    return _parse_time_str(start_str).replace(year=1970)

def _parse_end(section_soup):
    end_str = _parse_start_end(section_soup)[1]
    return _parse_time_str(end_str).replace(year=1970)

def _parse_time_str(time_str):
    if time_str.find(':') > -1:
        # Time is within the hour
        return datetime.strptime(time_str, '%I:%M%p')
    else: 
        # Time *is* the hour; for some reason UCLA doesn't standardize timestamps and assumes that 12:00 = 12. We will follow this assumption grudgingly.
        return datetime.strptime(time_str, '%I%p')

def _parse_location(section_soup):
    return section_soup.find("div", class_="locationColumn").text.strip()

def _parse_instructors(section_soup):
    instructor_soup = section_soup.find("div", class_="instructorColumn")
    return [x for x in instructor_soup.p.contents if getattr(x, 'name', None) != 'br']

def _parse_detail_restrictions(detail_soup):
    restrictions_soup = detail_soup.find('div', class_='enrollment_restrictions_content')
    if restrictions_soup == None:
        return None
    else:
        return restrictions_soup.text.strip()

def _parse_detail_webpage(detail_soup):
    return detail_soup.find('div', class_='grade_type_content').find_all('p')[1].find('span', class_='grade_type_content_text').text.strip()

def _parse_detail_gradetype(detail_soup):
    return detail_soup.find('div', class_='grade_type_content').find_all('p')[2].find('span', class_='grade_type_content_text').text.strip()

def _parse_detail_final(detail_soup):
    final_soup = detail_soup.find('div', class_='final_exam_content').find('div', class_='data-row').find_all('div')
    if final_soup[0].text == 'None listed':
        return None
    else:
        final = Final()
        final.meet_days = _parse_final_day(final_soup)
        final.start_time = time.mktime(_parse_final_start(final_soup).timetuple())
        final.end_time = time.mktime(_parse_final_end(final_soup).timetuple())
        final.location = _parse_final_location(final_soup)
        return final

def _parse_final_day(final_soup):
    day = final_soup[3].text
    if (day == 'Thu'):
        return 'R'
    else:
        return day[0]

def _parse_final_start(final_soup):
    date = final_soup[0].text
    time = final_soup[4].text.split('-')[0]
    return _parse_final_datetime(date, time)

def _parse_final_end(final_soup):
    date = final_soup[0].text
    time = final_soup[4].text.split('-')[1]
    return _parse_final_datetime(date, time)

def _parse_final_location(final_soup):
    return final_soup[5].text

def _parse_final_datetime(date, time):
    time = _parse_time_str(time)
    date = datetime.strptime(date, '%m/%d/%Y')
    delta = timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
    return date + delta

def _parse_detail_notes(detail_soup):
    notes_soup = detail_soup.find('div', 'class_notes_content').find_all('li')
    out = []
    for note in notes_soup:
        out.append(note.text.strip())
    return out