#!/usr/bin/env python3

import os
import os.path
import sys
import unittest

sys.path.append(os.path.join(sys.path[0], '../src'))
from java_code_checkr import check_for_author
from java_code_checkr import check_for_reference
from java_code_checkr import check_for_no_reference
from java_code_checkr import check_for_interface
from java_code_checkr import CodeOutOfSpecException


class CheckrTest(unittest.TestCase):
    def setUp(self):
        self.student_answer = '''
/**
 * Does something awesome.
 * @author J. Random Author
 */
public class Awesome {
    // something awesome
}
'''
        self.existing_author = 'J. Random Author'

    def test_existing_author_only(self):
        self.assertRaises(
            CodeOutOfSpecException,
            check_for_author,
            (self.student_answer, self.existing_author))

    def test_additional_author(self):
        student_answer = '''
/**
 * Does something awesome.
 * @author J. Random Author
 * @author Alfred E. Neuman
 */
public class Awesome {
    // something awesome
}
'''
        self.assertEqual(check_for_author(
            student_answer, self.existing_author), None)

    def test_reference(self):
        '''Checks that student code contain a
        reference to a given class.
        '''
        student_answer = '''
public class Awesome {
    private SomeClass sc;
}
'''
        self.assertEqual(check_for_reference(student_answer,
            'SomeClass'), None)

    def test_reference_KO(self):
        '''Checks that student code contain a
        reference to a given class.
        '''
        self.assertRaises(
            CodeOutOfSpecException,
            check_for_reference,
            self.student_answer, 'SomeClass')

    def test_no_reference(self):
        '''Checks that student code does not contain any
        reference to a given class.
        '''
        self.assertEqual(check_for_no_reference(self.student_answer,
            'NoSuchClass'), None)

    def test_no_reference_KO(self):
        '''Checks that student code does not contain any
        reference to a given class.
        '''
        student_answer = '''
public class Awesome {
    private SomeClass sc;
}
'''
        self.assertRaises(
            CodeOutOfSpecException,
            check_for_reference,
            self.student_answer, 'SomeClass')

    def test_interface(self):
        '''Checks that student code declares interface.
        '''
        interface = 'SomethingAble'
        student_answer = '''
public interface SomethingAble {
    // rest of code
}
'''
        self.assertEqual(check_for_interface(student_answer, interface),
            None)


if __name__ == '__main__':
    unittest.main()
