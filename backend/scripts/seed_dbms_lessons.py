"""
Seed 7 logically ordered, high-quality lessons for Database Management Systems (DBMS - Subject ID=3).
Covers:
Lesson 1 — Fundamentals: Relational Database Architecture & Foundations
Lesson 2 — Core Concepts: Entity-Relationship (ER) Modeling & Constraints
Lesson 3 — Intermediate Concept: Database Normalization (1NF to BCNF)
Lesson 4 — Practical Application: SQL Querying, Complex Joins & Aggregations
Lesson 5 — Advanced Concept: Transactions, ACID Properties & Concurrency Control
Lesson 6 — Practice / Problem Solving: Indexing Strategies, B-Trees & Query Optimization
Lesson 7 — Real-world Application: Distributed Databases, Replication & NoSQL Systems
"""
import sys
import os
import json

# Ensure backend root is on sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

from app.db.database import SessionLocal, create_tables
from app.db.models.academic import Subject, Topic, Lesson, StudyResource
from app.db.models.quiz import Quiz, Question, QuizQuestion
from app.db.models.puzzle import Puzzle

DBMS_LESSONS_DATA = [
    {
        "order": 1,
        "title": "01 — Fundamentals: Relational Database Architecture & Foundations",
        "short_description": "Understand RDBMS architecture, the relational model, tables, tuples, primary keys, and data independence.",
        "detailed_description": "Comprehensive introduction to relational databases, schema design, table structures, candidate keys, and domain constraints.",
        "difficulty": "EASY",
        "estimated_minutes": 15,
        "topic": {
            "name": "Relational Foundations",
            "desc": "Three-schema architecture, relational model, primary keys, foreign keys, and integrity constraints.",
            "difficulty": "EASY"
        },
        "content": """# 01 — Fundamentals: Relational Database Architecture & Foundations

### Short explanation
A Database Management System (DBMS) is specialized system software designed to store, manage, and retrieve structured data reliably. The relational model organizes data into mathematically grounded tables (relations) of rows (tuples) and columns (attributes), replacing error-prone file systems with declarative schemas and guaranteed integrity constraints.

### Learning objectives
- Understand the ANSI-SPARC Three-Schema Architecture (Internal, Conceptual, and External levels).
- Master core relational model primitives: Relations, Tuples, Attributes, Cardinality, and Degree.
- Differentiate between Candidate Keys, Primary Keys, Foreign Keys, and Super Keys.
- Enforce Entity Integrity (non-null primary keys) and Referential Integrity (valid foreign key references).

### Key concepts
- **Data Independence**: Logical data independence isolates conceptual schemas from application changes; physical data independence isolates storage disk structures from table definitions.
- **Relational Integrity Constraints**:
  - *Domain Constraints*: Attribute values must belong to the specified data type/set.
  - *Entity Integrity*: No primary key attribute can be NULL.
  - *Referential Integrity*: A foreign key must reference an existing primary key or be NULL.

### Example
```sql
-- Creating normalized relational tables with explicit integrity constraints
CREATE TABLE departments (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE students (
    student_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    dept_id INT NOT NULL,
    enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_student_dept FOREIGN KEY (dept_id)
        REFERENCES departments (dept_id)
        ON DELETE RESTRICT
);
```

### Practical/application section
When building an educational platform like SPECTRA, using flat files for student grades causes race conditions during simultaneous updates and risks orphaned records when a course is deleted. A relational database prevents duplicate emails through `UNIQUE` constraints and prevents invalid course references through `FOREIGN KEY` enforcement at the storage engine level.

### Quick recap
The relational model provides mathematical structure, declaratively enforces data integrity via primary and foreign keys, and shields software applications from physical storage concerns through strict data independence.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "Three-Schema Database Architecture",
            "question": "Arrange the layers of the ANSI-SPARC database architecture from user-facing down to physical disk:",
            "puzzle_data": [
                "Internal / Physical Schema (B-Trees, disk pages, blocks)",
                "External Schema / Views (Tailored student/teacher views)",
                "Conceptual / Logical Schema (Entities, tables, relationships)"
            ],
            "correct_answer": [
                "External Schema / Views (Tailored student/teacher views)",
                "Conceptual / Logical Schema (Entities, tables, relationships)",
                "Internal / Physical Schema (B-Trees, disk pages, blocks)"
            ],
            "explanation": "ANSI-SPARC architecture separates user views (External) from global entity structures (Conceptual) and disk block layout (Internal)."
        },
        "quiz": [
            ("Which constraint dictates that no component of a primary key may accept a NULL value?",
             ["A) Domain Integrity", "B) Entity Integrity", "C) Referential Integrity", "D) Key Cardinality"],
             "B) Entity Integrity", "Entity Integrity requires every primary key attribute to be non-null and unique.", "EASY"),
            ("What does a Foreign Key establish between two relational tables?",
             ["A) Physical disk co-location", "B) Referential link between child and parent tables", "C) Automatic duplicate deletion", "D) Symmetric encryption"],
             "B) Referential link between child and parent tables", "Foreign keys reference primary keys in another table to maintain referential integrity.", "EASY"),
            ("Which level of database architecture describes how data is physically stored on disk storage blocks?",
             ["A) External level", "B) Conceptual level", "C) Internal level", "D) Presentation level"],
             "C) Internal level", "The internal schema defines physical storage structures, indices, and file allocation.", "EASY"),
            ("What term refers to the number of tuples (rows) in a relational table?",
             ["A) Degree", "B) Domain", "C) Cardinality", "D) Schema"],
             "C) Cardinality", "Cardinality is the total number of rows (tuples) in a relation.", "EASY"),
            ("If a DBMS allows altering physical disk indices without changing application SQL queries, it provides:",
             ["A) Physical Data Independence", "B) Logical Data Independence", "C) Strict Serialization", "D) Strong Atomicity"],
             "A) Physical Data Independence", "Physical data independence allows storage tuning without altering logical queries.", "EASY")
        ]
    },
    {
        "order": 2,
        "title": "02 — Core Concepts: Entity-Relationship (ER) Modeling & Constraints",
        "short_description": "Design conceptual ER schemas, define entity types, attributes, cardinality ratios, and structural constraints.",
        "detailed_description": "Translate real-world domain requirements into robust Entity-Relationship (ER) diagrams and relational mapping tables.",
        "difficulty": "EASY",
        "estimated_minutes": 15,
        "topic": {
            "name": "ER Modeling",
            "desc": "Entities, attributes, relationships, cardinality ratios, weak entities, and relational conversion.",
            "difficulty": "EASY"
        },
        "content": """# 02 — Core Concepts: Entity-Relationship (ER) Modeling & Constraints

### Short explanation
Entity-Relationship (ER) modeling is the industry standard for high-level conceptual database design. It translates business rules into structured visual blueprints of real-world objects (Entities), their properties (Attributes), and the associations connecting them (Relationships), prior to writing SQL DDL.

### Learning objectives
- Distinguish between Strong Entity Sets and Weak Entity Sets.
- Classify attributes: Simple, Composite, Single-valued, Multi-valued, and Derived.
- Accurately determine relationship cardinality: One-to-One (1:1), One-to-Many (1:N), and Many-to-Many (M:N).
- Correctly map M:N relationships into normalized relational schemas using junction tables.

### Key concepts
- **Strong vs. Weak Entities**: Strong entities have an independent primary key. Weak entities depend on an owner entity for existence and use a partial discriminator (e.g., `Course` $\rightarrow$ `LessonSection`).
- **Cardinality Ratios**:
  - *1:1*: A student has one profile; a profile belongs to one student.
  - *1:N*: A department offers many courses; a course belongs to one department.
  - *M:N*: A student enrolls in many courses; a course enrolls many students.
- **Participation Constraints**: Total participation (every student must have an advisor) vs. Partial participation.

### Example
```sql
-- Resolving a Many-to-Many relationship (Students <-> Subjects) using a Junction Table
CREATE TABLE enrollments (
    enrollment_id INT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    enrolled_date DATE NOT NULL,
    grade VARCHAR(2),
    CONSTRAINT fk_enroll_student FOREIGN KEY (student_id) REFERENCES students(student_id),
    CONSTRAINT fk_enroll_subject FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
    CONSTRAINT uq_student_subject UNIQUE (student_id, subject_id)
);
```

### Practical/application section
In e-commerce, an `Order` contains multiple `Products`, and a `Product` appears in multiple `Orders`. Creating a column list in `Orders` (`product_1, product_2`) violates first normal form. An ER model cleanly introduces an `OrderItem` junction table recording `order_id`, `product_id`, `quantity`, and `unit_price_at_purchase`.

### Quick recap
ER diagrams model conceptual real-world domains. Cardinality ratios govern how foreign keys are placed, and Many-to-Many relationships are transformed into relational tables through associative junction tables.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "ER to Relational Schema Mapping Pipeline",
            "question": "Arrange the steps for transforming an ER diagram into a physical relational database schema:",
            "puzzle_data": [
                "Map Strong Entity sets into individual relational tables",
                "Create junction tables with composite primary keys for M:N relationships",
                "Map 1:N relationships by placing foreign keys on the Many side",
                "Map Weak Entity sets including the identifying owner primary key"
            ],
            "correct_answer": [
                "Map Strong Entity sets into individual relational tables",
                "Map Weak Entity sets including the identifying owner primary key",
                "Map 1:N relationships by placing foreign keys on the Many side",
                "Create junction tables with composite primary keys for M:N relationships"
            ],
            "explanation": "Strong entities are created first, followed by weak entities, 1:N foreign keys, and finally associative junction tables for M:N relationships."
        },
        "quiz": [
            ("Which type of attribute is calculated dynamically from existing data (e.g., Age from DateOfBirth)?",
             ["A) Composite attribute", "B) Multivalued attribute", "C) Derived attribute", "D) Key attribute"],
             "C) Derived attribute", "Derived attributes are computed from base stored attributes.", "EASY"),
            ("How is a Many-to-Many (M:N) relationship between two entities represented in a relational database?",
             ["A) A single combined table with repeating columns", "B) An associative junction table with foreign keys", "C) Two foreign keys placed in both original tables", "D) A nested JSON array column only"],
             "B) An associative junction table with foreign keys", "M:N relationships require an intermediate junction table to prevent repeating groups.", "EASY"),
            ("A Weak Entity Set is identified by its own partial key (discriminator) combined with:",
             ["A) A random UUID", "B) The primary key of its identifying owner entity", "C) A timestamp index", "D) A secondary hash"],
             "B) The primary key of its identifying owner entity", "Weak entities depend on the identifying owner's primary key plus their partial discriminator.", "EASY"),
            ("In an ER diagram, if every entity in entity set E must participate in relationship R, the participation is:",
             ["A) Total (Mandatory)", "B) Partial (Optional)", "C) Transitive", "D) Reflexive"],
             "A) Total (Mandatory)", "Total participation means every entity in the set must participate in at least one relationship instance.", "EASY"),
            ("Which visual shape conventionally represents an Entity Set in standard Chen ER notation?",
             ["A) Diamond", "B) Rectangle", "C) Oval", "D) Parallelogram"],
             "B) Rectangle", "In Chen notation, rectangles denote entities, diamonds denote relationships, and ovals denote attributes.", "EASY")
        ]
    },
    {
        "order": 3,
        "title": "03 — Intermediate Concept: Database Normalization (1NF to BCNF)",
        "short_description": "Eliminate insertion, update, and deletion anomalies through functional dependencies and 1NF, 2NF, 3NF, BCNF.",
        "detailed_description": "Master functional dependencies, identify update anomalies, and decompose relations systematically through normal forms.",
        "difficulty": "MEDIUM",
        "estimated_minutes": 20,
        "topic": {
            "name": "Normalization",
            "desc": "Functional dependencies, candidate keys, update anomalies, 1NF, 2NF, 3NF, and Boyce-Codd Normal Form.",
            "difficulty": "MEDIUM"
        },
        "content": """# 03 — Intermediate Concept: Database Normalization (1NF to BCNF)

### Short explanation
Database Normalization is the rigorous mathematical process of organizing attributes and relations to minimize data redundancy and eliminate destructive update anomalies. By analyzing Functional Dependencies ($X \rightarrow Y$), databases decompose monolithic tables into lean, well-structured relations with lossless joins and preserved dependencies.

### Learning objectives
- Detect the three classic update anomalies: Insertion, Deletion, and Modification anomalies.
- Understand and calculate Candidate Keys from Functional Dependency sets.
- Step-by-step test and enforce 1NF, 2NF, 3NF, and BCNF.
- Guarantee Lossless Decomposition and Dependency Preservation during table splits.

### Key concepts
- **1NF (First Normal Form)**:
  - All attributes contain only atomic (indivisible) values.
  - No repeating groups or comma-separated lists in a single field.
- **2NF (Second Normal Form)**:
  - Must be in 1NF.
  - No *Partial Dependency*: No non-prime attribute may depend on a subset of a composite candidate key.
- **3NF (Third Normal Form)**:
  - Must be in 2NF.
  - No *Transitive Dependency*: For every functional dependency $X \rightarrow Y$, $X$ must be a superkey, or $Y$ is a prime attribute.
- **BCNF (Boyce-Codd Normal Form)**:
  - Stricter form of 3NF: For every functional dependency $X \rightarrow Y$, $X$ must be a superkey without exception.

### Example
```sql
-- Unnormalized table suffering from transitive dependency:
-- student_id -> (name, dept_id) and dept_id -> (dept_name, dept_head)
-- Splitting into two 3NF normalized tables:

CREATE TABLE departments_3nf (
    dept_id INT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    dept_head VARCHAR(100) NOT NULL
);

CREATE TABLE students_3nf (
    student_id INT PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    dept_id INT NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments_3nf(dept_id)
);
```

### Practical/application section
Imagine storing `(StudentID, CourseID, Professor, ProfessorOffice)`. If the professor moves offices, updating the record requires modifying thousands of student rows. If one row is missed, data becomes inconsistent (Modification Anomaly). If the last student drops the course, deleting that row destroys information about the professor's office (Deletion Anomaly). Normalization splits this into `CourseInstructors` and `Enrollments`.

### Quick recap
Normalization progressively eliminates partial and transitive dependencies, ensuring every fact is stored exactly once and that non-key attributes depend on the key, the whole key, and nothing but the key.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "Normal Form Progression Hierarchy",
            "question": "Arrange the normal forms in ascending order of rigor and strictness:",
            "puzzle_data": [
                "3NF (Third Normal Form — eliminates transitive dependencies)",
                "1NF (First Normal Form — eliminates non-atomic values)",
                "BCNF (Boyce-Codd Normal Form — every determinant is a superkey)",
                "2NF (Second Normal Form — eliminates partial dependencies)"
            ],
            "correct_answer": [
                "1NF (First Normal Form — eliminates non-atomic values)",
                "2NF (Second Normal Form — eliminates partial dependencies)",
                "3NF (Third Normal Form — eliminates transitive dependencies)",
                "BCNF (Boyce-Codd Normal Form — every determinant is a superkey)"
            ],
            "explanation": "Normal forms progress strictly from 1NF (atomic values) to 2NF (full functional dependency), 3NF (no transitive dependencies), and BCNF (determinant is superkey)."
        },
        "quiz": [
            ("A relation is in 2NF if it is in 1NF and contains no:",
             ["A) Primary keys", "B) Foreign keys", "C) Partial dependencies on composite candidate keys", "D) Indexed columns"],
             "C) Partial dependencies on composite candidate keys", "2NF eliminates partial dependencies where a non-prime attribute depends on part of a composite key.", "MEDIUM"),
            ("In functional dependency theory, if X -> Y and Y -> Z, then X -> Z represents:",
             ["A) Reflexivity", "B) Augmentation", "C) Transitivity", "D) Decomposition"],
             "C) Transitivity", "Transitivity rule states that if X determines Y and Y determines Z, X determines Z.", "MEDIUM"),
            ("A table that stores a comma-separated list of telephone numbers in a single column violates:",
             ["A) 1NF", "B) 2NF", "C) 3NF", "D) BCNF"],
             "A) 1NF", "1NF requires all values to be atomic; multiple numbers in one field violates atomicity.", "EASY"),
            ("What makes BCNF stricter than standard 3NF?",
             ["A) BCNF permits no foreign keys", "B) In BCNF, every determinant X in X -> Y must be a superkey", "C) BCNF only applies to tables with 2 columns", "D) BCNF requires denormalized caching"],
             "B) In BCNF, every determinant X in X -> Y must be a superkey", "BCNF removes the 3NF allowance where Y can be a prime attribute.", "MEDIUM"),
            ("A decomposition of relation R into R1 and R2 is Lossless if and only if R1 ∩ R2 forms a superkey for:",
             ["A) Neither R1 nor R2", "B) At least one of R1 or R2", "C) All tables in the database", "D) The master catalog"],
             "B) At least one of R1 or R2", "Lossless join decomposition requires the common attributes to form a candidate/super key of at least one sub-relation.", "HARD")
        ]
    },
    {
        "order": 4,
        "title": "04 — Practical Application: SQL Querying, Complex Joins & Aggregations",
        "short_description": "Write advanced relational queries using multi-table joins, subqueries, grouping, and analytical window functions.",
        "detailed_description": "Master SQL querying, logical query execution stages, INNER/OUTER joins, aggregate filtering with HAVING, and CTEs.",
        "difficulty": "MEDIUM",
        "estimated_minutes": 20,
        "topic": {
            "name": "SQL Queries & Joins",
            "desc": "INNER JOIN, LEFT/RIGHT/FULL JOIN, GROUP BY, HAVING, subqueries, and window functions.",
            "difficulty": "MEDIUM"
        },
        "content": """# 04 — Practical Application: SQL Querying, Complex Joins & Aggregations

### Short explanation
Structured Query Language (SQL) is the declarative language used to communicate with relational database management systems. Rather than programming procedural iteration loops, SQL developers declare what data is required, allowing the database query optimizer to determine the most efficient access path, index scans, and join algorithms.

### Learning objectives
- Understand the 6-stage Logical Query Processing Order (`FROM` $\rightarrow$ `WHERE` $\rightarrow$ `GROUP BY` $\rightarrow$ `HAVING` $\rightarrow$ `SELECT` $\rightarrow$ `ORDER BY`).
- Differentiate and implement `INNER JOIN`, `LEFT OUTER JOIN`, `RIGHT OUTER JOIN`, and `FULL OUTER JOIN`.
- Aggregate multi-row metrics using `GROUP BY`, `COUNT`, `AVG`, `SUM`, and filter groupings with `HAVING`.
- Write Common Table Expressions (CTEs) to simplify complex multi-step reporting queries.

### Key concepts
- **Join Semantics**:
  - *INNER JOIN*: Returns rows with matching keys in both tables.
  - *LEFT JOIN*: Returns all rows from the left table, with matching right table rows or NULLs.
  - *CROSS JOIN*: Produces the Cartesian product of two tables.
- **WHERE vs. HAVING**:
  - `WHERE` filters individual rows *before* aggregation.
  - `HAVING` filters aggregated groups *after* `GROUP BY` computation.

### Example
```sql
-- Analytical Query: Departmental academic performance with CTE and LEFT JOIN
WITH student_perf AS (
    SELECT 
        s.student_id,
        s.name,
        s.department_id,
        COALESCE(AVG(qa.percentage), 0) AS avg_score,
        COUNT(qa.id) AS total_quizzes
    FROM students s
    LEFT JOIN quiz_attempts qa ON s.student_id = qa.student_id
    GROUP BY s.student_id, s.name, s.department_id
)
SELECT 
    d.department_name,
    COUNT(sp.student_id) AS enrolled_students,
    ROUND(AVG(sp.avg_score), 2) AS dept_average_score
FROM departments d
INNER JOIN student_perf sp ON d.id = sp.department_id
GROUP BY d.department_name
HAVING COUNT(sp.student_id) >= 5
ORDER BY dept_average_score DESC;
```

### Practical/application section
In educational analytics platforms like SPECTRA, querying student completion requires combining `users`, `student_profiles`, `lesson_progress`, and `quiz_attempts`. Using an INNER JOIN would mistakenly drop newly registered students who have not yet attempted a quiz. Using a `LEFT JOIN` preserves all student profiles while evaluating completion stats.

### Quick recap
SQL processes queries through logical stages. Joins recombine normalized tables, aggregate functions summarize groupings, and CTEs provide clear, modular query architecture for enterprise reporting.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "Logical Query Execution Stages",
            "question": "Order the stages of SQL query execution in the sequence the database engine evaluates them:",
            "puzzle_data": [
                "SELECT & Window Functions",
                "WHERE (Row-level filtering)",
                "FROM & JOIN (Source table assembly)",
                "GROUP BY & HAVING (Grouping and aggregate filtering)",
                "ORDER BY & LIMIT / OFFSET"
            ],
            "correct_answer": [
                "FROM & JOIN (Source table assembly)",
                "WHERE (Row-level filtering)",
                "GROUP BY & HAVING (Grouping and aggregate filtering)",
                "SELECT & Window Functions",
                "ORDER BY & LIMIT / OFFSET"
            ],
            "explanation": "SQL engines first assemble tables (FROM/JOIN), filter rows (WHERE), group and aggregate (GROUP BY/HAVING), project columns (SELECT), and finally sort (ORDER BY)."
        },
        "quiz": [
            ("Which join type returns all rows from table A regardless of whether matching rows exist in table B?",
             ["A) INNER JOIN", "B) LEFT OUTER JOIN", "C) CROSS JOIN", "D) NATURAL JOIN"],
             "B) LEFT OUTER JOIN", "A LEFT OUTER JOIN preserves all left-table rows and fills missing right-table columns with NULL.", "EASY"),
            ("Why cannot an aggregate function like AVG() or COUNT() be used directly in a WHERE clause?",
             ["A) WHERE clauses only accept integers", "B) WHERE evaluates row-by-row before groupings are created", "C) Aggregates are only supported in MySQL", "D) WHERE clauses run after ORDER BY"],
             "B) WHERE evaluates row-by-row before groupings are created", "WHERE filters individual rows before GROUP BY aggregation; HAVING must be used for aggregate conditions.", "MEDIUM"),
            ("What is the primary architectural purpose of a Common Table Expression (WITH clause)?",
             ["A) Creating permanent physical disk files", "B) Defining named temporary result sets for modular query readability", "C) Bypassing foreign key constraints", "D) Encrypting database backups"],
             "B) Defining named temporary result sets for modular query readability", "CTEs create readable, reusable temporary result sets within a single SQL statement execution.", "MEDIUM"),
            ("If table A has 5 rows and table B has 10 rows, how many rows does a CROSS JOIN produce?",
             ["A) 15", "B) 5", "C) 50", "D) 0"],
             "C) 50", "A CROSS JOIN produces the Cartesian product of all rows: 5 * 10 = 50 rows.", "EASY"),
            ("Which SQL clause is evaluated last during query execution?",
             ["A) SELECT", "B) WHERE", "C) ORDER BY", "D) FROM"],
             "C) ORDER BY", "ORDER BY sorts the final projected result set and is evaluated last before LIMIT/OFFSET.", "EASY")
        ]
    },
    {
        "order": 5,
        "title": "05 — Advanced Concept: Transactions, ACID Properties & Concurrency Control",
        "short_description": "Ensure absolute data integrity through transactions, ACID guarantees, lock protocols, and isolation levels.",
        "detailed_description": "Deep dive into transaction lifecycles, concurrency phenomena, 2PL locking protocols, write-ahead logging, and isolation levels.",
        "difficulty": "HARD",
        "estimated_minutes": 20,
        "topic": {
            "name": "Transactions & ACID",
            "desc": "Atomicity, Consistency, Isolation, Durability, dirty reads, phantom reads, and 2-Phase Locking.",
            "difficulty": "HARD"
        },
        "content": """# 05 — Advanced Concept: Transactions, ACID Properties & Concurrency Control

### Short explanation
A Database Transaction is a logical unit of work comprising one or more database operations that must execute with absolute reliability. In multi-user and high-throughput cloud environments, transactions guarantee that unexpected server crashes, network disruptions, or concurrent writes never corrupt stored data.

### Learning objectives
- Explain the four pillars of ACID: Atomicity, Consistency, Isolation, and Durability.
- Identify the three classic concurrency anomalies: Dirty Reads, Non-repeatable Reads, and Phantom Reads.
- Differentiate between the 4 ANSI SQL Transaction Isolation Levels.
- Understand Two-Phase Locking (2PL) and Write-Ahead Logging (WAL) recovery mechanisms.

### Key concepts
- **ACID Architecture**:
  - *Atomicity*: All operations succeed (`COMMIT`) or all are rolled back (`ROLLBACK`). All-or-nothing.
  - *Consistency*: A transaction moves the database from one valid state satisfying all schema constraints to another.
  - *Isolation*: Concurrent transactions execute as if they were running in serial isolation.
  - *Durability*: Committed updates survive power loss or system crashes via Write-Ahead Logs (WAL).
- **Concurrency Anomalies**:
  - *Dirty Read*: Transaction A reads uncommitted data written by Transaction B that is subsequently rolled back.
  - *Non-repeatable Read*: Transaction A re-reads the same row and finds modified values committed by Transaction B.
  - *Phantom Read*: Transaction A re-executes a range query and discovers newly inserted rows committed by Transaction B.

### Example
```sql
-- Atomic bank transfer demonstrating transaction commit and rollback guards
BEGIN TRANSACTION;

UPDATE accounts 
SET balance = balance - 500.00 
WHERE account_id = 101 AND balance >= 500.00;

-- Verification guard
UPDATE accounts 
SET balance = balance + 500.00 
WHERE account_id = 202;

-- If both operations succeeded without constraint violation:
COMMIT;
-- In case of failure or insufficient funds:
-- ROLLBACK;
```

### Practical/application section
In registration systems, when a student enrolls in a high-demand course with 1 seat remaining, two simultaneous web requests could both read `seats_available = 1` and both issue an insert, causing over-enrollment. By executing within a transaction using `SELECT ... FOR UPDATE` or `SERIALIZABLE` isolation, the database locks the row and ensures only one student secures the seat.

### Quick recap
ACID properties guarantee enterprise data integrity. Concurrency control uses locking protocols and isolation levels to balance throughput against isolation anomalies, while write-ahead logging secures durability.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "SQL Isolation Levels Hierarchy",
            "question": "Arrange the 4 ANSI SQL isolation levels from lowest isolation (most anomalies) to highest isolation (strictest):",
            "puzzle_data": [
                "Serializable (Strict serial order, no phantoms)",
                "Read Committed (Prevents dirty reads)",
                "Read Uncommitted (Permits dirty reads)",
                "Repeatable Read (Prevents non-repeatable reads)"
            ],
            "correct_answer": [
                "Read Uncommitted (Permits dirty reads)",
                "Read Committed (Prevents dirty reads)",
                "Repeatable Read (Prevents non-repeatable reads)",
                "Serializable (Strict serial order, no phantoms)"
            ],
            "explanation": "Isolation levels increase in strictness from Read Uncommitted to Read Committed, Repeatable Read, and Serializable."
        },
        "quiz": [
            ("Which ACID property ensures that all modifications in a transaction either complete entirely or are fully rolled back?",
             ["A) Consistency", "B) Atomicity", "C) Isolation", "D) Durability"],
             "B) Atomicity", "Atomicity guarantees the all-or-nothing execution of transaction operations.", "EASY"),
            ("A 'Dirty Read' anomaly occurs when a transaction reads data that:",
             ["A) Has been deleted 30 days ago", "B) Was written by an uncommitted concurrent transaction that might rollback", "C) Is stored on an unindexed table", "D) Has a NULL primary key"],
             "B) Was written by an uncommitted concurrent transaction that might rollback", "Dirty reads expose uncommitted changes that could subsequently be aborted and reverted.", "MEDIUM"),
            ("How does Write-Ahead Logging (WAL) ensure the Durability property in modern databases?",
             ["A) By saving backups directly to tape", "B) By writing log records to durable disk storage before modifying memory buffer pages", "C) By disabling concurrent user logins", "D) By running weekly table vacuuming"],
             "B) By writing log records to durable disk storage before modifying memory buffer pages", "WAL mandates that transaction redo log records must reach non-volatile disk before dirty memory pages are flushed.", "HARD"),
            ("Which isolation level completely prevents dirty reads, non-repeatable reads, and phantom reads?",
             ["A) Read Uncommitted", "B) Read Committed", "C) Repeatable Read", "D) Serializable"],
             "D) Serializable", "Serializable is the highest isolation level and guarantees execution equivalent to strict serial order.", "MEDIUM"),
            ("In Two-Phase Locking (2PL), once a transaction releases any lock, it enters the:",
             ["A) Growing Phase", "B) Shrinking Phase", "C) Commit Phase", "D) Deadlock Phase"],
             "B) Shrinking Phase", "In 2PL, once a transaction releases a lock, it enters the shrinking phase and cannot acquire any new locks.", "HARD")
        ]
    },
    {
        "order": 6,
        "title": "06 — Practice / Problem Solving: Indexing Strategies, B-Trees & Query Optimization",
        "short_description": "Boost database read performance from O(N) full scans to O(log N) indexed searches with B-Trees and execution plans.",
        "detailed_description": "Analyze query performance, understand B-Tree index mechanics, clustered vs non-clustered indices, and EXPLAIN ANALYZE.",
        "difficulty": "HARD",
        "estimated_minutes": 20,
        "topic": {
            "name": "Indexing & Optimization",
            "desc": "B-Trees, B+Trees, clustered indices, secondary indices, EXPLAIN query plans, and SARGable predicates.",
            "difficulty": "HARD"
        },
        "content": r"""# 06 — Practice / Problem Solving: Indexing Strategies, B-Trees & Query Optimization

### Short explanation
Without indices, searching a database table with 10 million rows requires scanning every single disk page from beginning to end ($O(N)$ Sequential Scan). An index is a specialized, auxiliary disk data structure—typically a self-balancing B+Tree—that allows the database engine to find specific records in logarithmic time ($O(\log N)$) through few disk I/O operations.

### Learning objectives
- Understand how B+Tree search trees organize root, internal branch, and leaf page nodes.
- Differentiate between Clustered Index (physical row storage order) and Non-Clustered Secondary Indices.
- Read and evaluate query execution plans using `EXPLAIN ANALYZE`.
- Recognize and eliminate non-SARGable query patterns that defeat index utilization.

### Key concepts
- **B+Tree Architecture**:
  - All data rows or record pointers reside exclusively in the *leaf nodes*.
  - Leaf nodes are linked sequentially as a doubly linked list, enabling hyper-fast range scans (`WHERE age BETWEEN 20 AND 30`).
- **Clustered vs. Non-Clustered**:
  - *Clustered Index*: Dictates the physical sort order of rows on disk. Exactly one per table (usually the primary key).
  - *Non-Clustered Index*: A separate tree whose leaf nodes store the indexed key and a pointer (or clustered key) back to the base row.
- **SARGable Predicates**: Search Argument Able. Writing queries where index keys are not wrapped in functions (e.g., `WHERE YEAR(created_at) = 2026` is non-SARGable; `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'` is SARGable).

### Example
```sql
-- Creating composite index optimized for multi-column lookup
CREATE INDEX idx_student_dept_enrolled ON students (dept_id, enrolled_at);

-- Inspecting execution plan: Index Scan vs. Sequential Scan
EXPLAIN ANALYZE
SELECT student_id, first_name, email
FROM students
WHERE dept_id = 4 AND enrolled_at >= '2026-01-01';
-- The query planner uses the index to jump directly to dept_id = 4 leaf pages!
```

### Practical/application section
When an e-commerce order table grows to 50 million records, running `SELECT * FROM orders WHERE customer_id = 94821` takes 14 seconds on a full table scan. Adding a non-clustered index on `customer_id` reduces the lookup to 3 disk page reads, returning the result in under 2 milliseconds.

### Quick recap
B+Tree indices accelerate query performance from linear scans to logarithmic lookups. Care must be taken with composite index column ordering and write-overhead trade-offs.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "Query Tuning Optimization Workflow",
            "question": "Arrange the steps for diagnosing and optimizing a slow database query in the correct logical sequence:",
            "puzzle_data": [
                "Run EXPLAIN ANALYZE to identify sequential scans and high-cost operators",
                "Detect slow queries in production using query logs (e.g. pg_stat_statements)",
                "Design a targeted B-Tree or composite index matching the WHERE/JOIN predicates",
                "Re-run EXPLAIN ANALYZE to verify index scan usage and reduced buffer hits"
            ],
            "correct_answer": [
                "Detect slow queries in production using query logs (e.g. pg_stat_statements)",
                "Run EXPLAIN ANALYZE to identify sequential scans and high-cost operators",
                "Design a targeted B-Tree or composite index matching the WHERE/JOIN predicates",
                "Re-run EXPLAIN ANALYZE to verify index scan usage and reduced buffer hits"
            ],
            "explanation": "Query optimization begins with monitoring detection, moves through execution plan analysis, index design, and verification."
        },
        "quiz": [
            ("Why are B+Trees preferred over standard binary search trees for disk-based database indices?",
             ["A) B+Trees are unindexed", "B) B+Trees have high fan-out, shallow depth, and minimize slow disk I/O", "C) B+Trees only work in main memory RAM", "D) Binary search trees store duplicate keys"],
             "B) B+Trees have high fan-out, shallow depth, and minimize slow disk I/O", "B+Trees feature high fan-out (thousands of keys per page), ensuring tree depth rarely exceeds 3 or 4 levels on disk.", "HARD"),
            ("How many Clustered Indices can a single relational database table possess?",
             ["A) Zero", "B) Exactly one", "C) Up to 256", "D) Unlimited"],
             "B) Exactly one", "Because the clustered index defines the actual physical sort order of data rows on disk, a table can only have one.", "EASY"),
            ("Which WHERE predicate pattern is non-SARGable and prevents the engine from utilizing an index on birth_date?",
             ["A) WHERE birth_date >= '2000-01-01'", "B) WHERE YEAR(birth_date) = 2000", "C) WHERE birth_date BETWEEN '2000-01-01' AND '2000-12-31'", "D) WHERE birth_date = '2000-05-15'"],
             "B) WHERE YEAR(birth_date) = 2000", "Wrapping the column in a function prevents index traversal because the engine must evaluate the function on every row.", "MEDIUM"),
            ("What is a primary trade-off of adding multiple indices to a high-write table?",
             ["A) Read queries slow down", "B) Write operations (INSERT, UPDATE, DELETE) become slower due to index maintenance", "C) Foreign keys stop functioning", "D) Database tables become read-only"],
             "B) Write operations (INSERT, UPDATE, DELETE) become slower due to index maintenance", "Every inserted or deleted row requires updating every index structure on that table.", "MEDIUM"),
            ("What information does EXPLAIN ANALYZE provide that plain EXPLAIN does not?",
             ["A) The SQL syntax grammar rules", "B) Actual execution runtime, actual loop counts, and exact memory buffer hits", "C) The table's primary key constraint", "D) The database version number"],
             "B) Actual execution runtime, actual loop counts, and exact memory buffer hits", "EXPLAIN ANALYZE actually executes the query and measures real timings vs planner estimates.", "MEDIUM")
        ]
    },
    {
        "order": 7,
        "title": "07 — Real-world Application: Distributed Databases, Replication & NoSQL Systems",
        "short_description": "Scale enterprise architectures horizontally with replication topologies, sharding, the CAP Theorem, and NoSQL models.",
        "detailed_description": "Explore distributed database trade-offs, Primary-Replica replication, sharding strategies, CAP/PACELC theorems, and NoSQL categories.",
        "difficulty": "HARD",
        "estimated_minutes": 25,
        "topic": {
            "name": "Distributed Databases & NoSQL",
            "desc": "CAP theorem, horizontal sharding, leader-follower replication, document stores, key-value stores, and distributed ACID.",
            "difficulty": "HARD"
        },
        "content": """# 07 — Real-world Application: Distributed Databases, Replication & NoSQL Systems

### Short explanation
When enterprise systems exceed the CPU, RAM, or storage capacities of a single physical server, databases must scale horizontally across clusters of networked machines. Distributed databases provide fault tolerance and massive throughput, requiring software engineers to navigate fundamental trade-offs between consistency, availability, and network latency.

### Learning objectives
- Analyze architectural trade-offs using the CAP Theorem (Consistency, Availability, Partition Tolerance) and PACELC theorem.
- Differentiate between Primary-Replica (Leader-Follower) and Multi-Master replication models.
- Implement Horizontal Sharding using Range-Based vs. Hash-Based partition keys.
- Categorize NoSQL architectures: Document (MongoDB), Key-Value (Redis), Wide-Column (Cassandra), and Graph (Neo4j).

### Key concepts
- **CAP Theorem**: In the presence of a network partition ($P$), a distributed system must choose between:
  - *Consistency ($CP$)*: Return error or wait for acknowledgment; guarantees every read gets the most recent write.
  - *Availability ($AP$)*: Return the best available local replica data immediately; permits stale reads.
- **Replication Topologies**:
  - *Synchronous Replication*: Primary waits for replica write acknowledgment. Strong consistency, higher latency.
  - *Asynchronous Replication*: Primary acknowledges write immediately; replicates in background. Lower latency, risks data loss on crash.
- **Sharding Strategies**: Partitioning data across multiple database instances based on a shard key (e.g. `tenant_id` or `user_id`).

### Example
```text
Distributed Microservice Architecture:
                     ┌───────────────────────┐
                     │ API Gateway / Client  │
                     └──────────┬────────────┘
                                │
        ┌───────────────────────┴───────────────────────┐
        ▼                                               ▼
┌─────────────────────────┐                 ┌─────────────────────────┐
│ Primary Database (RDBMS)│ (Async Replica) │ Read Replicas (RDBMS)   │
│ Handles INSERT / UPDATE ├────────────────►│ Handles heavy analytics │
└─────────────────────────┘                 └─────────────────────────┘
        │
        ▼ (Caching layer)
┌─────────────────────────┐
│ Redis In-Memory Cluster │ (Sub-millisecond session lookup)
└─────────────────────────┘
```

### Practical/application section
A global learning platform like SPECTRA utilizes PostgreSQL for student credentials, enrollments, and transactions where ACID integrity is mandatory. In tandem, it uses Redis for in-memory session tokens and leaderboard streaks ($O(1)$ operations), and a distributed Document store or S3 for large learning media assets.

### Quick recap
Distributed architectures overcome single-node hardware limits. The CAP theorem dictates trade-offs between consistency and availability during network partitions, while polyglot persistence pairs relational engines with specialized NoSQL stores.
""",
        "puzzle": {
            "type": "ORDERING",
            "title": "Scaling Relational Databases Architecture",
            "question": "Arrange database scaling strategies in order of architectural complexity, starting from single-node optimization:",
            "puzzle_data": [
                "Horizontal Sharding across multiple independent database clusters",
                "Vertical Scaling (Upgrading single server CPU, RAM, and NVMe SSDs)",
                "Read-Replication (Offloading SELECT queries to read replicas)",
                "In-Memory Caching (Adding Redis/Memcached to shield the database)"
            ],
            "correct_answer": [
                "Vertical Scaling (Upgrading single server CPU, RAM, and NVMe SSDs)",
                "In-Memory Caching (Adding Redis/Memcached to shield the database)",
                "Read-Replication (Offloading SELECT queries to read replicas)",
                "Horizontal Sharding across multiple independent database clusters"
            ],
            "explanation": "Systems scale first by upgrading hardware (Vertical), adding caching (Redis), introducing Read Replicas, and finally implementing complex Sharding."
        },
        "quiz": [
            ("According to the CAP Theorem, when a network partition (P) occurs, a distributed database must choose between:",
             ["A) Performance and Security", "B) Consistency (C) and Availability (A)", "C) SQL and NoSQL", "D) Backup and Recovery"],
             "B) Consistency (C) and Availability (A)", "The CAP theorem proves that in the event of network partition, a system can maintain Consistency or Availability, but not both.", "MEDIUM"),
            ("Which NoSQL database category is specifically optimized for high-speed sub-millisecond key lookups and in-memory caches?",
             ["A) Key-Value Store (e.g., Redis)", "B) Graph Database (e.g., Neo4j)", "C) Relational Store (e.g., SQLite)", "D) Object-Relational Database"],
             "A) Key-Value Store (e.g., Redis)", "Key-value stores like Redis store data in RAM to deliver microsecond lookup latencies.", "EASY"),
            ("What is Horizontal Sharding in database system design?",
             ["A) Purchasing a bigger single server with more RAM", "B) Partitioning table rows across multiple distinct database servers based on a shard key", "C) Creating secondary indices on all columns", "D) Converting all tables to CSV files"],
             "B) Partitioning table rows across multiple distinct database servers based on a shard key", "Sharding splits rows across multiple database servers to distribute storage and write capacity horizontally.", "MEDIUM"),
            ("What is an eventual consistency model in distributed data storage?",
             ["A) Replicas will never reach the same value", "B) All replicas will eventually converge on the same data value if no new updates are made", "C) Transactions are immediately rolled back", "D) Every query must execute on the primary leader node"],
             "B) All replicas will eventually converge on the same data value if no new updates are made", "Eventual consistency guarantees that all replicas will sync and converge given sufficient time.", "MEDIUM"),
            ("Which replication model allows write operations to be accepted by any node in the cluster?",
             ["A) Single-Leader Replication", "B) Multi-Leader (Multi-Master) Replication", "C) Read-Only Replication", "D) Snapshot Mirroring"],
             "B) Multi-Leader (Multi-Master) Replication", "In multi-leader setups, multiple nodes can accept writes and synchronize changes between each other.", "HARD")
        ]
    }
]


def seed_dbms_curriculum():
    print("=" * 60)
    print("SPECTRA – Seeding 7 Connected Lessons for DBMS (Subject ID=3)")
    print("=" * 60)

    create_tables()
    db = SessionLocal()

    try:
        # Find or create DBMS subject
        dbms = db.query(Subject).filter(Subject.code == "DBMS").first()
        if not dbms:
            dbms = db.query(Subject).filter(Subject.name.ilike("%Database%")).first()
        if not dbms:
            dbms = Subject(
                name="Database Management Systems",
                code="DBMS",
                description="Master relational database architecture, ER modeling, SQL querying, normalization, transactions, indexing, and distributed data systems.",
                category="COMPUTER_SCIENCE",
                difficulty_level="INTERMEDIATE",
                display_order=3,
                is_active=True
            )
            db.add(dbms)
            db.flush()

        print(f"[OK] Subject: {dbms.name} (ID: {dbms.id}, Code: {dbms.code})")

        # Clean existing lessons for this subject if re-seeding to keep exactly 7 clean sequential lessons
        # Keep any progress safely or clean orphaned lessons
        existing_lessons = db.query(Lesson).filter(Lesson.subject_id == dbms.id).all()
        existing_by_order = {l.lesson_order: l for l in existing_lessons}

        for l_data in DBMS_LESSONS_DATA:
            order = l_data["order"]
            title = l_data["title"]
            short_desc = l_data["short_description"]
            detailed_desc = l_data["detailed_description"]
            diff = l_data["difficulty"]
            est_min = l_data["estimated_minutes"]
            content = l_data["content"]
            t_data = l_data["topic"]

            # Create or update Topic
            topic = db.query(Topic).filter(
                Topic.subject_id == dbms.id,
                Topic.name == t_data["name"]
            ).first()
            if not topic:
                topic = Topic(
                    subject_id=dbms.id,
                    name=t_data["name"],
                    description=t_data["desc"],
                    difficulty_level=t_data["difficulty"],
                    display_order=order,
                    is_active=True
                )
                db.add(topic)
                db.flush()

            # Create or update Lesson
            lesson = existing_by_order.get(order)
            if not lesson:
                # Check by title
                lesson = db.query(Lesson).filter(
                    Lesson.subject_id == dbms.id,
                    Lesson.title == title
                ).first()

            if not lesson:
                lesson = Lesson(
                    subject_id=dbms.id,
                    topic_id=topic.id,
                    title=title,
                    short_description=short_desc,
                    detailed_description=detailed_desc,
                    description=short_desc,
                    content=content,
                    difficulty=diff,
                    difficulty_level=diff,
                    estimated_minutes=est_min,
                    estimated_duration=est_min,
                    lesson_order=order,
                    display_order=order,
                    is_active=True
                )
                db.add(lesson)
                db.flush()
                print(f"[CREATED] Lesson {order}: {title} (ID: {lesson.id})")
            else:
                lesson.topic_id = topic.id
                lesson.title = title
                lesson.short_description = short_desc
                lesson.detailed_description = detailed_desc
                lesson.description = short_desc
                lesson.content = content
                lesson.difficulty = diff
                lesson.difficulty_level = diff
                lesson.estimated_minutes = est_min
                lesson.estimated_duration = est_min
                lesson.lesson_order = order
                lesson.display_order = order
                lesson.is_active = True
                db.flush()
                print(f"[UPDATED] Lesson {order}: {title} (ID: {lesson.id})")

            # Link topic back to lesson
            topic.lesson_id = lesson.id

            # Seed Interactive Puzzle for this lesson
            p_data = l_data["puzzle"]
            existing_puzzle = db.query(Puzzle).filter(Puzzle.lesson_id == lesson.id).first()
            if not existing_puzzle:
                p_pdata = json.dumps(p_data["puzzle_data"]) if not isinstance(p_data["puzzle_data"], str) else p_data["puzzle_data"]
                p_canswer = json.dumps(p_data["correct_answer"]) if not isinstance(p_data["correct_answer"], str) else p_data["correct_answer"]
                puzzle = Puzzle(
                    subject_id=dbms.id,
                    topic_id=topic.id,
                    lesson_id=lesson.id,
                    puzzle_type=p_data["type"],
                    title=p_data["title"],
                    question=p_data["question"],
                    difficulty=diff,
                    puzzle_data=p_pdata,
                    correct_answer=p_canswer,
                    explanation=p_data.get("explanation"),
                    display_order=1,
                    is_active=True
                )
                db.add(puzzle)
                db.flush()

            # Seed Quiz and Questions for this lesson
            q_list = l_data["quiz"]
            existing_quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson.id).first()
            if not existing_quiz:
                quiz = Quiz(
                    subject_id=dbms.id,
                    topic_id=topic.id,
                    lesson_id=lesson.id,
                    title=f"Quiz: {t_data['name']}",
                    description=f"5-question knowledge checkpoint on {t_data['name']}.",
                    quiz_type="CONCEPT",
                    difficulty=diff,
                    question_count=len(q_list)
                )
                db.add(quiz)
                db.flush()

                for q_idx, (q_text, opts, ans, expl, q_diff) in enumerate(q_list, start=1):
                    opts_str = json.dumps(opts) if isinstance(opts, list) else opts
                    question = Question(
                        subject_id=dbms.id,
                        topic_id=topic.id,
                        lesson_id=lesson.id,
                        question_text=q_text,
                        question_type="MCQ",
                        options=opts_str,
                        correct_answer=ans,
                        explanation=expl,
                        difficulty=q_diff
                    )
                    db.add(question)
                    db.flush()

                    quiz_q = QuizQuestion(
                        quiz_id=quiz.id,
                        question_id=question.id,
                        order_index=q_idx
                    )
                    db.add(quiz_q)

        db.commit()
        print("\n[SUCCESS] Successfully seeded all 7 lessons for DBMS!")

        # Verify
        total_lessons = db.query(Lesson).filter(Lesson.subject_id == dbms.id).count()
        print(f"[VERIFIED] DBMS now has {total_lessons} active lessons.")

    except Exception as exc:
        db.rollback()
        print(f"[ERROR] Failed to seed DBMS lessons: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_dbms_curriculum()
