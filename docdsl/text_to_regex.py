"""
File: text_to_regex.py
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
from dataclasses import dataclass
from typing import NewType, List
from .dtformats import DTSAMPLE_PYFORMAT_MAP


@dataclass
class DateFormat:
    sample: str
    py_format: str|tuple[str]
    regex_pattern: str


RegExPattern = NewType('RegExPattern', str)

WEEKDAYS_FULL = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
WEEKDAYS_ABBR = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
MONTHS_FULL = ('January', 'February', 'March','April', 'May','June', 
               'July','August','September'	,'October','November','December')
MONTHS_ABBR = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

SEP_ENC_MAP = {
    ' ': '__SP_SPC__',
    '-': '__SP_HYPN__',
    '\\':'__SP_BKSLSH__',
    '/': '__SP_FWSLSH__',
    '.': '__SP_PRD__',
    ',': '__SP_CMA__'
}
# to find pattern in string
SEP_DEC_MAP = {
    '__SP_SPC__': '\\s+',
    '__SP_HYPN__': '-',
    '__SP_BKSLSH__': '\\\\',
    '__SP_FWSLSH__': '\\/',
    '__SP_PRD__': '\\.',
}
PUNCT_ENC_MAP = {
    '_': '__PNCT_UNSCR__', # encoded first
    '!': '__PNCT_EXCL__',
    '"': '__PNCT_DBLQT__',
    '#': '__PNCT_HSH__',
    '$': '__PNCT_DLR__',
    '%': '__PNCT_PRC__',
    '&': '__PNCT_AMPCNT__',
    "'": '__PNCT_SNGQT',
    '(': '__PNCT_OPRN__',
    ')': '__PNCT_CPRN__',
    '*': '__PNCT_ASTR__',
    '+': '__PNCT_PLS__',
    ',': '__PNCT_CMA__',
    '-': '__PNCT_HYPN__',
    '.': '__PNCT_PRD__',
    '/': '__PNCT_FWSLSH__',
    ':': '__PNCT_CLN__',
    ';': '__PNCT_SMCLN__',
    '<': '__PNCT_LAR__',
    '=': '__PNCT_EQ__',
    '>': '__PNCT_RAR__',
    '?': '__PNCT_QSMRK__',
    '@': '__PNCT_ATSYM__',
    '[': '__PNCT_OSQBRK__',
    '\\': '__PNCT_BKSLSH__',
    ']': '__PNCT_CSQBRK__',
    '^': '__PNCT_CRT__',
    '`': '__PNCT_BCKTCK__',
    '{': '__PNCT_OBRC__',
    '}': '__PNCT_CBRC__',
    '|': '__PNCT_PP__',
    '~': '__PNCT_TLD__'
}

REGEX_PAT_DEC_MAP = {
    '__PNCT_EXCL__': '!',
    '__PNCT_SNGQT': "'",
    '__PNCT_DBLQT__': '"',
    '__PNCT_HSH__': '#',
    '__PNCT_DLR__': '\\\\$',
    '__PNCT_PRC__': '%',
    '__PNCT_AMPCNT__': '&',
    '__PNCT_OPRN__': '\\\\(',
    '__PNCT_CPRN__': '\\\\)',
    '__PNCT_ASTR__': '\\\\*',
    '__PNCT_PLS__': '\\\\+',
    '__PNCT_CMA__': ',',
    '__PNCT_HYPN__': '-',
    '__PNCT_PRD__': '\\\\.',    
    '__PNCT_FWSLSH__': '\\\\/',    
    '__PNCT_BKSLSH__': '\\\\\\\\',
    '__PNCT_CLN__': ':',
    '__PNCT_SMCLN__': ';',
    '__PNCT_LAR__': '<',
    '__PNCT_RAR__': '>',
    '__PNCT_EQ__': '=',
    '__PNCT_QSMRK__': '\\\\?',
    '__PNCT_ATSYM__': '@',
    '__PNCT_OSQBRK__': '\\\\[',
    '__PNCT_CSQBRK__': '\\\\]',
    '__PNCT_CRT__': '\\\\^',
    '__PNCT_BCKTCK__': '`',
    '__PNCT_OBRC__': '\\\\{',
    '__PNCT_CBRC__': '\\\\}',
    '__PNCT_PP__': '\\\\|',
    '__PNCT_TLD__': '~',

    '__DT_FR_DG__': '(\\\\d{4})',
    '__DT_SNGLDBL_DG__': '(\\\\d{1,2})',
    '__DT_SFXD_DG__': '(\\\\d{1,2})(st|nd|rd|th)',
    '__DT_WD_FL__': f'({"|".join(WEEKDAYS_FULL)})',
    '__DT_WD_ABR__': f'({"|".join(WEEKDAYS_ABBR)})',
    '__DT_MN_FL__': f'({"|".join(MONTHS_FULL)})',
    '__DT_MN_ABR__': f'({"|".join(MONTHS_ABBR)})',

    '__SP_SPC__': '\\\\s+',
    '__SP_HYPN__': '-',
    '__SP_BKSLSH__': '\\\\\\\\',
    '__SP_FWSLSH__': '\\\\/',
    '__SP_PRD__': '\\\\.',
    '__SP_CMA__': ',',
    '__NWLNE__': '\\\\n*',

    '__PNCT_UNSCR__': '_' # decoded last
}

def is_plain_text(text: str) -> bool:
    """ Checks if a text is a regex patter or plain text """
    if not all([
        r'\s' in text,
        r'\s*' in text,
        r'\s+' in text,
        r'\n' in text,
        r'\n*' in text,
        r'\n+' in text]):
        return True
    return False


class TextToRegex:

    def __init__(self) -> None:
        """ TextToRegex class - text to regular expression pattern  """
        self._dt_patterns = {}
        self._dt_patterns[r'(\d{1,2})(st|nd|rd|th)'] = '__DT_SFXD_DG__'
        self._dt_patterns[f'({"|".join(WEEKDAYS_FULL)})'] = '__DT_WD_FL__'
        self._dt_patterns[f'({"|".join(WEEKDAYS_ABBR)})'] ='__DT_WD_ABR__'
        self._dt_patterns[f'({"|".join(MONTHS_FULL)})'] = '__DT_MN_FL__'
        self._dt_patterns[f'({"|".join(MONTHS_ABBR)})'] = '__DT_MN_ABR__'
        self._dt_patterns[r'\d{4}'] = '__DT_FR_DG__'
        self._dt_patterns[r'\d{1,2}'] = '__DT_SNGLDBL_DG__'

    def find_date_formats(self, text: str) -> List[DateFormat]:
        """Finds date format for a string with date

        Args:
            text (str): text containing date

        Returns:
            DateFormat
        """         
        matched_formats = []
        for dtsample, py_format in DTSAMPLE_PYFORMAT_MAP.items():
            # generate regex for date sample
            pattern = f'{self.dtsample_to_regex(dtsample)}'
            # try generated regex on source text
            matched = re.search(pattern, text)
            if matched: 
                matched_formats.append(DateFormat(
                    sample=dtsample,
                    py_format=py_format,
                    regex_pattern=pattern
                ))
        return matched_formats

    def dtsample_to_regex(self, dtstr: str):
        """ Returns regex pattern to parse a date sample """

        # encoding separators
        for ch, enc in SEP_ENC_MAP.items():
            # dtstr = re.sub(ch, enc, dtstr)
            dtstr = dtstr.replace(ch, enc)

        #encoding date patterns
        for pat, enc in self._dt_patterns.items():
            dtstr = re.sub(pat, enc, dtstr)

        # # decoding 
        for enc, pat in REGEX_PAT_DEC_MAP.items():
            dtstr = re.sub(enc, pat, dtstr)
        dtstr = f'({dtstr})'
        dtstr += '\\b'

        return dtstr
    
    def get_regex(
            self, 
            text: str, 
            include_pattern: RegExPattern = '', 
            keep_matched: bool = False, 
            text_after: bool = False, 
            spad_puncts: bool = True
        ) -> RegExPattern:
        """Returns regex pattern for a text

        Args:
            text (str): text for return the regex for
            include_pattern (RegExPattern, optional): regex pattern to include. Defaults to ''.
            keep_matched (bool, option): keep the text matched against included pattern. Defaults to False.
            text_after (bool, optional): places text after pattern specified with include_pattern. Defaults to False.
            spad_puncts (bool, optional): add spaces before and after punctuations. Defaults to True.

        Returns:
            RegExPattern: a regular expression pattern
        """
        if text_after and not include_pattern:
            raise Exception('No pattern specified to place text after. Specify a pattern with include_pattern argument.')
        
        pattern_str = text

        if include_pattern and not keep_matched:
            matched = re.search(include_pattern, pattern_str)
            if matched:
                pattern_str = ''
                # pattern_str = pattern_str.replace(matched.group(), '')
                pattern_str += self.get_regex(text[:matched.span()[0]])
                pattern_str += f'({include_pattern})'
                pattern_str += self.get_regex(text[matched.span()[1]:])
                return pattern_str

        # punctuations to encoding 
        for ch, enc in PUNCT_ENC_MAP.items():
            pattern_str = pattern_str.replace(ch, f' {enc} ' if spad_puncts else enc)
        
        # encoding to regex pattern
        for enc, pat in REGEX_PAT_DEC_MAP.items():
            pattern_str = re.sub(enc, pat, pattern_str)
        
        pattern_str = re.sub('\s+', '\\\\s*', pattern_str)
        pattern_str = re.sub(r'\n+', '\\\\n*', pattern_str)
        if include_pattern:
            if text_after:
                pattern_str = f'{include_pattern}\\s*{pattern_str}'
            else:
                pattern_str = f'{pattern_str}\\s*{include_pattern}'
        pattern_str = re.sub('(\\\\s\\*)+', '\\\\s*', pattern_str)
        pattern_str = re.sub('(\\\\s\\+)+', '\\\\s+', pattern_str)
        return pattern_str

if __name__ == '__main__':
    pass
