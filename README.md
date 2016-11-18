# CodeRunner-prototypes
Some prototypes for CodeRunner

Prototype template for static and / or dynamic checking of student answer Java code specifications.
The file _java_code_checkr.py_ should be included as a CodeRunner _Support file_ in a prototype,
eg, _LOCAL_PROTOTYPE_java_checkr_.
Java code questions then use this prototype as their _Question type_.

The support file java_code_checkr.py has the functions documented below:



 

__compile_and_run(student_answer, testcode, import_static=None, xception=None, ncoding='utf-8')

Assembles code (student answer, support files, tester class.
Then compiles and (hopefully) runs the tester code.
Example of use in template:

_from java_code_checkr import compile_and_run
compile_and_run("""{{STUDENT_ANSWER | e('py')}}""", '''{{TEST.testcode}}''')

When the student answer is expected to throw a given exception there is an additional argument:

_from java_code_checkr import compile_and_run
compile_and_run("""{{STUDENT_ANSWER | e('py')}}""", '''{{TEST.testcode}}''', xception='''{{QUESTION.parameters.exception}}''')
    
where the CodeRunner question type / Template params look like:

_{"exception": "IllegalArgumentException"}




__compile_and_findbugs(student_answer, testcode, import_static=None, xception=None, ncoding='utf-8')

Compiles the tester code and runs FindBugs on the bytecode.
Example of use in template:

_from java_code import compile_and_findbugs
compile_and_findbugs("""{{ STUDENT_ANSWER | e('py') }}""", '''{{TEST.testcode}}''')




__check_for_author(student_answer, existing_author=None)

Checks for an author tag in the javadoc comments. With an existing
author argument, checks that another author has been added.
This is in case the student was to modify existing code with an existing author.
If there's no additional author, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_author
check_for_author("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.existing_author}}''')

where the CodeRunner question type / Template params look like:

_{"existing_author": "J. Random Author"}




__check_for_enum(student_answer, enum)

Verifies that the appropriate enum is declared.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_enum
check_for_enum("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.enum}}''')

where the CodeRunner question type / Template params look like:

_{"enum": "DayOfWE"}


 

__check_for_enum_in_switch(student_answer, enum_const)

Verifies that the appropriate enum constant is used in a switch case statement.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_enum_in_switch
check_for_author("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.enum_const}}''')

where the CodeRunner question type / Template params look like:

_{{"enum": "DayOfWE", "enum_const": "SATURDAY"}}


 

__check_for_extends(student_answer, subclass, superclass)

Checks for 'class subclass extends superclass'.
If that's not the case, then raises an error and,stops further testing.
Example of use in template:

_from java_code_checkr import check_for_extends
check_for_extends("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.subclass}}''', '''{{QUESTION.parameters.superclass}}''')

where the CodeRunner question type / Template params look like:

_{"subclass": "Sub", "superclass":"Souper"}
