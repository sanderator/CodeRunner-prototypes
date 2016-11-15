'''Prototype static analyzer for student-submitted Java code. Can deal with
multiple files submitted into Answer, multiple support files, or some
combination of the two. Handles (public and / or abstract) classes,
interfaces and enums. The only limitation is that everything must be declared
in a single package (which must not be the Java default package; but this
would be bad style anyway).

This module must be imported into a CodeRunner template with
from java_code_findbugs import *
and included as a support file.

Works by:
- filtering out public from class, interface and enum declarations in
  the Answer and support files
  - these get package access so they can live in a single file
- replacing import statements with import statement for
  generally-useful packages
  - currently java.util.* and java.util.stream.*
- adding an executable class with a main method to run the tests
  - currently foobar.Tester
- smushing all code into a single .java file
  - currently Tester.java
- compiling Tester.java and then delegating the static code analysis
  heavy lifting to FindBugs
  - see http://findbugs.sourceforge.net/

Limitations and works-by are (sort of) sufficient for my current needs;
I may gradually be adding additional stuff.

(cc) CC BY-NC 4.0 2016 Peter Sander
'''

import os
import os.path
import subprocess
import sys


def _remove_cruft(student_answer):
    '''Filters the student answer, mostly to get rid of expressions
    and keywords that would be incompatible with all the code being
    smushed into one single file.
    '''
    return student_answer \
        .replace('public class ', 'class ') \
        .replace('public abstract class ', 'abstract class ') \
        .replace('abstract public class ', 'abstract class ') \
        .replace('public interface ', 'interface ') \
        .replace('public enum ', 'enum ') \
        .replace('package ', '// package ') \
        .replace('import ', '// import ')


def _add_cruft(student_answer, import_static=None):
    '''Adds expressions needed for the single code file.
    Code goes into an arbitrary package because Java hates
    having code in the default package (like nasty things happen
    to static import statements).
    '''
    # adds frequently-used imports to the submitted answer
    import_static = 'import static foobar.%s.*;' % import_static  \
        if import_static else ''
    return """
    package foobar;

    import java.util.*;
    import java.util.stream.*;

    // if you need a static import, it'll be put here
    %s
    %s
    """ % (import_static, student_answer)


#
# Obligatory functions
# These should always be called in order from the template
#

def assemble_student_answer(student_answer, import_static=None):
    '''Removes 'unneeded' expressions and adds necessary expressions.
    '''
    return _add_cruft(_remove_cruft(student_answer), import_static)


# all code end up in this file (the name is arbitrary)
_testfile = 'Tester.java'


def assemble_support_files(ncoding='utf-8'):
    '''Reads support files. Assembles files into a string,
    then filters out cruft.
    '''
    support_files = '\n\n\n'.join([open(f, encoding=ncoding).read()
                                   for f in os.listdir() if f.endswith('.java')])
    return _remove_cruft(support_files)


def assemble_tester(student_answer, support_files, testcode, ncoding='utf-8'):
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
        %s
    }
}
''' % (student_answer, support_files, testcode)
    # write out the string containing all the classes into a file
    with open(_testfile, mode='w', encoding=ncoding) as f:
        print(tester, file=f)


def compile_and_findbugs(ncoding='utf-8'):
    '''Compiles the tester code and runs FindBugs on the bytecode.
    The modified student code and all the support files should already be
    smushed into a single Tester.java file.
    '''
    if subprocess.call(['javac', '-d', '.', '-encoding', ncoding, _testfile]):
        # code didn't compile
        print("** Code doesn't compile - further testing aborted **",
                file=sys.stderr)
    else:
        # to be adapted to where your findbugs stuff lives
        findbugs = '/opt/findbugs-3.0.1/lib/findbugs.jar'
        fb_output = 'fb.out'
        subprocess.check_call(['java', '-jar', findbugs, '-textui',
                               '-output', fb_output, '.'])
        if os.path.exists(fb_output) and os.path.getsize(fb_output) != 0:
            # FB had something to criticize
            with open(fb_output) as fbo:
                print(fbo.read())
        else:
            print('Code looks clean')
