'''Checks whether student-submitted Java code conforms to specifications.
The remove_cruft and add_cruft functions must be run to set up the
student answer and any support files. Then further functions can be run
to test for various code features.
An informative exception is raised at the first out-of-spec code and
processing halts.

This module must be imported into a CodeRunner template with
from java_code_checker import *
and included as a support file.
This is in addition to any requirements for the java_code_tester module.

Limitations and shortcomings are sufficient for my current needs;
I may gradually be adding additional stuff.

(cc) CC BY-NC 4.0 2016 Peter Sander
'''

import re


class CodeOutOfSpecException(Exception):
    '''Specific exception to raise when the answer is out-of-spec,
    ie, doesn't define an enum anywhere.
    '''
    pass


#
# Optional functions
# These may be called from the template to check for
# various code features
#

def check_for_extends(student_answer, subclass, superclass):
    '''Checks for 'class subclass extends superclass'.
    If that's not the case, then raises an error and
    stops further testing.
    '''
    pattern = re.compile('''
            class\s+    # keyword and spaces
            %s\s+       # subclass name and spaces
            extends\s+  # keyword and spaces
            %s          # superclass name
            ''' % (subclass, superclass), re.VERBOSE)
    if not pattern.search(student_answer):
        raise CodeOutOfSpecException('''
    Your code may well execute...but:
    Your code is out of spec - you were supposed to define
        %s extends %s.
    ''' % (subclass, superclass))


def check_for_enum(student_answer, enumb):
    '''Verifies that the appropriate enum is declared.
    If that's not the case, then raises an error and
    stops further testing.
    That'll teach'em!
    '''
    pattern = re.compile('''
            enum\s+     # keyword and spaces
            %s          # enum name
            ''' % enumb, re.VERBOSE)
    match = pattern.search(student_answer)
    if not match:
        raise CodeOutOfSpecException('''
    Your code may well execute...but:
    Your code is out of spec - you were supposed to define
        enum %s.
    ''' % enumb)
