# CodeRunner-prototypes
CodeRunner (http://coderunner.org.nz/) is a nifty plugin for executing student code in Moodle. This prototype (should) makes it easier to develop questions for Java code. It is designed for static and / or dynamic checking of some student answers in Java.

The file _java_code_checkr.py_ should be included as a CodeRunner _Support file_ in a prototype, eg, _LOCAL_PROTOTYPE_java_checkr_.
Java code questions then use this prototype as their _Question type_.

A major limitation is that everything must be declared in a single package, and this must not be the Java default package; but that
would be bad style anyway.

The support file java_code_checkr.py has the functions documented below:



 

__compile_and_run(student_answer, testcode, import_static=None, xception=None, ncoding='utf-8')__

Assembles code (student answer, support files, tester class).
Then compiles and (hopefully) runs the tester code.
Example of use in template:

_from java_code_checkr import compile_and_run
compile_and_run("""{{STUDENT_ANSWER | e('py')}}""", '''{{TEST.testcode}}''')_

When the student answer is expected to throw a given exception there is an additional argument:

_from java_code_checkr import compile_and_run
compile_and_run("""{{STUDENT_ANSWER | e('py')}}""", '''{{TEST.testcode}}''', xception='''{{QUESTION.parameters.exception}}''')_
    
where the CodeRunner question type / Template params look like:

_{"exception": "IllegalArgumentException"}_




__compile_and_findbugs(student_answer, testcode, import_static=None, xception=None, ncoding='utf-8')__

Compiles the tester code and runs FindBugs on the bytecode.
Note that findbugs (http://findbugs.sourceforge.net/) must be installed on the CodeRunner server at the hardwired location /opt/findbugs-3.0.1/lib/findbugs.jar (change as necessary).
Example of use in template:

_from java_code import compile_and_findbugs
compile_and_findbugs("""{{ STUDENT_ANSWER | e('py') }}""", '''{{TEST.testcode}}''')_




__compile_and_junit(student_answer, testcode, import_static=None, xception=None, ncoding='utf-8')__

Compiles the tester code and runs JUnit 5. The student answer must contain both the class under test and the test class.
Note that JUnit 5 (https://junit.org/junit5/) must be installed on the CodeRunner server at the hardwired location /usr/share/java/junit-platform-console-standalone.jar (change as necessary).
Example of use in template:

_from java_code import compile_and_junit
compile_and_junit(student_answer, testcode, import_static=None, xception=None, ncoding='utf-8')_




__check_for_author(student_answer, existing_author=None)__

Checks for an author tag in the javadoc comments. With an existing
author argument, checks that another author has been added.
This is in case the student was to modify existing code with an existing author.
If there's no additional author, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_author
check_for_author("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.existing_author}}''')_

where the CodeRunner question type / Template params look like:

_{"existing_author": "J. Random Author"}_


 

__check_for_extends(student_answer, subclass, superclass)__

Checks for 'class subclass extends superclass'.
If that's not the case, then raises an error and,stops further testing.
Example of use in template:

_from java_code_checkr import check_for_extends
check_for_extends("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.subclass}}''', '''{{QUESTION.parameters.superclass}}''')_

where the CodeRunner question type / Template params look like:

_{"subclass": "Sub", "superclass":"Souper"}_


 

__check_for_public(student_answer)__

Checks that code contains no public atribute on method, except for the main method of course, and perhaps toString. If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_public
check_for_public("""{{ STUDENT_ANSWER | e('py') }}""")_


 

__check_for_static_method(student_answer)__

Checks that code contains no static method, except for the main method of course. If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_static_method
check_for_static_method("""{{ STUDENT_ANSWER | e('py') }}""")_


 

__check_for_enum(student_answer, enum)__

Verifies that the appropriate enum is declared. If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_enum
check_for_enum("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.enum}}''')_

where the CodeRunner question type / Template params look like:

_{{"enum": "DayOfWE", "enum_const": "SATURDAY"}}_


 

__check_for_enum_in_switch(student_answer, enum_const)__

Verifies that the appropriate enum constant is used in a switch case statement.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_enum_in_switch
check_for_enum_in_switch("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.enum_const}}''')_

where the CodeRunner question type / Template params look like:

_{{"enum": "DayOfWE", "enum_const": "SATURDAY"}}_


 

__check_for_reference(student_answer, some_class)__

Verifies that the code contains a reference to the given class.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_reference
check_for_reference("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.some_class}}''')_

where the CodeRunner question type / Template params look like:

_{{"some_class": "SomeClass"}}_


 

__check_for_no_reference(student_answer, some_class)__

Verifies that the code does not contain any reference to the given class.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_no_reference
check_for_no_reference("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.some_class}}''')_

where the CodeRunner question type / Template params look like:

_{{"some_class": "SomeClass"}}_


 

__check_for_interface(student_answer, some_interface)__

Verifies that the code contains a reference to the given interface.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_interface
check_for_interface("""{{ STUDENT_ANSWER | e('py') }}""", '''{{QUESTION.parameters.some_interface}}''')_

where the CodeRunner question type / Template params look like:

_{{"some_interface": "SomeAble"}}_


 

__check_for_no_procedural_style_loops(student_answer)__

Verifies that the code contains no procedural style loops, eg for.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_no_procedural_style_loops
check_for_no_procedural_style_loops("""{{ STUDENT_ANSWER | e('py') }}""")__


 

__check_for_functional_style_lambdas(student_answer)__

Verifies that the code contains some functional style
lambda, eg someCollection.forEach(e -> {}.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_functional_style_lambdas
check_for_functional_style_lambdas("""{{ STUDENT_ANSWER | e('py') }}""")__


 

__check_for_no_functional_style_lambdas(student_answer)__

Verifies that the code contains no functional style
lambdas.
If that's not the case, then raises an error and stops further testing.
Example of use in template:

_from java_code_checkr import check_for_no_functional_style_lambdas
check_for_no_functional_style_lambdas("""{{ STUDENT_ANSWER | e('py') }}""")__
