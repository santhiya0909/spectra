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
from app.db.models.performance import StudentTopicPerformance
from app.db.models.recommendation import Recommendation, LearningPlan, LearningPlanItem
from app.db.models.user import StudentProfile, User
from app.services.enrollment import enroll_student_in_default_subjects

def seed_curriculum_data():
    create_tables()
    db = SessionLocal()

    try:
        print("[INFO] Starting curriculum seed for 5 default subjects...")

        # 1. Subjects definition
        subject_defs = [
            ("JAVA", "Java Programming", "Master Java syntax, OOP principles, memory models, collections, and robust exception handling.", "PROGRAMMING", "INTERMEDIATE", 1),
            ("PYTHON", "Python Programming", "Learn Python data structures, functional paradigms, OOP, lambdas, and algorithmic problem solving.", "PROGRAMMING", "BEGINNER", 2),
            ("DBMS", "Database Management Systems", "Learn SQL queries, relational schema design, normalization, ACID transactions, and query optimization.", "DATA_ENGINEERING", "INTERMEDIATE", 3),
            ("STAT", "Statistics", "Understand descriptive statistics, probability distributions, hypothesis testing, and regression analysis.", "MATHEMATICS", "BEGINNER", 4),
            ("ECO", "Economics", "Explore micro and macro economic principles, supply-demand equilibrium, market structures, and fiscal policy.", "BUSINESS", "BEGINNER", 5)
        ]

        subjects_by_code = {}
        for code, name, desc, cat, diff, order in subject_defs:
            s = db.query(Subject).filter(Subject.code == code).first()
            if not s:
                s = Subject(code=code, name=name, description=desc, category=cat, difficulty_level=diff, display_order=order, is_active=True)
                db.add(s)
                db.flush()
            else:
                s.name = name
                s.description = desc
                s.category = cat
                s.difficulty_level = diff
                s.display_order = order
                s.is_active = True
                db.flush()
            subjects_by_code[code] = s

        print(f"[INFO] 5 subjects confirmed in database with full metadata.")


        # 2. Topics per subject
        topics_data = {
            "JAVA": [
                ("Java Variables & Data Types", "Primitives, wrapper classes, stack vs heap allocation, and variable scope.", "EASY"),
                ("Java Functions & Parameters", "Method declarations, pass-by-value, return types, method overloading, and recursion.", "MEDIUM"),
                ("Java OOP & Inheritance", "Classes, inheritance, polymorphism, abstract classes, and interface contracts.", "HARD"),
                ("Java Arrays & Collections", "ArrayList, LinkedList, HashSet, HashMap, and the Collections framework.", "MEDIUM"),
                ("Java Exception Handling", "Checked vs unchecked exceptions, try-catch-finally, and custom exceptions.", "MEDIUM")
            ],
            "PYTHON": [
                ("Python Variables & Types", "Dynamic typing, string methods, numbers, and type casting in Python.", "EASY"),
                ("Python Functions & Lambda", "Positional and keyword arguments, default parameters, lambda expressions, and scope.", "MEDIUM"),
                ("Python Lists & Tuples", "List slicing, mutable vs immutable sequences, and list comprehensions.", "EASY"),
                ("Python Dictionaries & Sets", "Key-value hash maps, set operations, dictionary comprehensions, and hashing.", "MEDIUM"),
                ("Python OOP & Classes", "Classes, __init__, dunder methods, inheritance, and encapsulation.", "HARD")
            ],
            "DBMS": [
                ("Relational Model & SQL Queries", "Relational algebra, SELECT, WHERE, GROUP BY, HAVING, and SQL aggregate functions.", "EASY"),
                ("Database Normalization & Design", "Functional dependencies, 1NF, 2NF, 3NF, BCNF, and anomaly elimination.", "MEDIUM"),
                ("Transactions & ACID Properties", "Atomicity, Consistency, Isolation, Durability, concurrency anomalies, and locks.", "HARD"),
                ("Indexing & Query Optimization", "B+ Trees, clustered vs non-clustered indexes, and query execution plans.", "HARD")
            ],
            "STAT": [
                ("Descriptive Statistics & Probability", "Mean, median, mode, variance, standard deviation, and sample spaces.", "EASY"),
                ("Discrete & Continuous Distributions", "Binomial, Poisson, Uniform, and Normal distributions with Z-scores.", "MEDIUM"),
                ("Hypothesis Testing & P-Values", "Null hypothesis, Type I and II errors, Z-test, T-test, and critical regions.", "HARD"),
                ("Regression & Correlation", "Pearson correlation coefficient, linear regression, R-squared, and residual analysis.", "MEDIUM")
            ],
            "ECO": [
                ("Demand, Supply & Market Equilibrium", "Law of demand, law of supply, equilibrium price and quantity, and market shortages.", "EASY"),
                ("Elasticity & Consumer Choice", "Price elasticity of demand, income elasticity, consumer surplus, and producer surplus.", "MEDIUM"),
                ("Market Structures & Competition", "Perfect competition, monopoly, monopolistic competition, and oligopoly dynamics.", "HARD"),
                ("Macroeconomic Indicators: GDP & Inflation", "Nominal vs Real GDP, CPI, inflation rate, and unemployment rate.", "MEDIUM")
            ]
        }

        topics_by_name = {}
        for code, top_list in topics_data.items():
            subj = subjects_by_code[code]
            for t_name, t_desc, t_diff in top_list:
                t = db.query(Topic).filter(Topic.subject_id == subj.id, Topic.name == t_name).first()
                if not t:
                    t = Topic(subject_id=subj.id, name=t_name, description=t_desc, difficulty_level=t_diff)
                    db.add(t)
                    db.flush()
                topics_by_name[t_name] = t

        print(f"[INFO] Topics seeded across all subjects.")

        # 3. Lessons per topic
        lessons_data = [
            # JAVA
            (
                "JAVA", "Java Variables & Data Types",
                "Primitives vs Reference Types in Java",
                "Deep dive into primitive data types (int, double, boolean, char) versus heap-allocated reference types.",
                """# Primitives vs Reference Types in Java

In Java, data types are divided into two fundamental categories:

## 1. Primitive Types
Java defines 8 primitive types: `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`, and `char`.
- **Memory**: Allocated directly on the call stack.
- **Value**: Holds the actual literal value.
- **Default value**: Numeric types default to `0` or `0.0`, boolean to `false`.

```java
int count = 42;
double price = 19.99;
boolean isActive = true;
```

## 2. Reference Types
Reference types include classes, interfaces, and arrays.
- **Memory**: The variable stores a reference (memory address) on the stack pointing to an object residing in the Garbage-Collected Heap.
- **Default value**: `null`.

```java
String title = "Spectra Intelligent Learning";
int[] numbers = new int[]{1, 2, 3, 4, 5};
```

## Key Takeaway
When comparing primitives, `==` compares values. When comparing reference types, `==` compares memory addresses; use `.equals()` to compare logical values!""",
                "EASY", 12
            ),
            (
                "JAVA", "Java Functions & Parameters",
                "Functions Basics & Method Declarations",
                "Understand method syntax, return types, access modifiers, and static vs instance methods.",
                """# Functions Basics & Method Declarations in Java

Methods in Java are blocks of code that execute actions and optionally return computed results.

## Anatomy of a Method Declaration
```java
public static int calculateScore(int correctCount, int totalQuestions) {
    if (totalQuestions <= 0) return 0;
    return (int) Math.round((double) correctCount / totalQuestions * 100);
}
```

- **`public`**: Access modifier accessible anywhere.
- **`static`**: Belonging to the class rather than an instantiated object.
- **`int`**: Return type. If no value is returned, specify `void`.
- **Parameters**: `(int correctCount, int totalQuestions)`.

## Pass-by-Value Rule
Java is strictly **pass-by-value**:
- For primitive arguments, a copy of the primitive value is passed.
- For object references, a copy of the reference address is passed, meaning changes to the object's fields mutate the object, but reassigning the reference itself has no external effect.""",
                "MEDIUM", 15
            ),
            (
                "JAVA", "Java Functions & Parameters",
                "Method Overloading & Parameter Polymorphism",
                "Master method signatures, compile-time polymorphism through method overloading, and type promotion.",
                """# Method Overloading in Java

Method overloading enables a class to have multiple methods with the exact same name, as long as their parameter lists differ.

## Overloading Criteria
Two methods are distinct overloads if they differ in:
1. The number of parameters.
2. The data types of parameters.
3. The sequential order of parameter data types.

> **Important**: Changing ONLY the return type does NOT overload a method and causes a compiler error!

```java
public class Formatter {
    public static String format(int value) {
        return "Integer: " + value;
    }
    
    public static String format(double value) {
        return String.format("Currency: $%.2f", value);
    }
    
    public static String format(String text, boolean uppercase) {
        return uppercase ? text.toUpperCase() : text;
    }
}
```""",
                "MEDIUM", 15
            ),
            (
                "JAVA", "Java OOP & Inheritance",
                "Classes, Inheritance, and Polymorphism",
                "Understand object-oriented inheritance, the `extends` keyword, `super()`, and dynamic method dispatch.",
                """# Object-Oriented Inheritance in Java

Inheritance is an OOP mechanism that allows a subclass to inherit fields and methods from a superclass.

## Core Concepts
- Java uses single-class inheritance using the `extends` keyword.
- A subclass inherits all `public` and `protected` members.
- `super()` invokes the superclass constructor and must be the first line of the subclass constructor.
- `@Override` indicates overriding a method for runtime dynamic polymorphism.

```java
class User {
    protected String name;
    public User(String name) { this.name = name; }
    public void displayRole() { System.out.println("User: " + name); }
}

class Student extends User {
    private String studentId;
    public Student(String name, String id) {
        super(name);
        this.studentId = id;
    }
    @Override
    public void displayRole() {
        System.out.println("Student: " + name + " (" + studentId + ")");
    }
}
```""",
                "HARD", 20
            ),
            # PYTHON
            (
                "PYTHON", "Python Functions & Lambda",
                "Python Functions, Closures, and Higher-Order Functions",
                "First-class functions in Python, *args, **kwargs, lambda functions, and decorators.",
                """# Python Functions and Closures

In Python, functions are first-class citizens. You can pass them as arguments, return them from other functions, and assign them to variables.

```python
def multiply_by(factor):
    def multiplier(n):
        return n * factor
    return multiplier

double = multiply_by(2)
print(double(10))  # Output: 20
```

## Lambda Functions
Anonymous inline functions:
```python
square = lambda x: x ** 2
print(list(map(square, [1, 2, 3, 4])))  # [1, 4, 9, 16]
```""",
                "MEDIUM", 15
            ),
            # DBMS
            (
                "DBMS", "Relational Model & SQL Queries",
                "SQL Queries, Joins, and Grouping Operations",
                "Master INNER JOIN, LEFT JOIN, GROUP BY, HAVING, and subqueries in relational databases.",
                """# Mastering SQL Queries and Joins

Relational databases structure data in tables with primary and foreign keys.

```sql
SELECT 
    s.name AS subject_name,
    COUNT(t.id) AS topic_count,
    AVG(p.mastery_score) AS avg_mastery
FROM subjects s
LEFT JOIN topics t ON s.id = t.subject_id
LEFT JOIN student_topic_performance p ON t.id = p.topic_id
GROUP BY s.id, s.name
HAVING COUNT(t.id) > 0
ORDER BY avg_mastery DESC;
```""",
                "EASY", 18
            ),
            # STAT
            (
                "STAT", "Descriptive Statistics & Probability",
                "Measures of Central Tendency and Dispersion",
                "Mean, median, mode, variance, standard deviation, and boxplots for data distributions.",
                """# Measures of Central Tendency & Dispersion

Statistical analysis begins with summarizing data distributions.

- **Mean**: The arithmetic average $\\bar{x} = \\frac{\\sum x_i}{n}$. Sensitive to extreme outliers.
- **Median**: The middle value of sorted data. Robust against outliers.
- **Variance ($\\sigma^2$)**: The average of squared deviations from the mean.
- **Standard Deviation ($\\sigma$)**: The square root of variance, measuring dispersion in the original units.""",
                "EASY", 15
            ),
            # ECO
            (
                "ECO", "Demand, Supply & Market Equilibrium",
                "Law of Demand, Supply Shifts, and Equilibrium",
                "Price mechanisms, demand and supply curves, equilibrium pricing, and elasticity.",
                """# Supply, Demand, and Market Equilibrium

The price of a good in a competitive market is determined at the intersection of supply and demand curves.

- **Law of Demand**: All else being equal, as the price of a good increases, the quantity demanded decreases.
- **Law of Supply**: As the price of a good increases, suppliers are willing to produce more of that good.
- **Equilibrium**: The price point where quantity demanded equals quantity supplied ($Q_d = Q_s$).""",
                "EASY", 15
            )
        ]

        for idx, (s_code, t_name, l_title, l_desc, l_content, l_diff, l_mins) in enumerate(lessons_data):
            subj = subjects_by_code[s_code]
            top = topics_by_name.get(t_name)
            if not top:
                continue
            lesson = db.query(Lesson).filter(Lesson.title == l_title).first()
            if not lesson:
                lesson = Lesson(
                    subject_id=subj.id,
                    topic_id=top.id,
                    title=l_title,
                    short_description=l_desc,
                    detailed_description=l_content[:250] + "...",
                    description=l_desc,
                    content=l_content,
                    difficulty=l_diff,
                    difficulty_level=l_diff,
                    estimated_minutes=l_mins,
                    estimated_duration=l_mins,
                    lesson_order=idx + 1,
                    display_order=idx + 1,
                    is_active=True
                )
                db.add(lesson)
                db.flush()
            else:
                lesson.subject_id = subj.id
                lesson.topic_id = top.id
                lesson.short_description = l_desc
                lesson.detailed_description = l_content[:250] + "..."
                lesson.description = l_desc
                lesson.content = l_content
                lesson.difficulty = l_diff
                lesson.difficulty_level = l_diff
                lesson.estimated_minutes = l_mins
                lesson.estimated_duration = l_mins
                lesson.lesson_order = idx + 1
                lesson.display_order = idx + 1
                lesson.is_active = True
                db.flush()

            # Link primary topic to this lesson
            top.lesson_id = lesson.id
            top.display_order = 1
            top.is_active = True
            db.flush()

        print("[INFO] Lessons and topic hierarchy seeded.")

        # Seed Study Resources
        study_resources_data = {
            "Primitives vs Reference Types in Java": [
                ("Oracle Java Types Specification", "Official Java tutorial on primitive values, byte widths, and IEEE 754 precision.", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html", "DOCUMENTATION", "Oracle Java SE Documentation", 1),
                ("W3Schools Java Data Types Guide", "Interactive code runner explaining memory footprint and primitive casting.", "https://www.w3schools.com/java/java_data_types.asp", "TUTORIAL", "W3Schools", 2),
                ("GeeksforGeeks Primitive vs Reference", "Deep architectural comparison between stack allocation and garbage-collected heap objects.", "https://www.geeksforgeeks.org/data-types-in-java/", "ARTICLE", "GeeksforGeeks", 3),
            ],
            "Functions Basics & Method Declarations": [
                ("Oracle Java Methods Guide", "Defining methods, return value handling, access modifiers, and this keyword usage.", "https://docs.oracle.com/javase/tutorial/java/javaOO/methods.html", "DOCUMENTATION", "Oracle Java SE Documentation", 1),
                ("W3Schools Java Methods Interactive", "Hands-on exercises and syntax drills for methods and parameters.", "https://www.w3schools.com/java/java_methods.asp", "TUTORIAL", "W3Schools", 2),
                ("Baeldung: Java is Pass-by-Value", "Exhaustive pictorial explanation proving that Java always evaluates arguments by value.", "https://www.baeldung.com/java-pass-by-value-or-pass-by-reference", "ARTICLE", "Baeldung", 3),
            ],
            "Method Overloading & Parameter Polymorphism": [
                ("Oracle Java Method Overloading", "Method signatures, compile-time static dispatch, and type promotion hierarchies.", "https://docs.oracle.com/javase/tutorial/java/javaOO/methods.html", "DOCUMENTATION", "Oracle Java SE Documentation", 1),
                ("GeeksforGeeks Overloading in Java", "Examples of valid and invalid overloading signatures with primitive widening.", "https://www.geeksforgeeks.org/overloading-in-java/", "ARTICLE", "GeeksforGeeks", 2),
            ],
            "Classes, Inheritance, and Polymorphism": [
                ("Oracle Subclasses & Inheritance", "Extending superclasses, constructor chaining with super(), and method overriding.", "https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html", "DOCUMENTATION", "Oracle Java SE Documentation", 1),
                ("W3Schools Java OOP & Inheritance", "Clear object-oriented inheritance modeling with practical code examples.", "https://www.w3schools.com/java/java_inheritance.asp", "TUTORIAL", "W3Schools", 2),
                ("freeCodeCamp OOP Core Concepts", "Comprehensive guide on abstraction, encapsulation, inheritance, and polymorphism.", "https://www.freecodecamp.org/news/java-object-oriented-programming-system-principles-oops-concepts-for-beginners/", "ARTICLE", "freeCodeCamp", 3),
            ],
            "Python Functions, Closures, and Higher-Order Functions": [
                ("Python Official Docs: Defining Functions", "Official language tutorial covering positional, keyword arguments, and docstrings.", "https://docs.python.org/3/tutorial/controlflow.html#defining-functions", "DOCUMENTATION", "Python Software Foundation", 1),
                ("Real Python: Defining Functions", "In-depth guide exploring lexical scoping, closures, and first-class function patterns.", "https://realpython.com/defining-your-own-python-function/", "ARTICLE", "Real Python", 2),
                ("W3Schools Python Lambda Tutorial", "Quick-start guide to anonymous inline lambda functions and list filtering.", "https://www.w3schools.com/python/python_lambda.asp", "TUTORIAL", "W3Schools", 3),
            ],
            "SQL Queries, Joins, and Grouping Operations": [
                ("PostgreSQL Official Tutorial", "Standard relational database manual detailing table relations, SELECT, and GROUP BY.", "https://www.postgresql.org/docs/current/tutorial-sql.html", "DOCUMENTATION", "PostgreSQL Global Development Group", 1),
                ("W3Schools SQL Joins Visualizer", "Visual explanation and interactive sandbox for INNER, LEFT, RIGHT, and FULL joins.", "https://www.w3schools.com/sql/sql_join.asp", "TUTORIAL", "W3Schools", 2),
                ("SQLBolt Interactive Exercises", "Hands-on browser-based query challenges with instant grading and schema feedback.", "https://sqlbolt.com/", "PRACTICE", "SQLBolt", 3),
            ],
            "Measures of Central Tendency and Dispersion": [
                ("Khan Academy Descriptive Statistics", "Video lessons and exercises covering mean, median, mode, and standard deviation.", "https://www.khanacademy.org/math/statistics-probability/summarizing-quantitative-data", "TUTORIAL", "Khan Academy", 1),
                ("OpenStax Introductory Statistics", "Free peer-reviewed college textbook chapter explaining quantitative data distributions.", "https://openstax.org/books/introductory-statistics/pages/2-introduction", "DOCUMENTATION", "OpenStax", 2),
            ],
            "Law of Demand, Supply Shifts, and Equilibrium": [
                ("Khan Academy Microeconomics: Equilibrium", "Graphic derivations of market equilibrium, surplus, shortage, and price elasticities.", "https://www.khanacademy.org/economics-finance-domain/microeconomics/supply-demand-equilibrium", "TUTORIAL", "Khan Academy", 1),
                ("Investopedia Law of Supply and Demand", "Economic breakdown of market equilibrium with supply chain real-world case studies.", "https://www.investopedia.com/terms/l/law-of-supply-demand.asp", "ARTICLE", "Investopedia", 2),
            ],
        }

        for l_title, res_list in study_resources_data.items():
            lesson = db.query(Lesson).filter(Lesson.title == l_title).first()
            if not lesson:
                continue
            for r_title, r_desc, r_url, r_type, r_provider, r_order in res_list:
                existing_res = db.query(StudyResource).filter(StudyResource.lesson_id == lesson.id, StudyResource.title == r_title).first()
                if not existing_res:
                    res = StudyResource(
                        lesson_id=lesson.id,
                        topic_id=lesson.topic_id,
                        title=r_title,
                        description=r_desc,
                        url=r_url,
                        resource_type=r_type,
                        provider=r_provider,
                        display_order=r_order,
                        is_active=True
                    )
                    db.add(res)
                else:
                    existing_res.description = r_desc
                    existing_res.url = r_url
                    existing_res.resource_type = r_type
                    existing_res.provider = r_provider
                    existing_res.display_order = r_order
                    existing_res.is_active = True
            db.flush()

        print("[INFO] Verified external Study Resources seeded.")


        # 4. Quizzes (Quiz 1 MUST be Java Functions & Parameters Assessment)
        java_subj = subjects_by_code["JAVA"]
        java_func_topic = topics_by_name["Java Functions & Parameters"]
        java_oop_topic = topics_by_name["Java OOP & Inheritance"]

        quiz_1 = db.query(Quiz).filter(Quiz.id == 1).first()
        if not quiz_1:
            quiz_1 = Quiz(
                id=1,
                subject_id=java_subj.id,
                title="Java Functions & Parameters Assessment",
                description="Diagnose your understanding of method declarations, pass-by-value semantics, and overloading.",
                quiz_type="ADAPTIVE",
                difficulty="MEDIUM",
                question_count=5
            )
            db.add(quiz_1)
            db.flush()
        else:
            quiz_1.subject_id = java_subj.id
            quiz_1.title = "Java Functions & Parameters Assessment"
            quiz_1.quiz_type = "ADAPTIVE"
            db.flush()

        quiz_2 = db.query(Quiz).filter(Quiz.id == 2).first()
        if not quiz_2:
            quiz_2 = Quiz(
                id=2,
                subject_id=java_subj.id,
                title="Java OOP & Inheritance Diagnostic",
                description="Evaluate mastery of polymorphism, inheritance hierarchy, and interface design.",
                quiz_type="ADAPTIVE",
                difficulty="HARD",
                question_count=5
            )
            db.add(quiz_2)
            db.flush()

        # Quizzes for other subjects
        quizzes_other = [
            ("PYTHON", "Python Core & Functional Programming Quiz", "Test dynamic types, closures, and lambda functions in Python.", "MEDIUM", 5),
            ("DBMS", "DBMS Relational Model & SQL Quiz", "Evaluate SQL join queries, grouping, and transactional ACID guarantees.", "MEDIUM", 5),
            ("STAT", "Statistics & Probability Foundations Quiz", "Assess central tendency, standard deviation, and normal distribution.", "EASY", 5),
            ("ECO", "Economics Principles & Market Dynamics Quiz", "Test supply-demand equilibrium, price elasticity, and market structures.", "EASY", 5),
        ]

        for s_code, q_title, q_desc, q_diff, q_count in quizzes_other:
            s_obj = subjects_by_code[s_code]
            q_obj = db.query(Quiz).filter(Quiz.subject_id == s_obj.id, Quiz.title == q_title).first()
            if not q_obj:
                q_obj = Quiz(
                    subject_id=s_obj.id,
                    title=q_title,
                    description=q_desc,
                    quiz_type="ADAPTIVE",
                    difficulty=q_diff,
                    question_count=q_count
                )
                db.add(q_obj)
                db.flush()

        print("[INFO] Quizzes seeded.")

        # 5. Questions for Quiz 1 (Java Functions & Parameters)
        questions_java_funcs = [
            {
                "topic": "Java Functions & Parameters",
                "text": "What happens when a primitive `int` variable is passed into a Java method and modified inside that method?",
                "options": [
                    "A) The caller's variable remains unchanged because Java is strictly pass-by-value.",
                    "B) The caller's variable changes because primitives are passed by reference.",
                    "C) A compiler error occurs if an argument is modified.",
                    "D) The variable is automatically converted into an Integer object."
                ],
                "correct": "A) The caller's variable remains unchanged because Java is strictly pass-by-value.",
                "explanation": "In Java, all arguments are passed by value. When passing a primitive, a copy of the bit value is created on the method's stack frame. Modifying it does not affect the original caller's variable.",
                "difficulty": "EASY"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "Can two methods in the same Java class share the identical name and parameter list, but differ solely by their return type?",
                "options": [
                    "A) Yes, the compiler uses the return type to disambiguate calls.",
                    "B) No, the method signature consists only of the method name and parameter types; differing only by return type causes a compilation error.",
                    "C) Yes, but only if one of the return types is void.",
                    "D) Yes, if both methods are marked private."
                ],
                "correct": "B) No, the method signature consists only of the method name and parameter types; differing only by return type causes a compilation error.",
                "explanation": "A Java method signature comprises the method name and the types of its parameters in order. Return types are not part of the signature, so having identical parameters results in a duplicate method error.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What keyword must be specified in a Java method declaration when the method performs an action but returns no data to the caller?",
                "options": [
                    "A) null",
                    "B) empty",
                    "C) void",
                    "D) static"
                ],
                "correct": "C) void",
                "explanation": "The 'void' return type explicitly informs the Java compiler that the method does not yield a value upon termination.",
                "difficulty": "EASY"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "When passing an object reference to a Java method, what is actually copied and passed on the stack?",
                "options": [
                    "A) A deep clone of the entire object in heap memory.",
                    "B) The memory address (reference pointer) pointing to the object on the heap.",
                    "C) A string representation of the object's fields.",
                    "D) A synchronized copy of the object's class metadata."
                ],
                "correct": "B) The memory address (reference pointer) pointing to the object on the heap.",
                "explanation": "Because Java is pass-by-value, the 'value' passed for an object is the reference pointer itself. Both caller and method references refer to the same underlying heap object.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What runtime exception occurs if a recursive function in Java lacks a valid base termination condition?",
                "options": [
                    "A) OutOfMemoryError in Heap space",
                    "B) StackOverflowError",
                    "C) NullPointerException",
                    "D) ConcurrentModificationException"
                ],
                "correct": "B) StackOverflowError",
                "explanation": "Every recursive call allocates a new stack frame on the thread's call stack. Without a terminating base condition, the stack memory is exhausted, throwing java.lang.StackOverflowError.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "Which of the following is a valid example of compile-time method overloading in Java?",
                "options": [
                    "A) void process(int a) and int process(int a)",
                    "B) void process(int a, String b) and void process(String b, int a)",
                    "C) void process(int a) and public void process(int a)",
                    "D) void process(int x) and void process(int y)"
                ],
                "correct": "B) void process(int a, String b) and void process(String b, int a)",
                "explanation": "Altering the order of parameter types produces distinct method signatures, enabling the compiler to resolve the correct overloaded method call.",
                "difficulty": "HARD"
            }
        ]

        # Link questions to Quiz 1
        q_order = 1
        for q_item in questions_java_funcs:
            t_obj = topics_by_name[q_item["topic"]]
            existing_q = db.query(Question).filter(Question.question_text == q_item["text"]).first()
            if not existing_q:
                existing_q = Question(
                    subject_id=java_subj.id,
                    topic_id=t_obj.id,
                    question_text=q_item["text"],
                    question_type="MCQ",
                    options=json.dumps(q_item["options"]),
                    correct_answer=q_item["correct"],
                    explanation=q_item["explanation"],
                    difficulty=q_item["difficulty"]
                )
                db.add(existing_q)
                db.flush()

            # Associate with Quiz 1
            assoc = db.query(QuizQuestion).filter(
                QuizQuestion.quiz_id == quiz_1.id,
                QuizQuestion.question_id == existing_q.id
            ).first()
            if not assoc:
                assoc = QuizQuestion(
                    quiz_id=quiz_1.id,
                    question_id=existing_q.id,
                    order_index=q_order
                )
                db.add(assoc)
            q_order += 1

        print("[INFO] Questions linked to Quiz 1.")

        # 6. Questions for other subjects (Python, DBMS, Statistics, Economics)
        other_questions = [
            ("PYTHON", "Python Functions & Lambda", "What is the output of `(lambda x, y: x * y)(3, 4)` in Python?",
             ["A) 7", "B) 12", "C) SyntaxError", "D) None"], "B) 12",
             "A lambda expression creates an anonymous function. Passing 3 and 4 computes 3 * 4 = 12.", "EASY"),
            ("PYTHON", "Python Lists & Tuples", "Which characteristic distinguishes a Python tuple from a Python list?",
             ["A) Tuples allow duplicate values whereas lists do not.", "B) Tuples are immutable whereas lists are mutable.", "C) Lists cannot store strings.", "D) Tuples do not support indexing."],
             "B) Tuples are immutable whereas lists are mutable.", "Once constructed, elements in a tuple cannot be reassigned or deleted.", "EASY"),
            ("DBMS", "Relational Model & SQL Queries", "Which SQL clause is used to filter records AFTER an aggregation with GROUP BY has occurred?",
             ["A) WHERE", "B) HAVING", "C) ORDER BY", "D) LIMIT"], "B) HAVING",
             "WHERE filters individual rows prior to grouping, while HAVING filters aggregated group metrics.", "EASY"),
            ("DBMS", "Transactions & ACID Properties", "In the ACID transaction model, which property ensures that all sub-operations in a transaction succeed or all roll back?",
             ["A) Consistency", "B) Isolation", "C) Atomicity", "D) Durability"], "C) Atomicity",
             "Atomicity represents the 'all-or-nothing' principle of transactional units of work.", "MEDIUM"),
            ("STAT", "Descriptive Statistics & Probability", "Which measure of central tendency is least sensitive to extreme high or low outliers?",
             ["A) Mean", "B) Median", "C) Variance", "D) Standard Deviation"], "B) Median",
             "The median relies on ordinal rank rather than numeric magnitudes, making it highly robust against outliers.", "EASY"),
            ("ECO", "Demand, Supply & Market Equilibrium", "According to the Law of Demand, what happens when the market price of a normal good rises, ceteris paribus?",
             ["A) Quantity demanded increases.", "B) Quantity demanded decreases.", "C) Demand curve shifts to the right.", "D) Market equilibrium remains static."],
             "B) Quantity demanded decreases.", "Price and quantity demanded exhibit an inverse relationship under standard market conditions.", "EASY")
        ]

        for s_code, t_name, q_text, q_opts, q_corr, q_exp, q_diff in other_questions:
            s_obj = subjects_by_code[s_code]
            t_obj = topics_by_name.get(t_name)
            if not t_obj:
                continue
            ex_q = db.query(Question).filter(Question.question_text == q_text).first()
            if not ex_q:
                ex_q = Question(
                    subject_id=s_obj.id,
                    topic_id=t_obj.id,
                    question_text=q_text,
                    question_type="MCQ",
                    options=json.dumps(q_opts),
                    correct_answer=q_corr,
                    explanation=q_exp,
                    difficulty=q_diff
                )
                db.add(ex_q)
                db.flush()

        db.commit()
        # 7. Ensure default ADMIN and STUDENT exist
        from app.core.security import get_password_hash
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
            print("[INFO] Created default admin user admin@example.com")
        elif admin_user.role != "ADMIN":
            admin_user.role = "ADMIN"
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
            stu_profile = StudentProfile(
                user_id=student_user.id,
                student_id="STU-2026-0042",
                department="Computer Science & Engineering",
                semester=4
            )
            db.add(stu_profile)
            db.flush()
            print("[INFO] Created default student user student@example.com")


        # 8. Auto-enroll all student profiles in all 5 subjects
        students = db.query(StudentProfile).all()
        for student in students:
            enroll_student_in_default_subjects(db, student.id)
            print(f"[INFO] Student {student.id} (user {student.user_id}) enrolled in default subjects.")


        # 8. Seed baseline diagnostics for Student Profiles so Dashboard, Analytics, and Recommendations are active
        for student in students:
            # Check if student has topic performance
            perf_cnt = db.query(StudentTopicPerformance).filter(StudentTopicPerformance.student_id == student.id).count()
            if perf_cnt == 0:
                # Add Strong area in Java Variables (88% mastery)
                p_strong = StudentTopicPerformance(
                    student_id=student.id,
                    topic_id=topics_by_name["Java Variables & Data Types"].id,
                    attempts=2,
                    correct_answers=9,
                    total_questions=10,
                    accuracy=90.0,
                    mastery_score=88.0,
                    last_attempt_at=datetime.now(timezone.utc) - timedelta(days=2)
                )
                db.add(p_strong)

                # Add Weak area in Java Functions (38% mastery)
                p_weak = StudentTopicPerformance(
                    student_id=student.id,
                    topic_id=topics_by_name["Java Functions & Parameters"].id,
                    attempts=3,
                    correct_answers=6,
                    total_questions=15,
                    accuracy=40.0,
                    mastery_score=38.0,
                    last_attempt_at=datetime.now(timezone.utc) - timedelta(hours=4)
                )
                db.add(p_weak)
                db.flush()

                # Add a completed lesson
                l_prog = LessonProgress(
                    student_id=student.id,
                    lesson_id=1,
                    status="COMPLETED",
                    completion_percentage=100.0,
                    completed_at=datetime.now(timezone.utc) - timedelta(days=1)
                )
                db.add(l_prog)

                # Add active recommendation for the weak topic
                rec = Recommendation(
                    student_id=student.id,
                    topic_id=topics_by_name["Java Functions & Parameters"].id,
                    recommendation_type="CONCEPT_REVISION",
                    title="Targeted Practice: Java Functions & Parameters",
                    reason="Your mastery score in Java Functions & Parameters is 38.0%. Review the core lesson and complete practice questions to eliminate knowledge gaps.",
                    priority="HIGH",
                    resource_id=2,  # Lesson 2
                    status="ACTIVE"
                )
                db.add(rec)
                db.flush()

                # Add adaptive learning plan
                plan = LearningPlan(
                    student_id=student.id,
                    title="Personalized Adaptive Learning Path",
                    active=True
                )
                db.add(plan)
                db.flush()

                db.add(LearningPlanItem(
                    learning_plan_id=plan.id,
                    resource_type="LESSON",
                    resource_id=2,
                    order_index=1,
                    completed=False
                ))
                db.add(LearningPlanItem(
                    learning_plan_id=plan.id,
                    resource_type="QUIZ",
                    resource_id=1,
                    order_index=2,
                    completed=False
                ))

                # Add a past quiz attempt for history analytics
                attempt = QuizAttempt(
                    student_id=student.id,
                    quiz_id=1,
                    score=2.0,
                    percentage=40.0,
                    started_at=datetime.now(timezone.utc) - timedelta(days=2),
                    completed_at=datetime.now(timezone.utc) - timedelta(days=2) + timedelta(minutes=5)
                )
                db.add(attempt)
                db.flush()

                print(f"[INFO] Initialized baseline diagnostic data for student {student.id}")

        db.commit()
        print("[SUCCESS] Curriculum seeding completed successfully!")

    finally:
        db.close()

if __name__ == "__main__":
    seed_curriculum_data()
