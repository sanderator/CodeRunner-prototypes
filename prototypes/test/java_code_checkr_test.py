#!/usr/bin/env python3

import os
import os.path
import sys
import unittest

sys.path.append(os.path.join(sys.path[0], '../src'))
from java_code_checkr import check_for_author
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


if __name__ == '__main__':
    unittest.main()
