import sys
import os
import json
from datetime import datetime, timedelta, timezone

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import SessionLocal, create_tables
from app.core.security import get_password_hash
from app.db.models.user import User, StudentProfile, TeacherProfile, AuditLog
from app.db.models.academic import Subject, Topic, Enrollment, Lesson, LessonProgress
from app.db.models.quiz import Question, Quiz, QuizQuestion, QuizAttempt, QuizResponse
from app.db.models.performance import StudentTopicPerformance
from app.db.models.recommendation import Recommendation, LearningPlan, LearningPlanItem
from app.db.models.teacher import TeacherAlert
from app.db.models.puzzle import Puzzle

def seed_database():
    print("=" * 60)
    print("SPECTRA – Initializing Realistic Database Seed Data")
    print("=" * 60)

    create_tables()
    db = SessionLocal()

    try:
        # Check if already seeded
        existing_user = db.query(User).filter(User.email == "student@example.com").first()
        if existing_user:
            print("[INFO] Database already contains seed users. Refreshing demo relationships...")
            # We can return or continue. Let's make sure it's fully populated.

        # 1. SEED USERS
        users_data = [
            {
                "email": "student@example.com",
                "name": "Alex Mercer",
                "role": "STUDENT",
                "password": "student123",  # Demo credentials
                "student_id": "STU-2026-0042",
                "dept": "Computer Science & Engineering",
                "semester": 4
            },
            {
                "email": "teacher@example.com",
                "name": "Dr. Sarah Jenkins",
                "role": "TEACHER",
                "password": "teacher123",  # Demo credentials
                "employee_id": "TCH-CS-101",
                "dept": "Computer Science & Engineering"
            },
            {
                "email": "admin@example.com",
                "name": "System Administrator",
                "role": "ADMIN",
                "password": "admin123",  # Demo credentials
            }
        ]

        created_users = {}
        for udata in users_data:
            user = db.query(User).filter(User.email == udata["email"]).first()
            if not user:
                user = User(
                    email=udata["email"],
                    name=udata["name"],
                    role=udata["role"],
                    password_hash=get_password_hash(udata["password"])
                )
                db.add(user)
                db.flush()

                if udata["role"] == "STUDENT":
                    profile = StudentProfile(
                        user_id=user.id,
                        student_id=udata["student_id"],
                        department=udata["dept"],
                        semester=udata["semester"],
                        academic_year="2025-2026",
                        learning_preferences="Interactive code exercises, visual debugging, practice quizzes"
                    )
                    db.add(profile)
                elif udata["role"] == "TEACHER":
                    profile = TeacherProfile(
                        user_id=user.id,
                        employee_id=udata["employee_id"],
                        department=udata["dept"]
                    )
                    db.add(profile)

            created_users[udata["role"]] = user

        db.commit()
        student_user = created_users["STUDENT"]
        student_profile = db.query(StudentProfile).filter(StudentProfile.user_id == student_user.id).first()

        # 2. SEED SUBJECTS & TOPICS
        curriculum = [
            {
                "name": "Java Programming",
                "code": "CS-201",
                "description": "Master object-oriented programming, standard libraries, robust memory models, and exception control in Java.",
                "topics": [
                    {"name": "Java Variables & Data Types", "difficulty": "EASY", "desc": "Primitives, reference types, scope, and memory storage."},
                    {"name": "Java Functions & Parameters", "difficulty": "MEDIUM", "desc": "Method signatures, pass-by-value, return values, overloading, and recursion."},
                    {"name": "Java OOP & Inheritance", "difficulty": "HARD", "desc": "Classes, polymorphism, encapsulation, abstraction, and interfaces."},
                    {"name": "Java Arrays & Collections", "difficulty": "MEDIUM", "desc": "Single & multi-dimensional arrays, ArrayList, and Map interfaces."},
                    {"name": "Java Exception Handling", "difficulty": "MEDIUM", "desc": "Try-catch-finally, checked vs unchecked exceptions, custom exceptions."}
                ]
            },
            {
                "name": "Python Programming",
                "code": "CS-102",
                "description": "Modern Python concepts, data structures, functional paradigms, and algorithm design.",
                "topics": [
                    {"name": "Python Variables & Types", "difficulty": "EASY", "desc": "Dynamic typing, strings, numeric operations."},
                    {"name": "Python Functions & Lambda", "difficulty": "MEDIUM", "desc": "Arguments, keyword arguments, scope, higher-order functions."},
                    {"name": "Python Lists & Tuples", "difficulty": "EASY", "desc": "List comprehensions, slicing, immutability."},
                    {"name": "Python Dictionaries & Sets", "difficulty": "MEDIUM", "desc": "Hash tables, key-value mappings, set operations."},
                    {"name": "Python OOP", "difficulty": "HARD", "desc": "Classes, dunder methods, inheritance, composition."}
                ]
            },
            {
                "name": "Mathematics for Computing",
                "code": "MATH-201",
                "description": "Discrete mathematics, linear algebra, calculus, and probability underpinning computer science.",
                "topics": [
                    {"name": "Linear Algebra", "difficulty": "MEDIUM", "desc": "Matrices, vectors, determinants, transformations."},
                    {"name": "Fractions & Number Theory", "difficulty": "EASY", "desc": "Divisibility, modular arithmetic, prime numbers."},
                    {"name": "Probability & Statistics", "difficulty": "MEDIUM", "desc": "Random variables, Bayes theorem, distributions."},
                    {"name": "Differential Calculus", "difficulty": "HARD", "desc": "Limits, derivatives, optimization, rates of change."}
                ]
            },
            {
                "name": "Engineering Chemistry",
                "code": "CHEM-101",
                "description": "Atomic structure, chemical bonding, materials science, and thermodynamic systems.",
                "topics": [
                    {"name": "Atomic Structure", "difficulty": "EASY", "desc": "Bohr model, quantum numbers, electron configurations."},
                    {"name": "Chemical Bonding", "difficulty": "MEDIUM", "desc": "Covalent, ionic, metallic bonds, molecular geometry."},
                    {"name": "Thermodynamics", "difficulty": "HARD", "desc": "Enthalpy, entropy, Gibbs free energy, equilibrium."}
                ]
            }
        ]

        topic_dict = {}
        for subj_data in curriculum:
            subj = db.query(Subject).filter(
                (Subject.code == subj_data["code"]) | (Subject.name == subj_data["name"])
            ).first()
            if not subj:
                subj = Subject(name=subj_data["name"], code=subj_data["code"], description=subj_data["description"])
                db.add(subj)
                db.flush()

            # Enroll student in subject
            existing_enrollment = db.query(Enrollment).filter(
                Enrollment.student_id == student_profile.id,
                Enrollment.subject_id == subj.id
            ).first()
            if not existing_enrollment:
                db.add(Enrollment(student_id=student_profile.id, subject_id=subj.id))

            for top_data in subj_data["topics"]:
                top = db.query(Topic).filter(Topic.subject_id == subj.id, Topic.name == top_data["name"]).first()
                if not top:
                    top = Topic(
                        subject_id=subj.id,
                        name=top_data["name"],
                        description=top_data["desc"],
                        difficulty_level=top_data["difficulty"]
                    )
                    db.add(top)
                    db.flush()
                topic_dict[top.name] = (subj, top)

        db.commit()

        # 3. SEED LESSONS
        lessons_data = [
            # Java Functions
            {
                "subject": "Java Programming",
                "topic": "Java Functions & Parameters",
                "title": "Functions Basics & Method Declarations",
                "description": "Understand method headers, return types, parameter lists, and pass-by-value in Java.",
                "difficulty": "EASY",
                "minutes": 15,
                "content": """# Java Functions & Method Declarations

In Java, every function is declared as a method inside a class. 

### Method Anatomy
```java
public static int calculateAverage(int num1, int num2) {
    int sum = num1 + num2;
    return sum / 2;
}
```

### Core Rules:
1. **Pass-by-Value**: Java is **always** pass-by-value. When passing primitive variables, a copy of the actual bits is passed into the parameter.
2. **Return Type**: The method must return a value matching the declared type unless declared as `void`.
3. **Scope**: Local variables defined within a function are destroyed when execution returns to the caller.

### Common Pitfalls:
- Forgetting to return a value in non-void branches.
- Attempting to reassign an argument expecting the caller's variable to change.
"""
            },
            {
                "subject": "Java Programming",
                "topic": "Java Functions & Parameters",
                "title": "Method Overloading & Parameter Polymorphism",
                "description": "How the Java compiler distinguishes methods with the same name via different signatures.",
                "difficulty": "MEDIUM",
                "minutes": 20,
                "content": """# Method Overloading in Java

Method overloading occurs when two or more methods in the same class have the **same name** but **different parameter lists**.

### Criteria for Overloading:
- Different number of parameters
- Different types of parameters
- Different order of parameter types

```java
public class Calculator {
    public int multiply(int a, int b) {
        return a * b;
    }
    
    public double multiply(double a, double b) {
        return a * b;
    }
}
```

> **Important**: Changing *only* the return type does **NOT** overload a method and produces a compiler error!
"""
            },
            # Java Variables
            {
                "subject": "Java Programming",
                "topic": "Java Variables & Data Types",
                "title": "Primitives vs Reference Types in Java",
                "description": "Deep dive into stack vs heap allocation, primitive types, and object references.",
                "difficulty": "EASY",
                "minutes": 12,
                "content": """# Primitives vs Reference Types

Java divides data types into two primary categories:
1. **Primitives**: `byte`, `short`, `int`, `long`, `float`, `double`, `boolean`, `char`. Allocated directly on the call stack.
2. **References**: Arrays, Strings, Objects. The reference variable sits on the stack, pointing to memory in the heap.
"""
            },
            # Python Functions
            {
                "subject": "Python Programming",
                "topic": "Python Functions & Lambda",
                "title": "Python First-Class Functions and Closures",
                "description": "Functional programming paradigms in Python: *args, **kwargs, and lambda expressions.",
                "difficulty": "MEDIUM",
                "minutes": 18,
                "content": """# First-Class Functions in Python

In Python, functions are first-class citizens. You can pass them as arguments, return them from other functions, and assign them to variables.
"""
            }
        ]

        created_lessons = {}
        for ldata in lessons_data:
            subj, top = topic_dict[ldata["topic"]]
            lesson = db.query(Lesson).filter(Lesson.topic_id == top.id, Lesson.title == ldata["title"]).first()
            if not lesson:
                lesson = Lesson(
                    subject_id=subj.id,
                    topic_id=top.id,
                    title=ldata["title"],
                    description=ldata["description"],
                    difficulty=ldata["difficulty"],
                    estimated_minutes=ldata["minutes"],
                    content=ldata["content"]
                )
                db.add(lesson)
                db.flush()
            created_lessons[ldata["title"]] = lesson

        # Mark Java Variables lesson as completed for the student
        var_lesson = created_lessons.get("Primitives vs Reference Types in Java")
        if var_lesson:
            lp = db.query(LessonProgress).filter(
                LessonProgress.student_id == student_profile.id,
                LessonProgress.lesson_id == var_lesson.id
            ).first()
            if not lp:
                db.add(LessonProgress(
                    student_id=student_profile.id,
                    lesson_id=var_lesson.id,
                    status="COMPLETED",
                    completion_percentage=100.0,
                    completed_at=datetime.now(timezone.utc) - timedelta(days=2)
                ))

        db.commit()

        # 4. SEED QUESTIONS (With rich options and clear correct answers)
        questions_data = [
            # Java Functions (10 questions for diagnostic / practice)
            {
                "topic": "Java Functions & Parameters",
                "text": "What happens when an `int` primitive is passed into a Java method and modified inside that method?",
                "options": [
                    "A) The caller's variable is also modified",
                    "B) The caller's variable remains unchanged because Java is pass-by-value",
                    "C) A NullPointerException is thrown",
                    "D) The code will fail to compile"
                ],
                "correct": "B) The caller's variable remains unchanged because Java is pass-by-value",
                "explanation": "Java always passes arguments by value. For primitives, a copy of the actual value is provided; modifying it inside the method body has zero impact on the caller's variable.",
                "difficulty": "EASY"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "Can two methods in the same Java class differ solely by their return type?",
                "options": [
                    "A) Yes, the compiler distinguishes them by return type at call site",
                    "B) No, method overloading requires different parameter counts or parameter types",
                    "C) Only if both methods are marked `static`",
                    "D) Only if both methods are marked `private`"
                ],
                "correct": "B) No, method overloading requires different parameter counts or parameter types",
                "explanation": "Return type is not part of the method signature for overloading. Having identical names and parameter lists with different return types causes a compile-time collision error.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What keyword is required when a method should not return any data to the caller?",
                "options": [
                    "A) null",
                    "B) empty",
                    "C) void",
                    "D) static"
                ],
                "correct": "C) void",
                "explanation": "The `void` keyword explicitly declares that the method does not yield any return value.",
                "difficulty": "EASY"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What is the result of executing a recursive method that lacks an adequate base case condition?",
                "options": [
                    "A) OutOfMemoryError in heap storage",
                    "B) StackOverflowError due to infinite call frames",
                    "C) Memory leak without process termination",
                    "D) Program pauses indefinitely without error"
                ],
                "correct": "B) StackOverflowError due to infinite call frames",
                "explanation": "Each recursive call allocates a stack frame. Without a termination base case, the thread's call stack exhausts its limit, raising a `java.lang.StackOverflowError`.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "When passing an object reference to a method in Java, what is copied into the parameter?",
                "options": [
                    "A) The entire object heap memory is cloned",
                    "B) The memory address (reference value) pointing to the object",
                    "C) A read-only snapshot of the object properties",
                    "D) Nothing, references are always passed by reference"
                ],
                "correct": "B) The memory address (reference value) pointing to the object",
                "explanation": "Java passes the reference value (the address pointer) by value. Both caller and callee reference the exact same object in the heap.",
                "difficulty": "HARD"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "Which modifier allows a method to be invoked without creating an instance of the class?",
                "options": [
                    "A) public",
                    "B) final",
                    "C) static",
                    "D) abstract"
                ],
                "correct": "C) static",
                "explanation": "`static` methods belong to the class itself rather than any individual object instance.",
                "difficulty": "EASY"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What is the variable-length argument (varargs) syntax in Java method parameters?",
                "options": [
                    "A) Type[]... name",
                    "B) Type... name",
                    "C) varargs Type name",
                    "D) *name"
                ],
                "correct": "B) Type... name",
                "explanation": "Java uses the ellipsis syntax `Type... name` to declare varargs, which is treated internally as an array.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What must be the position of a variable-length argument (varargs) in a method signature?",
                "options": [
                    "A) As the first parameter",
                    "B) It can appear in any position",
                    "C) As the last parameter in the parameter list",
                    "D) It cannot be combined with other parameters"
                ],
                "correct": "C) As the last parameter in the parameter list",
                "explanation": "A method can have only one varargs parameter, and it must be the final parameter so the compiler can unambiguously bind preceding arguments.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "Which of the following statements about Java constructor methods is TRUE?",
                "options": [
                    "A) Constructors must declare `void` as their return type",
                    "B) Constructors cannot accept parameters",
                    "C) Constructors have no return type and share the exact class name",
                    "D) Constructors can be declared `abstract`"
                ],
                "correct": "C) Constructors have no return type and share the exact class name",
                "explanation": "Constructors initialize objects, do not specify any return type (not even void), and must exactly match the class identifier.",
                "difficulty": "MEDIUM"
            },
            {
                "topic": "Java Functions & Parameters",
                "text": "What happens if a non-void method fails to execute a `return` statement along an execution branch?",
                "options": [
                    "A) The method returns 0 or null automatically",
                    "B) A compile-time error: 'missing return statement'",
                    "C) A runtime NullPointerException is raised",
                    "D) Execution loops back to the top of the method"
                ],
                "correct": "B) A compile-time error: 'missing return statement'",
                "explanation": "Java requires that all possible execution paths through a non-void method return an expression compatible with the declared return type.",
                "difficulty": "HARD"
            },
            # Java Variables Questions
            {
                "topic": "Java Variables & Data Types",
                "text": "What is the default initial value of an uninitialized `int` instance variable in Java?",
                "options": [
                    "A) null",
                    "B) 0",
                    "C) Garbage value",
                    "D) -1"
                ],
                "correct": "B) 0",
                "explanation": "Instance field variables of numeric primitive types are default-initialized to 0 by the Java runtime.",
                "difficulty": "EASY"
            },
            {
                "topic": "Java Variables & Data Types",
                "text": "What is the size of a `boolean` data type in Java as specified by the JVM specification?",
                "options": [
                    "A) Exactly 1 bit",
                    "B) Exactly 1 byte",
                    "C) The JVM specification does not define an exact size; it is virtual machine dependent",
                    "D) 4 bytes"
                ],
                "correct": "C) The JVM specification does not define an exact size; it is virtual machine dependent",
                "explanation": "The JVM specification defines boolean representations conceptually, typically implemented as 1 byte or 4-byte integers in stack operations.",
                "difficulty": "HARD"
            }
        ]

        created_questions = []
        for qdata in questions_data:
            subj, top = topic_dict[qdata["topic"]]
            existing_q = db.query(Question).filter(
                Question.topic_id == top.id,
                Question.question_text == qdata["text"]
            ).first()
            if not existing_q:
                q = Question(
                    subject_id=subj.id,
                    topic_id=top.id,
                    question_text=qdata["text"],
                    question_type="MCQ",
                    options=json.dumps(qdata["options"]),
                    correct_answer=qdata["correct"],
                    explanation=qdata["explanation"],
                    difficulty=qdata["difficulty"]
                )
                db.add(q)
                db.flush()
                created_questions.append(q)
            else:
                created_questions.append(existing_q)

        db.commit()

        # 5. SEED QUIZZES
        java_subj = db.query(Subject).filter(Subject.name == "Java Programming").first()
        java_functions_topic = db.query(Topic).filter(Topic.name == "Java Functions & Parameters").first()

        quiz = db.query(Quiz).filter(Quiz.title == "Java Functions & Parameters Assessment").first()
        if not quiz:
            quiz = Quiz(
                subject_id=java_subj.id,
                title="Java Functions & Parameters Assessment",
                description="Comprehensive evaluation of Java method syntax, parameter passing, return semantics, and recursion.",
                quiz_type="TOPIC_ASSESSMENT",
                difficulty="MEDIUM",
                question_count=10
            )
            db.add(quiz)
            db.flush()

            # Attach the 10 Java Functions questions
            func_questions = db.query(Question).filter(Question.topic_id == java_functions_topic.id).all()
            for idx, fq in enumerate(func_questions[:10]):
                db.add(QuizQuestion(quiz_id=quiz.id, question_id=fq.id, order_index=idx + 1))

        # Adaptive Practice Quiz
        adaptive_quiz = db.query(Quiz).filter(Quiz.title == "Java Adaptive Diagnostic").first()
        if not adaptive_quiz:
            adaptive_quiz = Quiz(
                subject_id=java_subj.id,
                title="Java Adaptive Diagnostic",
                description="Dynamically adjusts question difficulty according to your mastery level in real time.",
                quiz_type="ADAPTIVE",
                difficulty="MEDIUM",
                question_count=5
            )
            db.add(adaptive_quiz)
            db.flush()

        db.commit()

        # 6. SEED NATURAL BASELINE DEMO DATA
        # As required by Phase 26 & 27:
        # Establish an initial state where the student took a prior diagnostic and scored ~52% in Java Functions
        # This naturally triggers WEAK TOPIC: Java Functions, and produces targeted recommendations.
        func_questions = db.query(Question).filter(Question.topic_id == java_functions_topic.id).all()
        existing_attempt = db.query(QuizAttempt).filter(
            QuizAttempt.student_id == student_profile.id,
            QuizAttempt.quiz_id == quiz.id
        ).first()

        if not existing_attempt and len(func_questions) >= 10:
            # Create baseline attempt with 5 out of 10 or 5.2/10 -> 52.0%
            started = datetime.now(timezone.utc) - timedelta(days=1, hours=3)
            completed = started + timedelta(minutes=7, seconds=45)

            attempt = QuizAttempt(
                student_id=student_profile.id,
                quiz_id=quiz.id,
                score=5.2,
                percentage=52.0,
                started_at=started,
                completed_at=completed
            )
            db.add(attempt)
            db.flush()

            # Create individual responses (5 correct, 5 incorrect with realistic mistakes)
            for idx, fq in enumerate(func_questions[:10]):
                is_correct = idx in [0, 2, 5, 6, 8]  # 5 correct out of 10
                opts = json.loads(fq.options)
                selected = fq.correct_answer if is_correct else opts[0] if opts[0] != fq.correct_answer else opts[1]
                
                resp = QuizResponse(
                    attempt_id=attempt.id,
                    question_id=fq.id,
                    selected_answer=selected,
                    is_correct=is_correct,
                    time_taken=42
                )
                db.add(resp)

            # Establish initial Topic Performance at 52.0%
            perf = StudentTopicPerformance(
                student_id=student_profile.id,
                topic_id=java_functions_topic.id,
                attempts=1,
                correct_answers=5,
                total_questions=10,
                accuracy=52.0,
                mastery_score=52.0,
                last_attempt_at=completed
            )
            db.add(perf)

            # High mastery on Variables to demonstrate contrast (e.g. 85%)
            java_var_topic = db.query(Topic).filter(Topic.name == "Java Variables & Data Types").first()
            if java_var_topic:
                var_perf = StudentTopicPerformance(
                    student_id=student_profile.id,
                    topic_id=java_var_topic.id,
                    attempts=2,
                    correct_answers=9,
                    total_questions=10,
                    accuracy=90.0,
                    mastery_score=86.0,
                    last_attempt_at=started - timedelta(days=1)
                )
                db.add(var_perf)

            # Generate natural baseline recommendation
            fn_lesson = created_lessons.get("Functions Basics & Method Declarations")
            rec = Recommendation(
                student_id=student_profile.id,
                topic_id=java_functions_topic.id,
                recommendation_type="CONCEPT_REVISION",
                title="Targeted Revision & 10 Practice Questions: Java Functions & Parameters",
                reason="Your accuracy in Java Functions is 52.0%. You are making repeated mistakes in function parameters. Review the Functions Basics lesson and complete 10 targeted questions before retaking the quiz.",
                priority="HIGH",
                resource_id=fn_lesson.id if fn_lesson else None,
                status="ACTIVE",
                created_at=completed
            )
            db.add(rec)

            # Build initial Learning Plan
            plan = LearningPlan(
                student_id=student_profile.id,
                title="Personalized Adaptive Learning Path",
                active=True,
                generated_at=completed
            )
            db.add(plan)
            db.flush()

            if fn_lesson:
                db.add(LearningPlanItem(
                    learning_plan_id=plan.id,
                    resource_type="LESSON",
                    resource_id=fn_lesson.id,
                    order_index=1,
                    completed=False
                ))

            db.add(LearningPlanItem(
                learning_plan_id=plan.id,
                resource_type="QUIZ",
                resource_id=quiz.id,
                order_index=2,
                completed=False
            ))

            # Teacher Alert
            db.add(TeacherAlert(
                student_id=student_profile.id,
                topic_id=java_functions_topic.id,
                alert_type="LOW_PERFORMANCE",
                severity="MEDIUM",
                message=f"Student {student_user.name} scored 52.0% in Java Functions. System assigned targeted parameter revision.",
                status="ACTIVE",
                created_at=completed
            ))

            db.commit()

        # Guarantee all lessons have at least 1 puzzle and quiz
        for l in db.query(Lesson).all():
            has_p = db.query(Puzzle).filter(Puzzle.lesson_id == l.id).first()
            if not has_p:
                db.add(Puzzle(
                    subject_id=l.subject_id,
                    lesson_id=l.id,
                    topic_id=l.topic_id,
                    title=f"Knowledge Check: {l.title}",
                    description="Interactive concept verification.",
                    puzzle_type="MULTIPLE_CHOICE",
                    question=f"Which concept is essential to {l.title}?",
                    puzzle_data=json.dumps(["Understanding core fundamentals", "Ignoring errors", "Skipping documentation", "Guessing values"]),
                    correct_answer="Understanding core fundamentals",
                    explanation="Mastering core fundamentals ensures robust application architecture.",
                    difficulty=l.difficulty or "EASY",
                    xp_reward=10
                ))
            has_q = db.query(Quiz).filter(Quiz.lesson_id == l.id).first()
            if not has_q:
                qz = Quiz(
                    subject_id=l.subject_id,
                    lesson_id=l.id,
                    topic_id=l.topic_id,
                    title=f"Lesson Quiz: {l.title}",
                    description="Quiz testing lesson mastery.",
                    quiz_type="CONCEPTUAL",
                    difficulty=l.difficulty or "MEDIUM",
                    question_count=5
                )
                db.add(qz)
                db.flush()
                for qi in range(5):
                    q_obj = Question(
                        subject_id=l.subject_id,
                        topic_id=l.topic_id,
                        lesson_id=l.id,
                        question_text=f"Question {qi+1} on {l.title}: What is a key principle?",
                        options=json.dumps(["A) Precision and correctness", "B) Ignoring edge cases", "C) Arbitrary execution", "D) None of these"]),
                        correct_answer="A) Precision and correctness",
                        explanation="Precision and correctness are critical.",
                        difficulty=l.difficulty or "EASY"
                    )
                    db.add(q_obj)
                    db.flush()
                    db.add(QuizQuestion(quiz_id=qz.id, question_id=q_obj.id, order_index=qi + 1))
        db.commit()

        print("[SUCCESS] Database seeding complete!")
        print("  - Student Login: student@example.com (Password: student123)")
        print("  - Teacher Login: teacher@example.com (Password: teacher123)")
        print("  - Admin Login:   admin@example.com   (Password: admin123)")
        print("  - Initial Diagnostic: Java Functions = 52.0% (Natural baseline ready)")
        print("=" * 60)

    except Exception as e:
        db.rollback()
        print(f"[ERROR] Database seeding failed: {e}")
        import traceback
        traceback.print_exc()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
