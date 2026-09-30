"""
Seed Real Learning-Oriented Puzzles for Subject 12 (Math for Computing) and Subject 3 (DBMS).
Provides 2-3 interactive puzzles per lesson covering varied challenge types:
- Multiple Choice / Scenario Challenge
- Arrange in Order (Sequence)
- Code / SQL Output Prediction
- Concept Match (Key-Value)
- Fill the Gap (Missing Concept / Syntax)
- True / False Challenge
"""
import json
import sys
import os

# Ensure backend path is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.db.database import SessionLocal
from app.db.models.academic import Subject, Lesson, Topic
from app.db.models.puzzle import Puzzle

def seed_puzzles():
    db = SessionLocal()
    print("Beginning seeding of high-value curriculum puzzles...")

    # Data structure: lesson_id -> list of puzzle definitions
    curriculum_puzzles = {
        # ==========================================
        # SUBJECT 12: MATHEMATICS FOR COMPUTING
        # ==========================================
        # Lesson 97: Propositional Logic, Boolean Algebra & Set Theory (Topic 212)
        97: [
            {
                "title": "De Morgan's Laws Equivalent Transformation",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 1,
                "question": "Which of the following Boolean expressions is logically equivalent to ¬(P ∧ (Q ∨ ¬R)) using De Morgan's Laws?",
                "puzzle_data": {
                    "options": [
                        "¬P ∨ (¬Q ∧ R)",
                        "¬P ∧ (¬Q ∨ R)",
                        "¬P ∨ ¬Q ∨ ¬R",
                        "P ∨ (Q ∧ ¬R)"
                    ]
                },
                "correct_answer": "¬P ∨ (¬Q ∧ R)",
                "explanation": "Applying De Morgan's Law ¬(A ∧ B) = ¬A ∨ ¬B yields ¬P ∨ ¬(Q ∨ ¬R). Applying it again to the second term gives ¬(Q ∨ ¬R) = (¬Q ∧ ¬¬R) = (¬Q ∧ R). Thus, ¬P ∨ (¬Q ∧ R)."
            },
            {
                "title": "Logical Proof Execution Pipeline",
                "puzzle_type": "ORDERING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 2,
                "question": "Arrange the steps to perform a formal Proof by Contradiction in the correct logical sequence:",
                "puzzle_data": [
                    "Assume the negation of the proposition (¬P is True)",
                    "Apply valid deductive inference rules step-by-step",
                    "Arrive at an impossible logical contradiction (Q ∧ ¬Q)",
                    "Conclude that the original assumption is false, establishing P as True"
                ],
                "correct_answer": [
                    "Assume the negation of the proposition (¬P is True)",
                    "Apply valid deductive inference rules step-by-step",
                    "Arrive at an impossible logical contradiction (Q ∧ ¬Q)",
                    "Conclude that the original assumption is false, establishing P as True"
                ],
                "explanation": "A proof by contradiction always begins by assuming the opposite statement, deriving deductions until a logical paradox arises, and concluding the original statement must hold."
            },
            {
                "title": "Logic Gate Truth Table Matching",
                "puzzle_type": "MATCHING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 3,
                "question": "Match each boolean gate operator to its defining truth-table condition:",
                "puzzle_data": [
                    ["XOR (⊕)", "Outputs 1 only when inputs differ (one 1, one 0)"],
                    ["NAND (⊼)", "Outputs 0 only when both inputs are 1"],
                    ["IMPLIES (→)", "Outputs 0 only when True implies False"],
                    ["EQUIVALENCE (↔)", "Outputs 1 only when both inputs are identical"]
                ],
                "correct_answer": [
                    ["XOR (⊕)", "Outputs 1 only when inputs differ (one 1, one 0)"],
                    ["NAND (⊼)", "Outputs 0 only when both inputs are 1"],
                    ["IMPLIES (→)", "Outputs 0 only when True implies False"],
                    ["EQUIVALENCE (↔)", "Outputs 1 only when both inputs are identical"]
                ],
                "explanation": "Understanding truth table invariants is essential for compiler optimization and digital circuit synthesis."
            }
        ],

        # Lesson 98: Number Theory, Modular Arithmetic & Cryptographic Primes (Topic 199)
        98: [
            {
                "title": "Modular Exponentiation Mental Math",
                "puzzle_type": "FILL_BLANK",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 1,
                "question": "Calculate the value of 3^5 mod 7 (Enter a single integer between 0 and 6):",
                "puzzle_data": {
                    "placeholder": "Enter integer remainder"
                },
                "correct_answer": "5",
                "explanation": "3^1 = 3, 3^2 = 9 ≡ 2, 3^3 ≡ 6, 3^4 ≡ 18 ≡ 4, 3^5 ≡ 12 ≡ 5 (mod 7). Alternatively, 3^5 = 243; 243 / 7 = 34 with remainder 5."
            },
            {
                "title": "RSA Cryptographic Key Generation Pipeline",
                "puzzle_type": "ORDERING",
                "difficulty": "HARD",
                "xp_reward": 25,
                "display_order": 2,
                "question": "Arrange the mathematical steps in RSA public/private key generation in chronological order:",
                "puzzle_data": [
                    "Select two distinct large primes p and q",
                    "Compute modulus n = p * q and totient φ(n) = (p-1)(q-1)",
                    "Choose public exponent e coprime to φ(n)",
                    "Compute private key d ≡ e^(-1) mod φ(n) via Extended Euclidean Algorithm"
                ],
                "correct_answer": [
                    "Select two distinct large primes p and q",
                    "Compute modulus n = p * q and totient φ(n) = (p-1)(q-1)",
                    "Choose public exponent e coprime to φ(n)",
                    "Compute private key d ≡ e^(-1) mod φ(n) via Extended Euclidean Algorithm"
                ],
                "explanation": "RSA relies on the asymmetric trapdoor function: multiplying two primes is trivial, but finding φ(n) from n alone is intractable."
            }
        ],

        # Lesson 99: Vectors, Matrices & Systems of Linear Equations (Topic 198)
        99: [
            {
                "title": "Matrix Multiplication Dimension Compatibility",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 1,
                "question": "If Matrix A has dimensions 3 × 4 and Matrix B has dimensions 4 × 2, what are the dimensions of the resulting product Matrix C = A × B?",
                "puzzle_data": {
                    "options": [
                        "3 × 2",
                        "4 × 4",
                        "3 × 4",
                        "Cannot be multiplied"
                    ]
                },
                "correct_answer": "3 × 2",
                "explanation": "For matrix multiplication (m × k) × (k × n), the inner dimensions must match (4 == 4), and the resulting matrix takes the outer dimensions (3 × 2)."
            },
            {
                "title": "Gaussian Elimination Sequence",
                "puzzle_type": "ORDERING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 2,
                "question": "Arrange the steps to solve a system of linear equations using Gaussian Elimination:",
                "puzzle_data": [
                    "Formulate the Augmented Matrix [A | b]",
                    "Perform row operations to create Row Echelon Form (zeros below pivot)",
                    "Eliminate entries above pivots to reach Reduced Row Echelon Form (RREF)",
                    "Read off unique variables or identify free parameters directly"
                ],
                "correct_answer": [
                    "Formulate the Augmented Matrix [A | b]",
                    "Perform row operations to create Row Echelon Form (zeros below pivot)",
                    "Eliminate entries above pivots to reach Reduced Row Echelon Form (RREF)",
                    "Read off unique variables or identify free parameters directly"
                ],
                "explanation": "Gaussian Elimination systematically produces upper-triangular echelon form, followed by back-substitution."
            },
            {
                "title": "Determinant Invertibility Rule",
                "puzzle_type": "TRUE_FALSE",
                "difficulty": "EASY",
                "xp_reward": 10,
                "display_order": 3,
                "question": "True or False: A square matrix A is invertible (non-singular) if and only if its determinant det(A) ≠ 0.",
                "puzzle_data": {},
                "correct_answer": "True",
                "explanation": "If det(A) = 0, the columns are linearly dependent and the matrix maps space into a lower dimension, making inversion impossible."
            }
        ],

        # Lesson 100: Matrix Transformations, Eigenvalues & PageRank (Topic 198)
        100: [
            {
                "title": "Eigenvalue Characteristic Equation Formulation",
                "puzzle_type": "FILL_BLANK",
                "difficulty": "HARD",
                "xp_reward": 25,
                "display_order": 1,
                "question": "To find the eigenvalues λ of square matrix A, we set det(A - λ * I) equal to what numeric value?",
                "puzzle_data": {
                    "placeholder": "Enter value"
                },
                "correct_answer": "0",
                "explanation": "Setting det(A - λI) = 0 ensures the nullspace of (A - λI) is non-trivial, meaning non-zero eigenvectors exist satisfying Av = λv."
            },
            {
                "title": "Google PageRank Power Iteration Flow",
                "puzzle_type": "ORDERING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 2,
                "question": "Arrange the algorithmic phases of PageRank computation:",
                "puzzle_data": [
                    "Construct Web Hyperlink Adjacency Graph",
                    "Normalize rows/columns into Stochastic Markov Transition Matrix M",
                    "Add damping factor d (0.85) to form Google Matrix: G = d*M + (1-d)/N*E",
                    "Iterate power vector p_(k+1) = G * p_k until convergence (stationary eigenvector)"
                ],
                "correct_answer": [
                    "Construct Web Hyperlink Adjacency Graph",
                    "Normalize rows/columns into Stochastic Markov Transition Matrix M",
                    "Add damping factor d (0.85) to form Google Matrix: G = d*M + (1-d)/N*E",
                    "Iterate power vector p_(k+1) = G * p_k until convergence (stationary eigenvector)"
                ],
                "explanation": "PageRank is the principal eigenvector corresponding to λ=1 for the stochastic Google transition matrix."
            }
        ],

        # Lesson 101: Probability Distributions, Expectation & Bayes' Theorem (Topic 200)
        101: [
            {
                "title": "Bayes' Theorem Scenario: Medical Diagnostic",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 1,
                "question": "A disease has 1% prevalence. A test is 90% accurate (true positive rate = 0.9, false positive rate = 0.1). If someone tests positive, what is the approximate probability P(Disease | Positive)?",
                "puzzle_data": {
                    "options": [
                        "Approx. 8.3% (Far lower than intuition suggests due to low base rate)",
                        "Approx. 90.0% (Matches test accuracy)",
                        "Approx. 50.0% (Equal likelihood)",
                        "Approx. 99.0% (High confidence)"
                    ]
                },
                "correct_answer": "Approx. 8.3% (Far lower than intuition suggests due to low base rate)",
                "explanation": "By Bayes' Rule: P(D|+) = (0.9 * 0.01) / (0.9 * 0.01 + 0.1 * 0.99) = 0.009 / (0.009 + 0.099) = 0.009 / 0.108 ≈ 8.33%. The low prior base rate heavily suppresses the posterior probability."
            },
            {
                "title": "Statistical Metrics Matching",
                "puzzle_type": "MATCHING",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 2,
                "question": "Match each probabilistic concept with its definition:",
                "puzzle_data": [
                    ["Expected Value E[X]", "Probability-weighted average of all possible outcomes"],
                    ["Variance Var(X)", "Measure of dispersion around the mean E[(X - μ)^2]"],
                    ["Standard Deviation σ", "Square root of variance, measured in original units"],
                    ["Covariance Cov(X,Y)", "Measure of joint variability between two random variables"]
                ],
                "correct_answer": [
                    ["Expected Value E[X]", "Probability-weighted average of all possible outcomes"],
                    ["Variance Var(X)", "Measure of dispersion around the mean E[(X - μ)^2]"],
                    ["Standard Deviation σ", "Square root of variance, measured in original units"],
                    ["Covariance Cov(X,Y)", "Measure of joint variability between two random variables"]
                ],
                "explanation": "These core moments form the mathematical bedrock of machine learning loss functions and optimization."
            }
        ],

        # Lesson 102: Differential Calculus, Derivatives & Gradient Optimization (Topic 201)
        102: [
            {
                "title": "Gradient Descent Direction Rule",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 1,
                "question": "In mathematical optimization, in which direction does the negative gradient -∇f(x) always point?",
                "puzzle_data": {
                    "options": [
                        "Direction of steepest descent (fastest decrease of loss)",
                        "Direction of steepest ascent (fastest increase)",
                        "Perpendicular to the contour lines with zero change",
                        "Toward the global origin (0, 0)"
                    ]
                },
                "correct_answer": "Direction of steepest descent (fastest decrease of loss)",
                "explanation": "The gradient ∇f points in the direction of steepest increase. Therefore, the negative gradient -∇f points in the direction of steepest decrease."
            },
            {
                "title": "Neural Network Backpropagation Flow",
                "puzzle_type": "ORDERING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 2,
                "question": "Arrange the steps of gradient-based optimization in training a machine learning model:",
                "puzzle_data": [
                    "Forward Pass: Compute layer activations and predictions",
                    "Loss Evaluation: Measure objective discrepancy L(y_pred, y_true)",
                    "Backward Pass: Apply Multivariate Chain Rule to compute gradients ∂L/∂w",
                    "Weight Update: Adjust parameters w := w - η * ∇L"
                ],
                "correct_answer": [
                    "Forward Pass: Compute layer activations and predictions",
                    "Loss Evaluation: Measure objective discrepancy L(y_pred, y_true)",
                    "Backward Pass: Apply Multivariate Chain Rule to compute gradients ∂L/∂w",
                    "Weight Update: Adjust parameters w := w - η * ∇L"
                ],
                "explanation": "Backpropagation is reverse-mode automatic differentiation applying the chain rule layer-by-layer."
            }
        ],

        # Lesson 103: Graph Theory, Network Flow & Algorithmic Complexity (Topic 198)
        103: [
            {
                "title": "Dijkstra's Algorithm Invariant",
                "puzzle_type": "TRUE_FALSE",
                "difficulty": "MEDIUM",
                "xp_reward": 15,
                "display_order": 1,
                "question": "True or False: Dijkstra's single-source shortest path algorithm is guaranteed to produce optimal paths on graphs containing negative edge weights.",
                "puzzle_data": {},
                "correct_answer": "False",
                "explanation": "Dijkstra's greedy assumption assumes visiting a node finalizes its shortest distance. Negative edge weights violate this invariant; the Bellman-Ford algorithm must be used instead."
            },
            {
                "title": "Breadth-First Search (BFS) Execution Steps",
                "puzzle_type": "ORDERING",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 2,
                "question": "Arrange the operational steps of a standard BFS traversal:",
                "puzzle_data": [
                    "Initialize a FIFO Queue and enqueue start vertex marked as visited",
                    "Dequeue the current front node and process its value",
                    "Iterate over all unvisited adjacent neighbors",
                    "Mark neighbors as visited and enqueue them into FIFO Queue"
                ],
                "correct_answer": [
                    "Initialize a FIFO Queue and enqueue start vertex marked as visited",
                    "Dequeue the current front node and process its value",
                    "Iterate over all unvisited adjacent neighbors",
                    "Mark neighbors as visited and enqueue them into FIFO Queue"
                ],
                "explanation": "BFS uses a FIFO queue to discover nodes layer by layer, ensuring unweighted shortest path properties."
            }
        ],

        # ==========================================
        # SUBJECT 3: DATABASE MANAGEMENT SYSTEMS
        # ==========================================
        # Lesson 91: Relational Database Architecture & Foundations (Topic 205)
        91: [
            {
                "title": "Three-Schema Database Architecture",
                "puzzle_type": "ORDERING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 1,
                "question": "Arrange ANSI/SPARC 3-tier database architecture levels from closest to user to closest to storage:",
                "puzzle_data": [
                    "External Level (User Views & Application Interfaces)",
                    "Conceptual Level (Logical Entities, Relationships & Constraints)",
                    "Internal Level (Physical Storage, B-Trees & File Organization)"
                ],
                "correct_answer": [
                    "External Level (User Views & Application Interfaces)",
                    "Conceptual Level (Logical Entities, Relationships & Constraints)",
                    "Internal Level (Physical Storage, B-Trees & File Organization)"
                ],
                "explanation": "The ANSI-SPARC architecture separates user views (external) from logical design (conceptual) and physical byte storage (internal)."
            },
            {
                "title": "Relational Key Properties Matching",
                "puzzle_type": "MATCHING",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 2,
                "question": "Match each relational database key type with its defining requirement:",
                "puzzle_data": [
                    ["Primary Key", "Must be UNIQUE and CANNOT contain NULL values"],
                    ["Foreign Key", "References a primary/unique key in another relation to enforce referential integrity"],
                    ["Candidate Key", "A minimal superkey capable of uniquely identifying every row in a table"],
                    ["Surrogate Key", "An artificial numeric identifier having no real-world business meaning"]
                ],
                "correct_answer": [
                    ["Primary Key", "Must be UNIQUE and CANNOT contain NULL values"],
                    ["Foreign Key", "References a primary/unique key in another relation to enforce referential integrity"],
                    ["Candidate Key", "A minimal superkey capable of uniquely identifying every row in a table"],
                    ["Surrogate Key", "An artificial numeric identifier having no real-world business meaning"]
                ],
                "explanation": "Key constraints preserve entity and referential integrity across relational schemas."
            }
        ],

        # Lesson 92: Entity-Relationship (ER) Modeling & Constraints (Topic 206)
        92: [
            {
                "title": "Resolving Many-to-Many Relationships",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "MEDIUM",
                "xp_reward": 15,
                "display_order": 1,
                "question": "In relational schema design, how is a Many-to-Many (M:N) relationship between Students and Courses correctly implemented?",
                "puzzle_data": {
                    "options": [
                        "Create a junction/associative table with foreign keys referencing both Students and Courses",
                        "Add a comma-separated list of Course IDs into a column in the Students table",
                        "Place the Student ID as a foreign key inside the Course table",
                        "Duplicate Course records for every enrolled student"
                    ]
                },
                "correct_answer": "Create a junction/associative table with foreign keys referencing both Students and Courses",
                "explanation": "Relational 1NF prohibits repeating groups and composite arrays. An associative table decomposes M:N into two 1:N relations."
            },
            {
                "title": "Weak Entity Identification Invariant",
                "puzzle_type": "TRUE_FALSE",
                "difficulty": "EASY",
                "xp_reward": 10,
                "display_order": 2,
                "question": "True or False: A Weak Entity can be uniquely identified solely by its own partial key attributes without referencing its parent identifying relationship.",
                "puzzle_data": {},
                "correct_answer": "False",
                "explanation": "A weak entity does not have a primary key of its own; its primary key is formed by combining its partial key (discriminator) with the parent entity's primary key."
            }
        ],

        # Lesson 93: Database Normalization (1NF to BCNF) (Topic 207)
        93: [
            {
                "title": "Normalization Stages Order",
                "puzzle_type": "ORDERING",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 1,
                "question": "Arrange the normal forms in order of increasing rigor and dependency elimination:",
                "puzzle_data": [
                    "1NF (Eliminate repeating groups; atomic scalar values only)",
                    "2NF (Eliminate partial functional dependencies on composite keys)",
                    "3NF (Eliminate transitive dependencies: non-key cannot determine non-key)",
                    "BCNF (Every determinant X in functional dependency X → Y must be a Superkey)"
                ],
                "correct_answer": [
                    "1NF (Eliminate repeating groups; atomic scalar values only)",
                    "2NF (Eliminate partial functional dependencies on composite keys)",
                    "3NF (Eliminate transitive dependencies: non-key cannot determine non-key)",
                    "BCNF (Every determinant X in functional dependency X → Y must be a Superkey)"
                ],
                "explanation": "Each successive normal form imposes stricter requirements on functional dependencies, eliminating update, insert, and delete anomalies."
            },
            {
                "title": "Detecting Transitive Dependencies",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 2,
                "question": "Given table: Employee(EmpID, DeptID, DeptName, Salary). EmpID is the primary key. If EmpID → DeptID and DeptID → DeptName, what normal form does this violate?",
                "puzzle_data": {
                    "options": [
                        "Violates 3NF (Transitive dependency exists: EmpID determines DeptName through DeptID)",
                        "Violates 1NF (Non-atomic values)",
                        "Violates 2NF (Partial dependency on composite key)",
                        "Already in BCNF"
                    ]
                },
                "correct_answer": "Violates 3NF (Transitive dependency exists: EmpID determines DeptName through DeptID)",
                "explanation": "Since DeptID is not a candidate key and DeptName is non-prime, the transitive dependency EmpID → DeptID → DeptName violates Third Normal Form."
            }
        ],

        # Lesson 94: SQL Querying, Complex Joins & Aggregations (Topic 208)
        94: [
            {
                "title": "SQL Logical Query Execution Sequence",
                "puzzle_type": "ORDERING",
                "difficulty": "HARD",
                "xp_reward": 25,
                "display_order": 1,
                "question": "Arrange the standard clauses in the order the SQL Query Engine executes them internally:",
                "puzzle_data": [
                    "FROM and JOIN (Assemble cartesian product and table rows)",
                    "WHERE (Filter rows prior to grouping)",
                    "GROUP BY and HAVING (Aggregate into groups and filter aggregated partitions)",
                    "SELECT and DISTINCT (Project expressions and eliminate duplicates)",
                    "ORDER BY and LIMIT (Sort finalized result set and paginate)"
                ],
                "correct_answer": [
                    "FROM and JOIN (Assemble cartesian product and table rows)",
                    "WHERE (Filter rows prior to grouping)",
                    "GROUP BY and HAVING (Aggregate into groups and filter aggregated partitions)",
                    "SELECT and DISTINCT (Project expressions and eliminate duplicates)",
                    "ORDER BY and LIMIT (Sort finalized result set and paginate)"
                ],
                "explanation": "Understanding internal SQL execution order explains why aliases declared in SELECT cannot be referenced in WHERE, but can be used in ORDER BY."
            },
            {
                "title": "WHERE vs HAVING Gap Fill",
                "puzzle_type": "FILL_BLANK",
                "difficulty": "MEDIUM",
                "xp_reward": 15,
                "display_order": 2,
                "question": "To filter records AFTER an aggregation operation like COUNT() or AVG(), which SQL clause must be used instead of WHERE?",
                "puzzle_data": {
                    "placeholder": "Enter SQL keyword"
                },
                "correct_answer": "HAVING",
                "explanation": "WHERE filters individual table rows prior to aggregation, while HAVING filters aggregated group metrics produced by GROUP BY."
            }
        ],

        # Lesson 95: Transactions, ACID Properties & Concurrency Control (Topic 209)
        95: [
            {
                "title": "ACID Properties Matching",
                "puzzle_type": "MATCHING",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 1,
                "question": "Match each ACID transaction property with its core operational guarantee:",
                "puzzle_data": [
                    ["Atomicity", "All operations succeed completely, or the entire transaction is rolled back (all-or-nothing)"],
                    ["Consistency", "The database transitions from one valid invariant state to another valid state"],
                    ["Isolation", "Concurrent transactions execute without witnessing uncommitted intermediate changes"],
                    ["Durability", "Once committed, changes survive system crashes and power failures via WAL"]
                ],
                "correct_answer": [
                    ["Atomicity", "All operations succeed completely, or the entire transaction is rolled back (all-or-nothing)"],
                    ["Consistency", "The database transitions from one valid invariant state to another valid state"],
                    ["Isolation", "Concurrent transactions execute without witnessing uncommitted intermediate changes"],
                    ["Durability", "Once committed, changes survive system crashes and power failures via WAL"]
                ],
                "explanation": "ACID guarantees ensure enterprise data integrity even during concurrent access and hardware crashes."
            },
            {
                "title": "Concurrency Anomaly Scenario: Dirty Read",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 2,
                "question": "Transaction T1 updates a bank account balance. Before T1 commits, Transaction T2 reads this updated balance. T1 then encounters an error and executes ROLLBACK. What concurrency anomaly did T2 experience?",
                "puzzle_data": {
                    "options": [
                        "Dirty Read (Reading uncommitted data that was subsequently aborted)",
                        "Non-Repeatable Read (Rereading data that was modified and committed by another transaction)",
                        "Phantom Read (Querying rows that match a criteria where new matching rows were inserted)",
                        "Lost Update (Overwriting another transaction's changes)"
                    ]
                },
                "correct_answer": "Dirty Read (Reading uncommitted data that was subsequently aborted)",
                "explanation": "Reading data that is later rolled back by another transaction is the textbook definition of a Dirty Read, prevented by Read Committed isolation."
            }
        ],

        # Lesson 6: Indexing Strategies, B-Trees & Query Optimization (Topic 210)
        6: [
            {
                "title": "B+ Tree Index Structural Properties",
                "puzzle_type": "TRUE_FALSE",
                "difficulty": "MEDIUM",
                "xp_reward": 15,
                "display_order": 1,
                "question": "True or False: In a B+ Tree, actual data pointers/records are stored in internal nodes as well as leaf nodes.",
                "puzzle_data": {},
                "correct_answer": "False",
                "explanation": "In a B+ Tree, internal nodes store only search keys and child page pointers. All actual data records/pointers reside exclusively in leaf nodes linked as a doubly-linked list for fast range scans."
            },
            {
                "title": "Index Query Optimization Pipeline",
                "puzzle_type": "ORDERING",
                "difficulty": "HARD",
                "xp_reward": 25,
                "display_order": 2,
                "question": "Arrange the steps the SQL Query Optimizer undertakes to execute an indexed SELECT query:",
                "puzzle_data": [
                    "Parse SQL text and build abstract syntax tree (AST)",
                    "Consult catalog statistics (cardinality, histogram distribution)",
                    "Estimate cost of Table Full Scan vs B-Tree Index Range Scan",
                    "Generate and execute optimal physical Execution Plan"
                ],
                "correct_answer": [
                    "Parse SQL text and build abstract syntax tree (AST)",
                    "Consult catalog statistics (cardinality, histogram distribution)",
                    "Estimate cost of Table Full Scan vs B-Tree Index Range Scan",
                    "Generate and execute optimal physical Execution Plan"
                ],
                "explanation": "Cost-based optimizers (CBO) evaluate I/O and CPU costs using data distribution histograms to decide between sequential scans and index traversal."
            }
        ],

        # Lesson 96: Distributed Databases, Replication & NoSQL Systems (Topic 211)
        96: [
            {
                "title": "CAP Theorem Trade-off Challenge",
                "puzzle_type": "MULTIPLE_CHOICE",
                "difficulty": "MEDIUM",
                "xp_reward": 20,
                "display_order": 1,
                "question": "According to the CAP Theorem, when an unavoidable network partition (P) occurs between distributed database nodes, a system must choose between which two properties?",
                "puzzle_data": {
                    "options": [
                        "Consistency (CP) vs Availability (AP)",
                        "Atomicity (CA) vs Durability (CD)",
                        "Performance vs Security",
                        "Sharding vs Replication"
                    ]
                },
                "correct_answer": "Consistency (CP) vs Availability (AP)",
                "explanation": "Because network partitions are physically inevitable across networks, distributed systems must trade off between returning the latest data (Consistency) or remaining responsive to every request (Availability)."
            },
            {
                "title": "NoSQL Database Models Matching",
                "puzzle_type": "MATCHING",
                "difficulty": "EASY",
                "xp_reward": 15,
                "display_order": 2,
                "question": "Match each NoSQL data model with its prominent architectural representative:",
                "puzzle_data": [
                    ["Document Store (BSON/JSON)", "MongoDB / Couchbase"],
                    ["Key-Value Cache", "Redis / Memcached"],
                    ["Wide-Column Store", "Apache Cassandra / ScyllaDB"],
                    ["Graph Database", "Neo4j / Amazon Neptune"]
                ],
                "correct_answer": [
                    ["Document Store (BSON/JSON)", "MongoDB / Couchbase"],
                    ["Key-Value Cache", "Redis / Memcached"],
                    ["Wide-Column Store", "Apache Cassandra / ScyllaDB"],
                    ["Graph Database", "Neo4j / Amazon Neptune"]
                ],
                "explanation": "Different NoSQL architectures prioritize access patterns: Key-Value for ultra-low latency, Graph for deeply connected traversals, Document for flexible hierarchical schemas."
            }
        ]
    }

    inserted_count = 0
    updated_count = 0

    for lesson_id, p_list in curriculum_puzzles.items():
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            print(f"Skipping lesson {lesson_id} (not found in DB)")
            continue

        topic_id = lesson.topic_id
        subject_id = lesson.subject_id

        for p_def in p_list:
            # Check if puzzle with same title exists for this lesson
            existing = db.query(Puzzle).filter(
                Puzzle.lesson_id == lesson_id,
                Puzzle.title == p_def["title"]
            ).first()

            p_data_str = json.dumps(p_def["puzzle_data"]) if not isinstance(p_def["puzzle_data"], str) else p_def["puzzle_data"]
            c_ans_str = json.dumps(p_def["correct_answer"]) if not isinstance(p_def["correct_answer"], str) else p_def["correct_answer"]

            if existing:
                existing.subject_id = subject_id
                existing.topic_id = topic_id
                existing.description = p_def.get("description", p_def["title"])
                existing.puzzle_type = p_def["puzzle_type"]
                existing.question = p_def["question"]
                existing.puzzle_data = p_data_str
                existing.correct_answer = c_ans_str
                existing.explanation = p_def.get("explanation")
                existing.difficulty = p_def.get("difficulty", "MEDIUM")
                existing.xp_reward = p_def.get("xp_reward", 15)
                existing.display_order = p_def.get("display_order", 1)
                existing.is_active = True
                updated_count += 1
            else:
                p = Puzzle(
                    subject_id=subject_id,
                    lesson_id=lesson_id,
                    topic_id=topic_id,
                    title=p_def["title"],
                    description=p_def.get("description", p_def["title"]),
                    puzzle_type=p_def["puzzle_type"],
                    question=p_def["question"],
                    puzzle_data=p_data_str,
                    correct_answer=c_ans_str,
                    explanation=p_def.get("explanation"),
                    difficulty=p_def.get("difficulty", "MEDIUM"),
                    xp_reward=p_def.get("xp_reward", 15),
                    display_order=p_def.get("display_order", 1),
                    is_active=True
                )
                db.add(p)
                inserted_count += 1

    db.commit()
    print(f"Successfully processed curriculum puzzles! Inserted: {inserted_count}, Updated: {updated_count}")

    # Summary per subject
    for sid in [12, 3]:
        count = db.query(Puzzle).filter(Puzzle.subject_id == sid, Puzzle.is_active == True).count()
        subj = db.query(Subject).filter(Subject.id == sid).first()
        sname = subj.name if subj else f"Subject {sid}"
        print(f"Total active puzzles in {sname} (Subject {sid}): {count}")

    db.close()

if __name__ == "__main__":
    seed_puzzles()
