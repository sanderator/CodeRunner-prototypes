'''Catches Python unittest output. This is specific for CodeRunner; it should
be included as a support file in the LOCAL_PROTOTYPES_python_checkr question type.

Catching the output serves two purposes:
First, unittest outputs to stderr. When CR detects stderr output it panics
and prints an ***Error*** message. This interferes with unittest's
expected output.
Second, unittest outputs the time taken for tests. This has to be neutralized
because it can vary for different users.
:author: Peter Sander
'''
import contextlib
import io
import unittest

# find all tests in this module
import __main__

def diddle():
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    with io.StringIO() as buf:
        # run the tests
        with contextlib.redirect_stdout(buf):
            unittest.TextTestRunner(stream=buf).run(suite)
        # process the results - neutralise the time taken
        # since this can vary depending on the phases of the moon
        result = buf.getvalue()
        start = result.find(' in ') + len(' in ')
        end = result.find('s', start, len(result))
        result = result.replace(result[start:end], 'X.XXX')
        print(result)