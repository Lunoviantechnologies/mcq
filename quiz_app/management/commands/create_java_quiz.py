from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quiz_app.models import Quiz, Question, Choice


class Command(BaseCommand):
    help = "Creates a Java Fundamentals quiz with 10 questions (including text questions)"

    def handle(self, *args, **options):
        # Ensure we have an admin user to own the quiz
        admin_user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin_user.set_password("admin123")
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created admin user (admin/admin123)"))

        quiz, created = Quiz.objects.get_or_create(
            title="Java Fundamentals Quiz",
            defaults={
                "description": "Core Java questions including JVM, OOP, collections, and streams.",
                "created_by": admin_user,
                "is_active": True,
            },
        )

        if not created:
            self.stdout.write(self.style.WARNING("Quiz already exists; no new questions added."))
            return

        q_order = 0

        def add_mc(question_text, time_min, choices_with_correct):
            nonlocal q_order
            q = Question.objects.create(
                quiz=quiz,
                question_text=question_text,
                question_type="multiple_choice",
                order=q_order,
                time_limit_minutes=time_min,
            )
            q_order += 1
            for text, is_correct in choices_with_correct:
                Choice.objects.create(question=q, choice_text=text, is_correct=is_correct)

        def add_text(question_text, time_min):
            nonlocal q_order
            Question.objects.create(
                quiz=quiz,
                question_text=question_text,
                question_type="text",
                order=q_order,
                time_limit_minutes=time_min,
            )
            q_order += 1

        # 10 questions: 7 MCQ + 3 text
        add_mc(
            "Which tool builds and packages Java projects?",
            1,
            [
                ("Maven", True),
                ("npm", False),
                ("pip", False),
                ("cargo", False),
            ],
        )

        add_mc(
            "What does the JVM primarily do?",
            1,
            [
                ("Executes Java bytecode on a host system", True),
                ("Compiles Java to native binaries only", False),
                ("Replaces the JDK", False),
                ("Provides a source code editor", False),
            ],
        )

        add_mc(
            "Which keyword prevents a class from being inherited?",
            1,
            [
                ("final", True),
                ("static", False),
                ("private", False),
                ("sealed", False),
            ],
        )

        add_mc(
            "Which collection is NOT ordered?",
            1,
            [
                ("HashSet", True),
                ("ArrayList", False),
                ("LinkedList", False),
                ("LinkedHashSet", False),
            ],
        )

        add_mc(
            "What must be true about equals() and hashCode()?",
            1,
            [
                ("Equal objects must have equal hash codes", True),
                ("Equal objects can have different hash codes", False),
                ("hashCode is optional when overriding equals", False),
                ("equals need not be consistent", False),
            ],
        )

        add_mc(
            "Which statement about Strings is true?",
            1,
            [
                ("String is immutable", True),
                ("StringBuilder is immutable", False),
                ("StringBuffer is immutable", False),
                ("String can be modified in place", False),
            ],
        )

        add_mc(
            "Checked exceptions in Java:",
            1,
            [
                ("Must be declared or handled", True),
                ("Are subclasses of RuntimeException", False),
                ("Cannot be created by developers", False),
                ("Are never used in I/O APIs", False),
            ],
        )

        # Text questions (for free-form answers)
        add_text(
            "Explain the difference between JDK, JRE, and JVM.",
            2,
        )

        add_text(
            "List the four main OOP pillars and briefly describe each.",
            2,
        )

        add_text(
            "When would you prefer Streams over traditional loops in Java? Provide a brief example scenario.",
            2,
        )

        self.stdout.write(self.style.SUCCESS("✅ Java Fundamentals Quiz created with 10 questions (includes text questions)."))
        self.stdout.write(self.style.SUCCESS("Run the quiz at http://127.0.0.1:8000/"))

