import os
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import httpx
from sqlalchemy.orm import Session
from app.core.config import settings
from app.db.models.ai import AIConversation, AIMessage
from app.db.models.academic import Subject, Topic
from app.db.models.performance import StudentTopicPerformance
from app.schemas.ai import AIChatResponse

class BaseTutorProvider(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        context: Dict[str, Any],
        is_during_quiz: bool = False
    ) -> Dict[str, Any]:
        """Generate tutor response given context and chat history."""
        pass

class ExternalLLMProvider(BaseTutorProvider):
    """Integrates with standard OpenAI-compatible API providers via environment variables."""
    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    async def generate_response(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        context: Dict[str, Any],
        is_during_quiz: bool = False
    ) -> Dict[str, Any]:
        subject_name = context.get("subject_name", "General Computer Science")
        topic_name = context.get("topic_name", "General Concepts")
        weak_topics = context.get("weak_topics", [])

        system_instruction = (
            f"You are the SPECTRA Intelligent AI Tutor specializing in {subject_name} and {topic_name}. "
            f"Student context: Weak areas: {', '.join(weak_topics) if weak_topics else 'None identified'}. "
            "Adopt an encouraging, pedagogical Socratic method. Break complex concepts into intuitive analogies and clear code snippets. "
        )

        if is_during_quiz:
            system_instruction += (
                "IMPORTANT: The student is currently taking an assessment. "
                "DO NOT provide direct answers or letter choices. "
                "Guide the student by asking guiding questions, clarifying definitions, or explaining underlying rules."
            )

        messages = [{"role": "system", "content": system_instruction}]
        messages.extend(history[-6:])  # Recent context
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 800
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(f"{self.base_url}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return {
                "reply": content,
                "hints": ["Review parameters", "Check return types"],
                "recommended_topics": [topic_name]
            }

class FallbackTutorProvider(BaseTutorProvider):
    """
    Intelligent built-in fallback tutor providing context-aware guidance,
    concept breakdowns, analogies, and targeted hints without requiring external API keys.
    """
    async def generate_response(
        self,
        prompt: str,
        history: List[Dict[str, str]],
        context: Dict[str, Any],
        is_during_quiz: bool = False
    ) -> Dict[str, Any]:
        p_lower = prompt.lower()
        subject_name = context.get("subject_name", "Computer Science")
        topic_name = context.get("topic_name", "Core Principles")
        weak_topics = context.get("weak_topics", [])

        if is_during_quiz:
            return {
                "reply": (
                    f"### 💡 Socratic Hint for {topic_name}\n\n"
                    f"During an active assessment, I cannot directly give you the answer key. "
                    f"However, think about how {topic_name} handles data flow and scope.\n\n"
                    f"- Ask yourself: What is the expected return type and state transition?\n"
                    f"- Watch out for edge cases, variable scope, and parameter ordering.\n\n"
                    f"Take a moment to re-read the question stem carefully!"
                ),
                "hints": [
                    f"Focus on the definition of {topic_name}",
                    "Trace the code step-by-step with sample inputs",
                    "Eliminate options that produce syntax or type errors"
                ],
                "recommended_topics": [topic_name]
            }

        # Check for specific prompt actions (Requirement 37)
        lesson_title = context.get("lesson_title")
        puzzle_info = context.get("recent_puzzle_mistake")
        quiz_mistake_info = context.get("recent_quiz_mistake")
        action = context.get("action_type") or ""

        if action == "EXPLAIN_LESSON" or "explain this lesson" in p_lower:
            target_lesson = lesson_title or f"this lesson on {topic_name}"
            reply = (
                f"### 📖 Concept Breakdown: {target_lesson}\n\n"
                f"In **{subject_name}**, {topic_name} forms an essential foundation. Here is how to think about it:\n\n"
                "1. **Core Motivation**: Why does this concept exist? It provides modularity, clarity, and predictable execution.\n"
                "2. **Mental Model**: Visualize the flow of data through memory—from inputs, through transformations, to expected outputs.\n"
                "3. **Practical Application**: In real-world software, this pattern prevents edge cases and ensures robust error handling.\n\n"
                "**Pro-Tip**: Read through each code block in the lesson carefully, then try the quick interactive puzzle to test your mental model!"
            )
            hints = ["Trace code execution line by line", "Review key syntax declarations"]

        elif action == "HINT" or "give me a hint" in p_lower or "hint" in p_lower:
            reply = (
                f"### 💡 Thought Hint for {topic_name}\n\n"
                "Before jumping to conclusions, consider these clues:\n\n"
                "- Look closely at the data types and method signatures.\n"
                "- What are the input constraints and expected return guarantees?\n"
                "- Eliminate answers that violate fundamental language syntax or type bounds.\n\n"
                "*Remember: Think about what happens step-by-step rather than guessing.*"
            )
            hints = ["Check parameter types and count", "Verify return statements"]

        elif action == "EXPLAIN_PUZZLE" or "explain why my puzzle answer was incorrect" in p_lower:
            if puzzle_info:
                p_title = puzzle_info.get("title", "the puzzle")
                p_q = puzzle_info.get("question", "")
                p_exp = puzzle_info.get("explanation", "")
                reply = (
                    f"### 🧩 Puzzle Feedback: {p_title}\n\n"
                    f"**Challenge Context**: {p_q}\n\n"
                    "**Why this common misconception happens**:\n"
                    "In interactive learning puzzles, common traps usually involve:\n"
                    "1. Overlooking operator precedence or type conversion nuances.\n"
                    "2. Confusing pass-by-value with reference mutations.\n"
                    "3. Off-by-one errors or ordering of execution steps.\n\n"
                    f"{f'**Key Insight**: {p_exp}' if p_exp else 'Trace the variables through each line of code.'}\n\n"
                    "Try re-reading the question and testing the logic step-by-step!"
                )
            else:
                reply = (
                    f"### 🧩 Puzzle Analysis for {topic_name}\n\n"
                    "When solving code and logic puzzles, common mistakes include:\n"
                    "- Confusing the order of method invocation with definition.\n"
                    "- Overlooking return value types.\n"
                    "- Forgetting that arguments are evaluated before entering function bodies.\n\n"
                    "Re-trace your steps and give it another try!"
                )
            hints = ["Identify the execution entry point", "Track variable values in each step"]

        elif action == "SIMILAR_PRACTICE" or "similar practice problem" in p_lower:
            reply = (
                f"### ✍️ Similar Practice Challenge for {topic_name}\n\n"
                f"Here is a targeted problem to test your understanding:\n\n"
                "```text\n"
                "Given a function that takes two integer parameters, (a, b),\n"
                "what will be the final value returned if a = 4 and b is doubled\n"
                "inside the function body before returning (a * b)?\n"
                "```\n\n"
                "**Question**: Does the original variable `b` in the caller change?\n\n"
                "Think about pass-by-value and memory scope!"
            )
            hints = ["Primitive values are passed by value", "Local reassignments do not affect caller"]

        elif action == "EXPLAIN_QUIZ" or "explain my quiz mistake" in p_lower:
            if quiz_mistake_info:
                q_text = quiz_mistake_info.get("question_text", "the question")
                q_exp = quiz_mistake_info.get("explanation", "Review the concept rules.")
                reply = (
                    f"### 📝 Reviewing Your Assessment Question\n\n"
                    f"**Question**: *\"{q_text}\"*\n\n"
                    f"**Explanation**: {q_exp}\n\n"
                    "**Takeaway**: Focus on understanding why the correct option is uniquely true, and why alternative options are invalid syntax or logic."
                )
            else:
                reply = (
                    f"### 📝 Quiz Mistake Analysis for {topic_name}\n\n"
                    "Reviewing mistakes is the fastest path to mastery. When you miss a question:\n"
                    "1. Isolate the specific rule being tested (e.g. method overriding vs overloading).\n"
                    "2. Check if you fell for a distractor option with subtle syntax errors.\n"
                    "3. Review the lesson section covering this specific topic."
                )
            hints = ["Review topic reference documentation", "Solve 3 practice questions"]

        # Context-tailored response
        elif "function" in p_lower or "method" in p_lower:
            reply = (
                f"### 📘 Understanding Functions & Parameters in {subject_name}\n\n"
                "A **function** is a reusable block of code that takes inputs (arguments), performs an operation, and returns an output.\n\n"
                "#### Core Components:\n"
                "1. **Signature & Return Type**: Defines what the function yields (`void`, `int`, etc.).\n"
                "2. **Parameters**: Placeholders for input values.\n"
                "3. **Scope**: Variables declared inside exist only during execution.\n\n"
                "```java\n"
                "// Example Java Function\n"
                "public static int calculateScore(int correct, int total) {\n"
                "    if (total == 0) return 0;\n"
                "    return (correct * 100) / total;\n"
                "}\n"
                "```\n\n"
                "Would you like to try a targeted practice question on parameter passing?"
            )
            hints = ["Check parameter types", "Ensure every execution branch returns a value"]
        elif "variable" in p_lower or "data type" in p_lower:
            reply = (
                f"### 📦 Variables & Memory in {subject_name}\n\n"
                "Variables represent labeled storage locations in memory. Key considerations:\n\n"
                "- **Primitive Types** (`int`, `boolean`, `double`): Store actual values.\n"
                "- **Reference Types** (`String`, Objects, Arrays): Store memory addresses referencing objects in heap storage.\n\n"
                "Always ensure variables are initialized before reading their values to prevent runtime exceptions."
            )
            hints = ["Distinguish primitive vs reference types", "Check null references"]
        elif "oop" in p_lower or "class" in p_lower or "object" in p_lower:
            reply = (
                f"### 🏛️ Object-Oriented Principles in {subject_name}\n\n"
                "Object-Oriented Programming (OOP) organizes software around four primary pillars:\n\n"
                "1. **Encapsulation**: Bundling state and behaviors while restricting direct access via access modifiers (`private`, `public`).\n"
                "2. **Inheritance**: Creating hierarchical relationships (`extends`).\n"
                "3. **Polymorphism**: Ability for different classes to respond to the same interface.\n"
                "4. **Abstraction**: Hiding internal implementation details.\n"
            )
            hints = ["Use getter/setter methods for encapsulation", "Override methods with @Override"]
        else:
            weak_summary = f"Based on your recent diagnostic, you might also benefit from practicing {', '.join(weak_topics)}." if weak_topics else ""
            reply = (
                f"### 🎓 SPECTRA Intelligent Tutor – {topic_name}\n\n"
                f"You asked: *\"{prompt}\"*\n\n"
                f"In **{subject_name}**, mastering **{topic_name}** requires connecting fundamental theory with systematic code tracing. "
                f"{weak_summary}\n\n"
                f"**Key Recommendation:**\n"
                f"1. Review the foundational lesson for {topic_name}.\n"
                f"2. Solve 5-10 targeted diagnostic questions to reinforce memory retrieval.\n"
                f"3. Retake the topic assessment to verify mastery score growth above 70%."
            )
            hints = ["Practice active recall", "Break problem into smaller subroutines"]

        return {
            "reply": reply,
            "hints": hints,
            "recommended_topics": [topic_name] + weak_topics[:2]
        }

class AIService:
    def __init__(self):
        # Graceful selection: use External LLM only if API key is populated
        if settings.AI_API_KEY and settings.AI_API_KEY.strip():
            self.provider: BaseTutorProvider = ExternalLLMProvider(
                api_key=settings.AI_API_KEY,
                base_url=settings.AI_BASE_URL,
                model=settings.AI_MODEL
            )
        else:
            self.provider: BaseTutorProvider = FallbackTutorProvider()

    async def chat(
        self,
        db: Session,
        student_id: int,
        prompt: str,
        conversation_id: Optional[int] = None,
        subject_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        lesson_id: Optional[int] = None,
        puzzle_id: Optional[int] = None,
        action_type: Optional[str] = None,
        is_during_quiz: bool = False
    ) -> AIChatResponse:
        """Processes a student's tutoring question, saving context and responses."""
        from app.db.models.puzzle import Puzzle, PuzzleAttempt
        from app.db.models.quiz import QuizResponse, Question
        from app.db.models.academic import Lesson

        # Find or create conversation
        if conversation_id:
            conv = db.query(AIConversation).filter(
                AIConversation.id == conversation_id,
                AIConversation.student_id == student_id
            ).first()
        else:
            conv = None

        if not conv:
            title = prompt[:40] + ("..." if len(prompt) > 40 else "")
            conv = AIConversation(student_id=student_id, title=title)
            db.add(conv)
            db.flush()

        # Build context from student performance
        weak_performances = db.query(StudentTopicPerformance).filter(
            StudentTopicPerformance.student_id == student_id,
            StudentTopicPerformance.mastery_score < 60.0
        ).all()
        weak_topic_names = []
        for wp in weak_performances:
            t = db.query(Topic).filter(Topic.id == wp.topic_id).first()
            if t:
                weak_topic_names.append(t.name)

        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first() if lesson_id else None
        subject = db.query(Subject).filter(Subject.id == subject_id).first() if subject_id else (lesson.subject if lesson else None)
        topic = db.query(Topic).filter(Topic.id == topic_id).first() if topic_id else (lesson.topic if lesson else None)

        recent_puzzle_mistake = None
        if puzzle_id:
            p = db.query(Puzzle).filter(Puzzle.id == puzzle_id).first()
            if p:
                recent_puzzle_mistake = {"id": p.id, "title": p.title, "question": p.question, "explanation": p.explanation}
        else:
            last_failed_puzzle = db.query(PuzzleAttempt).filter(
                PuzzleAttempt.student_id == student_id,
                PuzzleAttempt.is_correct == False
            ).order_by(PuzzleAttempt.completed_at.desc()).first()
            if last_failed_puzzle and last_failed_puzzle.puzzle:
                p = last_failed_puzzle.puzzle
                recent_puzzle_mistake = {"id": p.id, "title": p.title, "question": p.question, "explanation": p.explanation}

        recent_quiz_mistake = None
        last_failed_resp = db.query(QuizResponse).join(Question).filter(
            QuizResponse.is_correct == False
        ).order_by(QuizResponse.id.desc()).first()
        if last_failed_resp and last_failed_resp.question:
            q = last_failed_resp.question
            recent_quiz_mistake = {"question_text": q.question_text, "explanation": q.explanation}

        context = {
            "subject_name": subject.name if subject else "General Computer Science",
            "topic_name": topic.name if topic else (weak_topic_names[0] if weak_topic_names else "Core Topics"),
            "lesson_title": lesson.title if lesson else None,
            "weak_topics": weak_topic_names,
            "recent_puzzle_mistake": recent_puzzle_mistake,
            "recent_quiz_mistake": recent_quiz_mistake,
            "action_type": action_type
        }

        # Gather history
        past_msgs = db.query(AIMessage).filter(AIMessage.conversation_id == conv.id).order_by(AIMessage.created_at).all()
        history = [{"role": m.role, "content": m.content} for m in past_msgs]

        # Record User Message
        user_msg = AIMessage(
            conversation_id=conv.id,
            role="user",
            content=prompt
        )
        db.add(user_msg)
        db.commit()

        # Generate Response
        try:
            result = await self.provider.generate_response(
                prompt=prompt,
                history=history,
                context=context,
                is_during_quiz=is_during_quiz
            )
        except Exception as e:
            # If external fails, use fallback safely
            fallback = FallbackTutorProvider()
            result = await fallback.generate_response(
                prompt=prompt,
                history=history,
                context=context,
                is_during_quiz=is_during_quiz
            )

        # Record Assistant Message
        assistant_msg = AIMessage(
            conversation_id=conv.id,
            role="assistant",
            content=result["reply"]
        )
        db.add(assistant_msg)
        db.commit()

        return AIChatResponse(
            reply=result["reply"],
            conversation_id=conv.id,
            hints=result.get("hints", []),
            recommended_topics=result.get("recommended_topics", [])
        )

ai_service = AIService()
