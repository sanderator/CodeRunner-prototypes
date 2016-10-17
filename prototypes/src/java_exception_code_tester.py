''' Prototype student-submitted Java code tester. Can deal with
multiple files submitted into Answer, multiple support files, or some
combination of the two. Handles (public and / or abstract) classes,
interfaces and enums. The only limitation is that everything must be declared
in a single package (this must not be the Java default package; but this
would be bad style anyway).

This module must be imported into a CodeRunner template with
from java_code_tester import *
and included as a support file.

Works by:
- filtering out public declarations from the Answer and support files
  - everything gets package access so it can live in one file
- replacing import statements with import statement for
  generally-useful packages
  - currently java.util.* and java.util.stream.*
- adding an executable class with a main method to run the tests
  - currently foobar.Tester
- smushing all code into one single .java file
  - currently Tester.java
- compiling and hopefully running the Java file

Limitations and works-by are sufficient for my current needs;
I may gradually be adding additional stuff.

(cc) CC BY-NC 4.0 2016 Peter Sander
'''

import os
import subprocess
import sys

from java_code_tester import *


# def _remove_cruft(student_answer):
#     '''Filters the student answer, mostly to get rid of expressions
#     and keywords that would be incompatible with all the code being
#     smushed into one single file.
#     '''
#     return student_answer \
#         .replace('public class ', 'class ') \
#         .replace('public abstract class ', 'abstract class ') \
#         .replace('abstract public class ', 'abstract class ') \
#         .replace('public interface ', 'interface ') \
#         .replace('public enum ', 'enum ') \
#         .replace('package ', '// package ') \
#         .replace('import ', '// import ')


# def _add_cruft(student_answer, import_static=None):
#     '''Adds expressions needed for the single code file.
#     Code goes into an arbitrary package because Java hates
#     having code in the default package (like nasty things happen
#     to static import statements).
#     '''
#     # adds frequently-used imports to the submitted answer
#     import_static = 'import static foobar.%s.*;' % import_static  \
#             if import_static else ''
#     return """
#     package foobar;

#     import java.util.*;
#     import java.util.stream.*;

#     // if you need a static import, it'll be put here
#     %s

#     %s

#     """ % (import_static, student_answer)


# #
# # Obligatory functions
# # These should always be called in order from the template
# #

# def assemble_student_answer(student_answer, import_static=None):
#     '''Removes 'unneeded' expressions and adds necessary expressions.
#     '''
#     return _add_cruft(_remove_cruft(student_answer), import_static)


# testfile = 'Tester.java'


# def assemble_support_files(ncoding='utf-8'):
#     '''Reads support files. Assembles files into a string,
#     then filters out cruft.
#     '''
#     support_files = '\n\n\n'.join([open(f, encoding=ncoding).read()
#             for f in os.listdir() if f.endswith('.java')])
#     return _remove_cruft(support_files)


def assemble_tester(student_answer, support_files,
            testcode, xception, ncoding='utf-8'):
    '''Smushes student answer and support files together and
    writes it out as one file.
    The resultant code goes into an arbitrary package because
    Java just doesn't like code in the default package.
    Adds a tester class which runs the tests.
    '''
    tester = '''
%s


%s


public class Tester {
    public static void main(String[] args) {
        try {
            %s
            System.out.println("Didn't raise any exception");
        } catch (%s e) {
            System.out.println(e.getMessage());
        } catch (Exception e) {
            System.out.println("Didn't raise an IllegalArgumentException");
        }
    }
}
''' % (student_answer, support_files, testcode, xception)
    # write out the string containing all the classes into a file
    with open(testfile, mode='w', encoding=ncoding) as fd:
        print(tester, file=fd)
        fd.close()


# def compile_and_run(ncoding='utf-8'):
#     '''Compiles and (hopefully) runs the tester code. The modified
#     student code and all the support files should already be smushed into a
#     single class foobar.Tester in the foobar/Tester.java file.
#     '''
#     if (subprocess.call(['javac', '-d', '.', '-encoding', ncoding, testfile])
#             or subprocess.call(['java', 'foobar.Tester'])):
#         print('** Further testing aborted **', file=sys.stderr)
