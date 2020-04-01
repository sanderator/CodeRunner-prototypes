'''Checks student-submitted Java code.
Can handle multiple files submitted into Answer, multiple support files,
or some combination of the two. Handles (public and / or abstract) classes,
interfaces and enums. The only limitation is that everything must be declared
in a single package, and this must not be the Java default package; but that
would be bad style anyway.

Does both
- dynamic code testing by providing the structure for running test cases
  and comparing expected and actual results
- static code analysis by
  - running FindBugs on student answers to check soundness
  - checking for specific features in the answers, eg, is a switch used

Functions from this module must be imported into a CR template with, eg,
from java_code_checkr import compile_and_run
This file is intended to be a support file for some CR prototype, eg, we use
LOCAL_PROTOTYPE_java_code_checkr

Works (mostly) by:
- filtering out public from class, interface and enum declarations in
  the Answer and .java support files
  - these then get package access so they can live in a single file
  - doesn't modify variable or method acces
- filtering out package declarations and placing everything into the same
  package
  - currently called foobar (for sentimental reasons)
- replacing import statements with import statement for
  generally-useful packages
  - currently java.util.*, java.util.function.*, and java.util.stream.*.
    And some others (see the code below)
- adding an executable class with a main method to run the tests
  - currently foobar.Tester
- smushing all code into a single .java file
  - currently Tester.java
- compiling Tester.java and then delegating static code analysis
  heavy lifting to FindBugs (see below in this file)
  - see http://findbugs.sourceforge.net/

Limitations and works-by are sufficient for my current needs;
I may gradually be adding additional stuff.

(cc) CC BY-NC 4.0 2016-2020 Peter Sander
'''

import os
import re
import subprocess
import sys


# arbitrary names
_package = 'foobar'
_testclass = 'foobar.Tester'
_testfile = 'Tester.java'


def _remove_cruft(student_answer):
    '''Filters the student answer, mostly to get rid of expressions
    and keywords that would be incompatible with all the code being
    smushed into one single file.
    '''
    num_main_calls = student_answer.count("if __name__ == '__main__'")
    return student_answer \
        .replace('import ', '#import ') \
        .replace('from ', '#from ') \
        .replace("if __name__ == '__main__'",
                 "if __name__ == '__main__'",
                 num_main_calls - 1) \
        .replace('''if __name__ == '__main__':
    main()
''', '''if __name__ == '__main__':
    diddle()
''')


def _add_cruft(student_answer, import_static=None):
    '''Adds expressions needed for the single code file.
    Code goes into an arbitrary package because Java hates
    having code in the default package (with nasty things happening
    to import static statements).
    '''
    # adds frequently-used imports to the submitted answer
    import_static = 'import static foobar.%s.*;' % import_static  \
        if import_static else ''
    return f'''
import unittest
from diddle_unittest_for_coderunner import diddle

{student_answer}
'''


def _assemble_student_answer(student_answer, import_static=None):
    '''Removes 'unneeded' expressions and adds necessary expressions.
    '''
    return _add_cruft(_remove_cruft(student_answer), import_static)


def _assemble_support_files(ncoding='utf-8'):
    '''Inputs support files, assembles files into a string,
    then filters out cruft.
    '''
    support_files = '\n\n\n'.join([
        open(f, encoding=ncoding).read()
        for f in os.listdir()
        if f.endswith('.py')])
    return _remove_cruft(support_files)


def _assemble_tester(student_answer, testcode, support_files,
                     xception=None, ncoding='utf-8'):
    '''Smushes student answer and support files together with an
    executable tester class and writes everything out into one file.
    The resultant code goes into an arbitrary package because
    Java just doesn't like code in the default package.
    '''
    if not xception:
        # not expecting to deal with exceptions
        tester = f'''
{student_answer}
{support_files}
{testcode}
'''

    # write out the string containing all the classes into a file
    with open(_testfile, mode='w', encoding=ncoding) as f:
        print(tester, file=f)


def compile_and_run(student_answer, testcode,
                    import_static=None, xception=None, ncoding='utf-8'):
    '''Assembles code (student answer, support files, tester class.
    Then compiles and (hopefully) runs the tester code.
    '''
    student_answer = _assemble_student_answer(student_answer, import_static)
    support_files = _assemble_support_files(ncoding)
    _assemble_tester(student_answer, testcode, support_files, xception)
    if subprocess.call(['python3', _testfile]):
        # code didn't compile
        print('** Further testing aborted **', file=sys.stderr)
