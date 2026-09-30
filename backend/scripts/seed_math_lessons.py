"""
Seed 7 logically ordered, high-quality lessons for Mathematics for Computing (Subject ID=12).
Covers:
Lesson 1 — Fundamentals: Propositional Logic, Boolean Algebra & Set Theory
Lesson 2 — Core Concepts: Number Theory, Modular Arithmetic & Cryptographic Primes
Lesson 3 — Intermediate Concept: Vectors, Matrices & Systems of Linear Equations
Lesson 4 — Practical Application: Matrix Transformations, Eigenvalues & PageRank
Lesson 5 — Advanced Concept: Probability Distributions, Expectation & Bayes' Theorem
Lesson 6 — Practice / Problem Solving: Differential Calculus, Derivatives & Gradient Optimization
Lesson 7 — Real-world Application: Graph Theory, Network Flow & Algorithmic Complexity
"""
import sys
import os
import json

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_dir)

from app.db.database import SessionLocal, create_tables
from app.db.models.academic import Subject, Topic, Lesson, StudyResource
from app.db.models.quiz import Quiz, Question, QuizQuestion
from app.db.models.puzzle import Puzzle
from app.services.youtube_service import get_or_create_lesson_youtube_recommendations

MATH_LESSONS_DATA = [
    {
        "order": 1,
        "title": "01 — Fundamentals: Propositional Logic, Boolean Algebra & Set Theory",
        "short_description": "Foundations of mathematical reasoning, truth tables, logical connectives, and set operations.",
        "difficulty": "EASY",
        "estimated_minutes": 20,
        "topic": {
            "name": "Propositional Logic & Set Theory",
            "desc": "Logical propositions, truth values, boolean operators, Venn diagrams, and set cardinalities."
        },
        "content": r"""# Propositional Logic, Boolean Algebra & Set Theory

Mathematics for computing begins with formal mathematical reasoning: establishing what statements are true, under what conditions, and how truth values combine to produce dependable software systems.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- Formulate mathematical statements using propositional variables ($p, q, r$).
- Construct and evaluate truth tables for conjunction ($\land$), disjunction ($\lor$), negation ($\neg$), implication ($\rightarrow$), and biconditional ($\leftrightarrow$).
- Apply De Morgan's Laws and Boolean algebra identities to simplify conditional branching in software.
- Perform set operations including union ($\cup$), intersection ($\cap$), difference ($\setminus$), and Cartesian products ($A \times B$).

---

## 2. Core Concepts

### 2.1 Propositions and Truth Values
A **proposition** is a declarative statement that is either strictly **True (T)** or **False (F)**, but never both simultaneously.
- Proposition: *"The database transaction committed successfully."* (True or False)
- Non-proposition: *"Optimize this query!"* (An imperative command)

### 2.2 Truth Table of Core Connectives
| $p$ | $q$ | $\neg p$ | $p \land q$ | $p \lor q$ | $p \rightarrow q$ | $p \leftrightarrow q$ |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| T | T | F | T | T | T | T |
| T | F | F | F | T | F | F |
| F | T | T | F | T | T | F |
| F | F | T | F | F | T | T |

> **Crucial Rule:** The conditional $p \rightarrow q$ is False **only** when a True premise leads to a False conclusion. If the premise $p$ is False, the implication is vacuously True!

### 2.3 De Morgan's Laws in Code
$$\neg(p \land q) \equiv \neg p \lor \neg q$$
$$\neg(p \lor q) \equiv \neg p \land \neg q$$

In programming, this identity is vital for simplifying defensive `if` conditions:
```python
# Before simplification:
if not (user.is_authenticated and user.has_active_subscription):
    return redirect("/login")

# Equivalent via De Morgan's Law:
if not user.is_authenticated or not user.has_active_subscription:
    return redirect("/login")
```

---

## 3. Concrete Example: Access Control Evaluation
Suppose an API endpoint requires:
- $p$: User has admin role
- $q$: Request originates from an internal VPN
- $r$: Multi-Factor Authentication (MFA) was verified

Security policy: Allow access if $(p \land q) \lor (p \land r)$.
Using distributive laws of Boolean algebra:
$$(p \land q) \lor (p \land r) \equiv p \land (q \lor r)$$
This reduces two database lookups to one combined condition, saving CPU cycles at scale.

---

## 4. Practical Application: Set Theory in Relational Databases
Relational databases are direct physical implementations of E.F. Codd's Relational Algebra, which is built entirely on mathematical set theory:
- **Set Union ($A \cup B$)**: `SELECT id FROM Students UNION SELECT id FROM Teachers;`
- **Set Intersection ($A \cap B$)**: `SELECT id FROM Students INTERSECT SELECT id FROM Athletes;`
- **Set Difference ($A \setminus B$)**: `SELECT id FROM Students EXCEPT SELECT id FROM Graduated;`
- **Cartesian Product ($A \times B$)**: `CROSS JOIN` generating all ordered pairs $(a, b)$.

---

## 5. Quick Recap
- A proposition has a definitive binary truth value ($T$ or $F$).
- $p \rightarrow q$ evaluates to True whenever $p$ is False, regardless of $q$.
- De Morgan's laws allow rewriting inverted conjunctions and disjunctions.
- Sets are collections of distinct elements; relational operations (UNION, INTERSECT, EXCEPT) derive directly from set theory.
""",
        "resources": [
            ("MIT OpenCourseWare: Mathematics for Computer Science", "Lecture notes and video units on logic, proofs, and sets.", "https://ocw.mit.edu/courses/6-042j-mathematics-for-computer-science-fall-2010/", "DOCUMENTATION", "MIT OCW"),
            ("Stanford CS103: Mathematical Foundations of Computing", "Discrete mathematics and mathematical reasoning for CS undergraduates.", "https://web.stanford.edu/class/cs103/", "ARTICLE", "Stanford University")
        ],
        "puzzle": {
            "type": "ORDERING",
            "title": "Logical Operator Precedence Ordering",
            "question": "Arrange the Boolean logic operators in standard mathematical order of precedence from highest (evaluated first) to lowest (evaluated last):",
            "puzzle_data": [
                "Disjunction (OR: ∨)",
                "Negation (NOT: ¬)",
                "Implication (→)",
                "Conjunction (AND: ∧)"
            ],
            "correct_answer": [
                "Negation (NOT: ¬)",
                "Conjunction (AND: ∧)",
                "Disjunction (OR: ∨)",
                "Implication (→)"
            ],
            "explanation": "Standard logical operator precedence evaluates Negation first, followed by Conjunction (AND), Disjunction (OR), and finally Conditional/Implication."
        },
        "quiz": [
            ("Under what single condition is the conditional statement p -> q FALSE?",
             ["A) p is False and q is False", "B) p is True and q is False", "C) p is False and q is True", "D) p is True and q is True"],
             "B) p is True and q is False", "An implication p -> q is only false when a true premise leads to a false conclusion.", "EASY"),
            ("According to De Morgan's Laws, the negation of (A AND B) is equivalent to:",
             ["A) (NOT A) AND (NOT B)", "B) (NOT A) OR (NOT B)", "C) NOT (A OR B)", "D) A OR B"],
             "B) (NOT A) OR (NOT B)", "De Morgan's law states that ~(A ^ B) = ~A v ~B.", "EASY"),
            ("What is the Cartesian Product of set A = {1, 2} and set B = {x, y}?",
             ["A) {1x, 2y}", "B) {(1,x), (1,y), (2,x), (2,y)}", "C) {1, 2, x, y}", "D) 4"],
             "B) {(1,x), (1,y), (2,x), (2,y)}", "The Cartesian product A x B is the set of all ordered pairs (a, b) where a in A and b in B.", "EASY"),
            ("A compound proposition that is always True regardless of the truth values of its variables is called a:",
             ["A) Contradiction", "B) Contingency", "C) Tautology", "D) Predicate"],
             "C) Tautology", "A tautology is a logical formula that is true under every possible interpretation.", "EASY"),
            ("If Set A has 5 elements and Set B has 3 elements, what is the cardinality of the power set of B?",
             ["A) 6", "B) 8", "C) 9", "D) 16"],
             "B) 8", "The power set of any finite set with n elements has 2^n elements. For n=3, 2^3 = 8.", "EASY")
        ]
    },
    {
        "order": 2,
        "title": "02 — Core Concepts: Number Theory, Modular Arithmetic & Cryptographic Primes",
        "short_description": "Divisibility, modular congruences, Euclidean GCD algorithm, and prime numbers in modern encryption.",
        "difficulty": "EASY",
        "estimated_minutes": 25,
        "topic": {
            "name": "Fractions & Number Theory",
            "desc": "Divisibility, modular arithmetic, prime numbers, Euclid GCD, and RSA foundations."
        },
        "content": r"""# Number Theory, Modular Arithmetic & Cryptographic Primes

Number theory—once considered the purest and least applied branch of mathematics—now secures every encrypted HTTPS connection, password hash, and digital signature across the internet.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- Compute modular arithmetic congruences: $a \equiv b \pmod{m}$.
- Implement the Euclidean Algorithm and Extended Euclidean Algorithm for Greatest Common Divisor ($\gcd$).
- Compute modular multiplicative inverses using Bézout's identity.
- Explain the role of large prime numbers in the RSA asymmetric encryption cryptosystem.

---

## 2. Core Concepts

### 2.1 The Division Algorithm and Modular Congruence
For any integer $a$ and positive integer $m$, there exist unique integers $q$ (quotient) and $r$ (remainder) such that:
$$a = q \cdot m + r, \quad 0 \le r < m$$

We write $a \equiv b \pmod{m}$ if $m$ evenly divides the difference $(a - b)$.
Example:
$$17 \equiv 5 \pmod{12} \quad \text{because } 17 - 5 = 12 = 1 \times 12$$

### 2.2 Properties of Modular Arithmetic
Modular arithmetic preserves addition and multiplication:
$$(a + b) \pmod m = ((a \pmod m) + (b \pmod m)) \pmod m$$
$$(a \cdot b) \pmod m = ((a \pmod m) \cdot (b \pmod m)) \pmod m$$
This property allows computing astronomical numbers without 64-bit integer overflow!

### 2.3 Euclidean Algorithm for GCD
To find $\gcd(a, b)$:
$$\gcd(a, b) = \gcd(b, a \pmod b) \quad \text{until } b = 0$$

```python
def gcd(a: int, b: int) -> int:
    while b != 0:
        a, b = b, a % b
    return a

print(gcd(252, 105)) # Output: 21
```

---

## 3. Concrete Example: Modular Multiplicative Inverse
In standard arithmetic, the multiplicative inverse of $5$ is $\frac{1}{5} = 0.2$. In modular arithmetic with modulus $m=7$, we seek an integer $x$ such that:
$$5x \equiv 1 \pmod 7$$
Testing values:
- $5 \times 1 = 5 \equiv 5 \pmod 7$
- $5 \times 2 = 10 \equiv 3 \pmod 7$
- $5 \times 3 = 15 \equiv 1 \pmod 7$ $\rightarrow$ Thus, $x = 3$ is the modular inverse of $5 \pmod 7$!

---

## 4. Practical Application: RSA Public-Key Cryptography
RSA security rests on the **asymmetry of prime multiplication versus prime factorization**:
1. Pick two massive primes $p$ and $q$ (each 1024+ bits).
2. Calculate modulus $n = p \cdot q$.
3. Compute Euler's totient function $\phi(n) = (p - 1)(q - 1)$.
4. Choose public exponent $e$ such that $\gcd(e, \phi(n)) = 1$.
5. Compute private exponent $d \equiv e^{-1} \pmod{\phi(n)}$.

Multiplying $p \times q$ takes milliseconds. Finding $p$ and $q$ given only $n$ takes millions of CPU years with known classical algorithms.

---

## 5. Quick Recap
- Modular arithmetic behaves like clock arithmetic, wrapping around at modulus $m$.
- Euclidean algorithm computes greatest common divisors in $O(\log(\min(a, b)))$ steps.
- Modular inverses exist if and only if $\gcd(a, m) = 1$.
- Asymmetric encryption (RSA) relies on the computational hardness of integer prime factorization.
""",
        "resources": [
            ("Khan Academy: Modular Arithmetic & Cryptography", "Interactive lessons on modular addition, inverses, and cryptography.", "https://www.khanacademy.org/computing/computer-science/cryptography", "TUTORIAL", "Khan Academy"),
            ("GeeksforGeeks: Extended Euclidean Algorithm", "Algorithm implementation with C++, Python, and Java code snippets.", "https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/", "ARTICLE", "GeeksforGeeks")
        ],
        "puzzle": {
            "type": "FILL_BLANK",
            "title": "Modular Arithmetic Calculation",
            "question": "What is the remainder when (13 * 17) is evaluated modulo 5?",
            "puzzle_data": {
                "hint": "Use the property: (a * b) mod m = ((a mod m) * (b mod m)) mod m."
            },
            "correct_answer": "1",
            "explanation": "13 mod 5 = 3; 17 mod 5 = 2. Then (3 * 2) = 6. Finally, 6 mod 5 = 1. Alternatively, 13 * 17 = 221, and 221 mod 5 = 1."
        },
        "quiz": [
            ("What is gcd(48, 18) computed via Euclid's algorithm?",
             ["A) 3", "B) 6", "C) 12", "D) 2"],
             "B) 6", "48 = 2 * 18 + 12; 18 = 1 * 12 + 6; 12 = 2 * 6 + 0. The last non-zero remainder is 6.", "EASY"),
            ("Two integers a and b are called coprime (relatively prime) if:",
             ["A) Both a and b are prime numbers", "B) gcd(a, b) = 1", "C) a mod b = 0", "D) a + b is prime"],
             "B) gcd(a, b) = 1", "Two numbers are coprime if their greatest common divisor is 1.", "EASY"),
            ("In RSA cryptography, what mathematical problem provides the primary computational security guarantee?",
             ["A) Sorting large arrays", "B) Prime factorization of the product of two large primes", "C) Computing the determinant of a matrix", "D) Inverting a binary tree"],
             "B) Prime factorization of the product of two large primes", "RSA relies on the difficulty of factoring the product of two very large prime numbers.", "EASY"),
            ("What is 23 mod 7?",
             ["A) 1", "B) 2", "C) 3", "D) 4"],
             "B) 2", "23 = 3 * 7 + 2, so the remainder is 2.", "EASY"),
            ("Under what condition does the modular multiplicative inverse of a modulo m exist?",
             ["A) a must be greater than m", "B) gcd(a, m) must equal 1", "C) m must be an even number", "D) a must be a prime number"],
             "B) gcd(a, m) must equal 1", "a has a modular inverse modulo m if and only if a and m are coprime (gcd(a, m) = 1).", "EASY")
        ]
    },
    {
        "order": 3,
        "title": "03 — Intermediate Concept: Vectors, Matrices & Systems of Linear Equations",
        "short_description": "Vector spaces, dot products, matrix algebra, Gaussian elimination, and solving linear systems.",
        "difficulty": "MEDIUM",
        "estimated_minutes": 30,
        "topic": {
            "name": "Linear Algebra",
            "desc": "Matrices, vectors, determinants, linear combinations, and systems of linear equations."
        },
        "content": r"""# Vectors, Matrices & Systems of Linear Equations

Linear algebra is the mathematical engine powering 3D computer graphics, recommendation engines, quantum computing simulators, and deep neural network training.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- Represent geometric and data vectors in $\mathbb{R}^n$.
- Calculate vector dot products ($\mathbf{u} \cdot \mathbf{v}$) and vector norms ($\|\mathbf{v}\|$).
- Perform matrix addition, scalar multiplication, and matrix-matrix multiplication ($AB$).
- Solve systems of linear equations using Gaussian elimination and row echelon reduction.
- Calculate determinants of $2 \times 2$ and $3 \times 3$ matrices to determine invertibility.

---

## 2. Core Concepts

### 2.1 Vectors as Geometric Arrows and Feature Arrays
In computing, an $n$-dimensional vector $\mathbf{x} \in \mathbb{R}^n$ represents:
1. **Geometry**: A direction and magnitude in $n$-dimensional space.
2. **Machine Learning**: An entity's features (e.g., `[age, income, credit_score, clicks]`).

$$\mathbf{u} = \begin{bmatrix} u_1 \\ u_2 \\ \dots \\ u_n \end{bmatrix}, \quad \mathbf{v} = \begin{bmatrix} v_1 \\ v_2 \\ \dots \\ v_n \end{bmatrix}$$

### 2.2 Dot Product & Cosine Similarity
$$\mathbf{u} \cdot \mathbf{v} = \sum_{i=1}^n u_i v_i = u_1 v_1 + u_2 v_2 + \dots + u_n v_n$$
Geometric identity:
$$\mathbf{u} \cdot \mathbf{v} = \|\mathbf{u}\| \|\mathbf{v}\| \cos(\theta)$$

In document search and Large Language Models, **Cosine Similarity** measures how closely two semantic text embeddings align:
$$\text{Cosine Similarity} = \frac{\mathbf{u} \cdot \mathbf{v}}{\|\mathbf{u}\| \|\mathbf{v}\|}$$

### 2.3 Matrix Multiplication
For matrices $A \in \mathbb{R}^{m \times k}$ and $B \in \mathbb{R}^{k \times n}$, their product $C = AB \in \mathbb{R}^{m \times n}$ is defined by:
$$C_{ij} = \sum_{r=1}^k A_{ir} B_{rj}$$
> **Rule:** Matrix multiplication is associative ($A(BC) = (AB)C$), but **not commutative** ($AB \neq BA$).

---

## 3. Concrete Example: Solving a Linear System
Consider the linear system representing server resource allocation:
$$\begin{cases} 2x + y = 8 \\ x + 3y = 14 \end{cases}$$

Writing in augmented matrix form $[A | \mathbf{b}]$:
$$\begin{bmatrix} 2 & 1 & | & 8 \\ 1 & 3 & | & 14 \end{bmatrix}$$

Performing row operations ($R_1 \leftrightarrow R_2$, then $R_2 \leftarrow R_2 - 2R_1$):
$$\begin{bmatrix} 1 & 3 & | & 14 \\ 0 & -5 & | & -20 \end{bmatrix}$$
From row 2: $-5y = -20 \implies y = 4$.
Back-substituting into row 1: $x + 3(4) = 14 \implies x = 2$.
Solution: $(x=2, y=4)$.

---

## 4. Practical Application: GPU Acceleration
Why do AI companies buy thousands of GPUs (Nvidia H100s)?
A neural network layer computing $\mathbf{y} = \sigma(W\mathbf{x} + \mathbf{b})$ consists entirely of thousands of dot products. Modern GPUs contain specialized Tensor Cores that execute $4 \times 4$ or $16 \times 16$ matrix multiplications in a single hardware clock cycle.

---

## 5. Quick Recap
- Vectors store coordinates or feature sets; dot products measure projection and alignment.
- Cosine similarity evaluates text and image embeddings in AI systems.
- Matrix multiplication requires inner dimensions to match: $(m \times k) \times (k \times n) \to (m \times n)$.
- Gaussian elimination systematically solves linear systems via row operations.
""",
        "resources": [
            ("3Blue1Brown: Essence of Linear Algebra", "World-renowned visual series introducing vectors, transformations, and matrices.", "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "VIDEO", "3Blue1Brown"),
            ("Khan Academy: Linear Algebra Course", "Comprehensive curriculum on vectors, spaces, matrices, and determinants.", "https://www.khanacademy.org/math/linear-algebra", "TUTORIAL", "Khan Academy")
        ],
        "puzzle": {
            "type": "MULTIPLE_CHOICE",
            "title": "Matrix Multiplication Dimension Check",
            "question": "If Matrix A has dimensions 3 x 4, and Matrix B has dimensions 4 x 2, what are the dimensions of product matrix AB?",
            "puzzle_data": [
                "3 x 2",
                "4 x 4",
                "2 x 3",
                "Cannot be multiplied"
            ],
            "correct_answer": "3 x 2",
            "explanation": "Multiplying an (m x k) matrix by a (k x n) matrix produces an (m x n) matrix. Here, (3 x 4) * (4 x 2) yields a (3 x 2) matrix."
        },
        "quiz": [
            ("What is the dot product of vectors u = [2, 3] and v = [4, -1]?",
             ["A) 8", "B) 5", "C) 11", "D) -6"],
             "B) 5", "u . v = (2 * 4) + (3 * -1) = 8 - 3 = 5.", "MEDIUM"),
            ("If the dot product of two non-zero vectors is zero, the vectors are:",
             ["A) Parallel", "B) Orthogonal (Perpendicular)", "C) Identical", "D) Linearly Dependent"],
             "B) Orthogonal (Perpendicular)", "When u . v = 0, cos(theta) = 0, meaning the angle between them is 90 degrees (orthogonal).", "MEDIUM"),
            ("What is the determinant of the 2x2 matrix [[3, 2], [1, 4]]?",
             ["A) 10", "B) 14", "C) 12", "D) 8"],
             "A) 10", "det(A) = (3 * 4) - (2 * 1) = 12 - 2 = 10.", "MEDIUM"),
            ("Which statement about matrix multiplication is TRUE?",
             ["A) AB = BA for all square matrices", "B) Matrix multiplication is not associative", "C) AB is defined only if the number of columns in A equals the number of rows in B", "D) Inverting a matrix always produces a zero determinant"],
             "C) AB is defined only if the number of columns in A equals the number of rows in B", "For AB to exist, the inner dimensions must match: A is (m x k) and B is (k x n).", "MEDIUM"),
            ("A system of linear equations has NO solution if the geometric lines/hyperplanes are:",
             ["A) Intersecting at a single point", "B) Parallel and non-coincident", "C) Exactly the same line", "D) Orthogonal"],
             "B) Parallel and non-coincident", "Parallel lines with different intercepts never intersect, resulting in zero solutions (an inconsistent system).", "MEDIUM")
        ]
    },
    {
        "order": 4,
        "title": "04 — Practical Application: Matrix Transformations, Eigenvalues & PageRank",
        "short_description": "Linear transformations, change of basis, characteristic equations, eigenvalues, and Google PageRank.",
        "difficulty": "MEDIUM",
        "estimated_minutes": 35,
        "topic": {
            "name": "Linear Algebra",
            "desc": "Linear transformations, eigenvalues, eigenvectors, and Google PageRank algorithm."
        },
        "content": r"""# Matrix Transformations, Eigenvalues & PageRank

Eigenvalues and eigenvectors uncover the fundamental rotational axes and dominant scaling factors of high-dimensional data systems.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- Interpret a matrix as a geometric linear transformation (rotation, scaling, shear, reflection).
- Formulate the eigenvalue equation: $A\mathbf{v} = \lambda \mathbf{v}$.
- Solve for eigenvalues using the characteristic polynomial $\det(A - \lambda I) = 0$.
- Construct the stochastic link transition matrix of the World Wide Web.
- Formulate Google's PageRank algorithm as a stationary distribution power iteration problem.

---

## 2. Core Concepts

### 2.1 Matrices as Geometric Transformations
When a matrix $A$ multiplies a vector $\mathbf{x}$, it transforms space:
- Scaling: $\begin{bmatrix} 2 & 0 \\ 0 & 3 \end{bmatrix}$ stretches $x$ by 2 and $y$ by 3.
- Rotation by angle $\theta$: $\begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix}$
- Shear: $\begin{bmatrix} 1 & k \\ 0 & 1 \end{bmatrix}$ slides horizontal lines sideways.

### 2.2 The Eigenvalue Equation
Most vectors change direction when multiplied by matrix $A$. However, **eigenvectors** are special vectors whose direction remains completely unchanged—they are merely scaled by a scalar factor $\lambda$ (the **eigenvalue**):
$$A\mathbf{v} = \lambda \mathbf{v}$$

Rearranging gives the homogeneous system:
$$(A - \lambda I)\mathbf{v} = \mathbf{0}$$
For non-trivial solutions ($\mathbf{v} \neq \mathbf{0}$), the matrix $(A - \lambda I)$ must be non-invertible:
$$\det(A - \lambda I) = 0$$

---

## 3. Concrete Example: Finding Eigenvalues of a 2x2 Matrix
Let $A = \begin{bmatrix} 4 & 1 \\ 2 & 3 \end{bmatrix}$.
Step 1: Compute $\det(A - \lambda I)$:
$$\det\begin{bmatrix} 4 - \lambda & 1 \\ 2 & 3 - \lambda \end{bmatrix} = (4 - \lambda)(3 - \lambda) - (2 \times 1)$$
$$= \lambda^2 - 7\lambda + 12 - 2 = \lambda^2 - 7\lambda + 10 = 0$$

Step 2: Factor the characteristic equation:
$$(\lambda - 5)(\lambda - 2) = 0 \implies \lambda_1 = 5, \quad \lambda_2 = 2$$

---

## 4. Practical Application: Google's PageRank Algorithm
In 1998, Larry Page and Sergey Brin revolutionized web search by treating the internet as a gigantic directed graph.
1. Represent the web as a transition matrix $M$, where $M_{ij}$ is the probability of a random surfer clicking a link from page $j$ to page $i$.
2. To prevent dead ends, add a damping factor $d \approx 0.85$ to form the Google Matrix $G$:
$$G = d M + \frac{1 - d}{N} J$$
3. The long-term steady-state importance of every web page is the stationary probability vector $\mathbf{r}$ satisfying:
$$G\mathbf{r} = 1 \cdot \mathbf{r}$$
PageRank is literally finding the **eigenvector corresponding to eigenvalue $\lambda = 1$** of the web's stochastic matrix!

---

## 5. Quick Recap
- A matrix represents a linear mapping that shifts, rotates, or scales space.
- Eigenvectors maintain their directional orientation under transformation; eigenvalues represent their scaling factor.
- Principal Component Analysis (PCA) finds dominant data variance along eigenvectors of covariance matrices.
- Google PageRank is the principal eigenvector of the web's stochastic transition matrix.
""",
        "resources": [
            ("Stanford CS246: Mining Massive Datasets - PageRank", "Academic lecture on link analysis, web graphs, and PageRank mathematics.", "https://web.stanford.edu/class/cs246/", "ARTICLE", "Stanford University"),
            ("3Blue1Brown: Eigenvectors and Eigenvalues", "Geometric and visual explanation of eigenvalues and characteristic equations.", "https://www.youtube.com/watch?v=PFDu9oVAE-g", "VIDEO", "3Blue1Brown")
        ],
        "puzzle": {
            "type": "FILL_BLANK",
            "title": "Principal Eigenvalue of a Markov Matrix",
            "question": "According to the Perron-Frobenius theorem, what is the largest (principal) eigenvalue of any column-stochastic transition matrix in PageRank?",
            "puzzle_data": {
                "hint": "Probabilities sum to 1 in each column."
            },
            "correct_answer": "1",
            "explanation": "Every column-stochastic matrix has a maximum eigenvalue equal to 1, representing the stationary state probability vector."
        },
        "quiz": [
            ("In the equation A * v = lambda * v, what does v represent?",
             ["A) Eigenvalue", "B) Eigenvector", "C) Determinant", "D) Identity matrix"],
             "B) Eigenvector", "v is the eigenvector, while lambda is the scalar eigenvalue.", "MEDIUM"),
            ("To compute the eigenvalues of matrix A, we find the roots of which equation?",
             ["A) det(A - lambda * I) = 0", "B) trace(A) = 0", "C) A * v = 0", "D) det(A) = 1"],
             "A) det(A - lambda * I) = 0", "The characteristic equation det(A - lambda * I) = 0 yields the eigenvalues.", "MEDIUM"),
            ("What does the damping factor d (typically 0.85) in Google's PageRank algorithm represent?",
             ["A) Server crash probability", "B) Probability that a surfer follows an outbound link rather than jumping to a random page", "C) Rate of web page deletion", "D) Fraction of images on the page"],
             "B) Probability that a surfer follows an outbound link rather than jumping to a random page", "The damping factor models a user following hyperlinks with probability d and randomly teleporting with probability 1-d.", "MEDIUM"),
            ("If a 2x2 matrix has eigenvalues 3 and 7, what is the trace (sum of diagonal entries) of the matrix?",
             ["A) 21", "B) 10", "C) 4", "D) 14"],
             "B) 10", "The trace of any square matrix is equal to the sum of its eigenvalues: 3 + 7 = 10.", "MEDIUM"),
            ("What dimensionality reduction technique uses the eigenvectors of a feature covariance matrix?",
             ["A) Principal Component Analysis (PCA)", "B) QuickSort", "C) Binary Search", "D) K-Means Clustering"],
             "A) Principal Component Analysis (PCA)", "PCA projects high-dimensional data along the eigenvectors with the largest eigenvalues (highest variance).", "MEDIUM")
        ]
    },
    {
        "order": 5,
        "title": "05 — Advanced Concept: Probability Distributions, Expectation & Bayes' Theorem",
        "short_description": "Probability axioms, random variables, expected values, Bayes' rule, and Naive Bayes text classification.",
        "difficulty": "HARD",
        "estimated_minutes": 30,
        "topic": {
            "name": "Probability & Statistics",
            "desc": "Random variables, Bayes theorem, probability distributions, variance, and hypothesis testing."
        },
        "content": r"""# Probability Distributions, Expectation & Bayes' Theorem

Probability theory provides the rigorous mathematical framework for reasoning under uncertainty, making predictions from noisy data, and training statistical machine learning classifiers.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- State Kolmogorov's axioms of probability.
- Calculate conditional probability $P(A | B)$ and evaluate independent events.
- Formulate and calculate posterior probabilities using Bayes' Theorem.
- Compute the Expected Value $E[X]$ and Variance $\text{Var}(X)$ of discrete random variables.
- Understand the mathematical architecture of a Naive Bayes spam filter.

---

## 2. Core Concepts

### 2.1 Conditional Probability and Independence
The conditional probability of event $A$ occurring given that event $B$ has already occurred is:
$$P(A | B) = \frac{P(A \cap B)}{P(B)}, \quad P(B) > 0$$

Events $A$ and $B$ are **statistically independent** if and only if:
$$P(A \cap B) = P(A) \cdot P(B) \iff P(A | B) = P(A)$$

### 2.2 Bayes' Theorem
Bayes' Theorem provides the mathematical machinery to update our belief in a hypothesis $H$ as new evidence $E$ is observed:
$$P(H | E) = \frac{P(E | H) \cdot P(H)}{P(E)}$$

Where:
- $P(H)$: **Prior probability** (our belief before observing evidence)
- $P(E | H)$: **Likelihood** of evidence if hypothesis is true
- $P(E)$: **Marginal likelihood** of the evidence across all scenarios
- $P(H | E)$: **Posterior probability** (updated belief)

### 2.3 Expected Value & Variance
For a discrete random variable $X$ with outcomes $x_i$ and probabilities $p_i$:
- **Expected Value**: $E[X] = \mu = \sum x_i p_i$
- **Variance**: $\text{Var}(X) = \sigma^2 = E[(X - \mu)^2] = \sum (x_i - \mu)^2 p_i = E[X^2] - (E[X])^2$

---

## 3. Concrete Example: Disease Testing Paradox
Suppose a rare server anomaly occurs in $1\%$ of requests ($P(Anomaly) = 0.01$).
An automated monitoring alert has:
- $95\%$ True Positive rate: $P(Alert | Anomaly) = 0.95$
- $5\%$ False Positive rate: $P(Alert | Normal) = 0.05$

If an alert triggers, what is the probability that the server is *actually* abnormal?
$$P(Anomaly | Alert) = \frac{P(Alert | Anomaly) \cdot P(Anomaly)}{P(Alert)}$$
$$P(Alert) = (0.95 \times 0.01) + (0.05 \times 0.99) = 0.0095 + 0.0495 = 0.059$$
$$P(Anomaly | Alert) = \frac{0.0095}{0.059} \approx 16.1\%$$
Even with a $95\%$ accurate test, an alert only means a $16\%$ chance of a true anomaly because the prior rate is so low!

---

## 4. Practical Application: Naive Bayes Email Spam Filter
Given an incoming email with words $\mathbf{w} = (w_1, w_2, \dots, w_k)$:
$$P(Spam | \mathbf{w}) \propto P(Spam) \prod_{i=1}^k P(w_i | Spam)$$
The "naive" assumption is that individual words appear conditionally independently given the email category. Despite this simplification, Naive Bayes classifiers achieve high accuracy with minimal computation.

---

## 5. Quick Recap
- Probability quantifies uncertainty between $0$ (impossible) and $1$ (certain).
- Bayes' Theorem updates prior beliefs using observed likelihoods.
- Low base-rate events require high evidential standards to avoid false-positive dominance.
- Expected value represents the probability-weighted long-run average outcome.
""",
        "resources": [
            ("StatQuest: Probability & Bayes' Theorem Clearly Explained", "Intuitive visual explanations of conditional probability and Bayesian inference.", "https://statquest.org/", "VIDEO", "StatQuest"),
            ("Harvard Statistics 110: Probability", "Complete introductory probability course from Harvard University.", "https://projects.iq.harvard.edu/stat110", "ARTICLE", "Harvard University")
        ],
        "puzzle": {
            "type": "MULTIPLE_CHOICE",
            "title": "Expected Value of a Fair Die",
            "question": "What is the expected value E[X] of rolling a standard, fair 6-sided die?",
            "puzzle_data": [
                "3.5",
                "3.0",
                "4.0",
                "3.66"
            ],
            "correct_answer": "3.5",
            "explanation": "E[X] = (1+2+3+4+5+6)/6 = 21/6 = 3.5. Note that expected values do not need to be possible single outcomes."
        },
        "quiz": [
            ("If events A and B are mutually exclusive, what is P(A and B)?",
             ["A) 1.0", "B) 0.5", "C) 0.0", "D) P(A) * P(B)"],
             "C) 0.0", "Mutually exclusive events cannot occur simultaneously, so P(A and B) = 0.", "HARD"),
            ("In Bayes' theorem P(H|E) = [P(E|H) * P(H)] / P(E), what is P(H) called?",
             ["A) Posterior probability", "B) Prior probability", "C) Likelihood", "D) Evidence"],
             "B) Prior probability", "P(H) represents the initial degree of belief in hypothesis H before receiving evidence E.", "HARD"),
            ("What is the variance of a constant value C (where P(X = C) = 1)?",
             ["A) C", "B) 1", "C) 0", "D) C^2"],
             "C) 0", "A constant value has zero spread or variability around its mean, so its variance is 0.", "HARD"),
            ("Why is the Naive Bayes classifier described as 'naive'?",
             ["A) It does not use training data", "B) It assumes all feature attributes are conditionally independent given the class label", "C) It only handles binary numbers", "D) It cannot make predictions"],
             "B) It assumes all feature attributes are conditionally independent given the class label", "It naively assumes complete feature independence to simplify joint probability calculations.", "HARD"),
            ("If a coin is tossed 3 times, what is the probability of obtaining exactly 2 heads?",
             ["A) 1/8", "B) 3/8", "C) 1/2", "D) 5/8"],
             "B) 3/8", "Outcomes with 2 heads: {HHT, HTH, THH} (3 outcomes out of 2^3 = 8 total outcomes), so P = 3/8.", "HARD")
        ]
    },
    {
        "order": 6,
        "title": "06 — Practice / Problem Solving: Differential Calculus, Derivatives & Gradient Optimization",
        "short_description": "Limits, derivatives, tangent slopes, multivariate partial derivatives, and Gradient Descent optimization.",
        "difficulty": "HARD",
        "estimated_minutes": 35,
        "topic": {
            "name": "Differential Calculus",
            "desc": "Limits, derivatives, optimization, rates of change, and gradient descent algorithms."
        },
        "content": r"""# Differential Calculus, Derivatives & Gradient Optimization

Calculus is the mathematical study of continuous change. In computational systems, differential calculus allows algorithms to systematically "learn" by computing slopes of error functions and descending toward global minima.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- Evaluate limits and interpret the formal definition of a derivative: $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$.
- Apply differentiation rules: Power rule, Product rule, Quotient rule, and Chain rule.
- Compute partial derivatives $\frac{\partial f}{\partial x}$ and $\frac{\partial f}{\partial y}$ for multivariate functions.
- Formulate the gradient vector $\nabla f$ and directional derivatives.
- Implement the Gradient Descent update rule: $\theta \leftarrow \theta - \alpha \nabla L(\theta)$.

---

## 2. Core Concepts

### 2.1 The Derivative as an Instantaneous Rate of Change
The derivative of function $f(x)$ at point $x$ measures the slope of the tangent line to the curve at that exact point.
- **Power Rule**: $\frac{d}{dx} x^n = n x^{n-1}$
- **Exponential**: $\frac{d}{dx} e^{kx} = k e^{kx}$
- **Chain Rule**: $\frac{d}{dx} f(g(x)) = f'(g(x)) \cdot g'(x)$

The Chain Rule is the fundamental mathematical basis for the **Backpropagation algorithm** used to train all modern neural networks and deep learning models!

### 2.2 Multivariate Calculus: The Gradient Vector
For a scalar loss function with multiple parameters $f(x, y, z)$, the **gradient vector** $\nabla f$ collects all partial derivatives:
$$\nabla f = \begin{bmatrix} \frac{\partial f}{\partial x} \\ \frac{\partial f}{\partial y} \\ \frac{\partial f}{\partial z} \end{bmatrix}$$
> **Fundamental Theorem of Gradients:** The gradient vector $\nabla f$ always points in the direction of **steepest ascent** of the function, and its magnitude $\|\nabla f\|$ gives the rate of increase.

---

## 3. Concrete Example: Gradient of a Loss Function
Consider a Mean Squared Error loss surface:
$$L(w_1, w_2) = (w_1 - 3)^2 + 2(w_2 - 5)^2$$

Compute partial derivatives:
$$\frac{\partial L}{\partial w_1} = 2(w_1 - 3)$$
$$\frac{\partial L}{\partial w_2} = 4(w_2 - 5)$$

At initial weights $(w_1 = 1, w_2 = 2)$:
$$\nabla L(1, 2) = \begin{bmatrix} 2(1 - 3) \\ 4(2 - 5) \end{bmatrix} = \begin{bmatrix} -4 \\ -12 \end{bmatrix}$$

---

## 4. Practical Application: Gradient Descent in Machine Learning
To minimize loss function $L(\theta)$, we step in the **opposite direction** of the gradient:
$$\theta_{new} = \theta_{old} - \alpha \nabla L(\theta_{old})$$
Where $\alpha > 0$ is the **learning rate**.

With initial point $(1, 2)$ and learning rate $\alpha = 0.1$:
$$w_1 = 1 - 0.1(-4) = 1 + 0.4 = 1.4$$
$$w_2 = 2 - 0.1(-12) = 2 + 1.2 = 3.2$$
Notice that both weights moved closer to the optimal minimum $(w_1 = 3, w_2 = 5)$!

---

## 5. Quick Recap
- The derivative measures the sensitivity of a function's output to changes in its input.
- The Chain Rule allows calculating derivatives through composite functional layers.
- The gradient vector $\nabla f$ points toward the steepest uphill increase.
- Gradient descent optimizes parameters by moving in the opposite direction ($-\nabla L$).
""",
        "resources": [
            ("3Blue1Brown: Essence of Calculus", "Visual explanations of limits, derivatives, chain rule, and integrals.", "https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr", "VIDEO", "3Blue1Brown"),
            ("Khan Academy: Multivariable Calculus", "Partial derivatives, gradient vectors, directional derivatives, and optimization.", "https://www.khanacademy.org/math/multivariable-calculus", "TUTORIAL", "Khan Academy")
        ],
        "puzzle": {
            "type": "FILL_BLANK",
            "title": "Derivative Power Rule Calculation",
            "question": "What is the derivative of f(x) = 4x^3 evaluated at x = 2?",
            "puzzle_data": {
                "hint": "First find f'(x) using the power rule, then substitute x=2."
            },
            "correct_answer": "48",
            "explanation": "f'(x) = 4 * 3 * x^2 = 12x^2. Evaluating at x = 2 gives 12 * (2^2) = 12 * 4 = 48."
        },
        "quiz": [
            ("What does the gradient vector of a function indicate?",
             ["A) The direction of steepest descent", "B) The direction of steepest ascent", "C) The root of the equation", "D) The area under the curve"],
             "B) The direction of steepest ascent", "The gradient vector points in the direction where the function value increases most rapidly.", "HARD"),
            ("Which calculus differentiation rule enables backpropagation in multi-layer neural networks?",
             ["A) Power Rule", "B) Quotient Rule", "C) Chain Rule", "D) L'Hopital's Rule"],
             "C) Chain Rule", "The chain rule allows computing derivatives of composite nested functions layer by layer.", "HARD"),
            ("What happens in Gradient Descent if the learning rate alpha is set too large?",
             ["A) The algorithm converges in one step", "B) The algorithm may overshoot the minimum and diverge", "C) The gradient becomes exactly zero", "D) The weights become negative"],
             "B) The algorithm may overshoot the minimum and diverge", "An excessively large learning rate causes wild oscillations across the loss valley and prevents convergence.", "HARD"),
            ("What is the partial derivative of f(x, y) = 3x^2 * y with respect to x?",
             ["A) 6x * y", "B) 3x^2", "C) 6x", "D) 3y"],
             "A) 6x * y", "Treat y as a constant: d/dx(3x^2 * y) = 3y * d/dx(x^2) = 3y * 2x = 6xy.", "HARD"),
            ("At a local minimum of a smooth, unconstrained function, the gradient vector is:",
             ["A) Undefined", "B) Equal to the zero vector (0)", "C) Infinite", "D) Equal to 1"],
             "B) Equal to the zero vector (0)", "At critical points (including local minima, maxima, and saddle points), the gradient is zero.", "HARD")
        ]
    },
    {
        "order": 7,
        "title": "07 — Real-world Application: Graph Theory, Network Flow & Algorithmic Complexity",
        "short_description": "Graph representations, shortest path algorithms (Dijkstra), minimum spanning trees, and Big-O complexity.",
        "difficulty": "HARD",
        "estimated_minutes": 40,
        "topic": {
            "name": "Linear Algebra",  # Can map to existing topic or create specialized one
            "desc": "Graph theory, network flow, shortest paths, adjacency matrices, and algorithmic complexity."
        },
        "content": r"""# Graph Theory, Network Flow & Algorithmic Complexity

Graphs are the universal data structure of computer science: modeling computer networks, social connections, road maps, dependency chains, and neural network computation graphs.

---

## 1. Learning Objectives
By completing this lesson, you will be able to:
- Represent graphs as Adjacency Matrices ($A$) and Adjacency Lists.
- Analyze graph traversal algorithms: Breadth-First Search (BFS) and Depth-First Search (DFS).
- Trace Dijkstra's algorithm for single-source shortest paths on weighted graphs.
- Understand Minimum Spanning Tree algorithms (Kruskal's and Prim's).
- Classify algorithmic performance using Big-O asymptotic notation ($O(1), O(\log n), O(n), O(n \log n), O(n^2), O(2^n)$).

---

## 2. Core Concepts

### 2.1 Graph Definition and Representations
A graph $G = (V, E)$ consists of a set of vertices $V$ and a set of edges $E \subseteq V \times V$.
1. **Adjacency Matrix**: An $|V| \times |V|$ binary matrix where $A_{ij} = 1$ if edge $(i, j) \in E$.
   - Space: $O(|V|^2)$
   - Edge lookup: $O(1)$
2. **Adjacency List**: An array of lists where `adj[u]` stores all neighbors of vertex $u$.
   - Space: $O(|V| + |E|)$ (Optimal for sparse graphs)

### 2.2 Shortest Paths: Dijkstra's Algorithm
Dijkstra's greedy algorithm finds the shortest path from a starting source node $s$ to all other nodes in a graph with non-negative edge weights:
1. Initialize distances: $dist[s] = 0$, all other $dist[v] = \infty$.
2. Maintain a Priority Queue (min-heap) of unvisited nodes ordered by current distance.
3. Extract minimum distance node $u$, iterate over neighbors $v$:
$$\text{If } dist[u] + weight(u, v) < dist[v] \implies dist[v] = dist[u] + weight(u, v)$$
4. Repeat until all reachable nodes are finalized.
Time complexity with Fibonacci heap: $O(|E| + |V| \log |V|)$.

---

## 3. Concrete Example: Adjacency Matrix Powers and Path Counting
Let $A$ be the adjacency matrix of an unweighted graph. A profound theorem of spectral graph theory states:
> The entry $(A^k)_{ij}$ in the $k$-th power of the adjacency matrix equals the **exact number of walks of length $k$** between vertex $i$ and vertex $j$!

For graph with edges $(1-2)$ and $(2-3)$:
$$A = \begin{bmatrix} 0 & 1 & 0 \\ 1 & 0 & 1 \\ 0 & 1 & 0 \end{bmatrix}, \quad A^2 = \begin{bmatrix} 1 & 0 & 1 \\ 0 & 2 & 0 \\ 1 & 0 & 1 \end{bmatrix}$$
$(A^2)_{1,3} = 1$ because there is exactly 1 path of length 2 from node 1 to 3 (namely $1 \to 2 \to 3$).

---

## 4. Practical Application: Big-O Complexity and P vs NP
Algorithm scalability is classified by asymptotic growth bounds:
- $O(1)$: Constant hash table lookups
- $O(\log n)$: Binary search, balanced BST operations
- $O(n \log n)$: Optimal comparison sorting (MergeSort, QuickSort)
- $O(n^2)$: Nested loop brute-force algorithms
- $O(2^n)$: Combinatorial exponential search (Traveling Salesperson)

The **P vs NP Problem** is computer science's greatest open question:
- **P**: Problems solvable in polynomial time ($O(n^k)$).
- **NP**: Problems whose proposed solutions can be *verified* in polynomial time.
- If $P = NP$, every problem that is easy to check is also easy to solve!

---

## 5. Quick Recap
- Graphs represent relationships via vertices and edges.
- Adjacency matrices enable algebraic analysis; adjacency lists offer memory-efficient traversal.
- Dijkstra's algorithm solves weighted shortest path problems in $O(|E| \log |V|)$ time.
- Asymptotic notation ($O, \Omega, \Theta$) characterizes how resource usage scales as inputs grow.
""",
        "resources": [
            ("freeCodeCamp: Graph Theory Tutorial", "Algorithms, implementations, and problem-solving patterns for technical interviews.", "https://www.freecodecamp.org/news/graph-theory-tutorial-algorithms-for-interviews/", "TUTORIAL", "freeCodeCamp"),
            ("MIT OpenCourseWare: Introduction to Algorithms (SMA 5503)", "Foundational university course on graphs, shortest paths, and complexity.", "https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/", "ARTICLE", "MIT OCW")
        ],
        "puzzle": {
            "type": "ORDERING",
            "title": "Algorithmic Big-O Growth Rate Ordering",
            "question": "Arrange the following Big-O time complexities from fastest/most efficient (lowest growth) to slowest (highest growth):",
            "puzzle_data": [
                "O(n^2) - Quadratic",
                "O(1) - Constant",
                "O(2^n) - Exponential",
                "O(n log n) - Linearithmic",
                "O(log n) - Logarithmic"
            ],
            "correct_answer": [
                "O(1) - Constant",
                "O(log n) - Logarithmic",
                "O(n log n) - Linearithmic",
                "O(n^2) - Quadratic",
                "O(2^n) - Exponential"
            ],
            "explanation": "As input size n grows, the hierarchy from best to worst is O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n)."
        },
        "quiz": [
            ("What is the time complexity of Dijkstra's algorithm implemented with a binary min-heap?",
             ["A) O(|V|^3)", "B) O(|E| log |V|)", "C) O(1)", "D) O(2^|V|)"],
             "B) O(|E| log |V|)", "With a binary heap priority queue, Dijkstra's algorithm executes in O((|V| + |E|) log |V|) = O(|E| log |V|).", "HARD"),
            ("A graph that contains NO cycles is called an:",
             ["A) Complete Graph", "B) Acyclic Graph (or Forest/Tree if connected)", "C) Bipartite Graph", "D) Eulerian Graph"],
             "B) Acyclic Graph (or Forest/Tree if connected)", "A graph with no cycles is acyclic. A connected acyclic graph is a tree.", "HARD"),
            ("What does the entry (A^k)_ij in the k-th power of an adjacency matrix A represent?",
             ["A) The shortest path length between i and j", "B) The number of walks of length k between vertex i and vertex j", "C) The weight of edge (i, j)", "D) The degree of vertex i"],
             "B) The number of walks of length k between vertex i and vertex j", "Powers of the adjacency matrix count the exact number of walks of length k connecting any two vertices.", "HARD"),
            ("Which graph traversal algorithm uses a First-In-First-Out (FIFO) queue?",
             ["A) Depth-First Search (DFS)", "B) Breadth-First Search (BFS)", "C) QuickSort", "D) Bellman-Ford"],
             "B) Breadth-First Search (BFS)", "BFS explores nodes level-by-level using a FIFO queue, while DFS uses a LIFO stack.", "HARD"),
            ("Which computational complexity class contains problems whose solutions can be VERIFIED in polynomial time?",
             ["A) NP", "B) P", "C) EXPTIME", "D) O(1)"],
             "A) NP", "NP stands for Nondeterministic Polynomial time, representing problems verifiable in polynomial time.", "HARD")
        ]
    }
]


def seed_math_lessons():
    print("=" * 60)
    print("SPECTRA — Seeding 7 Connected Lessons for Subject 12 (MATH-201)")
    print("=" * 60)

    db = SessionLocal()
    try:
        math_subj = db.query(Subject).filter(Subject.id == 12).first()
        if not math_subj:
            print("[ERROR] Subject ID 12 not found!")
            return

        print(f"[OK] Found Subject: {math_subj.name} (Code: {math_subj.code}, ID: {math_subj.id})")

        # Map existing topics by keyword
        existing_topics = db.query(Topic).filter(Topic.subject_id == math_subj.id).all()
        topic_map = {}
        for t in existing_topics:
            topic_map[t.name.lower()] = t

        created_or_updated = 0
        for l_data in MATH_LESSONS_DATA:
            order = l_data["order"]
            title = l_data["title"]
            diff = l_data["difficulty"]
            t_data = l_data["topic"]

            # Match or create topic
            t_key = t_data["name"].lower()
            matched_topic = None
            for name, top in topic_map.items():
                if name in t_key or t_key in name:
                    matched_topic = top
                    break

            if not matched_topic:
                matched_topic = Topic(
                    subject_id=math_subj.id,
                    name=t_data["name"],
                    description=t_data["desc"],
                    difficulty_level=diff,
                    display_order=order,
                    is_active=True
                )
                db.add(matched_topic)
                db.flush()
                topic_map[matched_topic.name.lower()] = matched_topic

            # Check if lesson exists by subject_id and lesson_order
            lesson = db.query(Lesson).filter(
                Lesson.subject_id == math_subj.id,
                Lesson.lesson_order == order
            ).first()

            if not lesson:
                # Also check by title
                lesson = db.query(Lesson).filter(
                    Lesson.subject_id == math_subj.id,
                    Lesson.title == title
                ).first()

            if not lesson:
                lesson = Lesson(
                    subject_id=math_subj.id,
                    topic_id=matched_topic.id,
                    title=title,
                    short_description=l_data["short_description"],
                    detailed_description=l_data["short_description"],
                    description=l_data["short_description"],
                    content=l_data["content"],
                    difficulty=diff,
                    difficulty_level=diff,
                    estimated_minutes=l_data["estimated_minutes"],
                    estimated_duration=l_data["estimated_minutes"],
                    lesson_order=order,
                    display_order=order,
                    is_active=True
                )
                db.add(lesson)
                db.flush()
                print(f"[CREATED] Lesson {order}: {title} (ID: {lesson.id})")
            else:
                lesson.title = title
                lesson.topic_id = matched_topic.id
                lesson.short_description = l_data["short_description"]
                lesson.detailed_description = l_data["short_description"]
                lesson.description = l_data["short_description"]
                lesson.content = l_data["content"]
                lesson.difficulty = diff
                lesson.difficulty_level = diff
                lesson.estimated_minutes = l_data["estimated_minutes"]
                lesson.estimated_duration = l_data["estimated_minutes"]
                lesson.lesson_order = order
                lesson.display_order = order
                lesson.is_active = True
                db.flush()
                print(f"[UPDATED] Lesson {order}: {title} (ID: {lesson.id})")

            # Link topic back to lesson
            matched_topic.lesson_id = lesson.id

            # Seed Study Resources
            for res_idx, (r_title, r_desc, r_url, r_type, r_provider) in enumerate(l_data["resources"], start=1):
                existing_res = db.query(StudyResource).filter(
                    StudyResource.lesson_id == lesson.id,
                    StudyResource.url == r_url
                ).first()
                if not existing_res:
                    res = StudyResource(
                        lesson_id=lesson.id,
                        topic_id=matched_topic.id,
                        title=r_title,
                        description=r_desc,
                        url=r_url,
                        resource_type=r_type,
                        provider=r_provider,
                        display_order=res_idx,
                        is_active=True
                    )
                    db.add(res)

            # Seed Interactive Puzzle
            p_data = l_data["puzzle"]
            existing_puzzle = db.query(Puzzle).filter(Puzzle.lesson_id == lesson.id).first()
            p_pdata = json.dumps(p_data["puzzle_data"]) if not isinstance(p_data["puzzle_data"], str) else p_data["puzzle_data"]
            p_canswer = json.dumps(p_data["correct_answer"]) if not isinstance(p_data["correct_answer"], str) else p_data["correct_answer"]
            if not existing_puzzle:
                puzzle = Puzzle(
                    subject_id=math_subj.id,
                    topic_id=matched_topic.id,
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

            # Seed Quiz and Questions
            q_list = l_data["quiz"]
            existing_quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson.id).first()
            if not existing_quiz:
                quiz = Quiz(
                    subject_id=math_subj.id,
                    topic_id=matched_topic.id,
                    lesson_id=lesson.id,
                    title=f"Quiz: {matched_topic.name}",
                    description=f"5-question knowledge checkpoint on {matched_topic.name}.",
                    quiz_type="CONCEPT",
                    difficulty=diff,
                    question_count=len(q_list)
                )
                db.add(quiz)
                db.flush()

                for q_idx, (q_text, opts, ans, expl, q_diff) in enumerate(q_list, start=1):
                    opts_str = json.dumps(opts) if isinstance(opts, list) else opts
                    question = Question(
                        subject_id=math_subj.id,
                        topic_id=matched_topic.id,
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

            # Generate and Cache YouTube recommendations
            yt_res = get_or_create_lesson_youtube_recommendations(db, lesson.id)
            print(f"  -> YouTube recommendations: {len(yt_res.videos)} cached (query: '{yt_res.query_used}')")

            created_or_updated += 1

        db.commit()
        print(f"\n[SUCCESS] Successfully seeded {created_or_updated} lessons for Subject 12!")

        # Verification
        total_lessons = db.query(Lesson).filter(Lesson.subject_id == math_subj.id).count()
        print(f"[VERIFIED] Subject 12 (MATH-201) now has {total_lessons} active lessons.")

    except Exception as exc:
        db.rollback()
        print(f"[ERROR] Seeding failed: {exc}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    seed_math_lessons()
