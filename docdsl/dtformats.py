"""
File: dtformats.py
Project: Docdsl
File Created: Wed 15 Jul 2026 08:08:21 (Shine Jayakumar)
Author: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Last Modified: Wed 15 Jul 2026 08:08:21 (Shine Jayakumar)
Modified By: Shine Jayakumar (shinejayakumar@yahoo.com)
-----
Copyright (c) 2026 Shine Jayakumar
SPDX-License-Identifier: MIT

Licensed under the MIT License.
See the LICENSE file in the project root for the full license text.
"""

import re

WEEKDAYS_FULL = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
WEEKDAYS_ABBR = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
MONTHS_FULL = ('January', 'February', 'March','April', 'May','June', 
               'July','August','September'	,'October','November','December')
MONTHS_ABBR = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')


def get_dtformat_suffixed(dtstr: str):
    """ Returns date formats for dates with suffixes (st, nd, rd, th) """
    dtstr = re.sub(r'\s+', ' ', dtstr.strip())
    dtstr = re.sub(f'({"|".join(WEEKDAYS_FULL)})', '%A', dtstr) # Monday
    dtstr = re.sub(f'({"|".join(WEEKDAYS_ABBR)})', '%a', dtstr) # Mon
    dtstr = re.sub(f'({"|".join(MONTHS_FULL)})', '%B', dtstr) # January
    dtstr = re.sub(f'({"|".join(MONTHS_ABBR)})', '%b', dtstr) # Jan
    dtstr = re.sub(r'^(\d{1,2})(st|nd|rd|th)', r'%d\2', dtstr)
    dtstr = re.sub(r'\s+(\d{1,2})(st|nd|rd|th)', r' %d\2', dtstr)
    dtstr = re.sub(r'\d{4}', '%Y', dtstr)
    dtstr = re.sub(r'\d{2}', '%y', dtstr)
   
    patterns = []
    patterns.append(re.sub(r'(st|nd|rd|th)', 'st', dtstr))
    patterns.append(re.sub(r'(st|nd|rd|th)', 'nd', dtstr))
    patterns.append(re.sub(r'(st|nd|rd|th)', 'rd', dtstr))
    patterns.append(re.sub(r'(st|nd|rd|th)', 'th', dtstr))

    return patterns


DTSAMPLE_PYFORMAT_MAP = {
    "02 March 1999": "%d %B %Y",
    "02-March-1999": "%d-%B-%Y",
    "02/March/1999": "%d/%B/%Y",
    "02.March.1999": "%d.%B.%Y",

    "02 March 99": "%d %B %y",
    "02-March-99": "%d-%B-%y",
    "02/March/99": "%d/%B/%y",
    "02.March.99": "%d.%B.%y",

    "02 Mar 1999": "%d %b %Y",
    "02-Mar-1999": "%d-%b-%Y",
    "02/Mar/1999": "%d/%b/%Y",
    "02.Mar.1999": "%d.%b.%Y",

    "02 Mar 99": "%d %b %y",
    "02-Mar-99": "%d-%b-%y",
    "02/Mar/99": "%d/%b/%y",
    "02.Mar.99": "%d.%b.%y",
    
    "Mar 02 1999": "%b %d %Y",
    "Mar-02-1999": "%b-%d-%Y",
    "Mar/02/1999": "%b/%d/%Y",
    "Mar.02.1999": "%b.%d.%Y",

    "Mar 02 99": "%b %d %y",
    "Mar-02-99": "%b-%d-%y",
    "Mar/02/99": "%b/%d/%y",
    "Mar.02.99": "%b.%d.%y",


    "March 02 1999": "%B %d %Y",
    "March-02-1999": "%B-%d-%Y",
    "March/02/1999": "%B/%d/%Y",
    "March.02.1999": "%B.%d.%Y",

    "March 02 99": "%B %d %y",
    "March-02-99": "%B-%d-%y",
    "March/02/99": "%B/%d/%y",
    "March.02.99": "%B.%d.%y",

    "Monday, 02 March 1999": "%A, %d %B %Y",
    "Monday, 02 Mar 1999": "%A, %d %b %Y",

    "Mon, 02 March 1999": "%a, %d %B %Y",
    "Mon, 02 Mar 1999": "%a, %d %b %Y",

    "Monday, March 02, 1999": "%A, %B %d, %Y",
    "Monday, March 02 1999": "%A, %B %d %Y",

    "Monday, Mar 02, 1999": "%A, %b %d, %Y",
    "Monday, Mar 02 1999": "%A, %b %d %Y",

    "Mon, March 02, 1999": "%a, %B %d, %Y",
    "Mon, March 02 1999": "%a, %B %d %Y",

    "Mon, Mar 02, 1999": "%a, %b %d, %Y",
    "Mon, Mar 02 1999": "%a, %b %d %Y",

    "Monday, 02 March 99": "%A, %d %B %y",
    "Monday, 02 Mar 99": "%A, %d %b %y",

    "Mon, 02 March 99": "%a, %d %B %y",
    "Mon, 02 Mar 99": "%a, %d %b %y",

    "Monday, March 02, 99": "%A, %B %d, %y",
    "Monday, March 02 99": "%A, %B %d %y",

    "Monday, Mar 02, 99": "%A, %b %d, %y",
    "Monday, Mar 02 99": "%A, %b %d %y",

    "Mon, March 02, 99": "%a, %B %d, %y",
    "Mon, March 02 99": "%a, %B %d %y",

    "Mon, Mar 02, 99": "%a, %b %d, %y",
    "Mon, Mar 02 99": "%a, %b %d %y",

    "Monday 2nd March 1999": ('%A %dst %B %Y', '%A %dnd %B %Y', '%A %drd %B %Y', '%A %dth %B %Y'),
    "Monday 2nd Mar 1999": ('%A %dst %b %Y', '%A %dnd %b %Y', '%A %drd %b %Y', '%A %dth %b %Y'),
    "Monday 2nd March 99": ('%A %dst %B %y', '%A %dnd %B %y', '%A %drd %B %y', '%A %dth %B %y'),
    "Monday 2nd Mar 99": ('%A %dst %b %y', '%A %dnd %b %y', '%A %drd %b %y', '%A %dth %b %y'),

    "Mon 2nd March 1999": ('%a %dst %B %Y', '%a %dnd %B %Y', '%a %drd %B %Y', '%a %dth %B %Y'),
    "Mon 2nd Mar 1999": ('%a %dst %b %Y', '%a %dnd %b %Y', '%a %drd %b %Y', '%a %dth %b %Y'),
    "Mon 2nd March 99": ('%a %dst %B %y', '%a %dnd %B %y', '%a %drd %B %y', '%a %dth %B %y'),
    "Mon 2nd Mar 99": ('%a %dst %b %y', '%a %dnd %b %y', '%a %drd %b %y', '%a %dth %b %y'),

    "Monday, 2nd March 1999": ('%A, %dst %B %Y', '%A %dnd %B %Y', '%A %drd %B %Y', '%A %dth %B %Y'),
    "Monday, 2nd Mar 1999": ('%A, %dst %b %Y', '%A %dnd %b %Y', '%A %drd %b %Y', '%A %dth %b %Y'),
    "Monday, 2nd March 99": ('%A, %dst %B %y', '%A %dnd %B %y', '%A %drd %B %y', '%A %dth %B %y'),
    "Monday, 2nd Mar 99": ('%A, %dst %b %y', '%A %dnd %b %y', '%A %drd %b %y', '%A %dth %b %y'),

    "Mon, 2nd March 1999": ('%a, %dst %B %Y', '%a %dnd %B %Y', '%a %drd %B %Y', '%a %dth %B %Y'),
    "Mon, 2nd Mar 1999": ('%a, %dst %b %Y', '%a %dnd %b %Y', '%a %drd %b %Y', '%a %dth %b %Y'),
    "Mon, 2nd March 99": ('%a, %dst %B %y', '%a %dnd %B %y', '%a %drd %B %y', '%a %dth %B %y'),
    "Mon, 2nd Mar 99": ('%a, %dst %b %y', '%a %dnd %b %y', '%a %drd %b %y', '%a %dth %b %y'),

    "2nd March 1999":  ('%dst %B %Y', '%dnd %B %Y', '%drd %B %Y', '%dth %B %Y'),
    "2nd March 99":  ('%dst %B %y', '%dnd %B %y', '%drd %B %y', '%dth %B %y'),

    "2nd Mar 1999":  ('%dst %b %Y', '%dnd %b %Y', '%drd %b %Y', '%dth %b %Y'),
    "2nd Mar 99":  ('%dst %b %y', '%dnd %b %y', '%drd %b %y', '%dth %b %y'),

    # yyyy mm dd
    "1999-02-22": "%Y-%m-%d",
    "1999/02/22": "%Y/%m/%d",
    "1999.02.22": "%Y.%m.%d",
    "1999 02 22": "%Y %m %d",
    
    # yy mm dd
    "99-02-22": "%y-%m-%d",
    "99/02/22": "%y/%m/%d",
    "99.02.22": "%y.%m.%d",
    "99 02 22": "%y %m %d",

    # mm dd yy
    "02/22/99": "%m/%d/%y",
    "02-22-99": "%m-%d-%y",
    "02.22.99": "%m.%d.%y",
    "02 22 99": "%m %d %y",

    # mm dd yyyy
    "02/22/1999": "%m/%d/%Y",
    "02-22-1999": "%m-%d-%Y",
    "02.22.1999": "%m.%d.%Y",
    "02 22 1999": "%m %d %Y",

    # dd mm yy
    "22/02/99": "%d/%m/%y",
    "22-02-99": "%d-%m-%y",
    "22.02.99": "%d.%m.%y",
    "22 02 99": "%d %m %y",

    # dd mm yyyy
    "22/02/1999": "%d/%m/%Y",
    "22-02-1999": "%d-%m-%Y",
    "22.02.1999": "%d.%m.%Y",
    "22 02 1999": "%d %m %Y",
}

if __name__ == '__main__':
    pass
