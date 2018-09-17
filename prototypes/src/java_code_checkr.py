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
  - currently java.util.* and java.util.stream.*
- adding an executable class with a main method to run the tests
  - currently foobar.Tester
- smushing all code into a single .java file
  - currently Tester.java
- compiling Tester.java and then delegating static code analysis
  heavy lifting to FindBugs (see below in this file)
  - see http://findbugs.sourceforge.net/

Limitations and works-by are sufficient for my current needs;
I may gradually be adding additional stuff.

(cc) CC BY-NC 4.0 2016 Peter Sander
'''

import os
import re
import subprocess
import sys


# arbitrary names
_package = 'foobar'
_testclass = 'foobar.Tester'
_testfile = 'Tester.java'

# to be adapted to wherever your findbugs stuff lives
_findbugs = '/opt/findbugs-3.0.1/lib/findbugs.jar'


def _remove_cruft(student_answer):
    '''Filters the student answer, mostly to get rid of expressions
    and keywords that would be incompatible with all the code being
    smushed into one single file.
    '''
    return student_answer \
        .replace('public class ', 'class ') \
        .replace('public abstract class ', 'abstract class ') \
        .replace('abstract public class ', 'abstract class ') \
        .replace('public final class ', 'final class ') \
        .replace('final public class ', 'final class ') \
        .replace('public interface ', 'interface ') \
        .replace('public enum ', 'enum ') \
        .replace('package ', '// package ') \
        .replace('import ', '// import ')


def _add_cruft(student_answer, import_static=None):
    '''Adds expressions needed for the single code file.
    Code goes into an arbitrary package because Java hates
    having code in the default package (with nasty things happening
    to import static statements).
    '''
    # adds frequently-used imports to the submitted answer
    import_static = 'import static foobar.%s.*;' % import_static  \
        if import_static else ''
    return """
package %s;

import java.awt.Color;
import java.awt.BorderLayout;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Image;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.function.*;
import java.util.stream.*;
import javax.swing.*;

// if you need a static import, it'll be put here
%s
%s
""" % (_package, import_static, student_answer)


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
        if f.endswith('.java')
    ])
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
        tester = '''
%s
%s
public class Tester {
    public static void main(String[] args) {
        %s
    }
}
''' % (student_answer, support_files, testcode)

    else:
        # expecting student answer to throw an exception
        tester = '''
%s
%s
public class Tester {
    public static void main(String[] args) {
        try {
            %s
            // this is not normal - we were expecting an exception
            System.out.println("Didn't raise any exception");
        } catch (%s e) {
            System.out.println(e.getMessage());
        } catch (Exception e) {
            System.out.println("Didn't raise expected %s");
        }
    }
}
''' % (student_answer, support_files, testcode, xception, xception)
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
    if (subprocess.call(
            ['javac', '-d', '.', '-encoding', ncoding, _testfile]) or
            subprocess.call(['java', _testclass])):
        print('** Further testing aborted **', file=sys.stderr)


def compile_and_findbugs(student_answer, testcode,
                         import_static=None, xception=None, ncoding='utf-8'):
    '''Compiles the tester code and runs FindBugs on the bytecode.
    '''
    student_answer = _assemble_student_answer(student_answer, import_static)
    support_files = _assemble_support_files(ncoding)
    _assemble_tester(student_answer, testcode, support_files, xception)
    if subprocess.call(['javac', '-d', '.', '-encoding', ncoding, _testfile]):
        # code didn't compile
        print("** Code doesn't compile - further testing aborted **",
              file=sys.stderr)
    else:
        fb_output = 'fb.out'
        subprocess.check_call(['java', '-jar', _findbugs, '-textui',
                               '-exclude', 'fb_exclude_filter.xml',
                               '-output', fb_output, '.'])
        if os.path.exists(fb_output) and os.path.getsize(fb_output) != 0:
            # FB had something to criticize
            with open(fb_output) as fbo:
                print(fbo.read())
        else:
            print('Code looks clean')


'''Checks whether student-submitted Java code conforms to given
specifications.
'''


class CodeOutOfSpecException(Exception):
    '''Specific exception to raise when the answer is out-of-spec.
    '''
    pass


def check_for_author(student_answer, existing_author=None):
    '''Checks for an author tag in the javadoc comments. With an existing
    author argument, checks that another author has been added.
    This is in case the student was to modify existing code with an
    existing author.
    If there's no additional author, then raises an error and
    stops further testing.
    '''
    classes = student_answer.count('class')
    authors = student_answer.count('@author')
    existing_authors = student_answer.count(existing_author)  \
        if existing_author else 0
    if classes > authors or existing_authors >= authors:
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - doesn't credit all authors.
''')
    else:
        print('Additional author added')


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
    else:
        print('%s extends %s' % (subclass, superclass))


def check_for_static_method(student_answer):
    pattern = re.compile('''
        static\s+   # keyword and spaces
        (.*)        # other stuff, eg, return type, name
        \(          # start of args
        ''', re.VERBOSE)
    match = pattern.search(student_answer)
    if match and not 'main' in match.group(1):
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - your methods shouldn't be static.
''')
    else:
        print('No static methods')


def check_for_enum(student_answer, enumb):
    '''Verifies that the appropriate enum is declared.
    If that's not the case, then raises an error and
    stops further testing.
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
    else:
        print('Specified enum declared')


def check_for_enum_in_switch(student_answer, enumb_const):
    '''Verifies that the appropriate enum constant is used in a switch
    case statement.
    If that's not the case, then raises an error and
    stops further testing.
    '''
    pattern = re.compile('''
        switch.*?       # keyword and stuff
        case\s+         # keyword and spaces
        %s:             # enum constant and keymark
        ''' % enumb_const, re.DOTALL | re.VERBOSE)
    match = pattern.search(student_answer)
    if not match:
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - you were supposed to use
    case %s:.
''' % enumb_const)
    else:
        print('Switch uses enum constants')


def check_for_reference(student_answer, some_class):
    if not student_answer.count(some_class):
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - it doesn't contains any reference to
    %s :.
''' % some_class)
    else:
        print('Ok reference to %s' % some_class)


def check_for_no_reference(student_answer, no_such_class):
    if student_answer.count(no_such_class):
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - it contains a reference to
    %s :.
''' % no_such_class)
    else:
        print('No reference to %s' % no_such_class)


def check_for_interface(student_answer, interface):
    if not student_answer.count('interface ' + interface):
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - it doesn't declare
    interface %s :.
''' % interface)
    else:
        print('Declares interface %s' % interface)


def check_for_no_procedural_style_loops(student_answer):
    if student_answer.count('for ' or 'while '):
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - it contains procedural style loops
''')
    else:
        print('No procedural style loops')


def check_for_functional_style_lambdas(student_answer):
    if not student_answer.count('->'):
        raise CodeOutOfSpecException('''
Your code may well execute...but:
Your code is out of spec - it doesn't contain functional style lambdas
''')
    else:
        print('Uses functional style lambdas')
