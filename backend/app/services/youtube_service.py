import re
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.models.academic import Lesson, Subject, Topic, LessonYouTubeVideo
from app.schemas.academic import YouTubeVideoOut, LessonYouTubeResponse

logger = logging.getLogger(__name__)

# Curated, high-quality educational fallback videos for computer science topics
# Used when YOUTUBE_API_KEY is not configured or YouTube quota is exhausted
CURATED_EDUCATIONAL_VIDEOS: Dict[str, List[Dict[str, Any]]] = {
    # DBMS
    "dbms_foundations": [
        {
            "video_id": "HXV3zeRR3h4",
            "title": "SQL Tutorial - Full Database Course for Beginners",
            "thumbnail_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "4 hr 20 min",
            "description": "Comprehensive introduction to relational databases, schema design, tables, primary keys, and SQL queries.",
            "url": "https://www.youtube.com/watch?v=HXV3zeRR3h4",
            "published_at": "2023-04-10"
        },
        {
            "video_id": "ztHopE5Wnpc",
            "title": "Database Design Course - Learn how to design a database for beginners",
            "thumbnail_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "8 hr 12 min",
            "description": "Understand relational database architecture, entities, tables, relationships, and foreign key constraints.",
            "url": "https://www.youtube.com/watch?v=ztHopE5Wnpc",
            "published_at": "2022-11-15"
        },
        {
            "video_id": "wR0jg0eQsZA",
            "title": "What is a Relational Database? (RDBMS Explained)",
            "thumbnail_url": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=640&q=80",
            "channel_name": "IBM Technology",
            "duration": "8 min",
            "description": "IBM experts explain relational database architecture, ACID guarantees, tables, and structured data handling.",
            "url": "https://www.youtube.com/watch?v=wR0jg0eQsZA",
            "published_at": "2023-01-20"
        }
    ],
    "dbms_er_modeling": [
        {
            "video_id": "QpdhBUYk7Kk",
            "title": "Entity Relationship Diagram (ERD) Tutorial - Part 1",
            "thumbnail_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=640&q=80",
            "channel_name": "Lucidchart",
            "duration": "6 min",
            "description": "Learn ER diagram basics, entities, attributes, primary keys, and cardinality symbols for conceptual design.",
            "url": "https://www.youtube.com/watch?v=QpdhBUYk7Kk",
            "published_at": "2022-09-12"
        },
        {
            "video_id": "-CUy-EAZJYg",
            "title": "Entity Relationship Diagram (ERD) Tutorial - Part 2",
            "thumbnail_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=640&q=80",
            "channel_name": "Lucidchart",
            "duration": "7 min",
            "description": "Master one-to-one, one-to-many, and many-to-many entity relationships, junction tables, and foreign keys.",
            "url": "https://www.youtube.com/watch?v=-CUy-EAZJYg",
            "published_at": "2022-09-19"
        },
        {
            "video_id": "oUP7tUhn_7w",
            "title": "Conceptual, Logical & Physical Data Models Explained",
            "thumbnail_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=640&q=80",
            "channel_name": "IBM Technology",
            "duration": "9 min",
            "description": "Step-by-step breakdown of how business requirements translate into conceptual, logical, and physical database schemas.",
            "url": "https://www.youtube.com/watch?v=oUP7tUhn_7w",
            "published_at": "2023-05-04"
        }
    ],
    "dbms_normalization": [
        {
            "video_id": "GFQaEYEc8_8",
            "title": "Database Normalization - 1NF, 2NF, 3NF, BCNF Explained with Examples",
            "thumbnail_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=640&q=80",
            "channel_name": "Decomplexify",
            "duration": "16 min",
            "description": "Clear step-by-step walkthrough of First, Second, Third Normal Form and Boyce-Codd Normal Form with practical tables.",
            "url": "https://www.youtube.com/watch?v=GFQaEYEc8_8",
            "published_at": "2023-03-18"
        },
        {
            "video_id": "UrYLYV7WSHM",
            "title": "Database Normalization Tutorial (1NF, 2NF, 3NF)",
            "thumbnail_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=640&q=80",
            "channel_name": "Caleb Curry",
            "duration": "28 min",
            "description": "Comprehensive explanation of functional dependencies, insertion anomalies, update anomalies, and table decomposition.",
            "url": "https://www.youtube.com/watch?v=UrYLYV7WSHM",
            "published_at": "2022-08-25"
        },
        {
            "video_id": "px7m_mup1u0",
            "title": "Normalization in DBMS: 1NF, 2NF, 3NF, BCNF",
            "thumbnail_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=640&q=80",
            "channel_name": "Gate Smashers",
            "duration": "14 min",
            "description": "High-yield explanation of candidate keys, prime attributes, partial dependencies, and transitive dependencies.",
            "url": "https://www.youtube.com/watch?v=px7m_mup1u0",
            "published_at": "2022-04-11"
        }
    ],
    "dbms_sql_joins": [
        {
            "video_id": "9yeOJ0ZMUYw",
            "title": "SQL Joins Explained | INNER, LEFT, RIGHT, FULL OUTER",
            "thumbnail_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=640&q=80",
            "channel_name": "Alex The Analyst",
            "duration": "12 min",
            "description": "Visual breakdown of relational join operations in SQL with hands-on queries and Venn diagram illustrations.",
            "url": "https://www.youtube.com/watch?v=9yeOJ0ZMUYw",
            "published_at": "2023-02-14"
        },
        {
            "video_id": "7S_tz1z_5bA",
            "title": "SQL Tutorial - Full Database Course for Beginners",
            "thumbnail_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "4 hr 20 min",
            "description": "Learn SELECT, GROUP BY, HAVING, subqueries, aggregate functions, and multi-table joins in PostgreSQL and MySQL.",
            "url": "https://www.youtube.com/watch?v=7S_tz1z_5bA",
            "published_at": "2022-10-30"
        },
        {
            "video_id": "2HVMiPPuPIM",
            "title": "Advanced SQL Queries - Window Functions, CTEs and Aggregates",
            "thumbnail_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=640&q=80",
            "channel_name": "Luke Barousse",
            "duration": "22 min",
            "description": "Practical guide to Common Table Expressions (WITH clauses), analytical window functions, and partitioned groupings.",
            "url": "https://www.youtube.com/watch?v=2HVMiPPuPIM",
            "published_at": "2023-06-12"
        }
    ],
    "dbms_transactions": [
        {
            "video_id": "t_20e4vX2qM",
            "title": "Database Transactions and ACID Properties Explained",
            "thumbnail_url": "https://images.unsplash.com/photo-1507238691740-187a5b1d37b8?w=640&q=80",
            "channel_name": "Hussein Nasser",
            "duration": "18 min",
            "description": "Deep dive into Atomicity, Consistency, Isolation, and Durability with write-ahead logging and two-phase commit.",
            "url": "https://www.youtube.com/watch?v=t_20e4vX2qM",
            "published_at": "2022-07-19"
        },
        {
            "video_id": "pomxJODecUQ",
            "title": "ACID Transactions in Databases - Computerphile",
            "thumbnail_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=640&q=80",
            "channel_name": "Computerphile",
            "duration": "11 min",
            "description": "Professor Mike Pound explores why database transactions are essential for banking, e-commerce, and crash recovery.",
            "url": "https://www.youtube.com/watch?v=pomxJODecUQ",
            "published_at": "2022-03-05"
        },
        {
            "video_id": "wA_bKjH8G6Y",
            "title": "Database Isolation Levels & Concurrency Control",
            "thumbnail_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=640&q=80",
            "channel_name": "Hussein Nasser",
            "duration": "25 min",
            "description": "Read Uncommitted, Read Committed, Repeatable Read, and Serializable levels: dirty reads, non-repeatable reads, phantom reads.",
            "url": "https://www.youtube.com/watch?v=wA_bKjH8G6Y",
            "published_at": "2023-04-22"
        }
    ],
    "dbms_indexing": [
        {
            "video_id": "clrotA4Yc10",
            "title": "How Database B-Tree Indexing Works",
            "thumbnail_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=640&q=80",
            "channel_name": "Hussein Nasser",
            "duration": "24 min",
            "description": "Understand how B-Trees, B+Trees, clustered indices, and non-clustered indices accelerate point queries and range scans.",
            "url": "https://www.youtube.com/watch?v=clrotA4Yc10",
            "published_at": "2022-05-14"
        },
        {
            "video_id": "HubezKbFL7E",
            "title": "Database Indexing Explained (with visual diagrams)",
            "thumbnail_url": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=640&q=80",
            "channel_name": "ByteByteGo",
            "duration": "9 min",
            "description": "How indices work under the hood: index scan vs table scan, composite indices, and write overhead.",
            "url": "https://www.youtube.com/watch?v=HubezKbFL7E",
            "published_at": "2023-07-28"
        },
        {
            "video_id": "fsG1XaZEa78",
            "title": "SQL Query Optimization & EXPLAIN ANALYZE Tutorial",
            "thumbnail_url": "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=640&q=80",
            "channel_name": "Traversy Media",
            "duration": "17 min",
            "description": "Learn to inspect query execution plans, eliminate sequential scans, avoid index bloat, and optimize slow queries.",
            "url": "https://www.youtube.com/watch?v=fsG1XaZEa78",
            "published_at": "2023-08-10"
        }
    ],
    "dbms_distributed": [
        {
            "video_id": "0buKQHokLK8",
            "title": "SQL vs NoSQL Explained: When to Use Which",
            "thumbnail_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=640&q=80",
            "channel_name": "Fireship",
            "duration": "6 min",
            "description": "Fast-paced comparison of relational databases (PostgreSQL/MySQL) versus document, key-value, and graph NoSQL systems.",
            "url": "https://www.youtube.com/watch?v=0buKQHokLK8",
            "published_at": "2023-02-08"
        },
        {
            "video_id": "kpr8X7h5b-g",
            "title": "CAP Theorem Simplified for System Design",
            "thumbnail_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=640&q=80",
            "channel_name": "ByteByteGo",
            "duration": "8 min",
            "description": "Consistency, Availability, and Partition Tolerance explained in distributed databases with real-world architectural examples.",
            "url": "https://www.youtube.com/watch?v=kpr8X7h5b-g",
            "published_at": "2023-04-18"
        },
        {
            "video_id": "W2Z7Tqf2kX4",
            "title": "Database Replication, Sharding and High Availability",
            "thumbnail_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=640&q=80",
            "channel_name": "Hussein Nasser",
            "duration": "21 min",
            "description": "Primary-replica architectures, leaderless replication, sharding strategies, and failover mechanics in modern cloud systems.",
            "url": "https://www.youtube.com/watch?v=W2Z7Tqf2kX4",
            "published_at": "2023-09-02"
        }
    ],
    # General Computer Science / Programming Fallback
    "general": [
        {
            "video_id": "eIrMbAQSU34",
            "title": "Java Tutorial for Beginners - Programming with Mosh",
            "thumbnail_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=640&q=80",
            "channel_name": "Programming with Mosh",
            "duration": "2 hr 30 min",
            "description": "Comprehensive tutorial covering Java syntax, control structures, functions, and OOP.",
            "url": "https://www.youtube.com/watch?v=eIrMbAQSU34",
            "published_at": "2023-01-15"
        },
        {
            "video_id": "_uQrJ0TkZlc",
            "title": "Python for Beginners - Full Course [Programming Tutorial]",
            "thumbnail_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "4 hr 26 min",
            "description": "Complete Python programming course covering data types, functions, modules, and algorithms.",
            "url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
            "published_at": "2022-12-01"
        },
        {
            "video_id": "7wnove7K-ZQ",
            "title": "Machine Learning for Everybody – Full Course",
            "thumbnail_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "3 hr 53 min",
            "description": "Introductory machine learning course covering regression, classification, clustering, and neural networks.",
            "url": "https://www.youtube.com/watch?v=7wnove7K-ZQ",
            "published_at": "2023-03-20"
        }
    ],
    # Mathematics for Computing Curated Videos
    "math_linear_algebra": [
        {
            "video_id": "fNk_zzaMoSs",
            "title": "Vectors, what even are they? | Essence of linear algebra, chapter 1",
            "thumbnail_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=640&q=80",
            "channel_name": "3Blue1Brown",
            "duration": "14 min",
            "description": "Visual, geometric introduction to vectors, coordinate systems, linear combinations, and spanning sets.",
            "url": "https://www.youtube.com/watch?v=fNk_zzaMoSs",
            "published_at": "2022-08-04"
        },
        {
            "video_id": "J7DzL2_Nah0",
            "title": "1. The Geometry of Linear Equations - MIT 18.06 Linear Algebra",
            "thumbnail_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=640&q=80",
            "channel_name": "MIT OpenCourseWare",
            "duration": "39 min",
            "description": "Prof. Gilbert Strang presents row pictures and column pictures of matrix multiplication and linear systems.",
            "url": "https://www.youtube.com/watch?v=J7DzL2_Nah0",
            "published_at": "2021-11-15"
        },
        {
            "video_id": "k7RM-ot2NWY",
            "title": "Eigenvalues and Eigenvectors: A Complete Guide",
            "thumbnail_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=640&q=80",
            "channel_name": "3Blue1Brown",
            "duration": "17 min",
            "description": "Geometric understanding of matrix transformations that only stretch or squish vectors along characteristic lines.",
            "url": "https://www.youtube.com/watch?v=PFDu9oVAE-g",
            "published_at": "2022-09-12"
        }
    ],
    "math_number_theory": [
        {
            "video_id": "GSIDS_lvRv4",
            "title": "Public Key Cryptography & Modular Arithmetic - Computerphile",
            "thumbnail_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=640&q=80",
            "channel_name": "Computerphile",
            "duration": "12 min",
            "description": "How modular clock arithmetic, prime factorization, and trapdoor functions enable modern RSA cryptography.",
            "url": "https://www.youtube.com/watch?v=GSIDS_lvRv4",
            "published_at": "2022-07-20"
        },
        {
            "video_id": "4bL338765B4",
            "title": "Euclid's Algorithm and the Greatest Common Divisor",
            "thumbnail_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=640&q=80",
            "channel_name": "Numberphile",
            "duration": "11 min",
            "description": "Step-by-step breakdown of the Euclidean algorithm for GCD and its extended form for modular inverses.",
            "url": "https://www.youtube.com/watch?v=JUzYl1TYMcU",
            "published_at": "2022-05-18"
        },
        {
            "video_id": "2V81_r0lKcg",
            "title": "Discrete Math for Computer Science: Number Theory & Modular Arithmetic",
            "thumbnail_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "45 min",
            "description": "Comprehensive tutorial on divisibility rules, congruence modulo n, and prime testing algorithms.",
            "url": "https://www.youtube.com/watch?v=2V81_r0lKcg",
            "published_at": "2023-01-10"
        }
    ],
    "math_calculus": [
        {
            "video_id": "WUvTyaaNkzM",
            "title": "The Essence of Calculus, Chapter 1 | 3Blue1Brown",
            "thumbnail_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=640&q=80",
            "channel_name": "3Blue1Brown",
            "duration": "17 min",
            "description": "Visual foundation of calculus: derivatives as instantaneous rates of change and integrals as areas under curves.",
            "url": "https://www.youtube.com/watch?v=WUvTyaaNkzM",
            "published_at": "2022-06-14"
        },
        {
            "video_id": "sDv4f4s2SB8",
            "title": "Gradient Descent, Step-by-Step | StatQuest",
            "thumbnail_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=640&q=80",
            "channel_name": "StatQuest with Josh Starmer",
            "duration": "19 min",
            "description": "How partial derivatives guide the optimization process in machine learning, neural networks, and loss minimization.",
            "url": "https://www.youtube.com/watch?v=sDv4f4s2SB8",
            "published_at": "2022-10-05"
        },
        {
            "video_id": "7S-_979Q4U8",
            "title": "Calculus for Machine Learning and Computer Science",
            "thumbnail_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "1 hr 12 min",
            "description": "Hands-on multivariate calculus covering directional derivatives, gradients, Hessians, and convexity.",
            "url": "https://www.youtube.com/watch?v=7S-_979Q4U8",
            "published_at": "2023-04-22"
        }
    ],
    "math_probability": [
        {
            "video_id": "HZGCoVF3YvM",
            "title": "Bayes theorem, the geometry of changing beliefs | 3Blue1Brown",
            "thumbnail_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=640&q=80",
            "channel_name": "3Blue1Brown",
            "duration": "15 min",
            "description": "Visual explanation of conditional probability, prior odds, evidence likelihood, and posterior probability updates.",
            "url": "https://www.youtube.com/watch?v=HZGCoVF3YvM",
            "published_at": "2022-04-19"
        },
        {
            "video_id": "oI33PjyJVnw",
            "title": "Probability Distributions Clearly Explained | StatQuest",
            "thumbnail_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=640&q=80",
            "channel_name": "StatQuest with Josh Starmer",
            "duration": "16 min",
            "description": "Discrete versus continuous probability distributions: Binomial, Poisson, Gaussian, and expectation values.",
            "url": "https://www.youtube.com/watch?v=oI33PjyJVnw",
            "published_at": "2022-11-28"
        },
        {
            "video_id": "b2P1Z00fA8o",
            "title": "Independent Events & Conditional Probability - Khan Academy",
            "thumbnail_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=640&q=80",
            "channel_name": "Khan Academy",
            "duration": "11 min",
            "description": "Intuitive understanding of joint probability, independence tests, and conditional probability trees.",
            "url": "https://www.youtube.com/watch?v=b2P1Z00fA8o",
            "published_at": "2022-03-15"
        }
    ],
    "math_logic_graphs": [
        {
            "video_id": "L3LMbpZIKhQ",
            "title": "Mathematics for Computer Science: Proofs & Logic - MIT OCW",
            "thumbnail_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?w=640&q=80",
            "channel_name": "MIT OpenCourseWare",
            "duration": "48 min",
            "description": "Propositional logic, truth tables, logical equivalence, proof by contradiction, and mathematical induction.",
            "url": "https://www.youtube.com/watch?v=L3LMbpZIKhQ",
            "published_at": "2021-09-30"
        },
        {
            "video_id": "09_LlHjoEiY",
            "title": "Graph Theory Tutorial: Algorithms for Technical Interviews",
            "thumbnail_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=640&q=80",
            "channel_name": "freeCodeCamp.org",
            "duration": "2 hr 05 min",
            "description": "Nodes, edges, adjacency matrices, BFS, DFS, Dijkstra's algorithm, and topological sorting explained.",
            "url": "https://www.youtube.com/watch?v=09_LlHjoEiY",
            "published_at": "2022-08-16"
        },
        {
            "video_id": "e2cF8a5VGaU",
            "title": "P vs NP and Computational Complexity - Computerphile",
            "thumbnail_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=640&q=80",
            "channel_name": "Computerphile",
            "duration": "14 min",
            "description": "Understanding polynomial time, NP-completeness, reduction, and the millenium problem in computer science.",
            "url": "https://www.youtube.com/watch?v=e2cF8a5VGaU",
            "published_at": "2023-01-24"
        }
    ]
}


def clean_title_for_query(title: str) -> str:
    """Strip order numbers, symbols, and punctuation from lesson titles for cleaner YouTube searches."""
    # E.g. "01 — Relational Database Architecture" -> "Relational Database Architecture"
    cleaned = re.sub(r"^\d+\s*[\—\-\:\.]\s*", "", title)
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)
    return " ".join(cleaned.split())


def build_search_query(lesson: Lesson, subject: Subject, topic: Optional[Topic] = None) -> str:
    """
    Dynamically constructs a high-relevance educational search query
    based on the lesson's subject, title, topic, and difficulty.
    """
    cleaned_lesson_title = clean_title_for_query(lesson.title)
    subject_name = subject.name if subject else ""
    topic_name = clean_title_for_query(topic.name) if topic else ""

    # Build query prioritizing topic and lesson title
    parts = []
    if subject_name and subject_name not in cleaned_lesson_title:
        parts.append(subject_name)
    parts.append(cleaned_lesson_title)
    if topic_name and topic_name not in cleaned_lesson_title and topic_name not in subject_name:
        parts.append(topic_name)

    parts.append("tutorial explained")
    return " ".join(parts).strip()


def parse_iso8601_duration(duration_str: str) -> str:
    """Parse ISO 8601 duration (e.g., PT15M33S or PT1H5M) into human-readable format."""
    if not duration_str:
        return "15 min"
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not match:
        return "15 min"
    hours, minutes, seconds = match.groups()
    h = int(hours) if hours else 0
    m = int(minutes) if minutes else 0
    s = int(seconds) if seconds else 0

    if h > 0:
        return f"{h} hr {m} min" if m > 0 else f"{h} hr"
    if m > 0:
        return f"{m} min"
    return f"{s} sec"


def is_duration_short(duration_str: str) -> bool:
    """Check if the video is under 60 seconds (likely a YouTube Short)."""
    if not duration_str:
        return False
    match = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", duration_str)
    if not match:
        return False
    hours, minutes, seconds = match.groups()
    h = int(hours) if hours else 0
    m = int(minutes) if minutes else 0
    s = int(seconds) if seconds else 0
    total_seconds = h * 3600 + m * 60 + s
    return total_seconds < 60


def fetch_from_youtube_api(query: str, api_key: str) -> List[Dict[str, Any]]:
    """
    Searches YouTube Data API v3 for educational videos matching the query.
    Filters out Shorts, music/entertainment, and retrieves durations.
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoEmbeddable": "true",
        "maxResults": 10,
        "relevanceLanguage": "en",
        "safeSearch": "strict",
        "key": api_key,
    }

    headers = {
        "User-Agent": "SPECTRA-EduPlatform/1.0"
    }

    try:
        with httpx.Client(timeout=8.0) as client:
            resp = client.get(search_url, params=search_params, headers=headers)
            if resp.status_code != 200:
                logger.warning(f"YouTube search API returned status {resp.status_code}: {resp.text[:200]}")
                return []

            data = resp.json()
            items = data.get("items", [])
            if not items:
                return []

            video_ids = [item["id"]["videoId"] for item in items if "id" in item and "videoId" in item["id"]]
            if not video_ids:
                return []

            # Fetch video details for durations & contentDetails
            details_url = "https://www.googleapis.com/youtube/v3/videos"
            details_params = {
                "part": "contentDetails,snippet",
                "id": ",".join(video_ids[:10]),
                "key": api_key,
            }
            details_resp = client.get(details_url, params=details_params, headers=headers)
            details_map = {}
            if details_resp.status_code == 200:
                details_data = details_resp.json()
                for v in details_data.get("items", []):
                    details_map[v["id"]] = v

            results = []
            seen_ids = set()

            for item in items:
                vid = item["id"].get("videoId")
                if not vid or vid in seen_ids:
                    continue

                snippet = item.get("snippet", {})
                title = snippet.get("title", "")

                # Skip obvious Shorts
                if "#shorts" in title.lower() or "shorts" in title.lower():
                    continue

                # Check duration from details
                detail = details_map.get(vid, {})
                content_details = detail.get("contentDetails", {})
                iso_duration = content_details.get("duration", "")
                if is_duration_short(iso_duration):
                    continue

                duration_formatted = parse_iso8601_duration(iso_duration)
                thumbnails = snippet.get("thumbnails", {})
                thumb_url = (
                    thumbnails.get("high", {}).get("url")
                    or thumbnails.get("medium", {}).get("url")
                    or thumbnails.get("default", {}).get("url")
                    or f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"
                )

                seen_ids.add(vid)
                results.append({
                    "video_id": vid,
                    "title": title,
                    "description": snippet.get("description", ""),
                    "thumbnail_url": thumb_url,
                    "channel_name": snippet.get("channelTitle", "Educational Channel"),
                    "duration": duration_formatted,
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "published_at": snippet.get("publishedAt", "")[:10] if snippet.get("publishedAt") else None,
                })

                if len(results) >= 3:
                    break

            return results

    except Exception as exc:
        logger.error(f"Error fetching YouTube API for query '{query}': {exc}")
        return []


def select_curated_fallback(lesson: Lesson, subject: Subject) -> List[Dict[str, Any]]:
    """Select appropriate high-quality curated fallback educational videos based on lesson topic and title."""
    title_lower = (lesson.title or "").lower()
    subject_code = (subject.code or "").upper() if subject else ""

    if subject_code == "DBMS" or "database" in title_lower or "sql" in title_lower:
        if "er" in title_lower or "entity" in title_lower or "model" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_er_modeling"]
        elif "normal" in title_lower or "1nf" in title_lower or "bcnf" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_normalization"]
        elif "join" in title_lower or "query" in title_lower or "dml" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_sql_joins"]
        elif "transaction" in title_lower or "acid" in title_lower or "concurrency" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_transactions"]
        elif "index" in title_lower or "b-tree" in title_lower or "optim" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_indexing"]
        elif "distribut" in title_lower or "nosql" in title_lower or "replicat" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_distributed"]
        else:
            return CURATED_EDUCATIONAL_VIDEOS["dbms_foundations"]

    if subject_code in ["MATH", "MATH-201"] or "math" in title_lower or "algebra" in title_lower or "calculus" in title_lower:
        if "number" in title_lower or "modular" in title_lower or "prime" in title_lower or "arithmetic" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["math_number_theory"]
        elif "calculus" in title_lower or "derivative" in title_lower or "gradient" in title_lower or "limit" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["math_calculus"]
        elif "probab" in title_lower or "bayes" in title_lower or "statist" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["math_probability"]
        elif "graph" in title_lower or "logic" in title_lower or "network" in title_lower or "complex" in title_lower:
            return CURATED_EDUCATIONAL_VIDEOS["math_logic_graphs"]
        else:
            return CURATED_EDUCATIONAL_VIDEOS["math_linear_algebra"]

    return CURATED_EDUCATIONAL_VIDEOS.get("general", [])


def get_or_create_lesson_youtube_recommendations(db: Session, lesson_id: int) -> LessonYouTubeResponse:
    """
    Core Recommendation Workflow:
    1. Checks if recommendations for lesson_id already exist in database (cache).
    2. If present, returns cached results instantly.
    3. If absent:
       - Extracts lesson, subject, and topic metadata.
       - Constructs dynamic educational search query.
       - Calls YouTube Data API v3 if API key is configured.
       - Falls back gracefully to high-yield curated educational videos if API is unavailable.
       - Persists top 3 recommendations in the database with rank.
    """
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return LessonYouTubeResponse(lesson_id=lesson_id, lesson_title="", query_used="", videos=[])

    # 1. Check database cache
    cached_videos = (
        db.query(LessonYouTubeVideo)
        .filter(LessonYouTubeVideo.lesson_id == lesson_id)
        .order_by(LessonYouTubeVideo.rank.asc(), LessonYouTubeVideo.id.asc())
        .all()
    )

    if cached_videos and len(cached_videos) > 0:
        return LessonYouTubeResponse(
            lesson_id=lesson_id,
            lesson_title=lesson.title,
            query_used="cached",
            videos=[YouTubeVideoOut.model_validate(v) for v in cached_videos]
        )

    # 2. Extract metadata & build search query
    subject = db.query(Subject).filter(Subject.id == lesson.subject_id).first()
    topic = db.query(Topic).filter(Topic.id == lesson.topic_id).first() if lesson.topic_id else None
    query = build_search_query(lesson, subject, topic)

    videos_data = []

    # 3. Call YouTube Data API v3 if key available
    api_key = settings.YOUTUBE_API_KEY.strip() if settings.YOUTUBE_API_KEY else ""
    if api_key:
        videos_data = fetch_from_youtube_api(query, api_key)

    # 4. If API returned no results or key not configured, use curated educational fallback
    if not videos_data:
        videos_data = select_curated_fallback(lesson, subject)

    # 5. Persist recommendations into database
    created_models = []
    for rank, v in enumerate(videos_data[:3], start=1):
        rec_video = LessonYouTubeVideo(
            lesson_id=lesson.id,
            video_id=v["video_id"],
            title=v["title"],
            description=v.get("description", ""),
            thumbnail_url=v.get("thumbnail_url", f"https://img.youtube.com/vi/{v['video_id']}/hqdefault.jpg"),
            channel_name=v.get("channel_name", "Educational Channel"),
            duration=v.get("duration", "15 min"),
            url=v.get("url", f"https://www.youtube.com/watch?v={v['video_id']}"),
            published_at=v.get("published_at"),
            rank=rank
        )
        db.add(rec_video)
        created_models.append(rec_video)

    try:
        db.commit()
        for m in created_models:
            db.refresh(m)
    except Exception as exc:
        db.rollback()
        logger.error(f"Error persisting YouTube recommendations for lesson {lesson_id}: {exc}")

    return LessonYouTubeResponse(
        lesson_id=lesson_id,
        lesson_title=lesson.title,
        query_used=query,
        videos=[YouTubeVideoOut.model_validate(v) for v in created_models]
    )
