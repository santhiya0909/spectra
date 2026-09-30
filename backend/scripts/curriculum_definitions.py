"""
SPECTRA Curriculum Definitions
Comprehensive definitions for all 8 required subjects:
1. Java Programming (JAVA) - 10 Lessons
2. Python Programming (PYTHON) - 10 Lessons
3. Mathematics (MATH) - 10 Lessons
4. Chemistry (CHEM) - 10 Lessons
5. Artificial Intelligence (AI) - 10 Lessons
6. Data Structures (DSA) - 10 Lessons
7. Machine Learning (ML) - 10 Lessons
8. Web Development (WEB) - 10 Lessons

Each lesson contains:
- title, short_description, detailed_description, content, difficulty, estimated_minutes
- topics: list of (name, desc, difficulty)
- puzzle: (type, title, question, puzzle_data, correct_answer, explanation, difficulty)
- quiz: list of 5 (question_text, options, correct_answer, explanation, difficulty)
- resources: list of (title, desc, url, type, provider)
"""

SUBJECTS_DATA = [
    {
        "code": "JAVA",
        "name": "Java Programming",
        "description": "Master Java architecture, object-oriented programming, data structures, and robust exception handling.",
        "category": "PROGRAMMING",
        "difficulty": "INTERMEDIATE",
        "order": 1,
        "lessons": [
            {
                "order": 1,
                "title": "01 — Introduction to Java",
                "short_description": "Understand Java overview, JVM bytecode execution, JDK vs JRE, and write your first program.",
                "topics": [
                    ("Java Overview", "History, platform independence (WORA), and core language design goals.", "EASY"),
                    ("JVM, JDK and JRE", "Role of the Java Virtual Machine, runtime environment, and compiler tools.", "MEDIUM"),
                    ("First Java Program", "Class structure, public static void main method syntax, and compilation flow.", "EASY")
                ],
                "puzzle": {
                    "type": "ORDERING",
                    "title": "Java Compilation & Execution Pipeline",
                    "question": "Arrange the steps of the Java execution lifecycle in the correct sequential order:",
                    "puzzle_data": ["JVM JIT executes native machine code", "Write source code in .java file", "Bytecode loaded into memory by ClassLoader", "javac compiles source into .class bytecode"],
                    "correct_answer": ["Write source code in .java file", "javac compiles source into .class bytecode", "Bytecode loaded into memory by ClassLoader", "JVM JIT executes native machine code"],
                    "explanation": "Java programs are written as .java source files, compiled by javac into portable .class bytecode, loaded by the ClassLoader, and executed by the JVM."
                },
                "quiz": [
                    ("Which component of Java is responsible for converting bytecode into machine-specific instructions?",
                     ["A) javac compiler", "B) Java Virtual Machine (JVM)", "C) Java Development Kit (JDK)", "D) Java Archive (JAR)"],
                     "B) Java Virtual Machine (JVM)", "The JVM interprets and compiles bytecode into native machine instructions at runtime.", "EASY"),
                    ("What is the primary function of the javac command?",
                     ["A) Executes compiled Java code", "B) Packages classes into a JAR", "C) Compiles .java source code into .class bytecode", "D) Manages memory allocation"],
                     "C) Compiles .java source code into .class bytecode", "javac is the primary Java compiler that produces platform-independent bytecode.", "EASY"),
                    ("What does the 'WORA' acronym stand for in Java's architectural design?",
                     ["A) Write Once, Run Anywhere", "B) Write Objects, Read Arrays", "C) Windows Oriented Runtime Architecture", "D) Wide Open Resource Access"],
                     "A) Write Once, Run Anywhere", "WORA reflects Java's platform neutrality made possible by the JVM.", "EASY"),
                    ("Which signature correctly defines the application entry point in Java?",
                     ["A) public void main(String args)", "B) public static void main(String[] args)", "C) static void main()", "D) public int main(String[] args)"],
                     "B) public static void main(String[] args)", "The standard JVM entry point requires public static void main(String[] args).", "EASY"),
                    ("What is the relationship between JDK and JRE?",
                     ["A) JRE contains JDK and all developer compilers", "B) JDK includes JRE plus developer tools like javac and jdb", "C) JDK and JRE are completely identical", "D) JRE is used exclusively for mobile development"],
                     "B) JDK includes JRE plus developer tools like javac and jdb", "The JDK is a superset of the JRE, providing debugging and compilation tools.", "MEDIUM")
                ],
                "resources": [
                    ("Oracle Java Getting Started", "Official tutorial for compiling and running your first Java console application.", "https://docs.oracle.com/javase/tutorial/getStarted/", "DOCUMENTATION", "Oracle"),
                    ("W3Schools Java Introduction", "Interactive code runner explaining JVM, JRE, and the main method.", "https://www.w3schools.com/java/java_intro.asp", "TUTORIAL", "W3Schools")
                ]
            },
            {
                "order": 2,
                "title": "02 — Variables and Data Types",
                "short_description": "Explore primitive types, memory allocation, explicit/implicit type casting, and final constants.",
                "topics": [
                    ("Variables & Declaration", "Declaring, initializing, and scoping identifiers in Java.", "EASY"),
                    ("Primitive Types", "The 8 primitive types: byte, short, int, long, float, double, boolean, char.", "EASY"),
                    ("Type Casting & Constants", "Widening vs narrowing casting and the final keyword.", "MEDIUM")
                ],
                "puzzle": {
                    "type": "MULTIPLE_CHOICE",
                    "title": "Valid Java Identifier Challenge",
                    "question": "Which of the following is a syntactically legal variable identifier in Java?",
                    "puzzle_data": ["int 2totalScore = 100;", "double final = 4.5;", "int _studentCount = 28;", "float score-val = 90.0f;"],
                    "correct_answer": "int _studentCount = 28;",
                    "explanation": "Java identifiers cannot start with digits, cannot contain hyphens, and cannot use reserved keywords like final. An underscore prefix is completely valid."
                },
                "quiz": [
                    ("Which of the following is NOT a primitive data type in Java?",
                     ["A) int", "B) boolean", "C) String", "D) char"],
                     "C) String", "String in Java is a reference class type residing in java.lang, not a primitive.", "EASY"),
                    ("How many bytes of memory does an int primitive occupy in standard Java?",
                     ["A) 2 bytes", "B) 4 bytes", "C) 8 bytes", "D) 16 bytes"],
                     "B) 4 bytes", "An int in Java is a signed 32-bit (4-byte) two's complement integer.", "EASY"),
                    ("What happens during a narrowing primitive conversion (e.g. double to int) without explicit casting?",
                     ["A) Automatic promotion occurs", "B) The compiler reports a Type Mismatch compilation error", "C) The fractional value is rounded up", "D) It compiles with a warning"],
                     "B) The compiler reports a Type Mismatch compilation error", "Narrowing conversions can cause loss of precision and require explicit casting syntax like (int) val.", "MEDIUM"),
                    ("Which keyword is used in Java to declare an immutable variable (constant)?",
                     ["A) const", "B) static", "C) final", "D) immutable"],
                     "C) final", "The final keyword prevents reassigning a variable after its initial assignment.", "EASY"),
                    ("What is the default value of an uninitialized boolean instance variable in a class?",
                     ["A) true", "B) false", "C) null", "D) 0"],
                     "B) false", "Primitive boolean instance variables default to false in Java class fields.", "EASY")
                ],
                "resources": [
                    ("Oracle Primitive Data Types Guide", "Exhaustive specification of byte widths and literal ranges for all 8 primitives.", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/datatypes.html", "DOCUMENTATION", "Oracle")
                ]
            },
            {
                "order": 3,
                "title": "03 — Operators and Expressions",
                "short_description": "Master arithmetic, relational, boolean logical operators, short-circuit evaluation, and assignment shorthand.",
                "topics": [
                    ("Arithmetic Operators", "Addition, subtraction, modulus, and prefix/postfix increment.", "EASY"),
                    ("Comparison Operators", "Relational evaluations (==, !=, <, >, <=, >=).", "EASY"),
                    ("Logical & Bitwise Operators", "Short-circuit &&, ||, and negation !.", "MEDIUM")
                ],
                "puzzle": {
                    "type": "CODE_OUTPUT",
                    "title": "Arithmetic Evaluation Puzzle",
                    "question": "What is the exact output of this Java code snippet?\n\nint x = 5;\nint y = 2;\nSystem.out.println(x + y);",
                    "puzzle_data": "int x = 5;\nint y = 2;\nSystem.out.println(x + y);",
                    "correct_answer": "7",
                    "explanation": "x + y computes standard integer addition of 5 + 2 = 7."
                },
                "quiz": [
                    ("What is the result of the expression 17 % 5 in Java?",
                     ["A) 3", "B) 2", "C) 3.4", "D) 1"],
                     "B) 2", "The modulus operator (%) yields the remainder of integer division: 17 divided by 5 is 3 with a remainder of 2.", "EASY"),
                    ("How does short-circuit evaluation work with the logical AND (&&) operator?",
                     ["A) Both operands are always evaluated", "B) If the first operand evaluates to false, the second is skipped", "C) If the first operand evaluates to true, the second is skipped", "D) Evaluation occurs in reverse order"],
                     "B) If the first operand evaluates to false, the second is skipped", "&& stops evaluating as soon as the first operand is false because the entire expression cannot be true.", "MEDIUM"),
                    ("What is the difference between ++x (prefix) and x++ (postfix)?",
                     ["A) Prefix increments after the value is used; postfix increments before", "B) Prefix increments before the value is used; postfix increments after", "C) Prefix only works on floats", "D) There is no difference"],
                     "B) Prefix increments before the value is used; postfix increments after", "Prefix returns the incremented value immediately; postfix yields the prior value then increments.", "MEDIUM"),
                    ("What is the output of System.out.println(10 == 10.0); in Java?",
                     ["A) true", "B) false", "C) Compilation Error", "D) Runtime Exception"],
                     "A) true", "The integer 10 is widened to 10.0 before comparison, producing true.", "MEDIUM"),
                    ("Which assignment shorthand is equivalent to count = count * 2;?",
                     ["A) count =* 2;", "B) count *= 2;", "C) count ** 2;", "D) count += *2;"],
                     "B) count *= 2;", "The compound assignment operator is *=.", "EASY")
                ],
                "resources": [
                    ("Oracle Java Operators Specification", "Complete precedence table and behavior of arithmetic, relational, and bitwise operators.", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/operators.html", "DOCUMENTATION", "Oracle")
                ]
            },
            {
                "order": 4,
                "title": "04 — Conditional Statements",
                "short_description": "Control execution flow using if-else branching, switch statements, and ternary operators.",
                "topics": [
                    ("If-Else Branching", "Boolean condition evaluation and nested control structures.", "EASY"),
                    ("Switch Statements", "Multi-branch switching with cases, default, and switch expressions.", "MEDIUM"),
                    ("Ternary Operator", "Compact conditional assignment expressions.", "EASY")
                ],
                "puzzle": {
                    "type": "FILL_BLANK",
                    "title": "Switch Termination Challenge",
                    "question": "Fill in the missing keyword to prevent fall-through in this switch case:\n\nswitch(grade) {\n    case 'A':\n        System.out.println(\"Excellent\");\n        ______;\n    default:\n        System.out.println(\"Good\");\n}",
                    "puzzle_data": "switch(grade) { case 'A': System.out.println(\"Excellent\"); ______; default: ... }",
                    "correct_answer": "break",
                    "explanation": "The break keyword terminates the switch statement and prevents execution from falling through into subsequent cases."
                },
                "quiz": [
                    ("What happens if a switch case block does not contain a break statement in classic Java?",
                     ["A) The code will not compile", "B) Execution falls through into the next case statement", "C) The program terminates immediately", "D) An exception is thrown at runtime"],
                     "B) Execution falls through into the next case statement", "Without break, execution continues sequentially into the subsequent case block regardless of condition.", "MEDIUM"),
                    ("Which data types are valid switch expression variables in Java?",
                     ["A) byte, short, char, int, String, and enum", "B) float, double, and long only", "C) boolean and double only", "D) Any reference object"],
                     "A) byte, short, char, int, String, and enum", "Switch supports primitives (except long, float, double), their wrapper types, String, and enums.", "MEDIUM"),
                    ("What is the result of String status = (score >= 60) ? \"Pass\" : \"Fail\"; when score = 75?",
                     ["A) \"Pass\"", "B) \"Fail\"", "C) null", "D) Compilation error"],
                     "A) \"Pass\"", "Since 75 >= 60 evaluates to true, the ternary returns the first operand \"Pass\".", "EASY"),
                    ("When will the default block in a switch statement execute?",
                     ["A) It always executes before every case", "B) When none of the explicit case values match the switch variable", "C) Only when an exception is thrown", "D) Exactly twice per execution"],
                     "B) When none of the explicit case values match the switch variable", "The default case acts as a fallback when no case match is found.", "EASY"),
                    ("Can an if condition evaluate an integer value directly in Java (e.g. if (1))?",
                     ["A) Yes, 1 evaluates to true", "B) No, Java strictly requires a boolean expression in if statements", "C) Yes, if configured in compiler settings", "D) Yes, if using wrapper Integer"],
                     "B) No, Java strictly requires a boolean expression in if statements", "Unlike C/C++, Java does not treat non-zero integers as truthy values; condition must be boolean.", "MEDIUM")
                ],
                "resources": [
                    ("Oracle Control Flow Statements", "Branching logic, if-then-else hierarchies, and modern switch statements.", "https://docs.oracle.com/javase/tutorial/java/nutsandbolts/flow.html", "DOCUMENTATION", "Oracle")
                ]
            },
            {
                "order": 5,
                "title": "05 — Loops",
                "short_description": "Iterate systematically with for, while, do-while loops, and understand loop control with break and continue.",
                "topics": [
                    ("For Loops", "Indexed iteration, initialization, termination condition, and increment step.", "EASY"),
                    ("While & Do-While", "Pre-condition versus post-condition iteration loops.", "MEDIUM"),
                    ("Break & Continue", "Early termination and skipping iterations in nested loops.", "MEDIUM")
                ],
                "puzzle": {
                    "type": "FILL_BLANK",
                    "title": "Loop Termination Condition",
                    "question": "Fill in the blank operator so the loop prints numbers from 0 to 4 inclusive:\n\nfor (int i = 0; i ___ 5; i++) {\n    System.out.println(i);\n}",
                    "puzzle_data": "for (int i = 0; i ___ 5; i++)",
                    "correct_answer": "<",
                    "explanation": "i < 5 ensures i takes values 0, 1, 2, 3, and 4 before terminating when i reaches 5."
                },
                "quiz": [
                    ("What is the primary difference between a while loop and a do-while loop?",
                     ["A) A while loop always executes at least once", "B) A do-while loop always executes its body at least once", "C) A while loop cannot use break", "D) A do-while loop is only used for arrays"],
                     "B) A do-while loop always executes its body at least once", "The condition in a do-while loop is checked after executing the block, guaranteeing at least one run.", "EASY"),
                    ("What is the effect of the continue statement inside a loop body?",
                     ["A) Terminates the entire loop immediately", "B) Skips the rest of the current iteration and jumps to the next iteration step", "C) Re-initializes loop variables", "D) Exits the enclosing method"],
                     "B) Skips the rest of the current iteration and jumps to the next iteration step", "continue halts the current cycle and proceeds with condition evaluation / increment for the next.", "MEDIUM"),
                    ("How many times will this loop execute: for (int i = 10; i > 0; i -= 2)?",
                     ["A) 5 times", "B) 10 times", "C) 4 times", "D) Infinite loop"],
                     "A) 5 times", "i takes values 10, 8, 6, 4, 2 (5 iterations) before i = 0 terminates the loop.", "EASY"),
                    ("What happens when a loop has no termination condition, such as for(;;)?",
                     ["A) Compilation error", "B) Runs an infinite loop until terminated externally or via break", "C) Executes once and stops", "D) Automatically runs 100 times"],
                     "B) Runs an infinite loop until terminated externally or via break", "for(;;) is valid Java syntax declaring an intentional infinite loop.", "MEDIUM"),
                    ("Which loop structure is preferred when the number of iterations is known before entering the loop?",
                     ["A) do-while loop", "B) standard for loop", "C) recursion only", "D) switch block"],
                     "B) standard for loop", "A for loop cleanly encapsulates initialization, boundary checking, and step updating.", "EASY")
                ],
                "resources": [
                    ("W3Schools Java For Loop", "Hands-on exercises and syntax drills for for, while, and nested loops.", "https://www.w3schools.com/java/java_for_loop.asp", "TUTORIAL", "W3Schools")
                ]
            },
            {
                "order": 6,
                "title": "06 — Functions and Methods",
                "short_description": "Define reusable methods, understand pass-by-value argument semantics, return types, and method overloading.",
                "topics": [
                    ("Method Declaration", "Access modifiers, static vs instance, return types, and signatures.", "MEDIUM"),
                    ("Parameters & Return Values", "Pass-by-value evaluation rules for primitives versus object references.", "MEDIUM"),
                    ("Method Overloading", "Compile-time polymorphism using unique parameter lists.", "MEDIUM")
                ],
                "puzzle": {
                    "type": "ORDERING",
                    "title": "Method Call Execution Lifecycle",
                    "question": "Arrange the phases of calling and executing a Java method in order:",
                    "puzzle_data": ["Method call invoked by caller", "Method declaration in class definition", "Caller receives returned result", "Method executes internal statements", "Arguments pushed to stack frame"],
                    "correct_answer": ["Method declaration in class definition", "Method call invoked by caller", "Arguments pushed to stack frame", "Method executes internal statements", "Caller receives returned result"],
                    "explanation": "Methods are declared first, invoked by callers, arguments pushed onto call stack frames, instructions executed, and results returned to the caller."
                },
                "quiz": [
                    ("How does Java pass parameters to methods?",
                     ["A) Strictly pass-by-reference", "B) Strictly pass-by-value", "C) Pass-by-name", "D) Pass-by-reference for primitives and value for objects"],
                     "B) Strictly pass-by-value", "Java always evaluates arguments by value. For objects, a copy of the reference address is passed by value.", "HARD"),
                    ("Which criteria distinguishes two overloaded methods in the same class?",
                     ["A) Different return types with identical parameter lists", "B) Different parameter counts, types, or sequences", "C) Different access modifiers with identical parameters", "D) Different parameter variable names"],
                     "B) Different parameter counts, types, or sequences", "Method overloading requires different parameter types, numbers, or order. Changing only return type causes a compiler error.", "MEDIUM"),
                    ("What return type must be declared if a method does not produce any return value?",
                     ["A) null", "B) empty", "C) void", "D) boolean"],
                     "C) void", "void signifies that the method executes side-effects without returning a value.", "EASY"),
                    ("Can a static method directly access non-static instance variables of its class without an object instance?",
                     ["A) Yes, static methods inherit all instance fields", "B) No, because static methods exist independently of any specific object instance", "C) Yes, if marked public", "D) Only in the main method"],
                     "B) No, because static methods exist independently of any specific object instance", "Static context belongs to the class and has no implicit 'this' reference to instance state.", "MEDIUM"),
                    ("What is a recursive method in Java?",
                     ["A) A method that overrides a superclass method", "B) A method that calls itself with a base terminating condition", "C) A method with multiple return statements", "D) A method that cannot take parameters"],
                     "B) A method that calls itself with a base terminating condition", "Recursion involves a function invoking itself to solve progressively smaller subproblems.", "MEDIUM")
                ],
                "resources": [
                    ("Baeldung: Java Pass-by-Value", "In-depth visual proof demonstrating Java's pass-by-value mechanics with primitives and references.", "https://www.baeldung.com/java-pass-by-value-or-pass-by-reference", "ARTICLE", "Baeldung")
                ]
            },
            {
                "order": 7,
                "title": "07 — Arrays",
                "short_description": "Allocate, traverse, and manipulate one-dimensional and multidimensional arrays with index safety.",
                "topics": [
                    ("One-dimensional Arrays", "Fixed-size contiguous memory allocation and zero-based indexing.", "EASY"),
                    ("Multidimensional Arrays", "Arrays of arrays, matrix representation, and jagged arrays.", "MEDIUM"),
                    ("Array Traversal & Manipulation", "Iterating with standard for, enhanced for-each, and Arrays utility methods.", "MEDIUM")
                ],
                "puzzle": {
                    "type": "CODE_OUTPUT",
                    "title": "Array Indexing Challenge",
                    "question": "What is the printed output of the following Java snippet?\n\nint[] arr = {10, 20, 30, 40};\nSystem.out.println(arr[1]);",
                    "puzzle_data": "int[] arr = {10, 20, 30, 40};\nSystem.out.println(arr[1]);",
                    "correct_answer": "20",
                    "explanation": "Java arrays use zero-based indexing. arr[0] is 10, so arr[1] is 20."
                },
                "quiz": [
                    ("What exception is thrown if you access index 5 in an array of length 5?",
                     ["A) NullPointerException", "B) ArrayIndexOutOfBoundsException", "C) IllegalArgumentException", "D) ArrayOverflowException"],
                     "B) ArrayIndexOutOfBoundsException", "Valid indices for length 5 are 0 through 4; index 5 triggers ArrayIndexOutOfBoundsException.", "EASY"),
                    ("How do you obtain the number of elements in a Java array named data?",
                     ["A) data.length()", "B) data.size()", "C) data.length", "D) data.count"],
                     "C) data.length", "Arrays have a final length field, unlike collections which use a size() method.", "EASY"),
                    ("What is the default value of numeric elements in a newly initialized int[] array?",
                     ["A) -1", "B) 0", "C) null", "D) undefined"],
                     "B) 0", "Numeric arrays default to 0 (or 0.0 for floating-point values) upon allocation.", "EASY"),
                    ("Can the size of an initialized Java array be dynamically resized after creation?",
                     ["A) Yes, using the array.resize() method", "B) No, arrays have a fixed size once allocated in heap memory", "C) Yes, if marked dynamic", "D) Yes, by reassigning length"],
                     "B) No, arrays have a fixed size once allocated in heap memory", "Standard arrays are fixed in capacity; dynamic sizing requires collections such as ArrayList.", "MEDIUM"),
                    ("What does the java.util.Arrays.sort() method do?",
                     ["A) Reverses an array in place", "B) Sorts array elements into ascending natural order", "C) Removes duplicate elements", "D) Converts array to a string"],
                     "B) Sorts array elements into ascending natural order", "Arrays.sort() orders primitive and comparable elements into ascending order using Dual-Pivot Quicksort.", "EASY")
                ],
                "resources": [
                    ("GeeksforGeeks Java Arrays", "Comprehensive breakdown of single and multi-dimensional array memory layouts in Java.", "https://www.geeksforgeeks.org/arrays-in-java/", "TUTORIAL", "GeeksforGeeks")
                ]
            },
            {
                "order": 8,
                "title": "08 — Object Oriented Programming",
                "short_description": "Master classes, object instantiation, constructor initialization, and encapsulation with access modifiers.",
                "topics": [
                    ("Classes & Objects", "Class blueprints, heap object allocation, and reference pointers.", "MEDIUM"),
                    ("Constructors", "Default constructors, parameterized constructors, and the this reference.", "MEDIUM"),
                    ("Encapsulation & Access Modifiers", "Information hiding via private fields and public getters/setters.", "MEDIUM")
                ],
                "puzzle": {
                    "type": "MATCHING",
                    "title": "OOP Core Concepts Matching",
                    "question": "Match each Object-Oriented term with its primary responsibility:",
                    "puzzle_data": [
                        ["Class", "Blueprint defining state and behaviors"],
                        ["Object", "Concrete instance allocated in memory"],
                        ["Constructor", "Special method initializing state upon creation"],
                        ["Encapsulation", "Bundling data and restricting direct field access"]
                    ],
                    "correct_answer": {
                        "Class": "Blueprint defining state and behaviors",
                        "Object": "Concrete instance allocated in memory",
                        "Constructor": "Special method initializing state upon creation",
                        "Encapsulation": "Bundling data and restricting direct field access"
                    },
                    "explanation": "Classes serve as blueprints, objects are instances, constructors initialize instance state, and encapsulation shields raw fields behind access methods."
                },
                "quiz": [
                    ("What keyword is used to instantiate a new object in Java?",
                     ["A) create", "B) allocate", "C) new", "D) make"],
                     "C) new", "The new keyword requests dynamic memory allocation on the heap and invokes a constructor.", "EASY"),
                    ("Which access modifier restricts field visibility strictly to the declaring class?",
                     ["A) public", "B) protected", "C) default (package-private)", "D) private"],
                     "D) private", "private members can only be accessed from within the class in which they are declared.", "EASY"),
                    ("What is the primary objective of Encapsulation in OOP design?",
                     ["A) Allowing any class to modify internal fields directly", "B) Protecting object integrity by preventing unauthorized direct access to internal state", "C) Enabling faster compilation times", "D) Eliminating method calls"],
                     "B) Protecting object integrity by preventing unauthorized direct access to internal state", "Encapsulation enforces data validation and state invariants through controlled access points.", "MEDIUM"),
                    ("What is the purpose of the 'this' keyword in Java?",
                     ["A) References the current object instance within a method or constructor", "B) References the parent superclass", "C) Refers to a static utility class", "D) Declares a local variable"],
                     "A) References the current object instance within a method or constructor", "'this' disambiguates instance fields from shadowed parameter identifiers.", "MEDIUM"),
                    ("Can a Java class have multiple constructors with different parameter signatures?",
                     ["A) No, only one constructor is permitted", "B) Yes, this is known as constructor overloading", "C) Only if all constructors are private", "D) Only in abstract classes"],
                     "B) Yes, this is known as constructor overloading", "Constructor overloading lets a class be initialized in different configurations.", "MEDIUM")
                ],
                "resources": [
                    ("freeCodeCamp OOP Java Guide", "Core principles of encapsulation, abstraction, and class architecture with clean examples.", "https://www.freecodecamp.org/news/java-object-oriented-programming-system-principles-oops-concepts-for-beginners/", "ARTICLE", "freeCodeCamp")
                ]
            },
            {
                "order": 9,
                "title": "09 — Inheritance and Polymorphism",
                "short_description": "Extend classes, invoke super constructors, override methods for dynamic dispatch, and design with interfaces.",
                "topics": [
                    ("Class Inheritance", "The extends keyword, single inheritance, and super constructor chaining.", "HARD"),
                    ("Method Overriding", "Dynamic runtime dispatch, @Override annotation, and rules of overriding.", "HARD"),
                    ("Abstraction & Interfaces", "Abstract classes vs interface contracts with default and static methods.", "HARD")
                ],
                "puzzle": {
                    "type": "TRUE_FALSE",
                    "title": "Multiple Inheritance Verification",
                    "question": "True or False: Java allows a class to directly inherit state and implementation from multiple classes using 'extends ClassA, ClassB'.",
                    "puzzle_data": "Java supports multiple class inheritance with extends.",
                    "correct_answer": False,
                    "explanation": "Java strictly prohibits multiple class inheritance to avoid the diamond problem of ambiguity. Classes implement multiple interfaces instead."
                },
                "quiz": [
                    ("Which keyword is used by a class to inherit from a superclass?",
                     ["A) implements", "B) extends", "C) inherits", "D) super"],
                     "B) extends", "A class uses extends to inherit from another class in Java.", "EASY"),
                    ("What does the super() constructor call do in a subclass?",
                     ["A) Terminates the superclass", "B) Invokes the constructor of the immediate superclass", "C) Overrides all parent methods", "D) Creates a static copy"],
                     "B) Invokes the constructor of the immediate superclass", "super() chains constructor execution to the superclass and must be the first statement in the subclass constructor.", "MEDIUM"),
                    ("What happens during dynamic method dispatch (runtime polymorphism)?",
                     ["A) The JVM determines which overridden method to call at runtime based on the actual object instance type", "B) The compiler binds methods at compile time", "C) Private methods are invoked regardless of scope", "D) Methods are selected randomly"],
                     "A) The JVM determines which overridden method to call at runtime based on the actual object instance type", "Dynamic method dispatch executes the specific subclass override based on the underlying runtime object.", "HARD"),
                    ("Can an abstract class in Java be directly instantiated using the new keyword?",
                     ["A) Yes, if all methods have bodies", "B) No, abstract classes cannot be directly instantiated", "C) Yes, if constructor is public", "D) Only in test files"],
                     "B) No, abstract classes cannot be directly instantiated", "Abstract classes serve as incomplete base models that must be extended by concrete subclasses.", "MEDIUM"),
                    ("How many interfaces can a single Java class implement?",
                     ["A) Only one", "B) Up to two", "C) An unlimited number of interfaces", "D) Exactly four"],
                     "C) An unlimited number of interfaces", "Java supports multiple interface inheritance using the implements keyword with comma-separated interfaces.", "MEDIUM")
                ],
                "resources": [
                    ("Oracle Subclasses and Overriding", "Official guide on dynamic dispatch, super keyword, and interface contract implementations.", "https://docs.oracle.com/javase/tutorial/java/IandI/subclasses.html", "DOCUMENTATION", "Oracle")
                ]
            },
            {
                "order": 10,
                "title": "10 — Exception Handling and Collections",
                "short_description": "Handle runtime errors with try-catch-finally, write custom exceptions, and leverage ArrayList and HashMap.",
                "topics": [
                    ("Exception Hierarchy", "Checked exceptions vs Unchecked RuntimeExceptions and Errors.", "MEDIUM"),
                    ("Try-Catch-Finally", "Catching exceptions, multi-catch, and resource cleanup.", "MEDIUM"),
                    ("Collections Framework", "ArrayList, LinkedList, HashMap, and HashSet fundamentals.", "HARD")
                ],
                "puzzle": {
                    "type": "MATCHING",
                    "title": "Java Collections Structure Matching",
                    "question": "Match each Java collection interface/class with its core characteristic:",
                    "puzzle_data": [
                        ["ArrayList", "Resizable dynamic array with fast O(1) random access"],
                        ["HashMap", "Key-value pair store backed by hashing"],
                        ["Stack", "LIFO (Last-In-First-Out) data structure"],
                        ["Queue", "FIFO (First-In-First-Out) processing structure"]
                    ],
                    "correct_answer": {
                        "ArrayList": "Resizable dynamic array with fast O(1) random access",
                        "HashMap": "Key-value pair store backed by hashing",
                        "Stack": "LIFO (Last-In-First-Out) data structure",
                        "Queue": "FIFO (First-In-First-Out) processing structure"
                    },
                    "explanation": "ArrayList provides dynamic contiguous index access, HashMap hashes keys for value retrieval, Stack is LIFO, and Queue is FIFO."
                },
                "quiz": [
                    ("When is the finally block executed in a try-catch-finally statement?",
                     ["A) Only if an exception occurs", "B) Only if NO exception occurs", "C) Almost always, regardless of whether an exception was thrown or caught", "D) Only if System.exit() is called"],
                     "C) Almost always, regardless of whether an exception was thrown or caught", "The finally block executes cleanup code reliably after try and catch blocks finish.", "MEDIUM"),
                    ("What is the fundamental difference between checked and unchecked exceptions in Java?",
                     ["A) Checked exceptions extend RuntimeException; unchecked do not", "B) Checked exceptions are verified at compile time; unchecked exceptions occur at runtime and extend RuntimeException", "C) Unchecked exceptions cannot be caught", "D) Checked exceptions only occur in web apps"],
                     "B) Checked exceptions are verified at compile time; unchecked exceptions occur at runtime and extend RuntimeException", "The compiler forces handling or declaring checked exceptions, whereas RuntimeExceptions are unchecked.", "HARD"),
                    ("What is the average time complexity for key lookups in a standard Java HashMap?",
                     ["A) O(n)", "B) O(log n)", "C) O(1)", "D) O(n^2)"],
                     "C) O(1)", "HashMap uses hash indexing to achieve constant amortized O(1) retrieval time.", "MEDIUM"),
                    ("Which collection guarantees unique elements with no duplicates permitted?",
                     ["A) ArrayList", "B) LinkedList", "C) HashSet", "D) Vector"],
                     "C) HashSet", "Set implementations like HashSet enforce uniqueness and reject duplicate entries.", "EASY"),
                    ("Which method is called on a collection to retrieve the number of items it currently holds?",
                     ["A) length()", "B) count()", "C) size()", "D) capacity()"],
                     "C) size()", "All Collection interface implementors define the size() method.", "EASY")
                ],
                "resources": [
                    ("Oracle Java Collections Framework", "Overview of List, Set, Map, and Queue implementations in java.util.", "https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html", "DOCUMENTATION", "Oracle")
                ]
            }
        ]
    }
]
