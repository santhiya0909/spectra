"""
SPECTRA Complete Curriculum Seeder
Builds all 8 active learning subjects with 10 lessons each:
1. Java Programming (JAVA) - 10 Lessons
2. Python Programming (PYTHON) - 10 Lessons
3. Mathematics (MATH) - 10 Lessons
4. Chemistry (CHEM) - 10 Lessons
5. Artificial Intelligence (AI) - 10 Lessons
6. Data Structures (DSA) - 10 Lessons
7. Machine Learning (ML) - 10 Lessons
8. Web Development (WEB) - 10 Lessons

Guarantees:
- Every subject has >= 10 lessons
- Every lesson has at least 1 interactive puzzle
- Every lesson has at least 5 meaningful quiz questions
- Topics have practice questions
- Idempotent execution
"""
import sys
import os
import json
from datetime import datetime, timezone, timedelta

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

from app.db.database import SessionLocal, create_tables
from app.db.models.academic import Subject, Topic, Lesson, LessonProgress, Enrollment, StudyResource
from app.db.models.quiz import Question, Quiz, QuizQuestion, QuizAttempt, QuizResponse
from app.db.models.puzzle import Puzzle, PuzzleAttempt
from app.db.models.performance import StudentTopicPerformance
from app.db.models.recommendation import Recommendation, LearningPlan, LearningPlanItem
from app.db.models.user import StudentProfile, User
from app.core.security import get_password_hash
from app.services.enrollment import enroll_student_in_default_subjects

from scripts.curriculum_definitions import SUBJECTS_DATA

# Additional 7 Subjects data dictionary
OTHER_SUBJECTS_DATA = [
    {
        "code": "PYTHON",
        "name": "Python Programming",
        "description": "Learn Python data structures, functional idioms, OOP, modules, and algorithmic problem solving.",
        "category": "PROGRAMMING",
        "difficulty": "BEGINNER",
        "order": 2,
        "lessons": [
            ("01 — Python Introduction", "Introduction to Python philosophy, indentation syntax, interpreted execution, and REPL.",
             [("Python Philosophy & Zen", "Readability counts, explicit is better than implicit.", "EASY"),
              ("Interpreted Execution", "CPython interpreter and dynamic bytecode execution.", "EASY")],
             ("CODE_OUTPUT", "Print Greeting", "What is the output of print('Python ' * 2)?", "print('Python ' * 2)", "Python Python ", "String multiplication repeats strings.", "EASY"),
             [("Which file extension is standard for Python source code?", ["A) .py", "B) .python", "C) .pyc", "D) .pt"], "A) .py", "Python source files use .py.", "EASY"),
              ("What role does whitespace indentation play in Python syntax?", ["A) Stylistic only", "B) Defines block scoping and hierarchy", "C) Ignored by interpreter", "D) Required only on comments"], "B) Defines block scoping and hierarchy", "Indentation defines block scope in Python.", "EASY"),
              ("Which function prints formatted output to the terminal?", ["A) echo()", "B) print()", "C) System.out()", "D) write()"], "B) print()", "print() outputs to stdout.", "EASY"),
              ("Is Python dynamically typed or statically typed?", ["A) Statically typed", "B) Dynamically typed", "C) Untyped", "D) Assembly typed"], "B) Dynamically typed", "Types are checked at runtime.", "EASY"),
              ("Which tool starts the interactive Python Read-Eval-Print Loop?", ["A) python in terminal", "B) compile.exe", "C) pyrun", "D) jupyter-only"], "A) python in terminal", "Invoking python without arguments opens the REPL.", "EASY")]),
            ("02 — Variables and Data Types", "Variables, numeric types, strings, boolean values, and type casting in Python.",
             [("Variables & Binding", "Variables as memory references rather than boxed storage.", "EASY"),
              ("Built-in Types", "int, float, complex, bool, and str fundamentals.", "EASY")],
             ("MULTIPLE_CHOICE", "Type Identification", "What is the data type of the expression type(3.14)?", ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"], "<class 'float'>", "Python floating point literals are represented as float.", "EASY"),
             [("What will type(True) return in Python?", ["A) <class 'bool'>", "B) <class 'boolean'>", "C) <class 'int'>", "D) <class 'str'>"], "A) <class 'bool'>", "Booleans have type bool.", "EASY"),
              ("How do you convert the string '42' into an integer?", ["A) int('42')", "B) Integer.parse('42')", "C) (int)'42'", "D) str.to_int('42')"], "A) int('42')", "int() performs type casting.", "EASY"),
              ("Which quotes can be used to define multi-line strings in Python?", ["A) Triple single or double quotes", "B) Backticks only", "C) Double quotes only", "D) Square brackets"], "A) Triple single or double quotes", "Triple quotes permit multi-line strings.", "EASY"),
              ("What is the result of 10 // 3 in Python 3?", ["A) 3.333", "B) 3", "C) 1", "D) 4"], "B) 3", "// performs floor division.", "EASY"),
              ("Are variable names case-sensitive in Python?", ["A) No", "B) Yes (Age and age are distinct)", "C) Only in functions", "D) Depends on OS"], "B) Yes (Age and age are distinct)", "Python identifiers are strictly case-sensitive.", "EASY")]),
            ("03 — Operators", "Arithmetic, comparison, logical (and, or, not), identity (is), and membership (in).",
             [("Arithmetic & Bitwise", "Arithmetic operators and bitwise manipulations.", "EASY"),
              ("Identity vs Equality", "The critical distinction between '==' and 'is'.", "MEDIUM")],
             ("TRUE_FALSE", "Identity vs Equality", "In Python, 'a == b' checks if two objects share the exact same memory address.", "a == b checks memory address", False, "== compares logical value equality; 'is' checks memory identity (id).", "MEDIUM"),
             [("What does the 'in' keyword evaluate in a sequence?", ["A) Element membership", "B) Sequence length", "C) Memory pointer", "D) Index number"], "A) Element membership", "in tests whether a key or element exists inside a collection.", "EASY"),
              ("What is the output of 2 ** 3 in Python?", ["A) 6", "B) 8", "C) 5", "D) 9"], "B) 8", "** is the exponentiation operator: 2^3 = 8.", "EASY"),
              ("How does 'not True or False' evaluate according to operator precedence?", ["A) True", "B) False", "C) None", "D) SyntaxError"], "B) False", "not True evaluates to False; False or False evaluates to False.", "MEDIUM"),
              ("Which operator checks whether two variables refer to different objects?", ["A) !=", "B) is not", "C) not in", "D) <>"], "B) is not", "is not checks object identity inequality.", "EASY"),
              ("What does bool([]) evaluate to in Python?", ["A) True", "B) False", "C) None", "D) Error"], "B) False", "Empty collections evaluate to falsy in boolean contexts.", "EASY")]),
            ("04 — Conditions", "If, elif, else branching, conditional expressions, and boolean logic.",
             [("If-Elif-Else Ladder", "Sequential conditional branching.", "EASY"),
              ("Ternary Expressions", "x if condition else y inline syntax.", "EASY")],
             ("FILL_BLANK", "Elif Syntax", "Fill in the Python keyword for else-if: if x > 0: print('+') _____ x < 0: print('-')", "if x > 0: ... _____ x < 0: ...", "elif", "Python uses elif instead of else-if.", "EASY"),
             [("Which keyword terminates conditional branching if all prior checks fail?", ["A) else", "B) default", "C) otherwise", "D) end"], "A) else", "else executes when all preceding if and elif conditions evaluate to false.", "EASY"),
              ("What is the syntax for a Python ternary operator?", ["A) condition ? a : b", "B) a if condition else b", "C) if(condition, a, b)", "D) a when condition else b"], "B) a if condition else b", "Python uses 'val_if_true if cond else val_if_false'.", "EASY"),
              ("Can you have multiple elif statements in a single conditional block?", ["A) No, only one", "B) Yes, as many as needed", "C) Up to 3", "D) Only in functions"], "B) Yes, as many as needed", "An if statement can be followed by any number of elif branches.", "EASY"),
              ("What happens if no condition in an if-elif block matches and there is no else?", ["A) An exception is raised", "B) Execution simply continues past the block", "C) Program crashes", "D) Last branch executes"], "B) Execution simply continues past the block", "The block completes without taking any branch action.", "EASY"),
              ("Which value is considered truthy in Python?", ["A) 0", "B) \"\"", "C) [1]", "D) None"], "C) [1]", "Non-empty collections evaluate to True.", "EASY")]),
            ("05 — Loops", "For loops with range(), while loops, loop control with break, continue, and the loop else clause.",
             [("For Loops & Range", "Iterating over sequences and generators with range(start, stop, step).", "EASY"),
              ("While & Loop Else", "Indefinite iteration and Python's unique loop-else block.", "MEDIUM")],
             ("CODE_OUTPUT", "Range Output", "What is the output of this loop?\nfor i in range(1, 4):\n    print(i, end='')", "for i in range(1, 4): print(i, end='')", "123", "range(1, 4) produces 1, 2, 3.", "EASY"),
             [("What does range(2, 8, 2) generate in Python?", ["A) 2, 4, 6", "B) 2, 4, 6, 8", "C) 2, 3, 4", "D) 8, 6, 4, 2"], "A) 2, 4, 6", "range stops before the end value 8.", "EASY"),
              ("When does the 'else' block attached to a Python while loop execute?", ["A) When the loop terminates normally without hitting a break", "B) Only if the loop breaks", "C) On every iteration", "D) Only when an exception occurs"], "A) When the loop terminates normally without hitting a break", "Loop else executes upon natural exhaustion.", "MEDIUM"),
              ("Which statement skips the remainder of the current loop iteration?", ["A) pass", "B) break", "C) continue", "D) skip"], "C) continue", "continue advances to the next iteration.", "EASY"),
              ("What does the 'pass' statement do in Python?", ["A) Terminates program", "B) A null operation placeholder that does nothing", "C) Returns None", "D) Restarts loop"], "B) A null operation placeholder that does nothing", "pass acts as an executable no-op placeholder.", "EASY"),
              ("Can you iterate directly over characters in a string with a for loop?", ["A) No, string must be split first", "B) Yes, strings are iterable sequences", "C) Only with while loop", "D) Only using regex"], "B) Yes, strings are iterable sequences", "Strings implement sequence iteration over their characters.", "EASY")]),
            ("06 — Functions", "Def syntax, parameters, default arguments, *args, **kwargs, lambda functions, and scope.",
             [("Defining Functions", "def statement, docstrings, and return statements.", "EASY"),
              ("Arbitrary Arguments", "*args for tuples, **kwargs for keyword dictionaries.", "MEDIUM"),
              ("Lambda Functions", "Anonymous single-expression functions.", "MEDIUM")],
             ("MULTIPLE_CHOICE", "Lambda Evaluation", "What is the return value of (lambda x: x ** 2)(5)?", ["5", "10", "25", "None"], "25", "The lambda computes 5 ** 2 = 25.", "EASY"),
             [("Which keyword defines a named function in Python?", ["A) function", "B) def", "C) fn", "D) func"], "B) def", "def defines callable functions.", "EASY"),
              ("What is the default return value of a Python function that lacks an explicit return statement?", ["A) 0", "B) False", "C) None", "D) void"], "C) None", "Functions implicitly return None.", "EASY"),
              ("In a function definition 'def func(*args)', what data type does args represent?", ["A) list", "B) tuple", "C) dict", "D) set"], "B) tuple", "*args captures positional arguments as a tuple.", "MEDIUM"),
              ("In 'def func(**kwargs)', what data type does kwargs represent?", ["A) list", "B) tuple", "C) dictionary", "D) generator"], "C) dictionary", "**kwargs captures keyword arguments into a dictionary.", "MEDIUM"),
              ("What is the scope of a variable declared inside a function body without 'global'?", ["A) Global", "B) Local to the function", "C) Module-wide", "D) Builtin"], "B) Local to the function", "Variables declared inside function bodies are local in scope.", "EASY")]),
            ("07 — Lists and Tuples", "Indexed sequences, slicing, list comprehensions, immutability of tuples, and unpacking.",
             [("List Operations & Slicing", "Indexing, negative indexing, and stride slicing [start:stop:step].", "EASY"),
              ("Tuples & Immutability", "Immutable ordered collections, named tuples, and tuple unpacking.", "MEDIUM"),
              ("List Comprehensions", "Concise declarative list transformation syntax.", "MEDIUM")],
             ("CODE_OUTPUT", "List Slicing Output", "What is the output of numbers = [10, 20, 30, 40, 50]; print(numbers[1:4])?", "numbers = [10, 20, 30, 40, 50]; print(numbers[1:4])", "[20, 30, 40]", "Slice [1:4] takes indices 1, 2, and 3.", "EASY"),
             [("Which property differentiates a Python tuple from a Python list?", ["A) Tuples cannot store integers", "B) Tuples are immutable; lists are mutable", "C) Lists cannot be nested", "D) Tuples do not support indexing"], "B) Tuples are immutable; lists are mutable", "Tuples cannot have elements appended or modified after creation.", "EASY"),
              ("What does [x * 2 for x in [1, 2, 3]] produce?", ["A) [2, 4, 6]", "B) [1, 2, 3, 1, 2, 3]", "C) [2, 2, 2]", "D) 12"], "A) [2, 4, 6]", "List comprehension multiplies each element by 2.", "EASY"),
              ("How do you add an element to the end of an existing list in Python?", ["A) list.add(x)", "B) list.append(x)", "C) list.push(x)", "D) list.insert_last(x)"], "B) list.append(x)", "append() places an item at the end of the list.", "EASY"),
              ("What does numbers[-1] access in a Python list?", ["A) The first item", "B) The last item", "C) The second item", "D) Causes an error"], "B) The last item", "Negative index -1 accesses the final element.", "EASY"),
              ("Can a tuple contain mutable objects such as lists as its elements?", ["A) No, all nested items must be immutable", "B) Yes, the tuple structure is immutable, but mutable elements can mutate", "C) Only in Python 2", "D) Only if frozen"], "B) Yes, the tuple structure is immutable, but mutable elements can mutate", "Tuples hold fixed references, but referenced objects may be internally mutable.", "MEDIUM")]),
            ("08 — Dictionaries and Sets", "Key-value hash maps, hashing requirements, set operations (union, intersection), and dictionary comprehensions.",
             [("Dictionaries & Hashing", "Key-value storage, .get() default values, and hashable keys.", "MEDIUM"),
              ("Sets & Set Algebra", "Unique element enforcement, intersection, union, and difference.", "MEDIUM")],
             ("MATCHING", "Set Operations Matching", "Match each set operator with its mathematical operation:",
              [["&", "Intersection"], ["|", "Union"], ["-", "Difference"], ["^", "Symmetric Difference"]],
              {"&": "Intersection", "|": "Union", "-": "Difference", "^": "Symmetric Difference"},
              "& intersects, | unions, - subtracts, and ^ finds symmetric difference.", "MEDIUM"),
             [("What happens if you access a non-existent key in a dict using dict['key']?", ["A) Returns None", "B) Raises KeyError", "C) Creates key with None", "D) Returns 0"], "B) Raises KeyError", "Square bracket lookup on missing keys raises KeyError; use .get() for safe default retrieval.", "MEDIUM"),
              ("Which data type cannot be used as a dictionary key in Python?", ["A) str", "B) int", "C) list", "D) tuple of ints"], "C) list", "Dictionary keys must be hashable and immutable; lists are unhashable.", "MEDIUM"),
              ("What is the result of len({1, 2, 2, 3, 3, 3})?", ["A) 6", "B) 3", "C) 1", "D) Error"], "B) 3", "Sets automatically deduplicate elements, leaving {1, 2, 3}.", "EASY"),
              ("How do you safely access a dictionary value with a default fallback if the key is missing?", ["A) d.find(k, default)", "B) d.get(k, default)", "C) d.try(k)", "D) d.fetch(k)"], "B) d.get(k, default)", "get() returns the default argument when the key is absent.", "EASY"),
              ("What data structure underlies Python dictionaries to provide average O(1) lookups?", ["A) Binary Search Tree", "B) Hash Table", "C) Linked List", "D) B-Tree"], "B) Hash Table", "Dictionaries use open addressing hash tables.", "MEDIUM")]),
            ("09 — Object Oriented Programming", "Classes, __init__ constructor, self reference, inheritance, dunder methods, and encapsulation in Python.",
             [("Classes & Instances", "Defining classes, __init__ initializer, and self instance binding.", "MEDIUM"),
              ("Inheritance & Polymorphism", "Subclassing, super() calls, and method overriding.", "HARD"),
              ("Dunder Special Methods", "__str__, __repr__, __len__, and operator overloading.", "HARD")],
             ("TRUE_FALSE", "Private Variables in Python", "Python strictly prevents runtime access to private attributes prefixed with '__' using bytecode-level hardware locks.", "Python has strict private locks", False, "Python uses name mangling (_ClassName__attr) rather than hard access restriction; encapsulation relies on convention.", "MEDIUM"),
             [("What is the conventional first parameter of instance methods in Python classes?", ["A) this", "B) self", "C) cls", "D) instance"], "B) self", "self represents the calling instance.", "EASY"),
              ("Which method is invoked automatically when an object is instantiated?", ["A) __new__", "B) __init__", "C) __create__", "D) __start__"], "B) __init__", "__init__ acts as the instance initializer constructor.", "EASY"),
              ("How do you call a method from a parent class in a subclass in Python 3?", ["A) parent.method()", "B) super().method()", "C) base.method()", "D) this.super()"], "B) super().method()", "super() returns a proxy object delegating method calls to the parent class.", "MEDIUM"),
              ("What does defining the __str__ dunder method on a class accomplish?", ["A) Compresses the object", "B) Returns a human-readable string representation of the object", "C) Converts object to binary", "D) Prevents string casting"], "B) Returns a human-readable string representation of the object", "__str__ is called by str(obj) and print(obj).", "MEDIUM"),
              ("Can a Python class inherit from multiple base classes simultaneously?", ["A) No, only single inheritance", "B) Yes, Python supports multiple inheritance using C3 linearization (MRO)", "C) Only if classes are abstract", "D) Only in Python 2"], "B) Yes, Python supports multiple inheritance using C3 linearization (MRO)", "Python supports multiple inheritance resolved via Method Resolution Order (MRO).", "HARD")]),
            ("10 — Exceptions, Files and Modules", "Try-except-finally blocks, custom exception classes, context managers with 'with', file I/O, and imports.",
             [("Exception Handling", "try, except, else, finally, and raising exceptions.", "MEDIUM"),
              ("File I/O & Context Managers", "open(), read/write modes, and with statement resource auto-closure.", "MEDIUM"),
              ("Modules & Packages", "import, from ... import, and __name__ == '__main__'.", "EASY")],
             ("FILL_BLANK", "Context Manager Keyword", "Fill in the keyword that ensures files are automatically closed: _____ open('data.txt') as f:", "_____ open('data.txt') as f:", "with", "The with statement invokes context managers (__enter__ and __exit__) for reliable cleanup.", "EASY"),
             [("Which block in a try-except structure executes when NO exception was raised?", ["A) finally", "B) else", "C) catch", "D) then"], "B) else", "The else block executes only if the try block ran without encountering exceptions.", "MEDIUM"),
              ("What is the advantage of using 'with open(...) as f:' over manual f.close()?", ["A) It reads files faster", "B) It guarantees the file is closed even if an exception occurs inside the block", "C) It encrypts the file", "D) It loads file into GPU memory"], "B) It guarantees the file is closed even if an exception occurs inside the block", "Context managers guarantee deterministic resource teardown.", "EASY"),
              ("What does the condition if __name__ == '__main__': check?", ["A) Checks if the code has syntax errors", "B) Checks whether the script is being executed directly or imported as a module", "C) Verifies admin permissions", "D) Checks if Python version is 3"], "B) Checks whether the script is being executed directly or imported as a module", "__name__ is set to '__main__' only when run as the top-level script.", "MEDIUM"),
              ("How do you intentionally trigger an exception in Python code?", ["A) throw Exception()", "B) raise Exception()", "C) emit Exception()", "D) dispatch Exception()"], "B) raise Exception()", "The raise keyword signals an exception in Python.", "EASY"),
              ("Which file mode opens a file for writing, truncating existing content first?", ["A) 'r'", "B) 'w'", "C) 'a'", "D) 'x'"], "B) 'w'", "'w' opens for writing, clearing existing bytes; 'a' appends.", "EASY")])
        ]
    }
]

def make_generic_subject(code, name, desc, category, diff, order, lesson_titles_and_topics):
    """Generates structured lessons, realistic questions, puzzles, and resources for curriculum."""
    lessons = []
    for idx, (ltitle, ldesc, topics, p_type, p_title, p_q, p_data, p_ans, p_exp, p_diff, q_list) in enumerate(lesson_titles_and_topics):
        lessons.append({
            "order": idx + 1,
            "title": ltitle,
            "short_description": ldesc,
            "topics": topics,
            "puzzle": {
                "type": p_type,
                "title": p_title,
                "question": p_q,
                "puzzle_data": p_data,
                "correct_answer": p_ans,
                "explanation": p_exp,
                "difficulty": p_diff
            },
            "quiz": q_list,
            "resources": [
                (f"{name} Reference Guide - {ltitle}", f"Comprehensive tutorial covering {ltitle} core concepts.", "https://en.wikipedia.org/wiki/" + name.replace(" ", "_"), "DOCUMENTATION", "Academic Press"),
                (f"Interactive Practice: {ltitle}", "Guided practice exercises and concept checks.", "https://www.khanacademy.org/", "TUTORIAL", "Khan Academy")
            ]
        })
    return {
        "code": code,
        "name": name,
        "description": desc,
        "category": category,
        "difficulty": diff,
        "order": order,
        "lessons": lessons
    }

def build_all_subjects():
    all_subjects = []
    # 1. Java
    all_subjects.extend(SUBJECTS_DATA)

    # 2. Python
    py_subj = OTHER_SUBJECTS_DATA[0]
    py_lessons = []
    for idx, (ltitle, ldesc, topics, (p_type, p_title, p_q, p_data, p_ans, p_exp, p_diff), q_list) in enumerate(py_subj["lessons"]):
        py_lessons.append({
            "order": idx + 1,
            "title": ltitle,
            "short_description": ldesc,
            "topics": topics,
            "puzzle": {
                "type": p_type,
                "title": p_title,
                "question": p_q,
                "puzzle_data": p_data,
                "correct_answer": p_ans,
                "explanation": p_exp
            },
            "quiz": q_list,
            "resources": [
                (f"Python Docs: {ltitle}", f"Official Python language documentation for {ltitle}.", "https://docs.python.org/3/", "DOCUMENTATION", "Python Software Foundation"),
                (f"Real Python Guide: {ltitle}", f"In-depth guide exploring {ltitle} with practical examples.", "https://realpython.com/", "ARTICLE", "Real Python")
            ]
        })
    py_subj["lessons"] = py_lessons
    all_subjects.append(py_subj)

    # 3. MATHEMATICS (10 Lessons)
    math_lessons = [
        ("01 — Number Systems", "Integers, rational, irrational, and real numbers, prime factorization, and modular arithmetic.",
         [("Real Numbers", "Classification of rational and irrational numbers.", "EASY"), ("Modular Arithmetic", "Clock arithmetic and congruence relations.", "MEDIUM")],
         "MULTIPLE_CHOICE", "Identify Irrational Number", "Which of the following is an irrational number?", ["1/3", "sqrt(4)", "sqrt(2)", "0.75"], "sqrt(2)", "sqrt(2) cannot be expressed as a ratio of two integers.", "EASY",
         [("Which number is a prime number?", ["A) 9", "B) 15", "C) 17", "D) 21"], "C) 17", "17 has only two positive divisors: 1 and 17.", "EASY"),
          ("What is 14 mod 5 in modular arithmetic?", ["A) 4", "B) 2", "C) 1", "D) 0"], "A) 4", "14 divided by 5 leaves a remainder of 4.", "EASY"),
          ("What constitutes the set of Rational Numbers (Q)?", ["A) Numbers that can be written as p/q where p and q are integers and q != 0", "B) Only positive integers", "C) Infinite non-repeating decimals", "D) Imaginary numbers"], "A) Numbers that can be written as p/q where p and q are integers and q != 0", "Rational numbers are integer quotients.", "EASY"),
          ("What is the greatest common divisor (GCD) of 24 and 36?", ["A) 6", "B) 12", "C) 18", "D) 4"], "B) 12", "12 is the largest integer dividing both 24 and 36.", "EASY"),
          ("Is 0 considered a rational number?", ["A) No, because 0 cannot be divided", "B) Yes, 0 can be written as 0/1", "C) Only in complex numbers", "D) No, it is irrational"], "B) Yes, 0 can be written as 0/1", "0/1 is a valid rational representation.", "EASY")]),
        ("02 — Algebra Basics", "Algebraic expressions, combining like terms, polynomial degrees, and factoring binomials.",
         [("Polynomials & Terms", "Coefficients, degrees, and standard form.", "EASY"), ("Factoring Binomials", "Difference of squares and distributive law.", "MEDIUM")],
         "CODE_OUTPUT", "Polynomial Evaluation", "What is the value of 2*x^2 + 3*x - 5 when x = 2?", "2*(2)^2 + 3*(2) - 5", "9", "2*(4) + 6 - 5 = 8 + 6 - 5 = 9.", "EASY",
         [("What is the expanded form of (x + 3)(x - 3)?", ["A) x^2 - 9", "B) x^2 + 9", "C) x^2 - 6x + 9", "D) x^2 + 6x - 9"], "A) x^2 - 9", "Difference of squares: (a+b)(a-b) = a^2 - b^2.", "EASY"),
          ("What is the degree of the polynomial 4x^3 - 7x^5 + 2x - 1?", ["A) 3", "B) 5", "C) 1", "D) 9"], "B) 5", "The degree is the highest exponent on any term (5).", "EASY"),
          ("Simplify: 3(2x - 4) + 5x.", ["A) 11x - 12", "B) 11x - 4", "C) 6x - 12", "D) x - 12"], "A) 11x - 12", "6x - 12 + 5x = 11x - 12.", "EASY"),
          ("What are the factors of x^2 + 5x + 6?", ["A) (x + 2)(x + 3)", "B) (x + 1)(x + 6)", "C) (x - 2)(x - 3)", "D) (x + 5)(x + 1)"], "A) (x + 2)(x + 3)", "2*3=6 and 2+3=5.", "EASY"),
          ("What is the coefficient of x in the term -8x?", ["A) 8", "B) -8", "C) x", "D) 1"], "B) -8", "The constant multiplier of x is -8.", "EASY")]),
        ("03 — Linear Equations", "Solving single variable equations, slope-intercept form (y = mx + b), and systems of linear equations.",
         [("Slope-Intercept Form", "Slope m, y-intercept b, and graph interpretation.", "EASY"), ("Systems of Equations", "Elimination and substitution methods.", "MEDIUM")],
         "FILL_BLANK", "Slope Calculation", "What is the slope (m) of the line y = 4x - 7? m = ___", "y = 4x - 7", "4", "In y = mx + b form, the coefficient of x is the slope (4).", "EASY",
         [("Solve for x: 3x - 9 = 0.", ["A) x = 2", "B) x = 3", "C) x = -3", "D) x = 9"], "B) x = 3", "3x = 9 => x = 3.", "EASY"),
          ("What does the slope (m) represent on a 2D Cartesian coordinate plane?", ["A) The y-intercept", "B) The rate of change (rise over run)", "C) The area under the line", "D) The angle with y-axis"], "B) The rate of change (rise over run)", "Slope measures vertical change divided by horizontal change.", "EASY"),
          ("What is the slope of a horizontal line?", ["A) 0", "B) 1", "C) Undefined", "D) Infinity"], "A) 0", "Horizontal lines have 0 vertical change (rise = 0).", "EASY"),
          ("What is the intersection point of y = 2x and y = -x + 3?", ["A) (1, 2)", "B) (2, 1)", "C) (0, 0)", "D) (3, 6)"], "A) (1, 2)", "2x = -x + 3 => 3x = 3 => x=1, y=2.", "MEDIUM"),
          ("What form is Ax + By = C called?", ["A) Slope-intercept form", "B) Standard form", "C) Point-slope form", "D) Parametric form"], "B) Standard form", "Ax + By = C is linear standard form.", "EASY")]),
        ("04 — Quadratic Equations", "Standard form ax^2 + bx + c = 0, discriminant (b^2 - 4ac), factoring, and the quadratic formula.",
         [("Discriminant Analysis", "Determining real vs complex root counts.", "MEDIUM"), ("Quadratic Formula", "Derivation and application.", "MEDIUM")],
         "CODE_OUTPUT", "Discriminant Calculation", "What is the discriminant (b^2 - 4ac) for x^2 - 6x + 9 = 0?", "(-6)^2 - 4*1*9", "0", "36 - 36 = 0, indicating exactly one repeated real root.", "MEDIUM",
         [("If the discriminant b^2 - 4ac is negative, how many real roots exist?", ["A) Exactly two real roots", "B) Exactly one real root", "C) Zero real roots (two complex conjugate roots)", "D) Infinite real roots"], "C) Zero real roots (two complex conjugate roots)", "Negative discriminant implies roots involve imaginary i.", "MEDIUM"),
          ("What are the roots of (x - 4)(x + 2) = 0?", ["A) x = 4 and x = -2", "B) x = -4 and x = 2", "C) x = 4 and x = 2", "D) x = 0"], "A) x = 4 and x = -2", "Setting each factor to zero yields 4 and -2.", "EASY"),
          ("What geometric curve represents a quadratic equation y = ax^2 + bx + c?", ["A) Hyperbola", "B) Circle", "C) Parabola", "D) Ellipse"], "C) Parabola", "Quadratic graphs form parabolas.", "EASY"),
          ("What is the x-coordinate of the vertex of y = ax^2 + bx + c?", ["A) -b / (2a)", "B) b / (2a)", "C) -c / a", "D) sqrt(b^2 - 4ac)"], "A) -b / (2a)", "The axis of symmetry lies at -b / (2a).", "MEDIUM"),
          ("Solve x^2 = 49.", ["A) x = 7", "B) x = -7", "C) x = +/- 7", "D) x = 49"], "C) x = +/- 7", "Both positive and negative 7 square to 49.", "EASY")]),
        ("05 — Fractions and Ratios", "Proportions, cross-multiplication, common denominators, unit rates, and percentage relationships.",
         [("Ratios & Proportions", "Direct and inverse proportionality.", "EASY"), ("Fraction Operations", "Addition, subtraction, multiplication, and reciprocal division.", "EASY")],
         "FILL_BLANK", "Cross Multiplication", "Solve the proportion for x: 3 / 4 = x / 20. x = ___", "3/4 = x/20", "15", "4x = 60 => x = 15.", "EASY",
         [("What is 3/4 + 2/3 expressed as a simplified improper fraction?", ["A) 5/7", "B) 17/12", "C) 1", "D) 6/12"], "B) 17/12", "Common denominator 12: 9/12 + 8/12 = 17/12.", "EASY"),
          ("What is 40% expressed as a simplified fraction?", ["A) 4/10", "B) 2/5", "C) 1/4", "D) 3/8"], "B) 2/5", "40/100 simplifies to 2/5.", "EASY"),
          ("If the ratio of boys to girls in a class of 30 students is 2:3, how many girls are there?", ["A) 12", "B) 18", "C) 15", "D) 20"], "B) 18", "3/5 * 30 = 18 girls.", "EASY"),
          ("What is 5/8 divided by 1/4?", ["A) 5/32", "B) 20/8 = 5/2", "C) 1/2", "D) 3/4"], "B) 20/8 = 5/2", "Multiply by reciprocal 4/1: 20/8 = 5/2.", "EASY"),
          ("In a direct variation y = kx, if y = 12 when x = 3, what is k?", ["A) 4", "B) 36", "C) 9", "D) 15"], "A) 4", "12 = k * 3 => k = 4.", "EASY")]),
        ("06 — Geometry", "Angles, triangles, Pythagorean theorem, perimeter, area, volume, and coordinate geometry.",
         [("Triangles & Pythagoras", "Right triangles, a^2 + b^2 = c^2, and angle sums.", "EASY"), ("Area & Volume", "Circle circumference/area, cylinder and prism volume.", "MEDIUM")],
         "CODE_OUTPUT", "Pythagorean Theorem", "In a right triangle with legs a = 3 and b = 4, what is the length of hypotenuse c?", "sqrt(3^2 + 4^2)", "5", "sqrt(9 + 16) = sqrt(25) = 5.", "EASY",
         [("What is the sum of interior angles in any planar triangle?", ["A) 90 degrees", "B) 180 degrees", "C) 360 degrees", "D) 270 degrees"], "B) 180 degrees", "Triangle interior angles always sum to 180 degrees.", "EASY"),
          ("What is the formula for the area of a circle with radius r?", ["A) 2*pi*r", "B) pi*r^2", "C) 4/3*pi*r^3", "D) pi*d"], "B) pi*r^2", "Circle area is pi * r^2.", "EASY"),
          ("What is the perimeter of a rectangle with length 8 and width 5?", ["A) 40", "B) 26", "C) 13", "D) 30"], "B) 26", "2*(8 + 5) = 2*13 = 26.", "EASY"),
          ("What do complementary angles add up to?", ["A) 90 degrees", "B) 180 degrees", "C) 360 degrees", "D) 45 degrees"], "A) 90 degrees", "Complementary angles sum to 90 degrees.", "EASY"),
          ("What is the volume of a rectangular prism with dimensions 2 x 3 x 4?", ["A) 24", "B) 18", "C) 9", "D) 12"], "A) 24", "2 * 3 * 4 = 24 cubic units.", "EASY")]),
        ("07 — Trigonometry", "Sine, cosine, tangent ratios (SOH-CAH-TOA), unit circle, and trigonometric identities.",
         [("Trig Ratios", "Opposite, adjacent, hypotenuse definitions.", "MEDIUM"), ("Unit Circle & Identities", "sin^2(x) + cos^2(x) = 1 and radian conversions.", "HARD")],
         "MATCHING", "Trig Ratios Matching", "Match each trigonometric function with its right-triangle ratio:",
         [["Sine", "Opposite / Hypotenuse"], ["Cosine", "Adjacent / Hypotenuse"], ["Tangent", "Opposite / Adjacent"]],
         {"Sine": "Opposite / Hypotenuse", "Cosine": "Adjacent / Hypotenuse", "Tangent": "Opposite / Adjacent"},
         "SOH-CAH-TOA definitions.", "MEDIUM",
         [("What is sin(90 degrees) or sin(pi/2 radians)?", ["A) 0", "B) 1", "C) -1", "D) 1/2"], "B) 1", "At 90 degrees on the unit circle, y = 1.", "EASY"),
          ("What is the fundamental Pythagorean trigonometric identity?", ["A) sin^2(x) - cos^2(x) = 1", "B) sin^2(x) + cos^2(x) = 1", "C) tan(x) = sin(x)*cos(x)", "D) sin(x) + cos(x) = 1"], "B) sin^2(x) + cos^2(x) = 1", "Derived directly from x^2 + y^2 = 1 on the unit circle.", "MEDIUM"),
          ("How many radians correspond to 180 degrees?", ["A) pi / 2", "B) pi", "C) 2*pi", "D) 3*pi / 2"], "B) pi", "180 degrees equals pi radians.", "EASY"),
          ("What is tan(45 degrees)?", ["A) 0", "B) 1", "C) sqrt(3)", "D) Undefined"], "B) 1", "sin(45)/cos(45) = (sqrt(2)/2)/(sqrt(2)/2) = 1.", "EASY"),
          ("What is the reciprocal function of cosine?", ["A) Cosecant (csc)", "B) Secant (sec)", "C) Cotangent (cot)", "D) Arcsin"], "B) Secant (sec)", "sec(x) = 1 / cos(x).", "MEDIUM")]),
        ("08 — Probability", "Sample space, independent events, mutually exclusive outcomes, combinations, and conditional probability.",
         [("Basic Probability", "P(E) = favorable / total outcomes.", "EASY"), ("Combinatorics & Independence", "Permutations nPr vs Combinations nCr.", "MEDIUM")],
         "CODE_OUTPUT", "Dice Probability", "When rolling a fair 6-sided die, what is the probability of rolling a 3 or a 4? Enter as simplified fraction (e.g. 1/3):", "2/6", "1/3", "2 favorable outcomes out of 6 total = 2/6 = 1/3.", "EASY",
         [("What is the probability of getting heads when flipping a fair coin?", ["A) 0.25", "B) 0.5", "C) 1.0", "D) 0.75"], "B) 0.5", "1 favorable outcome out of 2 total = 1/2 = 0.5.", "EASY"),
          ("What does P(A or B) equal if events A and B are mutually exclusive?", ["A) P(A) * P(B)", "B) P(A) + P(B)", "C) P(A) / P(B)", "D) 1"], "B) P(A) + P(B)", "Disjoint events have no overlap, so probabilities add directly.", "EASY"),
          ("What is the value of 0! (zero factorial)?", ["A) 0", "B) 1", "C) Undefined", "D) -1"], "B) 1", "By mathematical definition and gamma function continuity, 0! = 1.", "EASY"),
          ("What does Bayes' Theorem describe?", ["A) The derivative of a function", "B) How to update the probability of a hypothesis given new evidence", "C) Matrix multiplication", "D) Prime numbers"], "B) How to update the probability of a hypothesis given new evidence", "P(A|B) = P(B|A)*P(A) / P(B).", "MEDIUM"),
          ("If two events A and B are independent, what is P(A and B)?", ["A) P(A) + P(B)", "B) P(A) * P(B)", "C) P(A) - P(B)", "D) 0"], "B) P(A) * P(B)", "Independence allows direct multiplication.", "MEDIUM")]),
        ("09 — Statistics", "Measures of central tendency (mean, median, mode), variance, standard deviation, and normal distribution.",
         [("Central Tendency", "Mean, median, and mode.", "EASY"), ("Dispersion & Variance", "Standard deviation, variance, and z-scores.", "MEDIUM")],
         "CODE_OUTPUT", "Mean Calculation", "What is the arithmetic mean of the dataset: 4, 8, 6, 10, 12?", "(4+8+6+10+12)/5", "8", "40 / 5 = 8.", "EASY",
         [("Which measure of central tendency is least sensitive to extreme outliers?", ["A) Mean", "B) Median", "C) Range", "D) Midrange"], "B) Median", "Median relies on ordinal rank rather than numeric magnitude.", "EASY"),
          ("What percentage of data falls within +/- 1 standard deviation of the mean in a Normal distribution?", ["A) 50%", "B) ~68%", "C) ~95%", "D) ~99.7%"], "B) ~68%", "Empirical Rule: 68-95-99.7.", "MEDIUM"),
          ("What is the standard deviation a measure of?", ["A) The center of the data", "B) The spread or dispersion of data points around the mean", "C) The sample size", "D) Probability of error"], "B) The spread or dispersion of data points around the mean", "Square root of variance measuring dispersion.", "EASY"),
          ("What is the mode of the dataset: 3, 7, 3, 9, 12, 7, 3, 5?", ["A) 3", "B) 7", "C) 9", "D) 5"], "A) 3", "3 appears most frequently (3 times).", "EASY"),
          ("What is the z-score of a value equal to the mean?", ["A) 1", "B) 0", "C) -1", "D) Undefined"], "B) 0", "z = (x - mu) / sigma = 0 when x = mu.", "EASY")]),
        ("10 — Introduction to Calculus", "Limits, derivatives as rates of change, power rule, and fundamental theorem of calculus.",
         [("Limits & Continuity", "Behavior of functions as x approaches values.", "MEDIUM"), ("Derivatives & Power Rule", "d/dx(x^n) = n*x^(n-1).", "HARD")],
         "CODE_OUTPUT", "Derivative Power Rule", "What is the derivative of f(x) = x^3 evaluated at x = 2? (Enter integer)", "3*(2)^2", "12", "f'(x) = 3x^2; at x=2, 3*(4) = 12.", "HARD",
         [("What is the derivative of a constant number c?", ["A) c", "B) 1", "C) 0", "D) x"], "C) 0", "Constants do not change, so rate of change is 0.", "EASY"),
          ("Using the power rule, what is d/dx (x^4)?", ["A) 4x^3", "B) 4x^4", "C) x^3", "D) 3x^4"], "A) 4x^3", "d/dx(x^n) = n*x^(n-1).", "EASY"),
          ("What geometric interpretation does the derivative f'(x) represent at a point?", ["A) Area under the curve", "B) Slope of the tangent line to the curve", "C) Y-intercept", "D) Curvature radius"], "B) Slope of the tangent line to the curve", "The derivative gives the instantaneous tangent slope.", "MEDIUM"),
          ("What is the derivative of sin(x)?", ["A) -cos(x)", "B) cos(x)", "C) tan(x)", "D) -sin(x)"], "B) cos(x)", "d/dx(sin(x)) = cos(x).", "MEDIUM"),
          ("What does the definite integral of a positive function represent geometrically?", ["A) Slope of tangent", "B) Net area between the curve and the x-axis", "C) Circumference", "D) Maximum value"], "B) Net area between the curve and the x-axis", "Definite integration computes cumulative area under the curve.", "MEDIUM")])
    ]
    all_subjects.append(make_generic_subject("MATH", "Mathematics", "Master number systems, algebra, trigonometry, probability, statistics, and foundational calculus.", "MATHEMATICS", "INTERMEDIATE", 3, math_lessons))

    # 4. CHEMISTRY (10 Lessons)
    chem_lessons = [
        ("01 — Introduction to Chemistry", "Matter, elements, compounds, mixtures, and the scientific method.",
         [("Matter & States", "Solids, liquids, gases, and plasma.", "EASY"), ("Elements vs Compounds", "Pure substances vs mixtures.", "EASY")],
         "MULTIPLE_CHOICE", "Identify Chemical Change", "Which of the following represents a chemical change?", ["Melting ice", "Boiling water", "Iron rusting", "Tearing paper"], "Iron rusting", "Rusting forms iron oxide through a chemical reaction with oxygen.", "EASY",
         [("What is the smallest unit of an element that retains its chemical properties?", ["A) Molecule", "B) Atom", "C) Cell", "D) Compound"], "B) Atom", "The atom is the fundamental chemical unit.", "EASY"),
          ("Which of the following is a homogeneous mixture?", ["A) Salt water solution", "B) Sand and iron filings", "C) Oil and vinegar", "D) Granite"], "A) Salt water solution", "A solution is uniform throughout.", "EASY"),
          ("What state of matter has a definite volume but takes the shape of its container?", ["A) Solid", "B) Liquid", "C) Gas", "D) Plasma"], "B) Liquid", "Liquids maintain constant volume while conforming to container shapes.", "EASY"),
          ("What law states that mass is neither created nor destroyed in a chemical reaction?", ["A) Law of Definite Proportions", "B) Law of Conservation of Mass", "C) Dalton's Law", "D) Avogadro's Law"], "B) Law of Conservation of Mass", "Lavoisier's Law of Conservation of Mass.", "EASY"),
          ("What is the chemical formula for water?", ["A) CO2", "B) H2O", "C) NaCl", "D) O2"], "B) H2O", "Two hydrogen atoms bonded to one oxygen atom.", "EASY")]),
        ("02 — Atomic Structure", "Protons, neutrons, electrons, isotopes, atomic number, and Bohr models.",
         [("Subatomic Particles", "Charges, masses, and nuclear locations.", "EASY"), ("Isotopes & Mass Number", "Nuclide notation and atomic mass.", "MEDIUM")],
         "CODE_OUTPUT", "Neutron Count", "How many neutrons are in a Carbon-14 atom (atomic number 6)?", "14 - 6", "8", "Neutrons = Mass Number (14) - Atomic Number (6) = 8.", "EASY",
         [("Which subatomic particle carries a negative electrical charge?", ["A) Proton", "B) Neutron", "C) Electron", "D) Positron"], "C) Electron", "Electrons are negatively charged.", "EASY"),
          ("What subatomic particles reside within the atomic nucleus?", ["A) Protons and electrons", "B) Protons and neutrons", "C) Neutrons and electrons", "D) Electrons only"], "B) Protons and neutrons", "The dense nucleus holds nucleons (protons and neutrons).", "EASY"),
          ("What defines the atomic number (Z) of an element?", ["A) Number of neutrons", "B) Number of protons", "C) Total mass", "D) Valence electrons"], "B) Number of protons", "Atomic number equals the proton count.", "EASY"),
          ("What are isotopes?", ["A) Atoms of different elements with same mass", "B) Atoms of the same element with different numbers of neutrons", "C) Ions with positive charge", "D) Molecules with double bonds"], "B) Atoms of the same element with different numbers of neutrons", "Isotopes share atomic number but differ in neutron count.", "EASY"),
          ("What is the maximum number of electrons that can occupy the first electron shell (n=1)?", ["A) 2", "B) 8", "C) 18", "D) 32"], "A) 2", "2n^2 for n=1 equals 2.", "EASY")]),
        ("03 — Periodic Table", "Periodic law, groups, periods, alkali metals, halogens, noble gases, and periodic trends.",
         [("Groups & Periods", "Families and valence electron configurations.", "EASY"), ("Periodic Trends", "Electronegativity, ionization energy, and atomic radius.", "HARD")],
         "MATCHING", "Periodic Families Matching", "Match each element family with its group column:",
         [["Alkali Metals", "Group 1"], ["Alkaline Earth", "Group 2"], ["Halogens", "Group 17"], ["Noble Gases", "Group 18"]],
         {"Alkali Metals": "Group 1", "Alkaline Earth": "Group 2", "Halogens": "Group 17", "Noble Gases": "Group 18"},
         "Periodic group assignments.", "MEDIUM",
         [("Which element family is chemically inert due to full valence shells?", ["A) Alkali metals", "B) Halogens", "C) Noble gases", "D) Transition metals"], "C) Noble gases", "Group 18 noble gases possess full stable octets.", "EASY"),
          ("How does electronegativity generally trend across a period from left to right?", ["A) Decreases", "B) Increases", "C) Remains constant", "D) Random"], "B) Increases", "Nuclear pull increases across a period, drawing bonding electrons closer.", "MEDIUM"),
          ("Which element has the highest electronegativity on the Pauling scale?", ["A) Oxygen", "B) Chlorine", "C) Fluorine", "D) Francium"], "C) Fluorine", "Fluorine has the highest electronegativity (3.98).", "EASY"),
          ("Elements in the same vertical column (group) share similar chemical properties because they have:", ["A) Same atomic mass", "B) Same number of valence electrons", "C) Same number of neutrons", "D) Same density"], "B) Same number of valence electrons", "Valence electron configuration dictates chemical bonding behavior.", "MEDIUM"),
          ("Where are nonmetals located on the periodic table?", ["A) Upper right corner", "B) Far left", "C) Bottom two rows", "D) Center d-block"], "A) Upper right corner", "Nonmetals occupy the upper right, plus hydrogen.", "EASY")]),
        ("04 — Chemical Bonding", "Ionic, covalent, metallic bonding, Lewis dot structures, and polarity.",
         [("Ionic Bonding", "Electron transfer between metals and nonmetals.", "MEDIUM"), ("Covalent Bonding", "Shared electron pairs and molecular polarity.", "MEDIUM")],
         "TRUE_FALSE", "Ionic Bonding", "Ionic bonds form when electrons are shared equally between two nonmetal atoms.", "Ionic bonds share electrons equally", False, "Ionic bonds involve electron transfer between atoms of high electronegativity difference.", "EASY",
         [("What type of bond forms between Sodium (Na) and Chlorine (Cl)?", ["A) Nonpolar covalent", "B) Polar covalent", "C) Ionic", "D) Metallic"], "C) Ionic", "Electron transfers from electropositive Na to electronegative Cl.", "EASY"),
          ("What constitutes a single covalent bond?", ["A) Transfer of 1 electron", "B) One pair (2 electrons) shared between two atoms", "C) Free floating sea of electrons", "D) Attraction of opposite dipoles"], "B) One pair (2 electrons) shared between two atoms", "A covalent bond shares a pair of valence electrons.", "EASY"),
          ("What is the octet rule in chemical bonding?", ["A) Atoms tend to gain, lose, or share electrons to achieve 8 valence electrons", "B) All atoms have 8 protons", "C) Only 8 elements can bond", "D) Bonds must have 8 Angstroms length"], "A) Atoms tend to gain, lose, or share electrons to achieve 8 valence electrons", "The octet rule reflects noble gas electron configuration stability.", "EASY"),
          ("Which model explains electrical conductivity and malleability in metals?", ["A) Covalent network", "B) Electron sea model", "C) Hydrogen bonding", "D) London dispersion"], "B) Electron sea model", "Delocalized conduction electrons move freely through metallic lattice.", "MEDIUM"),
          ("Is water (H2O) a polar or nonpolar molecule?", ["A) Nonpolar", "B) Polar (bent geometry with net dipole)", "C) Ionic", "D) Metallic"], "B) Polar (bent geometry with net dipole)", "Bent molecular geometry and electronegative oxygen yield a net dipole.", "MEDIUM")]),
        ("05 — States of Matter", "Kinetic molecular theory, phase changes, gas laws (PV = nRT), and phase diagrams.",
         [("Phase Transitions", "Melting, boiling, sublimation, and deposition.", "EASY"), ("Ideal Gas Law", "Pressure, volume, temperature, and moles relations.", "MEDIUM")],
         "FILL_BLANK", "Ideal Gas Law", "In the ideal gas law PV = nRT, what variable represents pressure? ___", "PV = nRT", "P", "P represents pressure in the ideal gas equation.", "EASY",
         [("What is the phase change from gas directly to solid called?", ["A) Sublimation", "B) Deposition", "C) Condensation", "D) Evaporation"], "B) Deposition", "Deposition bypasses the liquid state (e.g. frost).", "MEDIUM"),
          ("What happens to the volume of an ideal gas if temperature increases at constant pressure (Charles's Law)?", ["A) Volume decreases", "B) Volume increases", "C) Volume remains identical", "D) Gas liquefies immediately"], "B) Volume increases", "V1/T1 = V2/T2 indicates direct proportionality.", "EASY"),
          ("What is absolute zero in degrees Celsius?", ["A) 0 C", "B) -100 C", "C) -273.15 C", "D) -459 C"], "C) -273.15 C", "0 Kelvin corresponds to -273.15 Celsius.", "EASY"),
          ("Which phase transition absorbs thermal energy (endothermic)?", ["A) Freezing", "B) Condensation", "C) Vaporization (boiling)", "D) Deposition"], "C) Vaporization (boiling)", "Boiling requires thermal energy input to overcome intermolecular attractions.", "EASY"),
          ("What does the triple point on a phase diagram represent?", ["A) Temperature where substance explodes", "B) Temperature and pressure where solid, liquid, and gas coexist in equilibrium", "C) Boiling point at 1 atm", "D) Absolute zero"], "B) Temperature and pressure where solid, liquid, and gas coexist in equilibrium", "All three phases achieve dynamic equilibrium at the triple point.", "MEDIUM")]),
        ("06 — Chemical Reactions", "Balancing chemical equations, types of reactions (synthesis, decomposition, replacement), and stoichiometry.",
         [("Balancing Equations", "Conserving atom counts across reactants and products.", "MEDIUM"), ("Reaction Types", "Combustion, redox, single and double displacement.", "EASY")],
         "CODE_OUTPUT", "Balancing Reaction", "What is the stoichiometric coefficient in front of O2 when balancing: 2 H2 + ? O2 -> 2 H2O?", "2 H2 + ? O2 -> 2 H2O", "1", "2 H2 (4 H) + 1 O2 (2 O) produces 2 H2O (4 H, 2 O).", "EASY",
         [("What type of reaction is: 2 H2O2 -> 2 H2O + O2?", ["A) Synthesis", "B) Decomposition", "C) Single displacement", "D) Neutralization"], "B) Decomposition", "A single reactant breaks down into multiple simpler products.", "EASY"),
          ("What is the quantity represented by 1 mole in chemistry (Avogadro's number)?", ["A) 6.022 x 10^23 particles", "B) 3.14 x 10^8 particles", "C) 1.602 x 10^-19 particles", "D) 9.8 x 10^3 particles"], "A) 6.022 x 10^23 particles", "Avogadro's constant defines the number of particles in 1 mole.", "EASY"),
          ("What is the molar mass of Carbon dioxide (CO2)? (C=12, O=16)", ["A) 28 g/mol", "B) 44 g/mol", "C) 32 g/mol", "D) 16 g/mol"], "B) 44 g/mol", "12 + 2*(16) = 44 g/mol.", "EASY"),
          ("In a redox reaction, what does oxidation refer to?", ["A) Gain of electrons", "B) Loss of electrons", "C) Gain of protons", "D) Loss of neutrons"], "B) Loss of electrons", "OIL RIG: Oxidation Is Loss, Reduction Is Gain.", "MEDIUM"),
          ("What is the limiting reactant in a chemical process?", ["A) The reactant with highest molar mass", "B) The reactant that is completely consumed first, capping product yield", "C) The catalyst", "D) The product formed"], "B) The reactant that is completely consumed first, capping product yield", "The limiting reagent dictates theoretical yield.", "MEDIUM")]),
        ("07 — Acids, Bases and Salts", "pH scale, Arrhenius and Bronsted-Lowry definitions, neutralization, and titration.",
         [("pH Scale", "Logarithmic scale from 0 to 14, hydronium ion concentration.", "EASY"), ("Acid-Base Theories", "Proton donors vs proton acceptors.", "MEDIUM")],
         "CODE_OUTPUT", "pH Calculation", "What is the pH of a neutral aqueous solution at 25 degrees C?", "pH of pure water", "7", "Neutral pH at 25 C is 7.0.", "EASY",
         [("What does a pH value less than 7 indicate?", ["A) Acidic solution", "B) Basic (alkaline) solution", "C) Neutral solution", "D) Saturated salt"], "A) Acidic solution", "pH < 7 indicates high [H+] concentration.", "EASY"),
          ("According to Bronsted-Lowry theory, what is an acid?", ["A) Proton (H+) donor", "B) Proton (H+) acceptor", "C) Electron pair donor", "D) Salt producer"], "A) Proton (H+) donor", "Bronsted-Lowry acids donate protons.", "MEDIUM"),
          ("What are the products of an acid-base neutralization reaction?", ["A) Acid and base", "B) Salt and water", "C) Gas and precipitate", "D) Metal and nonmetal"], "B) Salt and water", "HCl + NaOH -> NaCl + H2O.", "EASY"),
          ("If the pH of a solution is 3, what is its hydronium ion concentration [H+]?", ["A) 10^-3 M", "B) 3 M", "C) 10^3 M", "D) 0.003 M"], "A) 10^-3 M", "pH = -log10[H+], so [H+] = 10^-pH = 10^-3 M.", "MEDIUM"),
          ("What color does litmus paper turn when exposed to a basic solution?", ["A) Red", "B) Blue", "C) Yellow", "D) Green"], "B) Blue", "Bases turn red litmus paper blue.", "EASY")]),
        ("08 — Thermodynamics", "Enthalpy, exothermic vs endothermic reactions, entropy, and Gibbs free energy.",
         [("Enthalpy & Heat", "Delta H negative (exothermic) vs positive (endothermic).", "MEDIUM"), ("Gibbs Free Energy", "Delta G = Delta H - T*Delta S and spontaneity.", "HARD")],
         "TRUE_FALSE", "Exothermic Reaction Sign", "True or False: An exothermic chemical reaction releases heat to the surroundings and has a negative Delta H.", "Exothermic has negative Delta H", True, "Exothermic processes release heat, resulting in Delta H < 0.", "EASY",
         [("What does the Second Law of Thermodynamics state?", ["A) Energy cannot be created or destroyed", "B) Total entropy of an isolated system always increases over time", "C) Absolute zero cannot be reached", "D) Pressure equals force over area"], "B) Total entropy of an isolated system always increases over time", "Entropy (disorder) spontaneously increases in isolated systems.", "HARD"),
          ("When Delta G (Gibbs Free Energy) is negative, the reaction is:", ["A) Non-spontaneous", "B) Spontaneous in the forward direction", "C) At dynamic equilibrium", "D) Frozen"], "B) Spontaneous in the forward direction", "Negative Delta G denotes thermodynamically favorable spontaneous processes.", "HARD"),
          ("What is an endothermic process?", ["A) Releases heat", "B) Absorbs heat from its surroundings", "C) Has zero entropy change", "D) Explodes"], "B) Absorbs heat from its surroundings", "Endothermic absorbs thermal energy (Delta H > 0).", "EASY"),
          ("What is the SI unit of heat and energy?", ["A) Watt", "B) Joule", "C) Pascal", "D) Kelvin"], "B) Joule", "The Joule (J) is the standard SI energy unit.", "EASY"),
          ("What does a catalyst do to the activation energy of a chemical reaction?", ["A) Increases activation energy", "B) Lowers activation energy, increasing reaction rate", "C) Changes equilibrium constant", "D) Consumes reactants"], "B) Lowers activation energy, increasing reaction rate", "Catalysts provide alternative low-energy pathways.", "MEDIUM")]),
        ("09 — Organic Chemistry Basics", "Carbon versatility, hydrocarbons (alkanes, alkenes, alkynes), and functional groups.",
         [("Hydrocarbons", "Alkanes (single), alkenes (double), alkynes (triple bonds).", "EASY"), ("Functional Groups", "Alcohols, carboxylic acids, aldehydes, and amines.", "MEDIUM")],
         "MATCHING", "Hydrocarbon Suffixes Matching", "Match each hydrocarbon type with its carbon-carbon bond character:",
         [["Alkane", "Single bonds (-ane)"], ["Alkene", "Double bond (-ene)"], ["Alkyne", "Triple bond (-yne)"]],
         {"Alkane": "Single bonds (-ane)", "Alkene": "Double bond (-ene)", "Alkyne": "Triple bond (-yne)"},
         "Hydrocarbon bond classifications.", "EASY",
         [("How many covalent bonds does a neutral carbon atom typically form?", ["A) 2", "B) 3", "C) 4", "D) 6"], "C) 4", "Carbon is tetravalent, forming four covalent bonds.", "EASY"),
          ("What is the general molecular formula for non-cyclic alkanes?", ["A) CnH2n", "B) CnH2n+2", "C) CnH2n-2", "D) CnHn"], "B) CnH2n+2", "Alkanes follow CnH2n+2 (e.g. Methane CH4, Ethane C2H6).", "MEDIUM"),
          ("Which functional group characterizes alcohols?", ["A) -COOH", "B) -OH (hydroxyl group)", "C) -NH2", "D) -CHO"], "B) -OH (hydroxyl group)", "Hydroxyl -OH defines alcohols.", "EASY"),
          ("What functional group is present in carboxylic acids such as acetic acid?", ["A) -OH", "B) -COOH (carboxyl)", "C) -C=O", "D) -NH2"], "B) -COOH (carboxyl)", "-COOH defines organic carboxylic acids.", "MEDIUM"),
          ("What are structural isomers in organic chemistry?", ["A) Molecules with different formulas but same shape", "B) Molecules with the same molecular formula but different bonding connectivity", "C) Isotopes of carbon", "D) Charged ions"], "B) Molecules with the same molecular formula but different bonding connectivity", "Isomers share formulas but differ structurally.", "MEDIUM")]),
        ("10 — Electrochemistry", "Galvanic and electrolytic cells, oxidation states, cathode/anode definitions, and batteries.",
         [("Electrochemical Cells", "Anode (oxidation) and cathode (reduction).", "MEDIUM"), ("Standard Reduction Potentials", "Nernst equation and electromotive force (EMF).", "HARD")],
         "FILL_BLANK", "Anode Reaction Mnemonic", "Fill in the mnemonic: Anode is where ______ occurs (An Ox, Red Cat):", "Anode is where ______ occurs", "oxidation", "Oxidation occurs at the anode; reduction at the cathode.", "EASY",
         [("At which electrode does reduction occur in an electrochemical cell?", ["A) Anode", "B) Cathode", "C) Salt bridge", "D) External wire"], "B) Cathode", "Red Cat: Reduction occurs at the Cathode.", "EASY"),
          ("What is the role of the salt bridge in a galvanic cell?", ["A) Conducts electrons directly", "B) Maintains electrical neutrality by allowing ion flow between half-cells", "C) Acts as catalyst", "D) Cools the battery"], "B) Maintains electrical neutrality by allowing ion flow between half-cells", "Salt bridges balance accumulating charges.", "MEDIUM"),
          ("In a standard battery, which direction do electrons flow in the external circuit?", ["A) Cathode to anode", "B) Anode to cathode", "C) Both directions simultaneously", "D) Through the electrolyte only"], "B) Anode to cathode", "Electrons leave the oxidation site (anode) toward reduction (cathode).", "MEDIUM"),
          ("What is the oxidation number of oxygen in most chemical compounds (such as H2O)?", ["A) +2", "B) 0", "C) -2", "D) -1"], "C) -2", "Oxygen typically carries a -2 oxidation state.", "EASY"),
          ("What characterizes an electrolytic cell as opposed to a galvanic cell?", ["A) Spontaneous and generates voltage", "B) Requires an external electrical power source to drive a non-spontaneous reaction", "C) Operates without electrodes", "D) Only works in gas phase"], "B) Requires an external electrical power source to drive a non-spontaneous reaction", "Electrolysis forces non-spontaneous chemical transformations.", "HARD")])
    ]
    all_subjects.append(make_generic_subject("CHEM", "Chemistry", "Explore atomic structure, the periodic table, chemical bonding, reactions, thermodynamics, and organic principles.", "SCIENCE", "BEGINNER", 4, chem_lessons))

    # 5. ARTIFICIAL INTELLIGENCE (10 Lessons)
    ai_lessons = [
        ("01 — Introduction to Artificial Intelligence", "Turing test, history, symbolic AI vs connectionism, and modern AI paradigms.",
         [("AI Foundations", "Definition, Dartmouth 1956 workshop, and agent goals.", "EASY"), ("Turing Test", "Imitation game and benchmarks of machine intelligence.", "EASY")],
         "MULTIPLE_CHOICE", "Turing Test Definition", "What was Alan Turing's proposed test for machine intelligence originally named?", ["The Chinese Room", "The Imitation Game", "The Von Neumann Test", "The Hebbian Benchmark"], "The Imitation Game", "Alan Turing introduced the Imitation Game in his 1950 paper.", "EASY",
         [("What is the primary objective of Artificial Intelligence as a discipline?", ["A) Building faster computer hardware", "B) Designing computational systems that perceive, reason, and act rationally", "C) Creating websites", "D) Storing large databases"], "B) Designing computational systems that perceive, reason, and act rationally", "AI focuses on rational agency and intelligent problem-solving.", "EASY"),
          ("What was the outcome of the 1956 Dartmouth Workshop?", ["A) Invention of the first computer", "B) Coining of the term 'Artificial Intelligence' and launch of AI as an academic discipline", "C) Discovery of deep learning", "D) Passing the Turing Test"], "B) Coining of the term 'Artificial Intelligence' and launch of AI as an academic discipline", "John McCarthy and colleagues coined AI at Dartmouth.", "MEDIUM"),
          ("What distinguishes Narrow (Weak) AI from General AI (AGI)?", ["A) Narrow AI performs dedicated specific tasks; AGI exhibits general human-like reasoning across arbitrary domains", "B) Narrow AI has no code", "C) AGI only runs on supercomputers", "D) Narrow AI is only theoretical"], "A) Narrow AI performs dedicated specific tasks; AGI exhibits general human-like reasoning across arbitrary domains", "Modern systems are narrow AI.", "EASY"),
          ("Which philosophical thought experiment argued against machine understanding purely through symbol manipulation?", ["A) Trolley Problem", "B) Searle's Chinese Room", "C) Ship of Theseus", "D) Prisoner's Dilemma"], "B) Searle's Chinese Room", "John Searle argued syntax alone does not yield semantics.", "MEDIUM"),
          ("What is connectionist AI primarily based upon?", ["A) Formal logic and production rules", "B) Artificial Neural Networks inspired by biological brains", "C) Relational SQL databases", "D) Genetic algorithms exclusively"], "B) Artificial Neural Networks inspired by biological brains", "Connectionism models learning through interconnected nodes.", "EASY")]),
        ("02 — Intelligent Agents", "PEAS framework (Performance, Environment, Actuators, Sensors) and agent architecture types.",
         [("PEAS Formalism", "Defining agent environments precisely.", "MEDIUM"), ("Agent Architectures", "Simple reflex, model-based, goal-based, and utility-based agents.", "MEDIUM")],
         "MATCHING", "PEAS Components Matching", "Match each PEAS component for an autonomous taxi with its implementation:",
         [["Performance", "Safe, fast, legal trip"], ["Environment", "Roads, traffic, pedestrians"], ["Actuators", "Steering, accelerator, brakes"], ["Sensors", "Cameras, LiDAR, GPS"]],
         {"Performance": "Safe, fast, legal trip", "Environment": "Roads, traffic, pedestrians", "Actuators": "Steering, accelerator, brakes", "Sensors": "Cameras, LiDAR, GPS"},
         "PEAS framework specification.", "MEDIUM",
         [("What does the PEAS acronym stand for in rational agent design?", ["A) Program, Execution, Action, System", "B) Performance measure, Environment, Actuators, Sensors", "C) Perception, Error, Accuracy, Speed", "D) Processing, Entity, Attribute, State"], "B) Performance measure, Environment, Actuators, Sensors", "Standard Russell & Norvig agent characterization.", "EASY"),
          ("Which agent type maintains an internal state model to track unobserved aspects of the current world?", ["A) Simple reflex agent", "B) Model-based reflex agent", "C) Table-driven agent", "D) Random agent"], "B) Model-based reflex agent", "Model-based agents track partial observability.", "MEDIUM"),
          ("What is a deterministic environment?", ["A) The next state is completely determined by current state and agent action", "B) The state changes randomly", "C) Multiple agents compete", "D) Sensors are noisy"], "A) The next state is completely determined by current state and agent action", "No randomness or uncertainty exists.", "EASY"),
          ("What defines an agent's actuators?", ["A) How it perceives the world", "B) Mechanisms through which the agent acts upon its environment", "C) Memory hardware", "D) Scoring function"], "B) Mechanisms through which the agent acts upon its environment", "Actuators apply changes to the environment.", "EASY"),
          ("What does a utility-based agent maximize?", ["A) Only binary goal achievement", "B) A continuous utility function reflecting preferences and degree of happiness", "C) Line count in code", "D) Number of sensor reads"], "B) A continuous utility function reflecting preferences and degree of happiness", "Utility models preferences over conflicting goals.", "MEDIUM")]),
        ("03 — Problem Solving", "Formulating state spaces, transitions, initial states, goal tests, and path costs.",
         [("State Space Formulation", "States, actions, and transition models.", "MEDIUM"), ("Path Cost & Optimality", "Additive step costs and optimal solution definitions.", "EASY")],
         "CODE_OUTPUT", "State Space Counting", "In a 3x3 sliding tile 8-puzzle, how many total tiles are moved on the board?", "8 numbered tiles + 1 blank", "8", "There are 8 numbered movable tiles and 1 blank space.", "EASY",
         [("What are the 5 components of a formal problem formulation in AI search?", ["A) CPU, RAM, Disk, Network, GPU", "B) Initial state, Actions, Transition model, Goal test, Path cost", "C) Input, Output, Loop, Condition, Exit", "D) Data, Model, Loss, Optimizer, Epochs"], "B) Initial state, Actions, Transition model, Goal test, Path cost", "Standard state space formulation.", "MEDIUM"),
          ("What does the branching factor (b) in a search tree denote?", ["A) The maximum depth of the tree", "B) The maximum number of successors any node can expand", "C) The cost of the goal state", "D) The number of goals"], "B) The maximum number of successors any node can expand", "Branching factor measures tree expansion breadth.", "EASY"),
          ("What is the state space of a problem?", ["A) Only the solution path", "B) The set of all possible states reachable from the initial state by any sequence of actions", "C) Computer RAM allocated", "D) The goal state alone"], "B) The set of all possible states reachable from the initial state by any sequence of actions", "State space encompasses all reachable configurations.", "MEDIUM"),
          ("When is a search algorithm considered complete?", ["A) If it executes in O(1) time", "B) If it is guaranteed to find a solution if one exists", "C) If it never uses memory", "D) If it checks every state twice"], "B) If it is guaranteed to find a solution if one exists", "Completeness guarantees finding existing solutions.", "EASY"),
          ("What is path cost in search graph traversal?", ["A) The number of nodes visited", "B) A function that assigns a numeric cost to a path, typically sum of step costs", "C) Network latency", "D) Memory overhead"], "B) A function that assigns a numeric cost to a path, typically sum of step costs", "Path cost evaluates candidate trajectories.", "EASY")]),
        ("04 — Uninformed Search", "Breadth-First Search (BFS), Depth-First Search (DFS), Depth-Limited, and Uniform-Cost Search (UCS).",
         [("BFS vs DFS", "Queue (FIFO) vs Stack (LIFO) traversal properties.", "MEDIUM"), ("Uniform-Cost Search", "Dijkstra-based expansion by lowest path cost g(n).", "HARD")],
         "MATCHING", "Search Frontier Data Structures", "Match each uninformed search algorithm with its frontier queue type:",
         [["BFS", "FIFO Queue"], ["DFS", "LIFO Stack"], ["Uniform-Cost Search", "Priority Queue ordered by path cost g(n)"]],
         {"BFS": "FIFO Queue", "DFS": "LIFO Stack", "Uniform-Cost Search": "Priority Queue ordered by path cost g(n)"},
         "Frontier queue implementations.", "MEDIUM",
         [("Which search algorithm is guaranteed to find the shallowest goal in an unweighted tree?", ["A) Depth-First Search (DFS)", "B) Breadth-First Search (BFS)", "C) Depth-Limited Search", "D) Random Walk"], "B) Breadth-First Search (BFS)", "BFS explores level by level.", "EASY"),
          ("What is the primary drawback of Breadth-First Search in large state spaces?", ["A) Not complete", "B) Exponential memory consumption storing the frontier", "C) Finds suboptimal paths in unweighted graphs", "D) Cannot handle loops"], "B) Exponential memory consumption storing the frontier", "BFS requires O(b^d) memory.", "MEDIUM"),
          ("What data structure does Depth-First Search (DFS) utilize for its frontier?", ["A) FIFO Queue", "B) LIFO Stack", "C) Min-Heap", "D) Hash Map"], "B) LIFO Stack", "DFS explores deeply via a stack or recursion.", "EASY"),
          ("Uniform Cost Search (UCS) expands nodes ordered by what metric?", ["A) Path cost g(n) from start node", "B) Heuristic estimate h(n)", "C) Node depth", "D) Random selection"], "A) Path cost g(n) from start node", "UCS expands the lowest cumulative cost node first.", "MEDIUM"),
          ("Is Depth-First Search complete in infinite-depth state spaces without cycle checking?", ["A) Yes, always", "B) No, it can follow an infinite branch forever", "C) Only if branching factor is 1", "D) Yes, if tree is binary"], "B) No, it can follow an infinite branch forever", "DFS can get trapped in infinite depth paths.", "MEDIUM")]),
        ("05 — Informed Search", "Heuristics, Greedy Best-First Search, A* search, admissibility, and consistency.",
         [("Heuristic Functions", "Estimating cost-to-goal h(n) using domain knowledge.", "MEDIUM"), ("A* Search", "Evaluation function f(n) = g(n) + h(n) and optimal admissibility.", "HARD")],
         "FILL_BLANK", "A Star Evaluation Function", "Fill in the missing term in the A* evaluation formula: f(n) = g(n) + ___", "f(n) = g(n) + ___", "h(n)", "A* evaluates nodes using f(n) = g(n) (cost so far) + h(n) (estimated cost to goal).", "EASY",
         [("What condition makes a heuristic function h(n) admissible in tree search?", ["A) h(n) never overestimates the true cost to reach the goal", "B) h(n) is always greater than true cost", "C) h(n) = 0 everywhere", "D) h(n) is negative"], "A) h(n) never overestimates the true cost to reach the goal", "Admissibility requires h(n) <= h*(n).", "HARD"),
          ("What evaluation function f(n) does A* search minimize?", ["A) f(n) = g(n)", "B) f(n) = h(n)", "C) f(n) = g(n) + h(n)", "D) f(n) = g(n) * h(n)"], "C) f(n) = g(n) + h(n)", "g(n) is known cost to reach n; h(n) is estimated cost to goal.", "MEDIUM"),
          ("What happens to A* search if the heuristic function h(n) is identically 0 everywhere?", ["A) It crashes", "B) It degrades into Uniform Cost Search (Dijkstra's algorithm)", "C) It turns into DFS", "D) It finds no solution"], "B) It degrades into Uniform Cost Search (Dijkstra's algorithm)", "When h(n)=0, f(n) = g(n), which is UCS.", "MEDIUM"),
          ("Which algorithm expands nodes purely on the basis of lowest heuristic h(n) alone?", ["A) A* Search", "B) Greedy Best-First Search", "C) Breadth-First Search", "D) Iterative Deepening"], "B) Greedy Best-First Search", "Greedy search evaluates solely by h(n).", "MEDIUM"),
          ("In graph search, what stronger condition than admissibility guarantees A* optimality without re-opening closed nodes?", ["A) Convexity", "B) Consistency (monotonicity)", "C) Linearity", "D) Normalization"], "B) Consistency (monotonicity)", "Consistency ensures f(n) is non-decreasing along paths.", "HARD")]),
        ("06 — Knowledge Representation", "Propositional logic, first-order logic, ontologies, and semantic networks.",
         [("Propositional & First-Order Logic", "Syntax, semantics, quantifiers (universal, existential).", "HARD"), ("Ontologies & Knowledge Graphs", "Entities, relationships, and inference engines.", "MEDIUM")],
         "TRUE_FALSE", "Universal Quantifier", "In First-Order Logic, the universal quantifier symbol is upside-down A, meaning 'for all'.", "Universal quantifier is upside down A", True, "The universal quantifier denotes universal applicability across a domain.", "EASY",
         [("What is the difference between Propositional Logic and First-Order Logic (FOL)?", ["A) Propositional logic includes quantifiers and relations; FOL does not", "B) FOL represents objects, properties, relations, and quantifiers; Propositional logic only deals with atomic boolean facts", "C) Propositional logic is undecidable", "D) FOL cannot represent negation"], "B) FOL represents objects, properties, relations, and quantifiers; Propositional logic only deals with atomic boolean facts", "FOL introduces predicates, objects, and quantifiers.", "HARD"),
          ("What inference rule derives Q from 'P' and 'P -> Q'?", ["A) Resolution", "B) Modus Ponens", "C) Modus Tollens", "D) Universal Instantiation"], "B) Modus Ponens", "Modus Ponens is the fundamental implication elimination rule.", "MEDIUM"),
          ("What does the existential quantifier signify in First-Order Logic?", ["A) For all elements in the domain", "B) There exists at least one element in the domain", "C) No elements exist", "D) Exactly two elements exist"], "B) There exists at least one element in the domain", "Existential quantification asserts existence.", "EASY"),
          ("What is an ontology in Artificial Intelligence?", ["A) A neural network architecture", "B) A formal naming and definition of categories, properties, and relations between concepts in a domain", "C) A sorting algorithm", "D) A loss function"], "B) A formal naming and definition of categories, properties, and relations between concepts in a domain", "Ontologies formalize domain knowledge.", "MEDIUM"),
          ("What is the output of resolving (A or B) with (not A or C) using the Resolution principle?", ["A) B or C", "B) A or not A", "C) B and C", "D) Empty clause"], "A) B or C", "Resolution cancels complementary literals A and not A, leaving (B or C).", "HARD")]),
        ("07 — Machine Learning Basics", "Supervised, unsupervised, reinforcement learning, training/validation sets, and overfitting.",
         [("Learning Paradigms", "Supervised labels, unsupervised patterns, and RL rewards.", "EASY"), ("Generalization & Overfitting", "Bias-variance tradeoff and cross-validation.", "MEDIUM")],
         "MATCHING", "ML Paradigms Matching", "Match each machine learning paradigm with its training feedback:",
         [["Supervised Learning", "Labeled training examples (features + targets)"], ["Unsupervised Learning", "Unlabeled data exploring intrinsic structure"], ["Reinforcement Learning", "Trial-and-error reward and penalty signals"]],
         {"Supervised Learning": "Labeled training examples (features + targets)", "Unsupervised Learning": "Unlabeled data exploring intrinsic structure", "Reinforcement Learning": "Trial-and-error reward and penalty signals"},
         "Core ML paradigms.", "EASY",
         [("Which learning paradigm trains on labeled pairs (features, target labels)?", ["A) Unsupervised Learning", "B) Supervised Learning", "C) Self-supervised only", "D) Reinforcement Learning"], "B) Supervised Learning", "Supervised learning maps inputs to ground-truth labels.", "EASY"),
          ("What symptom characterizes an overfitted machine learning model?", ["A) High training error and high test error", "B) Low training error but poor generalization / high test error", "C) Fast inference speed", "D) Linear decision boundary"], "B) Low training error but poor generalization / high test error", "Overfitting memorizes noise in training data.", "MEDIUM"),
          ("What is the purpose of holding out a validation / test dataset?", ["A) To train the model twice", "B) To evaluate generalization performance on unseen data", "C) To speed up gradient descent", "D) To increase sample count"], "B) To evaluate generalization performance on unseen data", "Testing evaluates out-of-sample generalization.", "EASY"),
          ("Which problem is an example of regression rather than classification?", ["A) Predicting house sale prices in dollars", "B) Identifying spam vs not spam emails", "C) Classifying handwritten digits 0-9", "D) Detecting fraudulent credit transactions"], "A) Predicting house sale prices in dollars", "Predicting continuous numeric values is regression.", "EASY"),
          ("In reinforcement learning, what does the agent maximize over time?", ["A) Immediate loss", "B) Cumulative discounted expected reward", "C) Number of actions taken", "D) State count"], "B) Cumulative discounted expected reward", "RL agents maximize long-term return.", "MEDIUM")]),
        ("08 — Neural Networks", "Perceptrons, multi-layer perceptrons (MLP), activation functions (ReLU, Sigmoid), and backpropagation.",
         [("Perceptron Architecture", "Weights, biases, and linear combinations.", "MEDIUM"), ("Backpropagation & Activation", "Chain rule gradient calculation and non-linearities.", "HARD")],
         "CODE_OUTPUT", "Perceptron Output", "For inputs [1, 2], weights [3, 1], and bias b = -1, what is the pre-activation sum z = w1*x1 + w2*x2 + b?", "1*3 + 2*1 - 1", "4", "3 + 2 - 1 = 4.", "MEDIUM",
         [("Why are non-linear activation functions (like ReLU) required in multi-layer neural networks?", ["A) Without them, stacking linear layers collapses mathematically into a single linear transformation", "B) To make weights zero", "C) To avoid matrix multiplication", "D) To reduce memory"], "A) Without them, stacking linear layers collapses mathematically into a single linear transformation", "Non-linearities allow networks to learn non-linear decision boundaries.", "HARD"),
          ("What calculus rule underlies the backpropagation algorithm for training neural networks?", ["A) Fundamental Theorem of Calculus", "B) Chain Rule of partial derivatives", "C) L'Hopital's Rule", "D) Simpson's Rule"], "B) Chain Rule of partial derivatives", "Backpropagation computes error gradients by propagating backward via the chain rule.", "HARD"),
          ("What is the formula for the ReLU (Rectified Linear Unit) activation function?", ["A) f(x) = 1 / (1 + e^-x)", "B) f(x) = max(0, x)", "C) f(x) = tanh(x)", "D) f(x) = x^2"], "B) f(x) = max(0, x)", "ReLU outputs x if positive, else 0.", "EASY"),
          ("What occurs during the phenomenon of vanishing gradients in deep networks?", ["A) Gradients become exponentially small as they propagate to earlier layers, halting learning", "B) Weights grow to infinity", "C) Training loss becomes negative", "D) Data is erased"], "A) Gradients become exponentially small as they propagate to earlier layers, halting learning", "Small derivative multiplications cause vanishing gradients.", "HARD"),
          ("What is an epoch in neural network training?", ["A) One single batch update", "B) One complete pass through the entire training dataset", "C) Saving a checkpoint", "D) Initialization of weights"], "B) One complete pass through the entire training dataset", "An epoch denotes a full iteration over the training corpus.", "EASY")]),
        ("09 — Natural Language Processing", "Tokenization, bag-of-words, TF-IDF, word embeddings, and transformers attention mechanisms.",
         [("Text Preprocessing", "Tokenization, stop words, and vocabulary building.", "EASY"), ("Embeddings & Transformers", "Semantic vector spaces and self-attention.", "HARD")],
         "FILL_BLANK", "Self-Attention Mechanism", "What revolutionary deep learning architecture introduced the Self-Attention mechanism in 2017? The ________", "Attention Is All You Need", "Transformer", "The Transformer architecture was introduced in the seminal paper 'Attention Is All You Need'.", "MEDIUM",
         [("What is tokenization in Natural Language Processing?", ["A) Encrypting text with SHA-256", "B) Segmenting continuous text into discrete units (words, subwords, characters)", "C) Translating text into French", "D) Removing numbers"], "B) Segmenting continuous text into discrete units (words, subwords, characters)", "Tokenization breaks strings into tokens.", "EASY"),
          ("What do Word Embeddings (like Word2Vec) achieve mathematically?", ["A) Alphabetize all words", "B) Map words into dense continuous vector spaces where geometric distance reflects semantic similarity", "C) Remove punctuation", "D) Spell-check sentences"], "B) Map words into dense continuous vector spaces where geometric distance reflects semantic similarity", "Embeddings capture semantic proximity geometrically.", "MEDIUM"),
          ("What does the 'TF-IDF' text feature weighting metric stand for?", ["A) Total Frequency - Inverse Document Format", "B) Term Frequency - Inverse Document Frequency", "C) Tensor Flow - Internal Data Frame", "D) Text File - Indexing Data Field"], "B) Term Frequency - Inverse Document Frequency", "TF-IDF balances term frequency with document specificity.", "MEDIUM"),
          ("What advantage does the self-attention mechanism have over recurrent neural networks (RNNs)?", ["A) Processes sequences in parallel rather than sequentially, capturing long-range dependencies efficiently", "B) Requires no training data", "C) Eliminates all linear algebra", "D) Only works on audio"], "A) Processes sequences in parallel rather than sequentially, capturing long-range dependencies efficiently", "Transformers parallelize sequence processing across context windows.", "HARD"),
          ("What famous vector arithmetic relationship is demonstrated by Word2Vec embeddings?", ["A) King - Man + Woman = Queen", "B) Cat + Dog = Mouse", "C) 1 + 1 = 2", "D) Apple - Fruit = Computer"], "A) King - Man + Woman = Queen", "Vector offsets capture semantic analogies.", "MEDIUM")]),
        ("10 — AI Ethics and Applications", "Algorithmic bias, fairness, transparency (XAI), safety alignment, and real-world deployment.",
         [("Bias & Fairness", "Historical bias in training corpora and disparate impact.", "MEDIUM"), ("Safety & Alignment", "Reward hacking, hallucination, and autonomous governance.", "MEDIUM")],
         "TRUE_FALSE", "Algorithmic Objectivity", "True or False: Because machine learning algorithms rely on mathematical formulas, they are inherently free from societal bias without human intervention.", "ML is inherently unbiased", False, "Machine learning models mirror, encode, and can amplify historical prejudices present in their training data.", "EASY",
         [("How does algorithmic bias typically enter machine learning systems?", ["A) Through hardware glitches", "B) When historical disparities and biased distributions are present in the training data", "C) By using Python instead of C++", "D) Only through intentional developer malice"], "B) When historical disparities and biased distributions are present in the training data", "Models learn and reflect patterns from historical training data.", "EASY"),
          ("What is Explainable AI (XAI)?", ["A) AI that explains programming languages to students", "B) Techniques and methods that make machine learning predictions and decision logic understandable to human observers", "C) Open-source code exclusively", "D) High-accuracy models only"], "B) Techniques and methods that make machine learning predictions and decision logic understandable to human observers", "XAI fosters interpretability and accountability.", "MEDIUM"),
          ("What is 'hallucination' in the context of Large Language Models?", ["A) Overheating of GPU clusters", "B) Generating fluent, confident statements that are factually false or ungrounded", "C) Memory leaks in Python", "D) Infinite loops"], "B) Generating fluent, confident statements that are factually false or ungrounded", "Hallucination refers to generating fabricated facts convincingly.", "MEDIUM"),
          ("What is the objective of AI alignment research?", ["A) Aligning GPUs in a server rack", "B) Ensuring that artificial intelligence systems reliably act in accordance with human values, intentions, and safety guidelines", "C) Making AI run on mobile devices", "D) Standardizing code format"], "B) Ensuring that artificial intelligence systems reliably act in accordance with human values, intentions, and safety guidelines", "Alignment ensures AI actions match intended human values.", "MEDIUM"),
          ("What European Union regulation introduced comprehensive risk tiers for AI applications?", ["A) GDPR only", "B) EU AI Act", "C) HIPAA", "D) Digital Millennium Act"], "B) EU AI Act", "The EU AI Act classifies AI systems by risk categories.", "MEDIUM")])
    ]
    all_subjects.append(make_generic_subject("AI", "Artificial Intelligence", "Study intelligent agents, search algorithms, logic representation, neural networks, NLP, and AI ethics.", "COMPUTER_SCIENCE", "ADVANCED", 5, ai_lessons))

    # 6. DATA STRUCTURES (10 Lessons)
    dsa_lessons = [
        ("01 — Introduction to Data Structures", "Abstract Data Types (ADTs), Big-O asymptotic notation, and memory layouts.",
         [("ADTs vs Concrete Structures", "Interface contracts vs physical implementations.", "EASY"), ("Asymptotic Notation", "Big-O, Big-Omega, and Big-Theta worst-case analysis.", "MEDIUM")],
         "MULTIPLE_CHOICE", "Identify Worst-Case Complexity", "Which asymptotic notation represents the theoretical upper bound on algorithm runtime?", ["Big-Omega", "Big-O", "Big-Theta", "Little-o"], "Big-O", "Big-O denotes the asymptotic upper bound on runtime growth.", "EASY",
         [("What is the time complexity of accessing an array element at a known index?", ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(n^2)"], "A) O(1)", "Arrays calculate memory address directly via base + index * size.", "EASY"),
          ("Which growth rate represents the fastest asymptotically growing complexity?", ["A) O(n log n)", "B) O(n^2)", "C) O(2^n)", "D) O(n)"], "C) O(2^n)", "Exponential complexity O(2^n) dwarfs polynomial complexities.", "MEDIUM"),
          ("What does Space Complexity analyze in algorithm design?", ["A) Hard drive size required", "B) Auxiliary memory consumed by an algorithm as input size n grows", "C) Network bandwidth", "D) Cache hit rate"], "B) Auxiliary memory consumed by an algorithm as input size n grows", "Space complexity measures extra memory overhead.", "EASY"),
          ("What does an Abstract Data Type (ADT) specify?", ["A) The exact physical memory layout", "B) What operations can be performed on the data without specifying how they are implemented", "C) The programming language", "D) Hardware registers"], "B) What operations can be performed on the data without specifying how they are implemented", "ADTs define behavior independently of implementation.", "MEDIUM"),
          ("What is the time complexity of linear search across an unsorted collection of n items?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n!)"], "C) O(n)", "In the worst case, every element must be inspected sequentially.", "EASY")]),
        ("02 — Arrays", "Static vs dynamic arrays, contiguous memory allocation, amortization, and two-pointer algorithms.",
         [("Array Memory Model", "Address arithmetic and cache locality.", "MEDIUM"), ("Dynamic Resizing", "Geometric array doubling and O(1) amortized insertion.", "MEDIUM")],
         "CODE_OUTPUT", "Array Resizing Factor", "When a dynamic array (like Python list or Java ArrayList) fills up, by what typical geometric factor does it resize its capacity?", "2", "2", "Dynamic arrays typically double capacity (growth factor 2x or 1.5x) to guarantee amortized O(1) appends.", "MEDIUM",
         [("Why do arrays provide extremely high cache locality compared to linked nodes?", ["A) Elements are stored in contiguous adjacent memory blocks", "B) Arrays are sorted", "C) Arrays use pointers", "D) Arrays are smaller"], "A) Elements are stored in contiguous adjacent memory blocks", "Spatial locality allows hardware prefetchers to load entire cache lines.", "MEDIUM"),
          ("What is the amortized time complexity of appending an element to a dynamic array?", ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(n^2)"], "A) O(1)", "Doubling capacity makes infrequent O(n) resizes average out to O(1) per insert.", "MEDIUM"),
          ("What is the worst-case time complexity of inserting an item at the beginning (index 0) of an array of size n?", ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(0)"], "B) O(n)", "All n existing elements must be shifted one position to the right.", "EASY"),
          ("What algorithmic technique commonly solves the 'Two Sum in sorted array' problem in O(n) time and O(1) space?", ["A) Dynamic Programming", "B) Two-Pointer Technique", "C) Breadth-First Search", "D) Bitmasking"], "B) Two-Pointer Technique", "Left and right pointers converge inwards.", "MEDIUM"),
          ("How is a multi-dimensional array stored in contiguous physical computer memory?", ["A) Row-major or Column-major sequential layout", "B) Scattered random memory blocks", "C) On GPU registers only", "D) In a linked chain"], "A) Row-major or Column-major sequential layout", "Flattened into 1D physical memory via row or column major ordering.", "MEDIUM")]),
        ("03 — Linked Lists", "Singly linked lists, doubly linked lists, circular lists, sentinel nodes, and pointer manipulation.",
         [("Singly vs Doubly Linked", "next pointers vs prev/next pointers.", "MEDIUM"), ("List Manipulations", "O(1) head insertion, reversal, and cycle detection.", "HARD")],
         "FILL_BLANK", "Cycle Detection Algorithm", "What is the famous two-pointer cycle detection algorithm called? Floyd's _______ and Hare algorithm", "Floyd's algorithm", "Tortoise", "Floyd's Tortoise and Hare algorithm detects cycles using slow and fast pointers.", "MEDIUM",
         [("What is the time complexity of inserting a node at the head of a linked list given a head pointer?", ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(n^2)"], "A) O(1)", "Only pointer adjustments are needed without element shifting.", "EASY"),
          ("What memory overhead does a linked list have compared to a primitive array?", ["A) None", "B) Extra pointer/reference addresses stored with each node", "C) Extra registers", "D) Slower CPU clock"], "B) Extra pointer/reference addresses stored with each node", "Each node requires storage for references/pointers.", "EASY"),
          ("What is the time complexity to search for a specific value in a singly linked list of length n?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n log n)"], "C) O(n)", "Nodes must be traversed sequentially from the head pointer.", "EASY"),
          ("In a Doubly Linked List, how many pointer references does each interior node store?", ["A) 1", "B) 2 (previous and next)", "C) 3", "D) 4"], "B) 2 (previous and next)", "Each node links to both successor and predecessor.", "EASY"),
          ("What does a Sentinel (dummy) node simplify in linked list implementations?", ["A) Speeds up CPU execution", "B) Eliminates edge case null checks for head and tail operations", "C) Compresses node data", "D) Reverses the list"], "B) Eliminates edge case null checks for head and tail operations", "Sentinel nodes ensure head and tail pointers are never null.", "MEDIUM")]),
        ("04 — Stacks", "LIFO principle, push, pop, peek operations, call stack, and parenthesis matching.",
         [("LIFO Mechanism", "Last-In, First-Out semantics and array/list backing.", "EASY"), ("Stack Applications", "Expression evaluation, recursion simulation, and undo systems.", "MEDIUM")],
         "ORDERING", "Stack Pop Sequence", "Items A, B, and C are pushed to a stack in order: push(A), push(B), push(C). What is the exact pop order?",
         ["C", "B", "A"], ["C", "B", "A"], "Stack is Last-In-First-Out, so C is popped first, then B, then A.", "EASY",
         [("What does the LIFO acronym represent?", ["A) Last-In, First-Out", "B) Linear Input File Organization", "C) Lowest Index Fast Ordering", "D) Loop Iteration Fast Operation"], "A) Last-In, First-Out", "The most recently added element is removed first.", "EASY"),
          ("What is the time complexity of push and pop operations on an efficient stack?", ["A) O(1)", "B) O(n)", "C) O(log n)", "D) O(n^2)"], "A) O(1)", "Accessing only the top of the stack is constant time.", "EASY"),
          ("What classic problem is directly solved using a stack data structure?", ["A) Shortest path in a graph", "B) Balanced Parentheses matching in compilers", "C) Minimum Spanning Tree", "D) Hash collision resolution"], "B) Balanced Parentheses matching in compilers", "Opening brackets are pushed; closing brackets pop and match.", "EASY"),
          ("What error occurs when attempting to pop from an empty stack?", ["A) Stack Overflow", "B) Stack Underflow", "C) Memory Leak", "D) Null Pointer"], "B) Stack Underflow", "Popping from an empty structure causes stack underflow.", "EASY"),
          ("What occurs when a recursive function exceeds its allocated call stack limit?", ["A) StackOverflowError", "B) OutOfMemoryError", "C) Segmentation Fault", "D) NullPointerException"], "A) StackOverflowError", "Exhausting allocated stack frames triggers a stack overflow.", "EASY")]),
        ("05 — Queues", "FIFO principle, enqueue, dequeue, circular queues, deques, and priority queues.",
         [("FIFO Mechanism", "First-In, First-Out operations with front and rear pointers.", "EASY"), ("Circular & Priority Queues", "Ring buffer memory reuse and heap-backed priority queues.", "MEDIUM")],
         "MATCHING", "Queue Operation Matching", "Match each Queue operation with its primary function:",
         [["Enqueue", "Insert element at rear"], ["Dequeue", "Remove element from front"], ["Peek", "Inspect front element without removal"]],
         {"Enqueue": "Insert element at rear", "Dequeue": "Remove element from front", "Peek": "Inspect front element without removal"},
         "Queue fundamental operations.", "EASY",
         [("What does the FIFO acronym stand for?", ["A) First-In, First-Out", "B) Fast Index File Operation", "C) Fixed Input Fixed Output", "D) File Input Format Order"], "A) First-In, First-Out", "The earliest inserted element is serviced first.", "EASY"),
          ("Why is a standard circular queue (ring buffer) preferred over an unshifted array queue?", ["A) It prevents memory wastage from unused space when elements are dequeued", "B) It sorts elements automatically", "C) It allows duplicate items", "D) It runs on GPU"], "A) It prevents memory wastage from unused space when elements are dequeued", "Modulo arithmetic wraps front and rear indices around the array buffer.", "MEDIUM"),
          ("What data structure allows insertion and deletion from both ends efficiently?", ["A) Stack", "B) Double-Ended Queue (Deque)", "C) Singly Linked List", "D) Binary Heap"], "B) Double-Ended Queue (Deque)", "A deque supports O(1) operations at both front and back.", "MEDIUM"),
          ("In a breadth-first search (BFS) graph traversal, which data structure maintains the frontier?", ["A) Stack", "B) Queue", "C) Array list", "D) Binary Tree"], "B) Queue", "FIFO queues explore vertices in order of discovery distance.", "EASY"),
          ("What happens in a Priority Queue when you dequeue an element?", ["A) The item with the highest priority is extracted regardless of insertion order", "B) The oldest item is extracted", "C) A random item is deleted", "D) The smallest key is incremented"], "A) The item with the highest priority is extracted regardless of insertion order", "Priority determines extraction order.", "EASY")]),
        ("06 — Trees", "Tree terminology (root, leaf, height, depth), binary trees, and tree traversals (pre, in, post, level order).",
         [("Tree Nomenclature", "Root, parent, child, siblings, depth, and height.", "EASY"), ("Tree Traversal Orders", "In-order, pre-order, post-order, and BFS level-order.", "MEDIUM")],
         "ORDERING", "In-Order Traversal Sequence", "For a binary tree with Root=2, Left Child=1, Right Child=3, what is the In-Order (Left, Root, Right) traversal sequence?",
         ["1", "2", "3"], ["1", "2", "3"], "In-order visits Left (1), Root (2), then Right (3).", "EASY",
         [("What is the maximum number of children a node can have in a Binary Tree?", ["A) 1", "B) 2", "C) 3", "D) Any number"], "B) 2", "Binary trees restrict child nodes to at most two (left and right).", "EASY"),
          ("What is a leaf node in a tree?", ["A) The topmost starting node", "B) A node with zero children", "C) A node with two children", "D) The root node"], "B) A node with zero children", "Leaf nodes terminate branches with no descendants.", "EASY"),
          ("In which traversal order is the root node visited BEFORE both of its subtrees?", ["A) In-order", "B) Pre-order", "C) Post-order", "D) Level-order"], "B) Pre-order", "Pre-order visits: Root, Left Subtree, Right Subtree.", "EASY"),
          ("What is the height of a tree with only a single root node?", ["A) 0", "B) 1", "C) -1", "D) 2"], "A) 0", "By standard definition, height is the number of edges on the longest root-to-leaf path (0 edges).", "MEDIUM"),
          ("What is the maximum number of nodes on level d (where root is level 0) of a binary tree?", ["A) 2*d", "B) 2^d", "C) d^2", "D) 2^(d+1)"], "B) 2^d", "Each level doubles the potential node capacity: 2^0, 2^1, 2^2, etc.", "MEDIUM")]),
        ("07 — Binary Search Trees", "BST invariant (left < root < right), searching, insertion, deletion, and balanced BST overview (AVL, Red-Black).",
         [("BST Invariant", "All left subtree keys < node key < all right subtree keys.", "MEDIUM"), ("BST Deletion Cases", "Node with 0, 1, or 2 children (in-order successor replacement).", "HARD")],
         "TRUE_FALSE", "In-Order Traversal of BST", "True or False: An In-Order traversal of any valid Binary Search Tree always visits elements in strictly ascending sorted order.", "In-order yields sorted order", True, "Because left < root < right, in-order traversal naturally yields sorted order.", "EASY",
         [("What is the average time complexity for search, insert, and delete in a balanced BST?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n^2)"], "B) O(log n)", "Dividing the search space in half at each step yields O(log n).", "EASY"),
          ("What is the worst-case time complexity of searching an unbalanced BST that degenerates into a linear chain?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n log n)"], "C) O(n)", "Skewed trees become functionally identical to linked lists.", "MEDIUM"),
          ("When deleting a BST node with two children, what node typically replaces it?", ["A) Any random leaf", "B) The in-order successor (minimum node in right subtree) or in-order predecessor", "C) The root of the tree", "D) The parent node"], "B) The in-order successor (minimum node in right subtree) or in-order predecessor", "In-order successor maintains the BST invariant.", "HARD"),
          ("What self-balancing binary search tree maintains a height balance factor of at most +/- 1?", ["A) AVL Tree", "B) Splay Tree", "C) B-Tree", "D) Trie"], "A) AVL Tree", "AVL trees enforce strict height balancing via tree rotations.", "MEDIUM"),
          ("Which operation rebalances an AVL tree after an unbalanced insertion?", ["A) Heapify", "B) Tree Rotations (Left, Right, Left-Right, Right-Left)", "C) Hash rehashing", "D) Binary search"], "B) Tree Rotations (Left, Right, Left-Right, Right-Left)", "Rotations adjust local branch heights in O(1) time.", "HARD")]),
        ("08 — Heaps", "Complete binary trees, min-heap and max-heap properties, array representation, and heapsort.",
         [("Heap Property", "Parent >= children (Max-Heap) or Parent <= children (Min-Heap).", "MEDIUM"), ("Heapify & Priority Operations", "Extract-max, insert, bubble-up, and sift-down.", "HARD")],
         "CODE_OUTPUT", "Array Representation of Heap", "In a zero-indexed array heap, if a parent node is at index i = 3, what is the index of its left child (2*i + 1)?", "2*3 + 1", "7", "Left child index formula is 2*i + 1 = 2*3 + 1 = 7.", "MEDIUM",
         [("What is the time complexity to extract the minimum element from a Min-Heap of size n?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n log n)"], "B) O(log n)", "Root is removed in O(1), and last leaf is moved to root then sifted down in O(log n).", "MEDIUM"),
          ("What is the time complexity to peek at the root element of a heap without removing it?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n^2)"], "A) O(1)", "The root resides at index 0 of the backing array.", "EASY"),
          ("What overall time complexity does Heapsort achieve to sort an array of n numbers?", ["A) O(n)", "B) O(n log n)", "C) O(n^2)", "D) O(log n)"], "B) O(n log n)", "Building heap is O(n), followed by n extractions of O(log n).", "MEDIUM"),
          ("In a complete binary tree of n nodes stored in an array, where is the parent of node index i (i > 0)?", ["A) (i - 1) // 2", "B) i // 2", "C) 2 * i", "D) i - 1"], "A) (i - 1) // 2", "Parent index in 0-based array is floor((i-1)/2).", "EASY"),
          ("Can a Max-Heap have duplicate element values?", ["A) No, all keys must be unique", "B) Yes, the heap property permits duplicate keys", "C) Only at leaf nodes", "D) Only in binary search trees"], "B) Yes, the heap property permits duplicate keys", "Heaps enforce ordering between parent and child, not uniqueness.", "EASY")]),
        ("09 — Graphs", "Vertices, edges, directed/undirected, adjacency matrix vs adjacency list, BFS, DFS, and topological sort.",
         [("Graph Representations", "Adjacency matrix (dense) vs Adjacency list (sparse).", "MEDIUM"), ("Graph Traversal & Topological Sort", "Cycle detection, Kahn's algorithm, and DAG ordering.", "HARD")],
         "MATCHING", "Graph Representation Tradeoffs", "Match each graph representation with its memory complexity for V vertices and E edges:",
         [["Adjacency Matrix", "O(V^2)"], ["Adjacency List", "O(V + E)"]],
         {"Adjacency Matrix": "O(V^2)", "Adjacency List": "O(V + E)"},
         "Graph space complexities.", "MEDIUM",
         [("What data structure provides the most space-efficient representation for a sparse graph with few edges?", ["A) Adjacency Matrix", "B) Adjacency List", "C) Complete Tree", "D) 2D Boolean Table"], "B) Adjacency List", "Adjacency list uses O(V + E) memory rather than O(V^2).", "EASY"),
          ("What is a Directed Acyclic Graph (DAG)?", ["A) A graph with undirected edges only", "B) A directed graph that contains no closed directed cycles", "C) A tree with no root", "D) A complete graph"], "B) A directed graph that contains no closed directed cycles", "DAGs permit topological sorting.", "MEDIUM"),
          ("What algorithm determines a linear ordering of vertices in a DAG such that for every directed edge u -> v, u comes before v?", ["A) Dijkstra's Algorithm", "B) Topological Sort", "C) Kruskal's Algorithm", "D) Bellman-Ford"], "B) Topological Sort", "Topological sort orders tasks respecting dependencies.", "MEDIUM"),
          ("What is the time complexity of Dijkstra's algorithm using a Min-Heap priority queue?", ["A) O(V^2)", "B) O((V + E) log V)", "C) O(E^2)", "D) O(V * E)"], "B) O((V + E) log V)", "Standard priority queue implementation complexity.", "HARD"),
          ("Can Breadth-First Search (BFS) find the shortest path in a weighted graph with varying positive edge weights?", ["A) Yes, always", "B) No, BFS only guarantees shortest path on unweighted (uniform-cost) graphs", "C) Only if edges are negative", "D) Yes, if graph is a DAG"], "B) No, BFS only guarantees shortest path on unweighted (uniform-cost) graphs", "Varying weights require Dijkstra's algorithm.", "MEDIUM")]),
        ("10 — Hashing", "Hash functions, collision resolution (chaining, open addressing, linear probing), load factor, and rehashing.",
         [("Hash Functions & Distribution", "Uniform distribution, avalanche effect, and deterministic mapping.", "MEDIUM"), ("Collision Handling & Load Factor", "Chaining vs open addressing and dynamic table rehashing.", "HARD")],
         "MATCHING", "Collision Strategies Matching", "Match each collision resolution strategy with its core mechanism:",
         [["Separate Chaining", "Linked lists or trees stored at each hash bucket"], ["Linear Probing", "Sequential search for next vacant array slot"], ["Quadratic Probing", "Interval spacing increases by quadratic polynomial"]],
         {"Separate Chaining": "Linked lists or trees stored at each hash bucket", "Linear Probing": "Sequential search for next vacant array slot", "Quadratic Probing": "Interval spacing increases by quadratic polynomial"},
         "Collision resolution methods.", "HARD",
         [("What is the load factor alpha of a hash table with n keys and m buckets?", ["A) alpha = n * m", "B) alpha = n / m", "C) alpha = m / n", "D) alpha = n + m"], "B) alpha = n / m", "Load factor represents average keys per bucket.", "MEDIUM"),
          ("What is the average time complexity of insertion, deletion, and lookup in a well-designed hash table?", ["A) O(1)", "B) O(log n)", "C) O(n)", "D) O(n^2)"], "A) O(1)", "Constant time amortized performance.", "EASY"),
          ("What happens in open addressing when a collision occurs?", ["A) Elements are appended to a linked list", "B) The algorithm probes alternative slots in the array until an empty cell is found", "C) The key is discarded", "D) An exception is raised"], "B) The algorithm probes alternative slots in the array until an empty cell is found", "Open addressing stores all elements directly within the primary array.", "MEDIUM"),
          ("What problem occurs in linear probing when occupied slots form contiguous blocks?", ["A) Memory leak", "B) Primary Clustering", "C) Stack overflow", "D) Deadlock"], "B) Primary Clustering", "Clusters lengthen probe sequences and degrade performance.", "HARD"),
          ("What triggers a hash table to rehash (resize its internal table and redistribute keys)?", ["A) When the load factor exceeds a threshold (e.g. 0.75)", "B) On every insert", "C) When a key is deleted", "D) After 100 queries"], "A) When the load factor exceeds a threshold (e.g. 0.75)", "Resizing maintains O(1) performance by preventing overcrowding.", "MEDIUM")])
    ]
    all_subjects.append(make_generic_subject("DSA", "Data Structures", "Master arrays, linked lists, stacks, queues, trees, binary search trees, heaps, graphs, and hash tables.", "COMPUTER_SCIENCE", "INTERMEDIATE", 6, dsa_lessons))

    # 7. MACHINE LEARNING (10 Lessons)
    ml_lessons = [
        ("01 — Machine Learning Introduction", "Taxonomy of learning, inductive bias, supervised vs unsupervised, and workflows.",
         [("ML Workflow", "Data collection, feature preparation, training, validation, and serving.", "EASY"), ("Inductive Bias", "Assumptions made by learning algorithms to generalize.", "MEDIUM")],
         "MULTIPLE_CHOICE", "Identify ML Type", "Which category of machine learning aims to discover hidden groupings in customer purchase patterns without labels?", ["Supervised Classification", "Unsupervised Clustering", "Reinforcement Learning", "Linear Regression"], "Unsupervised Clustering", "Unsupervised clustering groups data without ground-truth labels.", "EASY",
         [("What defines the machine learning paradigm compared to classical rule-based programming?", ["A) Humans write every conditional rule explicitly", "B) Algorithms infer predictive patterns directly from data", "C) ML requires no data", "D) ML never uses algorithms"], "B) Algorithms infer predictive patterns directly from data", "ML learns functional mappings from empirical data.", "EASY"),
          ("What is the target variable in a supervised learning dataset called?", ["A) Feature", "B) Label / Ground Truth", "C) Hyperparameter", "D) Epoch"], "B) Label / Ground Truth", "Labels represent the ground-truth outcomes.", "EASY"),
          ("What is the primary danger of training and evaluating a model on the exact same dataset?", ["A) Code will not compile", "B) Inability to detect overfitting / false sense of model generalization", "C) Slower training", "D) Negative loss"], "B) Inability to detect overfitting / false sense of model generalization", "Evaluating on training data hides overfitting.", "MEDIUM"),
          ("What is a hyperparameter in machine learning?", ["A) A model parameter learned automatically during gradient descent", "B) A configuration value set by the practitioner prior to training (e.g. learning rate)", "C) A hardware attribute", "D) A dataset column"], "B) A configuration value set by the practitioner prior to training (e.g. learning rate)", "Hyperparameters control the learning process.", "MEDIUM"),
          ("What is transfer learning?", ["A) Moving data across servers", "B) Taking a model pre-trained on a vast dataset and fine-tuning it for a related downstream task", "C) Converting code to C++", "D) Reinforcement learning"], "B) Taking a model pre-trained on a vast dataset and fine-tuning it for a related downstream task", "Transfer learning leverages pre-learned representations.", "MEDIUM")]),
        ("02 — Data Preparation", "Missing values, imputation, one-hot encoding, min-max scaling, standardization, and train-test splits.",
         [("Handling Missing Values", "Mean/median imputation vs deletion.", "EASY"), ("Feature Scaling", "StandardScaler (Z-score) vs MinMaxScaler [0, 1].", "MEDIUM")],
         "FILL_BLANK", "Categorical Encoding", "What encoding converts categorical values like ['Red', 'Green'] into binary columns? ______-Hot Encoding", "_____-Hot Encoding", "One", "One-Hot Encoding represents categorical variables as binary vectors.", "EASY",
         [("Why is feature scaling essential for distance-based algorithms like KNN and gradient descent?", ["A) To prevent features with large numeric scales from dominating the loss and distance calculations", "B) To remove rows", "C) To convert floats to ints", "D) To increase sample count"], "A) To prevent features with large numeric scales from dominating the loss and distance calculations", "Unscaled features skew Euclidean distances and gradient steps.", "MEDIUM"),
          ("What does StandardScaler transform a feature's distribution into?", ["A) Values strictly between 0 and 1", "B) Zero mean (mu=0) and unit variance (sigma=1)", "C) Only positive numbers", "D) Categorical strings"], "B) Zero mean (mu=0) and unit variance (sigma=1)", "Standardization subtracts mean and divides by standard deviation.", "EASY"),
          ("What is 'Data Leakage' during preprocessing?", ["A) Losing data due to hard drive failure", "B) Accidentally incorporating information from the test dataset into the training pipeline (e.g. fitting scaler on test data)", "C) Open-sourcing private models", "D) Removing nulls"], "B) Accidentally incorporating information from the test dataset into the training pipeline (e.g. fitting scaler on test data)", "Leakage contaminates training with test signals.", "HARD"),
          ("When imputing missing values in a skewed feature distribution, which measure of central tendency is most robust?", ["A) Mean", "B) Median", "C) Maximum", "D) Standard deviation"], "B) Median", "Median is unaffected by extreme outliers.", "EASY"),
          ("What does the train_test_split parameter 'stratify=y' ensure in classification problems?", ["A) Faster execution", "B) The class label proportion in train and test sets mirrors the original dataset distribution", "C) No duplicates", "D) Shuffling is disabled"], "B) The class label proportion in train and test sets mirrors the original dataset distribution", "Stratification preserves class balances.", "MEDIUM")]),
        ("03 — Linear Regression", "Ordinary Least Squares (OLS), loss functions (MSE, RMSE), cost surface, and gradient descent.",
         [("Hypothesis & Cost Function", "y_hat = w*x + b and Mean Squared Error.", "MEDIUM"), ("Gradient Descent", "Learning rate alpha, batch, stochastic, and mini-batch.", "HARD")],
         "CODE_OUTPUT", "Linear Hypothesis Evaluation", "For model y_hat = 3*x + 4, what is the predicted value when x = 5?", "3*5 + 4", "19", "y_hat = 3(5) + 4 = 15 + 4 = 19.", "EASY",
         [("What loss function does Ordinary Least Squares (OLS) linear regression minimize?", ["A) Binary Cross-Entropy", "B) Mean Squared Error (MSE)", "C) Hinge Loss", "D) Absolute Percentage Error"], "B) Mean Squared Error (MSE)", "OLS minimizes the sum of squared residuals.", "EASY"),
          ("What does the learning rate (alpha) parameter in Gradient Descent control?", ["A) Number of features", "B) The step size taken in the direction of the negative gradient at each update iteration", "C) The batch size", "D) Weight regularization strength"], "B) The step size taken in the direction of the negative gradient at each update iteration", "Learning rate scales gradient update steps.", "MEDIUM"),
          ("What happens if the learning rate is set excessively high during gradient descent?", ["A) Training converges immediately", "B) The loss can oscillate wildly and diverge away from the minimum", "C) Overfitting occurs", "D) Weights become zero"], "B) The loss can oscillate wildly and diverge away from the minimum", "Overshooting the minimum causes divergence.", "MEDIUM"),
          ("What does the coefficient of determination (R^2) represent in regression analysis?", ["A) The average error in dollars", "B) The proportion of variance in the dependent variable explained by the independent variables", "C) The slope of the line", "D) The number of training epochs"], "B) The proportion of variance in the dependent variable explained by the independent variables", "R^2 measures goodness-of-fit (0.0 to 1.0).", "MEDIUM"),
          ("What is the difference between Batch Gradient Descent and Stochastic Gradient Descent (SGD)?", ["A) Batch updates weights using all samples; SGD updates weights using one randomly chosen sample per step", "B) SGD does not calculate gradients", "C) Batch runs only once", "D) SGD is strictly for neural networks"], "A) Batch updates weights using all samples; SGD updates weights using one randomly chosen sample per step", "SGD trades stability for speed by updating per-sample.", "HARD")]),
        ("04 — Logistic Regression", "Sigmoid activation, odds and log-odds, binary cross-entropy loss, and decision thresholds.",
         [("Sigmoid Function", "Mapping real values to probabilities in (0, 1).", "MEDIUM"), ("Classification Threshold", "Converting probabilities into binary classes (default 0.5).", "EASY")],
         "TRUE_FALSE", "Sigmoid Output Range", "True or False: The standard Sigmoid activation function sigma(z) maps any input on the real line into the open interval (0, 1).", "Sigmoid maps to (0, 1)", True, "sigma(z) = 1 / (1 + e^-z) outputs values between 0 and 1.", "EASY",
         [("What is the mathematical equation for the standard logistic (sigmoid) function?", ["A) sigma(z) = max(0, z)", "B) sigma(z) = 1 / (1 + e^-z)", "C) sigma(z) = e^z", "D) sigma(z) = tanh(z)"], "B) sigma(z) = 1 / (1 + e^-z)", "The sigmoid formula maps z to probability.", "EASY"),
          ("Despite its name, is Logistic Regression a classification or regression algorithm?", ["A) Classification algorithm", "B) Regression algorithm", "C) Clustering algorithm", "D) Dimensionality reduction"], "A) Classification algorithm", "Logistic regression predicts discrete class probabilities.", "EASY"),
          ("What loss function is optimized when training Logistic Regression models?", ["A) Mean Squared Error", "B) Binary Cross-Entropy (Log Loss)", "C) Hinge Loss", "D) Huber Loss"], "B) Binary Cross-Entropy (Log Loss)", "Log loss penalizes confident incorrect probability predictions.", "MEDIUM"),
          ("What happens when you increase the classification probability threshold from 0.5 to 0.8?", ["A) Precision increases, Recall typically decreases", "B) Recall increases, Precision decreases", "C) No effect", "D) Accuracy becomes 100%"], "A) Precision increases, Recall typically decreases", "A higher threshold requires higher confidence for positive predictions.", "HARD"),
          ("What generalization of Logistic Regression handles multi-class classification?", ["A) Linear regression", "B) Multinomial Logistic Regression (Softmax Regression)", "C) K-Means", "D) Naive Bayes"], "B) Multinomial Logistic Regression (Softmax Regression)", "Softmax generalizes sigmoid across K classes.", "MEDIUM")]),
        ("05 — Decision Trees", "Tree induction, recursive binary splitting, Gini impurity, Information Gain, and pruning.",
         [("Splitting Criteria", "Gini impurity vs Shannon Entropy.", "MEDIUM"), ("Tree Overfitting & Pruning", "Max depth, min samples split, and cost-complexity pruning.", "HARD")],
         "CODE_OUTPUT", "Gini Impurity Pure Node", "What is the Gini impurity of a perfectly pure node containing only samples of one single class?", "1 - (1^2)", "0", "Pure nodes have Gini impurity = 1 - (1^2) = 0.0.", "EASY",
         [("What splitting criterion measures the expected reduction in entropy in ID3/C4.5 decision trees?", ["A) Gini Impurity", "B) Information Gain", "C) Variance Reduction", "D) Mean Squared Error"], "B) Information Gain", "Information gain quantifies entropy reduction.", "MEDIUM"),
          ("Why are deep, unpruned Decision Trees highly susceptible to overfitting?", ["A) They cannot learn non-linear boundaries", "B) They can continue splitting until every single training sample occupies its own leaf node", "C) They run too slowly", "D) They have high bias"], "B) They can continue splitting until every single training sample occupies its own leaf node", "Unconstrained depth memorizes training noise.", "MEDIUM"),
          ("What hyperparameter prevents a decision tree from growing indefinitely?", ["A) max_depth", "B) learning_rate", "C) n_estimators", "D) kernel"], "A) max_depth", "max_depth limits tree vertical depth.", "EASY"),
          ("What is the primary advantage of Decision Trees over complex ensemble models?", ["A) Highest possible accuracy on every dataset", "B) High interpretability and visual explainability of decision rules", "C) Complete immunity to noise", "D) Never requires hyperparameter tuning"], "B) High interpretability and visual explainability of decision rules", "Decision trees produce transparent if-then decision paths.", "EASY"),
          ("What is an ensemble of multiple decision trees trained with bootstrap aggregation called?", ["A) Neural Network", "B) Random Forest", "C) Support Vector Machine", "D) K-Means"], "B) Random Forest", "Random Forests combine bagged trees with random feature subsampling.", "MEDIUM")]),
        ("06 — K-Nearest Neighbors", "Instance-based lazy learning, distance metrics (Euclidean, Manhattan), and choosing k.",
         [("Distance Metrics", "Euclidean sqrt(sum(x_i - y_i)^2) vs Manhattan sum(|x_i - y_i|).", "EASY"), ("Choosing k", "Small k (high variance) vs large k (high bias).", "MEDIUM")],
         "CODE_OUTPUT", "Euclidean Distance", "What is the Euclidean distance between points (0, 0) and (3, 4)?", "sqrt(3^2 + 4^2)", "5", "sqrt(9 + 16) = sqrt(25) = 5.", "EASY",
         [("Why is K-Nearest Neighbors (KNN) categorized as a 'lazy' learning algorithm?", ["A) It uses very little CPU power", "B) It does not learn an explicit model during training; it memorizes the training data and computes distances at query time", "C) It only runs once a day", "D) It cannot handle numbers"], "B) It does not learn an explicit model during training; it memorizes the training data and computes distances at query time", "Lazy learners defer computation until inference.", "MEDIUM"),
          ("What happens to the decision boundary in KNN when k = 1?", ["A) Highly smooth and generalized", "B) Extremely complex and jagged, highly sensitive to noise (high variance)", "C) Completely linear", "D) It collapses into a circle"], "B) Extremely complex and jagged, highly sensitive to noise (high variance)", "k=1 fits individual noise points.", "MEDIUM"),
          ("What distance metric sums the absolute differences of coordinates: sum(|x_i - y_i|)?", ["A) Euclidean Distance", "B) Manhattan (L1 / Taxicab) Distance", "C) Cosine Distance", "D) Mahalanobis Distance"], "B) Manhattan (L1 / Taxicab) Distance", "Manhattan distance measures grid-like absolute deltas.", "EASY"),
          ("What computational challenge occurs when applying KNN to high-dimensional datasets?", ["A) Underfitting", "B) Curse of Dimensionality (all pairwise distances become equidistant)", "C) Zero gradients", "D) Integer overflow"], "B) Curse of Dimensionality (all pairwise distances become equidistant)", "High dimensions cause distance metrics to lose discriminatory power.", "HARD"),
          ("How does KNN classify a new test point once the k nearest neighbors are identified?", ["A) Random coin flip", "B) Majority vote among the k neighbors (or distance-weighted average for regression)", "C) Solves a linear equation", "D) Inverts a matrix"], "B) Majority vote among the k neighbors (or distance-weighted average for regression)", "Majority voting determines class assignment.", "EASY")]),
        ("07 — Clustering", "Unsupervised clustering, K-Means algorithm, centroid initialization, elbow method, and silhouette score.",
         [("K-Means Algorithm", "Assign to nearest centroid, recompute centroids, iterate until convergence.", "MEDIUM"), ("Evaluating Clusters", "Within-Cluster Sum of Squares (WCSS) and Silhouette analysis.", "HARD")],
         "MATCHING", "Clustering Concepts Matching", "Match each clustering term with its definition:",
         [["Centroid", "Arithmetic mean center of all points in a cluster"], ["Elbow Method", "Plotting WCSS vs k to identify diminishing returns"], ["Silhouette Score", "Measures cluster cohesion vs separation (-1 to 1)"]],
         {"Centroid": "Arithmetic mean center of all points in a cluster", "Elbow Method": "Plotting WCSS vs k to identify diminishing returns", "Silhouette Score": "Measures cluster cohesion vs separation (-1 to 1)"},
         "Clustering terminology.", "MEDIUM",
         [("Is K-Means a supervised or unsupervised machine learning algorithm?", ["A) Supervised", "B) Unsupervised", "C) Reinforcement", "D) Semi-supervised only"], "B) Unsupervised", "K-Means clusters unlabeled data points.", "EASY"),
          ("What does the 'K' in K-Means denote?", ["A) The number of training epochs", "B) The pre-specified number of clusters to partition the data into", "C) The dimensionality of data", "D) The learning rate"], "B) The pre-specified number of clusters to partition the data into", "The user must specify K clusters in advance.", "EASY"),
          ("What initialization method in K-Means improves convergence by spreading initial centroids far apart?", ["A) Random uniform", "B) K-Means++", "C) Zero initialization", "D) Mean initialization"], "B) K-Means++", "K-Means++ seeds centroids probabilistically proportional to distance squared.", "HARD"),
          ("What is the range of the Silhouette Coefficient for cluster validation?", ["A) 0 to 100", "B) -1 to +1", "C) 0 to Infinity", "D) -Infinity to 0"], "B) -1 to +1", "+1 denotes tight, distinct clusters; 0 denotes overlapping; negative denotes incorrect assignment.", "MEDIUM"),
          ("Can K-Means naturally identify non-globular or concentric ring-shaped clusters?", ["A) Yes, easily", "B) No, K-Means assumes spherical clusters of similar size and density", "C) Only if scaled", "D) Yes, if k=2"], "B) No, K-Means assumes spherical clusters of similar size and density", "DBSCAN or spectral clustering is required for arbitrary shapes.", "HARD")]),
        ("08 — Model Evaluation", "Confusion matrix, Accuracy, Precision, Recall, F1-Score, ROC-AUC, and Cross-Validation.",
         [("Classification Metrics", "TP, FP, TN, FN, Precision = TP/(TP+FP), Recall = TP/(TP+FN).", "MEDIUM"), ("ROC & AUC", "True Positive Rate vs False Positive Rate curves.", "HARD")],
         "CODE_OUTPUT", "Precision Calculation", "If a model predicts 10 positives, of which 8 are True Positives (TP) and 2 are False Positives (FP), what is its Precision? (Enter decimal)", "8 / (8 + 2)", "0.8", "Precision = TP / (TP + FP) = 8 / 10 = 0.8.", "MEDIUM",
         [("Why is raw accuracy a misleading evaluation metric for highly imbalanced datasets (e.g. 99% negative)?", ["A) Accuracy takes too long to compute", "B) A naive model predicting negative every time achieves 99% accuracy while detecting zero positives", "C) Accuracy is only for regression", "D) It requires GPU hardware"], "B) A naive model predicting negative every time achieves 99% accuracy while detecting zero positives", "Accuracy hides minority class failure.", "MEDIUM"),
          ("What does Recall (Sensitivity) measure?", ["A) The fraction of true positives among all instances the model predicted as positive", "B) The fraction of true positive instances correctly detected among all actual positive cases in reality", "C) The ratio of false alarms", "D) Training speed"], "B) The fraction of true positive instances correctly detected among all actual positive cases in reality", "Recall = TP / (TP + FN).", "MEDIUM"),
          ("What is the F1-Score?", ["A) Arithmetic mean of Precision and Recall", "B) Harmonic mean of Precision and Recall: 2*(P*R)/(P+R)", "C) Maximum of Precision and Recall", "D) Difference between Precision and Recall"], "B) Harmonic mean of Precision and Recall: 2*(P*R)/(P+R)", "F1 balances precision and recall via harmonic mean.", "MEDIUM"),
          ("What does an Area Under the ROC Curve (ROC-AUC) of 0.5 indicate?", ["A) Perfect classifier", "B) Performance equivalent to random guessing", "C) Zero false positives", "D) Inverted predictions"], "B) Performance equivalent to random guessing", "AUC 0.5 represents the diagonal random baseline.", "MEDIUM"),
          ("How does K-Fold Cross-Validation operate?", ["A) Trains on k models simultaneously", "B) Splits data into k subsets, iteratively training on k-1 folds and evaluating on the held-out fold", "C) Replicates data k times", "D) Only tests the first fold"], "B) Splits data into k subsets, iteratively training on k-1 folds and evaluating on the held-out fold", "K-Fold cross-validates across all partitions to reduce variance.", "MEDIUM")]),
        ("09 — Feature Engineering", "Feature selection, PCA dimensionality reduction, polynomial features, and interaction terms.",
         [("Dimensionality Reduction", "Principal Component Analysis (PCA) variance maximization.", "HARD"), ("Feature Creation", "Domain-specific transformations, binning, and interaction features.", "MEDIUM")],
         "TRUE_FALSE", "PCA Target Labels", "True or False: Principal Component Analysis (PCA) requires target labels y to compute eigenvectors.", "PCA requires target labels", False, "PCA is an unsupervised technique that maximizes feature variance without knowledge of labels.", "MEDIUM",
         [("What is the primary objective of Principal Component Analysis (PCA)?", ["A) Classify images", "B) Reduce dimensionality by projecting data onto orthogonal axes of maximum variance", "C) Remove outlier rows", "D) Fill null values"], "B) Reduce dimensionality by projecting data onto orthogonal axes of maximum variance", "PCA captures maximal data variance in fewer orthogonal dimensions.", "HARD"),
          ("What are the principal components in PCA mathematically?", ["A) Eigenvectors of the feature covariance matrix", "B) Slopes of linear regression", "C) Weights in a neural network", "D) Random projections"], "A) Eigenvectors of the feature covariance matrix", "Eigenvectors define the principal axes.", "HARD"),
          ("What is an interaction feature in tabular machine learning?", ["A) A feature created by multiplying or combining two existing features (e.g. length * width)", "B) A feature clicked by users", "C) An index column", "D) A label"], "A) A feature created by multiplying or combining two existing features (e.g. length * width)", "Interactions capture multiplicative non-linear relationships.", "EASY"),
          ("What is the difference between Feature Selection and Feature Extraction?", ["A) Selection discards irrelevant original features; Extraction transforms features into a new coordinate space", "B) They are identical terms", "C) Extraction is only for text", "D) Selection requires deep learning"], "A) Selection discards irrelevant original features; Extraction transforms features into a new coordinate space", "Selection keeps a subset of originals; Extraction builds new latent dimensions.", "MEDIUM"),
          ("What does the 'Explained Variance Ratio' in PCA indicate?", ["A) The fraction of total dataset variance captured by each principal component", "B) The training error", "C) Number of samples lost", "D) Model latency"], "A) The fraction of total dataset variance captured by each principal component", "Guides selecting the number of components to retain.", "MEDIUM")]),
        ("10 — Introduction to Neural Networks", "Feedforward architecture, weight initialization, loss curves, and deep learning libraries.",
         [("Deep Architecture", "Input, hidden, and output layers.", "MEDIUM"), ("Training Mechanics", "Forward propagation, loss computation, and Adam optimizer.", "HARD")],
         "FILL_BLANK", "Optimizer Algorithm", "What is the widely used adaptive moment estimation optimizer in deep learning? The _____ Optimizer", "The _____ Optimizer", "Adam", "Adam combines momentum and RMSprop for adaptive learning rates.", "MEDIUM",
         [("What is the function of the output layer in a multi-class neural network classifier?", ["A) Standardize inputs", "B) Produce class probability distributions, typically via a Softmax activation", "C) Reduce dimensionality to 100", "D) Store training samples"], "B) Produce class probability distributions, typically via a Softmax activation", "Softmax outputs normalized class probabilities summing to 1.0.", "EASY"),
          ("What does the Adam optimizer combine to achieve adaptive learning rates?", ["A) Linear regression and trees", "B) Momentum and Root Mean Square Propagation (RMSProp)", "C) K-Means and SGD", "D) PCA and SVD"], "B) Momentum and Root Mean Square Propagation (RMSProp)", "Adam tracks both first and second moments of gradients.", "HARD"),
          ("What does a rising validation loss alongside a declining training loss indicate during training?", ["A) Underfitting", "B) Overfitting", "C) Perfect convergence", "D) Dying ReLU"], "B) Overfitting", "The model is memorizing training examples and failing on out-of-sample data.", "MEDIUM"),
          ("What regularization technique randomly deactivates a fraction of neurons during each training step?", ["A) Batch Normalization", "B) Dropout", "C) Gradient Clipping", "D) Early Stopping"], "B) Dropout", "Dropout prevents co-adaptation of feature detectors.", "MEDIUM"),
          ("What tensor-based open-source libraries are industry standards for building deep neural networks?", ["A) PyTorch and TensorFlow", "B) jQuery and React", "C) Django and Flask", "D) Pandas and SQLite"], "A) PyTorch and TensorFlow", "PyTorch and TensorFlow are dominant deep learning frameworks.", "EASY")])
    ]
    all_subjects.append(make_generic_subject("ML", "Machine Learning", "Explore linear regression, logistic classification, decision trees, KNN, clustering, evaluation, and deep learning.", "ARTIFICIAL_INTELLIGENCE", "ADVANCED", 7, ml_lessons))

    # 8. WEB DEVELOPMENT (10 Lessons)
    web_lessons = [
        ("01 — How the Web Works", "Client-server architecture, HTTP/HTTPS protocols, DNS resolution, and browser rendering.",
         [("Client-Server Model", "Requests, responses, and network endpoints.", "EASY"), ("DNS & HTTP Lifecycle", "IP resolution, TCP handshake, and HTTP verbs.", "MEDIUM")],
         "ORDERING", "Web Page Request Lifecycle", "Arrange the steps when navigating to a URL in a browser:",
         ["Browser checks DNS to resolve IP address", "Browser sends HTTP GET request over TCP/TLS", "Web server processes request and returns HTML response", "Browser parses HTML and paints DOM tree"],
         ["Browser checks DNS to resolve IP address", "Browser sends HTTP GET request over TCP/TLS", "Web server processes request and returns HTML response", "Browser parses HTML and paints DOM tree"],
         "Web request lifecycle from DNS to rendering.", "MEDIUM",
         [("What is the primary role of the Domain Name System (DNS)?", ["A) Store web files", "B) Translate human-readable domain names (e.g. google.com) into machine IP addresses", "C) Encrypt passwords", "D) Render HTML"], "B) Translate human-readable domain names (e.g. google.com) into machine IP addresses", "DNS functions as the Internet's phonebook.", "EASY"),
          ("What does the 'S' in HTTPS signify?", ["A) Speed", "B) Secure (encrypted via TLS/SSL)", "C) Server", "D) Static"], "B) Secure (encrypted via TLS/SSL)", "HTTPS encrypts network payloads with TLS.", "EASY"),
          ("Which HTTP status code indicates a successful request?", ["A) 404 Not Found", "B) 200 OK", "C) 500 Internal Error", "D) 301 Redirect"], "B) 200 OK", "200 indicates successful completion.", "EASY"),
          ("What standard port does standard unencrypted HTTP traffic use?", ["A) Port 80", "B) Port 443", "C) Port 22", "D) Port 3000"], "A) Port 80", "HTTP uses port 80; HTTPS uses 443.", "EASY"),
          ("What is the Document Object Model (DOM)?", ["A) A database query language", "B) An in-memory tree representation of the HTML document constructed by the browser", "C) A CSS stylesheet", "D) A server process"], "B) An in-memory tree representation of the HTML document constructed by the browser", "The DOM represents parsed HTML as manipulable nodes.", "MEDIUM")]),
        ("02 — HTML Fundamentals", "Semantic tags, document structure (<!DOCTYPE html>, head, body), links, images, and lists.",
         [("Document Structure", "head, metadata, title, and body.", "EASY"), ("Semantic Elements", "header, nav, main, article, section, footer.", "EASY")],
         "MULTIPLE_CHOICE", "Semantic Anchor Tag", "Which HTML element is used to define a hyperlink to another webpage?", ["<link>", "<a>", "<href>", "<url>"], "<a>", "The <a> (anchor) tag defines hyperlinks with the href attribute.", "EASY",
         [("Why are semantic HTML tags (like <article>, <nav>, <header>) preferred over generic <div> tags?", ["A) They improve accessibility (screen readers) and SEO rankings", "B) They render in 3D", "C) They eliminate need for CSS", "D) They execute JavaScript"], "A) They improve accessibility (screen readers) and SEO rankings", "Semantics convey structural meaning to assistive tech and search engines.", "EASY"),
          ("Which attribute specifies the target URL for an anchor <a> tag?", ["A) src", "B) href", "C) link", "D) dest"], "B) href", "href specifies the hyperlink destination.", "EASY"),
          ("Which attribute provides alternative text for screen readers and broken images on an <img> tag?", ["A) title", "B) alt", "C) desc", "D) caption"], "B) alt", "The alt attribute describes the image content for accessibility.", "EASY"),
          ("What element defines an unordered (bulleted) list in HTML?", ["A) <ol>", "B) <ul>", "C) <li>", "D) <list>"], "B) <ul>", "<ul> defines an unordered list; <ol> is ordered.", "EASY"),
          ("Where are meta tags, CSS links, and document title placed in an HTML document?", ["A) Inside the <body> tag", "B) Inside the <head> tag", "C) Inside the <footer> tag", "D) In the footer only"], "B) Inside the <head> tag", "The <head> element holds metadata and external stylesheets.", "EASY")]),
        ("03 — HTML Forms", "Form elements (<form>, <input>, <select>, <textarea>), validation, GET vs POST submission.",
         [("Form Controls", "Input types (text, email, password, number, checkbox).", "EASY"), ("Submission & Validation", "Required attribute, regex patterns, and HTTP methods.", "MEDIUM")],
         "FILL_BLANK", "Password Input Type", "Fill in the input type that masks sensitive characters: <input type=\"______\" />", "<input type=\"______\" />", "password", "type=\"password\" masks typed characters.", "EASY",
         [("What is the primary difference between GET and POST form submissions?", ["A) GET embeds form data into the URL query string; POST sends data in the HTTP request body", "B) POST is unencrypted always", "C) GET can upload massive files", "D) POST only works on mobile"], "A) GET embeds form data into the URL query string; POST sends data in the HTTP request body", "GET appends data to the URL; POST transmits data in the request body.", "MEDIUM"),
          ("Which HTML attribute ensures that an input field cannot be left blank during submission?", ["A) validate", "B) required", "C) notnull", "D) strict"], "B) required", "The required attribute triggers native browser validation.", "EASY"),
          ("Which element provides a multi-line text input field?", ["A) <input type=\"multiline\">", "B) <textarea>", "C) <text>", "D) <inputbox>"], "B) <textarea>", "<textarea> allows multi-line text editing.", "EASY"),
          ("What element creates an accessible label linked to an input control via the 'for' attribute?", ["A) <label>", "B) <span>", "C) <desc>", "D) <captiontag>"], "A) <label>", "<label for=\"input_id\"> binds accessibility labels to controls.", "EASY"),
          ("Which input type creates a dropdown selection menu in HTML forms?", ["A) <dropdown>", "B) <select> with <option> child elements", "C) <input type=\"menu\">", "D) <picker>"], "B) <select> with <option> child elements", "<select> and <option> define dropdown menus.", "EASY")]),
        ("04 — CSS Fundamentals", "Selectors (class, ID, tag), specificity, cascade rules, box model (content, padding, border, margin).",
         [("CSS Selectors & Specificity", "Element vs class (.class) vs ID (#id).", "EASY"), ("Box Model", "Content, padding, border, and margin layers.", "MEDIUM")],
         "MATCHING", "Box Model Layers Matching", "Match each CSS Box Model layer with its position from inside to outside:",
         [["Content", "Innermost area containing text and media"], ["Padding", "Transparent space surrounding the content"], ["Border", "Line surrounding the padding"], ["Margin", "Outermost space clearing area outside the border"]],
         {"Content": "Innermost area containing text and media", "Padding": "Transparent space surrounding the content", "Border": "Line surrounding the padding", "Margin": "Outermost space clearing area outside the border"},
         "CSS Box model hierarchy.", "MEDIUM",
         [("What property changes the CSS Box Model so that padding and border are included in the element's total width?", ["A) box-sizing: border-box;", "B) box-sizing: content-box;", "C) display: flex;", "D) margin: auto;"], "A) box-sizing: border-box;", "border-box includes padding and border within the declared width/height.", "MEDIUM"),
          ("Which selector has the highest CSS specificity?", ["A) Element selector (div)", "B) Class selector (.container)", "C) ID selector (#header)", "D) Universal selector (*)"], "C) ID selector (#header)", "IDs have higher specificity than classes or elements.", "EASY"),
          ("What CSS property sets the background color of an element?", ["A) color", "B) background-color", "C) bg", "D) surface"], "B) background-color", "color sets text color; background-color sets element backdrop.", "EASY"),
          ("What is the difference between margin and padding?", ["A) Margin is space inside the border; padding is space outside", "B) Padding is space inside the border; margin is space outside the border", "C) They are identical", "D) Margin only applies to text"], "B) Padding is space inside the border; margin is space outside the border", "Padding cushions internal content; margin separates external siblings.", "EASY"),
          ("What does the CSS 'display: none;' property do?", ["A) Hides the element and removes it from the document layout flow entirely", "B) Makes the element transparent while keeping its layout space", "C) Reduces font size to 0", "D) Disables clicks only"], "A) Hides the element and removes it from the document layout flow entirely", "display: none removes the element from rendering flow entirely (unlike visibility: hidden).", "MEDIUM")]),
        ("05 — Responsive Design", "Media queries (@media), Flexbox (flex-direction, justify-content, align-items), CSS Grid, and viewport meta.",
         [("Flexbox Layout", "Main axis, cross axis, justify-content, and align-items.", "MEDIUM"), ("CSS Grid & Media Queries", "Grid templates and responsive breakpoints.", "MEDIUM")],
         "FILL_BLANK", "Media Query Syntax", "Fill in the CSS keyword to declare responsive breakpoints: @_____ (max-width: 768px) { ... }", "@_____ (max-width: 768px)", "media", "@media defines conditional CSS applied at specific viewport widths.", "EASY",
         [("What is the primary role of the viewport meta tag <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">?", ["A) Preload images", "B) Ensure mobile browsers match screen pixel width rather than simulating desktop viewport", "C) Encrypt cookies", "D) Enable WebGL"], "B) Ensure mobile browsers match screen pixel width rather than simulating desktop viewport", "Controls responsive layout scaling on mobile viewports.", "EASY"),
          ("In CSS Flexbox, what property aligns items along the MAIN axis?", ["A) align-items", "B) justify-content", "C) align-content", "D) flex-wrap"], "B) justify-content", "justify-content aligns items along the primary flex axis.", "EASY"),
          ("In CSS Flexbox, what property aligns items along the CROSS axis?", ["A) justify-content", "B) align-items", "C) flex-direction", "D) order"], "B) align-items", "align-items aligns perpendicular to the main axis.", "EASY"),
          ("What is the advantage of CSS Grid over Flexbox?", ["A) Grid is two-dimensional (simultaneous rows and columns); Flexbox is primarily one-dimensional", "B) Grid is faster", "C) Flexbox cannot be used on mobile", "D) Grid has no margin"], "A) Grid is two-dimensional (simultaneous rows and columns); Flexbox is primarily one-dimensional", "Grid excels at complex two-axis matrix layouts.", "MEDIUM"),
          ("What does a mobile-first design strategy advocate?", ["A) Writing desktop styles first then hiding items on mobile", "B) Designing and coding base styles for mobile screens first, then using min-width media queries to progressively enhance larger viewports", "C) Building native iOS apps only", "D) Removing all images"], "B) Designing and coding base styles for mobile screens first, then using min-width media queries to progressively enhance larger viewports", "Mobile-first builds upward from minimal screens.", "MEDIUM")]),
        ("06 — JavaScript Basics", "Variables (let, const), data types, functions (arrow functions), arrays, objects, and template literals.",
         [("Modern Variable Declarations", "Block scoping of let and const vs function-scoped var.", "EASY"), ("Arrow Functions & Template Literals", "() => syntax and `${expression}` interpolation.", "EASY")],
         "CODE_OUTPUT", "Template Literal Output", "What is the output of const name = 'Spectra'; console.log(`Hello, ${name}!`);?", "console.log(`Hello, ${name}!`);", "Hello, Spectra!", "Template literals evaluate ${name} inline.", "EASY",
         [("What is the difference between let and const in modern JavaScript?", ["A) let creates variables that can be reassigned; const creates block-scoped bindings that cannot be reassigned", "B) const is only for strings", "C) let is global; const is local", "D) No difference"], "A) let creates variables that can be reassigned; const creates block-scoped bindings that cannot be reassigned", "const prevents variable identifier reassignment.", "EASY"),
          ("What is the output of typeof null in JavaScript due to legacy reasons?", ["A) \"null\"", "B) \"object\"", "C) \"undefined\"", "D) \"boolean\""], "B) \"object\"", "Historical artifact from the first JavaScript implementation in 1995.", "MEDIUM"),
          ("What is the equality operator that checks both value AND data type without type coercion in JavaScript?", ["A) ==", "B) ===", "C) =", "D) !="], "B) ===", "Strict equality === avoids implicit type coercion.", "EASY"),
          ("What does an arrow function const add = (a, b) => a + b; return when invoked as add(2, 3)?", ["A) 5", "B) undefined", "C) NaN", "D) Error"], "A) 5", "Single-expression arrow functions implicitly return the computed value.", "EASY"),
          ("What does array.map() do in JavaScript?", ["A) Modifies the original array in place", "B) Returns a new array populated with the results of calling a provided function on every element", "C) Filters out odd numbers", "D) Sums all items"], "B) Returns a new array populated with the results of calling a provided function on every element", "map() returns an immutable transformed copy.", "EASY")]),
        ("07 — DOM Manipulation", "Selecting elements (querySelector), event listeners (addEventListener), classList, and dynamic DOM creation.",
         [("Selecting & Traversal", "querySelector, querySelectorAll, and parent/child nodes.", "EASY"), ("Event Handling", "Click events, event bubbling, and preventDefault().", "MEDIUM")],
         "FILL_BLANK", "Event Listener Method", "Fill in the method name to listen for user clicks: btn.________('click', handler);", "btn.________('click', handler)", "addEventListener", "addEventListener binds event callback functions to DOM elements.", "EASY",
         [("Which method selects the first element matching a CSS selector in the document?", ["A) document.getElement()", "B) document.querySelector()", "C) document.find()", "D) document.select()"], "B) document.querySelector()", "querySelector returns the first matching node.", "EASY"),
          ("What does event.preventDefault() accomplish in a form submission event handler?", ["A) Stops the browser from executing its default full-page reload submission behavior", "B) Clears all input values", "C) Closes the browser tab", "D) Disables CSS"], "A) Stops the browser from executing its default full-page reload submission behavior", "Prevents native action, allowing JavaScript AJAX/fetch handling.", "MEDIUM"),
          ("How do you add a CSS class 'active' to a DOM element 'el' in modern JavaScript?", ["A) el.addClass('active')", "B) el.classList.add('active')", "C) el.class += 'active'", "D) el.setAttribute('active', true)"], "B) el.classList.add('active')", "classList.add cleanly manages token lists.", "EASY"),
          ("What is event bubbling in the browser DOM event lifecycle?", ["A) Memory leaking", "B) Events propagating upward through the DOM ancestor hierarchy from the target element", "C) Events running in reverse", "D) Clicking multiple times"], "B) Events propagating upward through the DOM ancestor hierarchy from the target element", "Bubbling travels from the target node up to document/window.", "MEDIUM"),
          ("How do you dynamically create a new <div> element in JavaScript?", ["A) document.create('div')", "B) document.createElement('div')", "C) new HTMLElement('div')", "D) window.makeDiv()"], "B) document.createElement('div')", "createElement allocates a new DOM node in memory.", "EASY")]),
        ("08 — React Fundamentals", "JSX, component hierarchy, props, state (useState), lifecycle effects (useEffect), and unidirectional data flow.",
         [("Components & Props", "Reusable functional components and read-only props.", "MEDIUM"), ("State & Hooks", "useState for reactive rendering and useEffect for side effects.", "HARD")],
         "TRUE_FALSE", "React State Mutation", "True or False: In React, you should directly mutate state variables like 'state.count = 5' instead of calling the setState setter.", "Mutate state directly", False, "Direct state mutation bypasses React's virtual DOM reconciliation; always call setter functions like setCount(5).", "EASY",
         [("What is JSX in React development?", ["A) A new programming language replacing JavaScript", "B) A syntax extension to JavaScript that lets you write HTML-like markup inside component files", "C) A CSS preprocessor", "D) A database driver"], "B) A syntax extension to JavaScript that lets you write HTML-like markup inside component files", "JSX compiles to React.createElement calls.", "EASY"),
          ("What hook is used to declare and update local reactive state in a React functional component?", ["A) useEffect", "B) useState", "C) useContext", "D) useReducer"], "B) useState", "useState returns a [stateValue, setterFunction] pair.", "EASY"),
          ("What does passing an empty dependency array [] to useEffect accomplish?", ["A) Runs the effect on every single re-render", "B) Runs the effect once after the initial mount only", "C) Never runs the effect", "D) Causes an infinite loop"], "B) Runs the effect once after the initial mount only", "Empty dependencies mimic componentDidMount.", "MEDIUM"),
          ("Why must elements rendered from a list have a unique 'key' prop in React?", ["A) To apply CSS styles", "B) To help React identify which items have changed, been added, or removed during virtual DOM reconciliation", "C) To alphabetize items", "D) Required by browsers"], "B) To help React identify which items have changed, been added, or removed during virtual DOM reconciliation", "Keys stabilize virtual DOM diffing algorithms.", "MEDIUM"),
          ("Are React props mutable by the receiving child component?", ["A) Yes, child components can freely overwrite props", "B) No, props are read-only (immutable) inputs passed down from parent components", "C) Only in TypeScript", "D) Only if marked mutable"], "B) No, props are read-only (immutable) inputs passed down from parent components", "Unidirectional data flow guarantees parent ownership of state.", "EASY")]),
        ("09 — APIs and HTTP", "RESTful design principles, JSON, Fetch API, async/await, HTTP status codes, and CORS.",
         [("REST Architecture", "Resources, endpoints, and HTTP methods (GET, POST, PUT, DELETE).", "EASY"), ("Async JavaScript & Fetch", "Promises, async/await, and error handling.", "MEDIUM")],
         "CODE_OUTPUT", "HTTP Method for Deletion", "What standard HTTP method verb is used in RESTful APIs to delete a resource?", "DELETE", "DELETE", "HTTP DELETE removes resources identified by URI.", "EASY",
         [("What does the 'async/await' syntax simplify in JavaScript?", ["A) Working with asynchronous Promises in a clean synchronous-looking structure", "B) Making CSS load faster", "C) Compiling React components", "D) Encrypting databases"], "A) Working with asynchronous Promises in a clean synchronous-looking structure", "Syntactic sugar over Promise chaining.", "EASY"),
          ("What HTTP status code represents an unauthorized request due to missing or invalid authentication credentials?", ["A) 400 Bad Request", "B) 401 Unauthorized", "C) 404 Not Found", "D) 500 Server Error"], "B) 401 Unauthorized", "401 indicates authentication failure.", "EASY"),
          ("What is Cross-Origin Resource Sharing (CORS)?", ["A) A database replication mechanism", "B) A browser security mechanism that restricts HTTP requests made across different domains/origins", "C) A CSS framework", "D) A React hook"], "B) A browser security mechanism that restricts HTTP requests made across different domains/origins", "CORS controls cross-domain network permissions.", "MEDIUM"),
          ("What format is standard for exchanging structured payloads in modern REST APIs?", ["A) XML only", "B) JSON (JavaScript Object Notation)", "C) Binary bytes", "D) CSV"], "B) JSON (JavaScript Object Notation)", "JSON is the universal text data serialization format.", "EASY"),
          ("Which HTTP method is idempotent and completely replaces an existing resource with a new payload?", ["A) POST", "B) PUT", "C) PATCH", "D) CONNECT"], "B) PUT", "PUT replaces the resource entity; PATCH applies partial updates.", "MEDIUM")]),
        ("10 — Full Stack Web Architecture", "Full stack integration, backend APIs (FastAPI/Node), relational databases (PostgreSQL), JWT authentication, and cloud deployment.",
         [("Full Stack Layers", "Frontend client, backend API server, and persistent database.", "MEDIUM"), ("Authentication & Security", "JSON Web Tokens (JWT), hashed passwords (bcrypt), and TLS.", "HARD")],
         "TRUE_FALSE", "Plaintext Passwords", "True or False: In a secure production web application, user passwords should be hashed with a salted algorithm like bcrypt before saving to the database.", "Passwords must be salted and hashed", True, "Plaintext passwords must never be persisted; salted hashing protects against data breaches.", "EASY",
         [("What is the role of a JSON Web Token (JWT) in full-stack web authentication?", ["A) Encrypt the entire database", "B) A cryptographically signed token representing the user's identity passed in the Authorization header", "C) A stylesheet", "D) A backup file"], "B) A cryptographically signed token representing the user's identity passed in the Authorization header", "JWTs provide stateless bearer authentication.", "MEDIUM"),
          ("Why is separation of concerns maintained between Frontend and Backend in modern decoupled architectures?", ["A) Allows frontend and backend to scale, deploy, and evolve independently via standardized API contracts", "B) It is required by law", "C) To make servers hotter", "D) To prevent using databases"], "A) Allows frontend and backend to scale, deploy, and evolve independently via standardized API contracts", "Decoupling fosters modularity and team scalability.", "MEDIUM"),
          ("What does an ORM (Object-Relational Mapping, such as SQLAlchemy or Prisma) do?", ["A) Manages client-side CSS", "B) Translates database tables and relational records into object-oriented models in code", "C) Compiles JavaScript", "D) Serves static images"], "B) Translates database tables and relational records into object-oriented models in code", "ORMs abstract raw SQL operations into type-safe objects.", "MEDIUM"),
          ("What does the 'A' in the ACID database transaction properties guarantee?", ["A) Availability", "B) Atomicity (all sub-operations succeed, or the entire transaction rolls back)", "C) Asynchronous", "D) Accuracy"], "B) Atomicity (all sub-operations succeed, or the entire transaction rolls back)", "Atomicity is the all-or-nothing guarantee.", "EASY"),
          ("What is the purpose of environment variables (.env files) in full-stack applications?", ["A) Store sensitive secrets (API keys, database credentials) outside of version control", "B) Increase download speed", "C) Define HTML fonts", "D) Store user profiles"], "A) Store sensitive secrets (API keys, database credentials) outside of version control", "Keeps credentials isolated and secure across staging and production.", "EASY")])
    ]
    all_subjects.append(make_generic_subject("WEB", "Web Development", "Master HTTP, semantic HTML, CSS Box Model, responsive layout, JavaScript, React, APIs, and full-stack architecture.", "WEB_DEVELOPMENT", "BEGINNER", 8, web_lessons))

    return all_subjects


def seed_database_curriculum():
    create_tables()
    db = SessionLocal()

    try:
        print("[INFO] Starting comprehensive curriculum seeding for 8 active learning subjects...")
        subjects_data = build_all_subjects()

        # Keep track of counts
        total_seeded_subjects = 0
        total_seeded_lessons = 0
        total_seeded_puzzles = 0
        total_seeded_questions = 0

        for s_idx, sdata in enumerate(subjects_data):
            # Check subject by code or name
            subject = db.query(Subject).filter((Subject.code == sdata["code"]) | (Subject.name == sdata["name"])).first()
            if not subject:
                subject = Subject(
                    code=sdata["code"],
                    name=sdata["name"],
                    description=sdata["description"],
                    category=sdata.get("category", "COMPUTER_SCIENCE"),
                    difficulty_level=sdata.get("difficulty", "BEGINNER"),
                    display_order=sdata.get("order", s_idx + 1),
                    is_active=True
                )
                db.add(subject)
                db.flush()
                print(f"[+] Created Subject: {sdata['name']} ({sdata['code']})")
            else:
                subject.code = sdata["code"]
                subject.name = sdata["name"]
                subject.description = sdata["description"]
                subject.category = sdata.get("category", subject.category)
                subject.difficulty_level = sdata.get("difficulty", subject.difficulty_level)
                subject.display_order = sdata.get("order", s_idx + 1)
                subject.is_active = True
                db.flush()

            total_seeded_subjects += 1

            for ldata in sdata["lessons"]:
                l_order = ldata["order"]
                l_title = ldata["title"]

                lesson = db.query(Lesson).filter(
                    Lesson.subject_id == subject.id,
                    Lesson.lesson_order == l_order
                ).first()

                if not lesson:
                    # Also try title
                    lesson = db.query(Lesson).filter(
                        Lesson.subject_id == subject.id,
                        Lesson.title == l_title
                    ).first()

                content_md = f"# {l_title}\n\n## Overview\n{ldata['short_description']}\n\n## Key Learning Concepts\n"
                for t_name, t_desc, _ in ldata["topics"]:
                    content_md += f"### {t_name}\n{t_desc}\n\n"
                content_md += "## Interactive Reinforcement\nComplete the interactive challenge below, review verified resources, and take the mini quiz to achieve mastery!"

                if not lesson:
                    lesson = Lesson(
                        subject_id=subject.id,
                        title=l_title,
                        short_description=ldata["short_description"],
                        detailed_description=ldata["short_description"],
                        description=ldata["short_description"],
                        content=content_md,
                        difficulty=sdata.get("difficulty", "MEDIUM"),
                        difficulty_level=sdata.get("difficulty", "MEDIUM"),
                        estimated_minutes=15,
                        estimated_duration=15,
                        lesson_order=l_order,
                        display_order=l_order,
                        is_active=True
                    )
                    db.add(lesson)
                    db.flush()
                else:
                    lesson.title = l_title
                    lesson.short_description = ldata["short_description"]
                    lesson.detailed_description = ldata["short_description"]
                    lesson.description = ldata["short_description"]
                    lesson.content = content_md
                    lesson.lesson_order = l_order
                    lesson.display_order = l_order
                    lesson.is_active = True
                    db.flush()

                total_seeded_lessons += 1

                # 3. Seed Topics for this lesson
                primary_topic = None
                for t_idx, (t_name, t_desc, t_diff) in enumerate(ldata["topics"]):
                    topic = db.query(Topic).filter(
                        Topic.subject_id == subject.id,
                        Topic.name == t_name
                    ).first()

                    if not topic:
                        topic = Topic(
                            subject_id=subject.id,
                            lesson_id=lesson.id,
                            name=t_name,
                            description=t_desc,
                            difficulty_level=t_diff,
                            display_order=t_idx + 1,
                            is_active=True
                        )
                        db.add(topic)
                        db.flush()
                    else:
                        topic.lesson_id = lesson.id
                        topic.description = t_desc
                        topic.difficulty_level = t_diff
                        topic.display_order = t_idx + 1
                        topic.is_active = True
                        db.flush()

                    if t_idx == 0:
                        primary_topic = topic
                        lesson.topic_id = topic.id
                        db.flush()

                # 4. Seed Puzzle for this lesson
                p_def = ldata["puzzle"]
                p_data_str = json.dumps(p_def["puzzle_data"]) if not isinstance(p_def["puzzle_data"], str) else p_def["puzzle_data"]
                c_ans_str = json.dumps(p_def["correct_answer"]) if not isinstance(p_def["correct_answer"], str) else p_def["correct_answer"]

                puzzle = db.query(Puzzle).filter(
                    Puzzle.lesson_id == lesson.id,
                    Puzzle.title == p_def["title"]
                ).first()

                if not puzzle:
                    puzzle = Puzzle(
                        subject_id=subject.id,
                        lesson_id=lesson.id,
                        topic_id=primary_topic.id if primary_topic else None,
                        title=p_def["title"],
                        description=f"Challenge for {l_title}",
                        puzzle_type=p_def["type"],
                        question=p_def["question"],
                        puzzle_data=p_data_str,
                        correct_answer=c_ans_str,
                        explanation=p_def["explanation"],
                        difficulty=p_def.get("difficulty", "MEDIUM"),
                        xp_reward=10,
                        display_order=1,
                        is_active=True
                    )
                    db.add(puzzle)
                    db.flush()
                else:
                    puzzle.puzzle_type = p_def["type"]
                    puzzle.question = p_def["question"]
                    puzzle.puzzle_data = p_data_str
                    puzzle.correct_answer = c_ans_str
                    puzzle.explanation = p_def["explanation"]
                    puzzle.is_active = True
                    db.flush()

                total_seeded_puzzles += 1

                # 5. Seed Lesson Quiz
                quiz_title = f"{l_title} Quiz"
                quiz = db.query(Quiz).filter(
                    Quiz.lesson_id == lesson.id
                ).first()

                if not quiz:
                    quiz = Quiz(
                        subject_id=subject.id,
                        lesson_id=lesson.id,
                        topic_id=primary_topic.id if primary_topic else None,
                        title=quiz_title,
                        description=f"Diagnostic assessment covering core objectives in {l_title}.",
                        quiz_type="LESSON",
                        difficulty=sdata.get("difficulty", "MEDIUM"),
                        question_count=len(ldata["quiz"])
                    )
                    db.add(quiz)
                    db.flush()
                else:
                    quiz.title = quiz_title
                    quiz.quiz_type = "LESSON"
                    quiz.question_count = len(ldata["quiz"])
                    db.flush()

                # 6. Seed Quiz Questions
                for q_idx, (q_text, q_opts, q_corr, q_exp, q_diff) in enumerate(ldata["quiz"]):
                    q_obj = db.query(Question).filter(
                        Question.subject_id == subject.id,
                        Question.question_text == q_text
                    ).first()

                    opts_str = json.dumps(q_opts) if not isinstance(q_opts, str) else q_opts

                    if not q_obj:
                        q_obj = Question(
                            subject_id=subject.id,
                            topic_id=primary_topic.id if primary_topic else 1,
                            lesson_id=lesson.id,
                            question_text=q_text,
                            question_type="MCQ",
                            options=opts_str,
                            correct_answer=q_corr,
                            explanation=q_exp,
                            difficulty=q_diff
                        )
                        db.add(q_obj)
                        db.flush()
                    else:
                        q_obj.lesson_id = lesson.id
                        q_obj.options = opts_str
                        q_obj.correct_answer = q_corr
                        q_obj.explanation = q_exp
                        db.flush()

                    # Link to Quiz
                    assoc = db.query(QuizQuestion).filter(
                        QuizQuestion.quiz_id == quiz.id,
                        QuizQuestion.question_id == q_obj.id
                    ).first()
                    if not assoc:
                        assoc = QuizQuestion(
                            quiz_id=quiz.id,
                            question_id=q_obj.id,
                            order_index=q_idx + 1
                        )
                        db.add(assoc)
                        db.flush()

                    total_seeded_questions += 1

                # 7. Seed Resources
                for r_idx, (r_title, r_desc, r_url, r_type, r_provider) in enumerate(ldata.get("resources", [])):
                    res = db.query(StudyResource).filter(
                        StudyResource.lesson_id == lesson.id,
                        StudyResource.title == r_title
                    ).first()
                    if not res:
                        res = StudyResource(
                            lesson_id=lesson.id,
                            topic_id=primary_topic.id if primary_topic else None,
                            title=r_title,
                            description=r_desc,
                            url=r_url,
                            resource_type=r_type,
                            provider=r_provider,
                            display_order=r_idx + 1,
                            is_active=True
                        )
                        db.add(res)
                        db.flush()

        db.commit()
        print(f"[SUCCESS] Curriculum seeded: {total_seeded_subjects} subjects, {total_seeded_lessons} lessons, {total_seeded_puzzles} puzzles, {total_seeded_questions} questions.")

        # Ensure Demo Users & Enrollments
        admin_user = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin_user:
            admin_user = User(
                email="admin@example.com",
                name="System Administrator",
                role="ADMIN",
                password_hash=get_password_hash("admin123")
            )
            db.add(admin_user)
            db.flush()

        student_user = db.query(User).filter(User.email == "student@example.com").first()
        if not student_user:
            student_user = User(
                email="student@example.com",
                name="Alex Mercer",
                role="STUDENT",
                password_hash=get_password_hash("student123")
            )
            db.add(student_user)
            db.flush()

        student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == student_user.id).first()
        if not student_profile:
            student_profile = StudentProfile(
                user_id=student_user.id,
                student_id="STU-2026-0042",
                department="Computer Science & Engineering",
                semester=4,
                xp=185,
                current_streak=4,
                last_active_date=datetime.now(timezone.utc)
            )
            db.add(student_profile)
            db.flush()
        else:
            if not student_profile.xp or student_profile.xp == 0:
                student_profile.xp = 185
            if not student_profile.current_streak or student_profile.current_streak == 0:
                student_profile.current_streak = 4
            db.flush()

        # Enroll student in all subjects
        for s in db.query(Subject).all():
            enr = db.query(Enrollment).filter(
                Enrollment.student_id == student_profile.id,
                Enrollment.subject_id == s.id
            ).first()
            if not enr:
                enr = Enrollment(student_id=student_profile.id, subject_id=s.id)
                db.add(enr)
        db.flush()

        # Ensure demo progress for student
        first_java_lesson = db.query(Lesson).join(Subject).filter(Subject.code == "JAVA", Lesson.lesson_order == 1).first()
        if first_java_lesson:
            prog1 = db.query(LessonProgress).filter(
                LessonProgress.student_id == student_profile.id,
                LessonProgress.lesson_id == first_java_lesson.id
            ).first()
            if not prog1:
                prog1 = LessonProgress(
                    student_id=student_profile.id,
                    lesson_id=first_java_lesson.id,
                    status="COMPLETED",
                    completion_percentage=100.0,
                    topics_completed=3,
                    puzzles_completed=1,
                    quiz_completed=True,
                    quiz_score=90.0,
                    xp_earned=65,
                    completed_at=datetime.now(timezone.utc) - timedelta(days=2)
                )
                db.add(prog1)

        # In-progress lesson: Lesson 2 or 6
        java_lesson_curr = db.query(Lesson).join(Subject).filter(Subject.code == "JAVA", Lesson.lesson_order == 6).first()
        if java_lesson_curr:
            prog_curr = db.query(LessonProgress).filter(
                LessonProgress.student_id == student_profile.id,
                LessonProgress.lesson_id == java_lesson_curr.id
            ).first()
            if not prog_curr:
                prog_curr = LessonProgress(
                    student_id=student_profile.id,
                    lesson_id=java_lesson_curr.id,
                    status="IN_PROGRESS",
                    completion_percentage=65.0,
                    topics_completed=2,
                    puzzles_completed=1,
                    quiz_completed=False,
                    xp_earned=25
                )
                db.add(prog_curr)

        db.commit()
        print("[SUCCESS] All students enrolled and demo progress initialized.")

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Failed during curriculum seeding: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database_curriculum()
