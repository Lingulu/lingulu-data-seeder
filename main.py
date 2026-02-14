import os
from dotenv import load_dotenv
import psycopg2
import boto3
import uuid

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("LINGULU_DB_HOST", "localhost"),
    "port": int(os.getenv("LINGULU_DB_PORT", 5432)),
    "user": os.getenv("LINGULU_DB_USER", "postgres"),
    "password": os.getenv("LINGULU_DB_PASSWORD", "postgres"),
    "dbname": os.getenv("LINGULU_DB_NAME", "postgres"),
}

s3_client = boto3.client('s3')
BUCKET_NAME = os.getenv("LINGULU_S3_BUCKET_NAME", "lingulu-course")

def upload_to_s3(file_path, s3_key):
    try:
        s3_client.upload_file(file_path, BUCKET_NAME, s3_key)
        return f"https://{BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
    except Exception as e:
        print(f"Error upload: {e}")
        return None

connection = psycopg2.connect(**DB_CONFIG)
cursor = connection.cursor()

cursor.execute(
    """
    DO $$ DECLARE
        r RECORD;
    BEGIN
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
            EXECUTE 'TRUNCATE TABLE ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;
    """
)

course_list = [
    {
        "course_id": "f5058930-99f7-4de4-b7c6-cb1b8b4603c9",
        "difficulty_level": "Beginner",
        "course_title": "English for Beginners",
        "course_description": "A course designed for those who are new to the English language, covering basic grammar, vocabulary, and conversational skills.",
        "position": 1,
        "published": True,
    },
    {
        "course_id": "90e60335-0fa8-4e6f-8849-6111c1a39499",
        "difficulty_level": "Intermediate",
        "course_title": "English for Intermediate Learners",
        "course_description": "A course aimed at learners with some basic knowledge of English, focusing on improving grammar, expanding vocabulary, and enhancing conversational abilities.",
        "position": 2,
        "published": True,
    },
    {
        "course_id": "bcb0f085-528b-434c-85e8-c857394bae87",
        "difficulty_level": "Advanced",
        "course_title": "English for Advanced Learners",
        "course_description": "A course designed for advanced English learners, focusing on complex grammar structures, advanced vocabulary, and fluency in conversation.",
        "position": 3,
        "published": True,
    }
]

lessons_list = [
    # course 1 lessons
    {
        "lesson_id": "5a12bf28-9a46-4d75-bd30-b9d9a8e5be1f",
        "course_id": "f5058930-99f7-4de4-b7c6-cb1b8b4603c9",
        "lesson_title": "Nice to Meet You",
        "position": 1,
    },
    {
        "lesson_id": "d2b065cc-d28b-44e7-bbec-06b49ade7626",
        "course_id": "f5058930-99f7-4de4-b7c6-cb1b8b4603c9",
        "lesson_title": "Things Around Me",
        "position": 2,
    },
    {
        "lesson_id": "ad4a835d-a062-4c5d-aa49-9fbcef9a0986",
        "course_id": "f5058930-99f7-4de4-b7c6-cb1b8b4603c9",
        "lesson_title": "My Daily Life",
        "position": 3,
    },
    {
        "lesson_id": "9450005d-ed64-42cb-b48c-bb0a68e0deae",
        "course_id": "f5058930-99f7-4de4-b7c6-cb1b8b4603c9",
        "lesson_title": "Describing People and Things",
        "position": 4,
    },

    # course 2 lessons
    {
        "lesson_id": "62001bba-532c-4824-bc4c-3ab900ee2f20",
        "course_id": "90e60335-0fa8-4e6f-8849-6111c1a39499",
        "lesson_title": "Talking About the Past (Simple Past Tense)",
        "position": 1,
    },
    {
        "lesson_id": "58f30032-db8e-4a34-a328-6d3396c92cdd",
        "course_id": "90e60335-0fa8-4e6f-8849-6111c1a39499",
        "lesson_title": "Future Plans (Will & Going to)",
        "position": 2,
    },
    {
        "lesson_id": "20fc11c1-e3a0-498c-ab19-9a30bb76e8d2",
        "course_id": "90e60335-0fa8-4e6f-8849-6111c1a39499",
        "lesson_title": "What is Happening Now? (Present Continuous)",
        "position": 3,
    },
    {
        "lesson_id": "284714fe-3b56-4b16-8d49-a62155b975ae",
        "course_id": "90e60335-0fa8-4e6f-8849-6111c1a39499",
        "lesson_title": "Making Comparisons (Comparative & Superlative)",
        "position": 4,
    },

    # course 3 lessons
    {
        "lesson_id": "d73f36d6-2c6f-421c-a1e8-5231cb87a2c7",
        "course_id": "bcb0f085-528b-434c-85e8-c857394bae87",
        "lesson_title": "Life Experiences & Results (Present Perfect Tense)",
        "position": 1,
    },
    {
        "lesson_id": "193be07e-c02b-4714-abbc-3e961a3a57a4",
        "course_id": "bcb0f085-528b-434c-85e8-c857394bae87",
        "lesson_title": "Hypothetical Situations (Conditional Type 2)",
        "position": 2,
    },
    {
        "lesson_id": "e180fc7a-e3cc-4f26-bdb1-c8d1f6839b2b",
        "course_id": "bcb0f085-528b-434c-85e8-c857394bae87",
        "lesson_title": "Passive Voice (Focus on Object)",
        "position": 3,
    },
    {
        "lesson_id": "ba47ddec-dc94-469c-a4b6-f0ec303c592a",
        "course_id": "bcb0f085-528b-434c-85e8-c857394bae87",
        "lesson_title": "Deductions & Certainty (Modals)",
        "position": 4,
    }
]

course_1_lesson_1_sections = [
    {
        "section_id": "03aafc20-d593-404f-9313-ee1a6fae1e5c",
        "lesson_id": "5a12bf28-9a46-4d75-bd30-b9d9a8e5be1f",
        "section_title": "Grammar: Subject Pronouns & Basic Greetings",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "a18579b1-d283-4b28-ac95-2a71175774ca",
        "lesson_id": "5a12bf28-9a46-4d75-bd30-b9d9a8e5be1f",
        "section_title": "Vocabulary: Subject Pronouns & Basic Greetings",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "0daa2750-207d-4ae9-8e9c-9ac7756ca11d",
        "lesson_id": "5a12bf28-9a46-4d75-bd30-b9d9a8e5be1f",
        "section_title": "Speaking: Subject Pronouns & Basic Greetings",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "6e08ab36-e30d-44fc-855a-8c3e917ad35a",
        "lesson_id": "5a12bf28-9a46-4d75-bd30-b9d9a8e5be1f",
        "section_title": "MCQ: Subject Pronouns & Basic Greetings",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_1_lesson_2_sections = [
    {
        "section_id": "c04e3552-6f64-41e2-8cfd-a1254c754fcb",
        "lesson_id": "d2b065cc-d28b-44e7-bbec-06b49ade7626",
        "section_title": "Grammar: Demonstratives & Possessives",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "6c4fb5d9-04dc-42d0-92f3-4422c78e3255",
        "lesson_id": "d2b065cc-d28b-44e7-bbec-06b49ade7626",
        "section_title": "Vocabulary: Demonstratives & Possessives",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "8f2f070a-d319-458a-ae26-2017bee0b416",
        "lesson_id": "d2b065cc-d28b-44e7-bbec-06b49ade7626",
        "section_title": "Speaking: Demonstratives & Possessives",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "e566d78a-8b02-4498-91d6-bdd861538382",
        "lesson_id": "d2b065cc-d28b-44e7-bbec-06b49ade7626",
        "section_title": "MCQ: Demonstratives & Possessives",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_1_lesson_3_sections = [
    {
        "section_id": "002818a2-8263-4374-8ca2-ecdcbfd1221b",
        "lesson_id": "ad4a835d-a062-4c5d-aa49-9fbcef9a0986",
        "section_title": "Grammar: Simple Present & Time Expressions",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "0ecaf7e7-2409-4c16-9669-daf31d641260",
        "lesson_id": "ad4a835d-a062-4c5d-aa49-9fbcef9a0986",
        "section_title": "Vocabulary: Simple Present & Time Expressions",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "1b53ba73-1b76-4353-9473-c1ee848af1d3",
        "lesson_id": "ad4a835d-a062-4c5d-aa49-9fbcef9a0986",
        "section_title": "Speaking: Simple Present & Time Expressions",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "e0d5645e-5a67-428b-a580-c10f31d17986",
        "lesson_id": "ad4a835d-a062-4c5d-aa49-9fbcef9a0986",
        "section_title": "MCQ: Simple Present & Time Expressions",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_1_lesson_4_sections = [
    {
        "section_id": "9a9cf94e-8e67-4fb7-b9fc-5295e1b62ad6",
        "lesson_id": "9450005d-ed64-42cb-b48c-bb0a68e0deae",
        "section_title": "Grammar: Adjectives & Nouns",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "c0fef146-acef-4d9b-abe6-ee5802e30fd0",
        "lesson_id": "9450005d-ed64-42cb-b48c-bb0a68e0deae",
        "section_title": "Vocabulary: Adjectives & Nouns",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "d5da1923-141e-46b3-9991-bbf9dfa9beed",
        "lesson_id": "9450005d-ed64-42cb-b48c-bb0a68e0deae",
        "section_title": "Speaking: Adjectives & Nouns",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "c05824b4-3c0f-42c0-b846-8d349f39a772",
        "lesson_id": "9450005d-ed64-42cb-b48c-bb0a68e0deae",
        "section_title": "MCQ: Adjectives & Nouns",
        "section_type": "MCQ",
        "position": 4,
    }
]

# Course 2 sections
course_2_lesson_1_sections = [
    {
        "section_id": "f1a2b3c4-d5e6-7f89-0a1b-2c3d4e5f6a7b",
        "lesson_id": "62001bba-532c-4824-bc4c-3ab900ee2f20",
        "section_title": "Grammar: Simple Past Tense",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "a2b3c4d5-e6f7-8901-2a3b-4c5d6e7f8a9b",
        "lesson_id": "62001bba-532c-4824-bc4c-3ab900ee2f20",
        "section_title": "Vocabulary: Simple Past Tense",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "b3c4d5e6-f789-0123-4a5b-6c7d8e9f0a1b",
        "lesson_id": "62001bba-532c-4824-bc4c-3ab900ee2f20",
        "section_title": "Speaking: Simple Past Tense",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "c4d5e6f7-8901-2345-6a7b-8c9d0e1f2a3c",
        "lesson_id": "62001bba-532c-4824-bc4c-3ab900ee2f20",
        "section_title": "MCQ: Simple Past Tense",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_2_lesson_2_sections = [
    {
        "section_id": "d5e6f789-0123-4567-8a9b-0c1d2e3f4a5b",
        "lesson_id": "58f30032-db8e-4a34-a328-6d3396c92cdd",
        "section_title": "Grammar: Future Plans",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "e6f78901-2345-6789-0a1b-2c3d4e5f6a7c",
        "lesson_id": "58f30032-db8e-4a34-a328-6d3396c92cdd",
        "section_title": "Vocabulary: Future Plans",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "f7890123-4567-8901-2a3b-4c5d6e7f8a9c",
        "lesson_id": "58f30032-db8e-4a34-a328-6d3396c92cdd",
        "section_title": "Speaking: Future Plans",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "89012345-6789-0123-4a5b-6c7d8e9f0a1c",
        "lesson_id": "58f30032-db8e-4a34-a328-6d3396c92cdd",
        "section_title": "MCQ: Future Plans",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_2_lesson_3_sections = [
    {
        "section_id": "90123456-7890-1234-5a6b-7c8d9e0f1a2c",
        "lesson_id": "20fc11c1-e3a0-498c-ab19-9a30bb76e8d2",
        "section_title": "Grammar: Present Continuous",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "01234567-8901-2345-6a7b-8c9d0e1f2a3c",
        "lesson_id": "20fc11c1-e3a0-498c-ab19-9a30bb76e8d2",
        "section_title": "Vocabulary: Present Continuous",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "12345678-9012-3456-7a8b-9c0d1e2f3a4c",
        "lesson_id": "20fc11c1-e3a0-498c-ab19-9a30bb76e8d2",
        "section_title": "Speaking: Present Continuous",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "23456789-0123-4567-8a9b-0c1d2e3f4a5c",
        "lesson_id": "20fc11c1-e3a0-498c-ab19-9a30bb76e8d2",
        "section_title": "MCQ: Present Continuous",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_2_lesson_4_sections = [
    {
        "section_id": "34567890-1234-5678-9a0b-1c2d3e4f5a6c",
        "lesson_id": "284714fe-3b56-4b16-8d49-a62155b975ae",
        "section_title": "Grammar: Comparative & Superlative",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "45678901-2345-6789-0a1b-2c3d4e5f6a7c",
        "lesson_id": "284714fe-3b56-4b16-8d49-a62155b975ae",
        "section_title": "Vocabulary: Comparative & Superlative",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "56789012-3456-7890-1a2b-3c4d5e6f7a8c",
        "lesson_id": "284714fe-3b56-4b16-8d49-a62155b975ae",
        "section_title": "Speaking: Comparative & Superlative",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "67890123-4567-8901-2a3b-4c5d6e7f8a9c",
        "lesson_id": "284714fe-3b56-4b16-8d49-a62155b975ae",
        "section_title": "MCQ: Comparative & Superlative",
        "section_type": "MCQ",
        "position": 4,
    }
]

# Course 3 sections
course_3_lesson_1_sections = [
    {
        "section_id": "78901234-5678-9012-3a4b-5c6d7e8f9a0c",
        "lesson_id": "d73f36d6-2c6f-421c-a1e8-5231cb87a2c7",
        "section_title": "Grammar: Present Perfect Tense",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "89012345-6789-0123-4a5b-6c7d8e9f0a1d",
        "lesson_id": "d73f36d6-2c6f-421c-a1e8-5231cb87a2c7",
        "section_title": "Vocabulary: Present Perfect Tense",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "90123456-7890-1234-5a6b-7c8d9e0f1a2d",
        "lesson_id": "d73f36d6-2c6f-421c-a1e8-5231cb87a2c7",
        "section_title": "Speaking: Present Perfect Tense",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "01234567-8901-2345-6a7b-8c9d0e1f2a3d",
        "lesson_id": "d73f36d6-2c6f-421c-a1e8-5231cb87a2c7",
        "section_title": "MCQ: Present Perfect Tense",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_3_lesson_2_sections = [
    {
        "section_id": "12345678-9012-3456-7a8b-9c0d1e2f3a4d",
        "lesson_id": "193be07e-c02b-4714-abbc-3e961a3a57a4",
        "section_title": "Grammar: Conditional Type 2",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "23456789-0123-4567-8a9b-0c1d2e3f4a5d",
        "lesson_id": "193be07e-c02b-4714-abbc-3e961a3a57a4",
        "section_title": "Vocabulary: Conditional Type 2",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "34567890-1234-5678-9a0b-1c2d3e4f5a6d",
        "lesson_id": "193be07e-c02b-4714-abbc-3e961a3a57a4",
        "section_title": "Speaking: Conditional Type 2",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "45678901-2345-6789-0a1b-2c3d4e5f6a7d",
        "lesson_id": "193be07e-c02b-4714-abbc-3e961a3a57a4",
        "section_title": "MCQ: Conditional Type 2",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_3_lesson_3_sections = [
    {
        "section_id": "56789012-3456-7890-1a2b-3c4d5e6f7a8d",
        "lesson_id": "e180fc7a-e3cc-4f26-bdb1-c8d1f6839b2b",
        "section_title": "Grammar: Passive Voice",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "67890123-4567-8901-2a3b-4c5d6e7f8a9d",
        "lesson_id": "e180fc7a-e3cc-4f26-bdb1-c8d1f6839b2b",
        "section_title": "Vocabulary: Passive Voice",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "78901234-5678-9012-3a4b-5c6d7e8f9a0d",
        "lesson_id": "e180fc7a-e3cc-4f26-bdb1-c8d1f6839b2b",
        "section_title": "Speaking: Passive Voice",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "89012345-6789-0123-4a5b-6c7d8e9f0a1e",
        "lesson_id": "e180fc7a-e3cc-4f26-bdb1-c8d1f6839b2b",
        "section_title": "MCQ: Passive Voice",
        "section_type": "MCQ",
        "position": 4,
    }
]

course_3_lesson_4_sections = [
    {
        "section_id": "90123456-7890-1234-5a6b-7c8d9e0f1a2e",
        "lesson_id": "ba47ddec-dc94-469c-a4b6-f0ec303c592a",
        "section_title": "Grammar: Modals",
        "section_type": "GRAMMAR",
        "position": 1,
    },
    {
        "section_id": "01234567-8901-2345-6a7b-8c9d0e1f2a3e",
        "lesson_id": "ba47ddec-dc94-469c-a4b6-f0ec303c592a",
        "section_title": "Vocabulary: Modals",
        "section_type": "VOCABULARY",
        "position": 2,
    },
    {
        "section_id": "11234567-8901-2345-6a7b-8c9d0e1f2a3e",
        "lesson_id": "ba47ddec-dc94-469c-a4b6-f0ec303c592a",
        "section_title": "Speaking: Modals",
        "section_type": "SPEAKING",
        "position": 3,
    },
    {
        "section_id": "21234567-8901-2345-6a7b-8c9d0e1f2a3e",
        "lesson_id": "ba47ddec-dc94-469c-a4b6-f0ec303c592a",
        "section_title": "MCQ: Modals",
        "section_type": "MCQ",
        "position": 4,
    }
]

courses_query = """
INSERT INTO courses (course_id, difficulty_level, course_title, course_description, position, published)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for course in course_list:
    cursor.execute(
        courses_query,
        (
            course["course_id"],
            course["difficulty_level"],
            course["course_title"],
            course["course_description"],
            course["position"],
            course["published"],
        ),
    )

lessons_query = """
INSERT INTO lessons (lesson_id, course_id, lesson_title, position, created_at, updated_at)
VALUES (%s, %s, %s, %s, NOW(), NOW())
"""

for lesson in lessons_list:
    cursor.execute(
        lessons_query,
        (
            lesson["lesson_id"],
            lesson["course_id"],
            lesson["lesson_title"],
            lesson["position"],
        ),
    )

course_list_sections = [
    *course_1_lesson_1_sections,
    *course_1_lesson_2_sections,
    *course_1_lesson_3_sections,
    *course_1_lesson_4_sections,
    *course_2_lesson_1_sections,
    *course_2_lesson_2_sections,
    *course_2_lesson_3_sections,
    *course_2_lesson_4_sections,
    *course_3_lesson_1_sections,
    *course_3_lesson_2_sections,
    *course_3_lesson_3_sections,
    *course_3_lesson_4_sections,
]

sections_query = """
INSERT INTO sections (section_id, lesson_id, section_title, section_type, position, created_at, updated_at)
VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
"""

for section in course_list_sections:
    cursor.execute(
        """
        INSERT INTO sections (section_id, lesson_id, section_title, section_type, position, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """,
        (section["section_id"], section["lesson_id"], section["section_title"], section["section_type"], section["position"])
    )
    
    if section["section_type"] == "GRAMMAR":
        cursor.execute("INSERT INTO section_grammar (section_id) VALUES (%s)", (section["section_id"],))
    elif section["section_type"] == "VOCABULARY":
        cursor.execute("INSERT INTO section_vocabulary (section_id) VALUES (%s)", (section["section_id"],))
    elif section["section_type"] == "SPEAKING":
        cursor.execute("INSERT INTO section_speaking (section_id) VALUES (%s)", (section["section_id"],))
    elif section["section_type"] == "MCQ":
        cursor.execute("INSERT INTO section_mcq_question (section_id) VALUES (%s)", (section["section_id"],))

# Mapping course number to course_id, lesson_id, grammar section_id, vocabulary section_id, and speaking section_id
course_mapping = {
    1: {
        "course_id": "f5058930-99f7-4de4-b7c6-cb1b8b4603c9",
        "lessons": {
            1: {
                "lesson_id": "5a12bf28-9a46-4d75-bd30-b9d9a8e5be1f", 
                "grammar_section_id": "03aafc20-d593-404f-9313-ee1a6fae1e5c",
                "vocab_section_id": "a18579b1-d283-4b28-ac95-2a71175774ca",
                "speaking_section_id": "0daa2750-207d-4ae9-8e9c-9ac7756ca11d"
            },
            2: {
                "lesson_id": "d2b065cc-d28b-44e7-bbec-06b49ade7626", 
                "grammar_section_id": "c04e3552-6f64-41e2-8cfd-a1254c754fcb",
                "vocab_section_id": "6c4fb5d9-04dc-42d0-92f3-4422c78e3255",
                "speaking_section_id": "8f2f070a-d319-458a-ae26-2017bee0b416"
            },
            3: {
                "lesson_id": "ad4a835d-a062-4c5d-aa49-9fbcef9a0986", 
                "grammar_section_id": "002818a2-8263-4374-8ca2-ecdcbfd1221b",
                "vocab_section_id": "0ecaf7e7-2409-4c16-9669-daf31d641260",
                "speaking_section_id": "1b53ba73-1b76-4353-9473-c1ee848af1d3"
            },
            4: {
                "lesson_id": "9450005d-ed64-42cb-b48c-bb0a68e0deae", 
                "grammar_section_id": "9a9cf94e-8e67-4fb7-b9fc-5295e1b62ad6",
                "vocab_section_id": "c0fef146-acef-4d9b-abe6-ee5802e30fd0",
                "speaking_section_id": "d5da1923-141e-46b3-9991-bbf9dfa9beed"
            },
        }
    },
    2: {
        "course_id": "90e60335-0fa8-4e6f-8849-6111c1a39499",
        "lessons": {
            1: {
                "lesson_id": "62001bba-532c-4824-bc4c-3ab900ee2f20", 
                "grammar_section_id": "f1a2b3c4-d5e6-7f89-0a1b-2c3d4e5f6a7b",
                "vocab_section_id": "a2b3c4d5-e6f7-8901-2a3b-4c5d6e7f8a9b",
                "speaking_section_id": "b3c4d5e6-f789-0123-4a5b-6c7d8e9f0a1b"
            },
            2: {
                "lesson_id": "58f30032-db8e-4a34-a328-6d3396c92cdd", 
                "grammar_section_id": "d5e6f789-0123-4567-8a9b-0c1d2e3f4a5b",
                "vocab_section_id": "e6f78901-2345-6789-0a1b-2c3d4e5f6a7c",
                "speaking_section_id": "f7890123-4567-8901-2a3b-4c5d6e7f8a9c"
            },
            3: {
                "lesson_id": "20fc11c1-e3a0-498c-ab19-9a30bb76e8d2", 
                "grammar_section_id": "90123456-7890-1234-5a6b-7c8d9e0f1a2c",
                "vocab_section_id": "01234567-8901-2345-6a7b-8c9d0e1f2a3c",
                "speaking_section_id": "12345678-9012-3456-7a8b-9c0d1e2f3a4c"
            },
            4: {
                "lesson_id": "284714fe-3b56-4b16-8d49-a62155b975ae", 
                "grammar_section_id": "34567890-1234-5678-9a0b-1c2d3e4f5a6c",
                "vocab_section_id": "45678901-2345-6789-0a1b-2c3d4e5f6a7c",
                "speaking_section_id": "56789012-3456-7890-1a2b-3c4d5e6f7a8c"
            },
        }
    },
    3: {
        "course_id": "bcb0f085-528b-434c-85e8-c857394bae87",
        "lessons": {
            1: {
                "lesson_id": "d73f36d6-2c6f-421c-a1e8-5231cb87a2c7", 
                "grammar_section_id": "78901234-5678-9012-3a4b-5c6d7e8f9a0c",
                "vocab_section_id": "89012345-6789-0123-4a5b-6c7d8e9f0a1d",
                "speaking_section_id": "90123456-7890-1234-5a6b-7c8d9e0f1a2d"
            },
            2: {
                "lesson_id": "193be07e-c02b-4714-abbc-3e961a3a57a4", 
                "grammar_section_id": "12345678-9012-3456-7a8b-9c0d1e2f3a4d",
                "vocab_section_id": "23456789-0123-4567-8a9b-0c1d2e3f4a5d",
                "speaking_section_id": "34567890-1234-5678-9a0b-1c2d3e4f5a6d"
            },
            3: {
                "lesson_id": "e180fc7a-e3cc-4f26-bdb1-c8d1f6839b2b", 
                "grammar_section_id": "56789012-3456-7890-1a2b-3c4d5e6f7a8d",
                "vocab_section_id": "67890123-4567-8901-2a3b-4c5d6e7f8a9d",
                "speaking_section_id": "78901234-5678-9012-3a4b-5c6d7e8f9a0d"
            },
            4: {
                "lesson_id": "ba47ddec-dc94-469c-a4b6-f0ec303c592a", 
                "grammar_section_id": "90123456-7890-1234-5a6b-7c8d9e0f1a2e",
                "vocab_section_id": "01234567-8901-2345-6a7b-8c9d0e1f2a3e",
                "speaking_section_id": "11234567-8901-2345-6a7b-8c9d0e1f2a3e"
            },
        }
    }
}

def extract_title_from_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
        return "Grammar Section"
    except Exception as e:
        print(f"Error reading title from {file_path}: {e}")
        return "Grammar Section"

all_grammar_data = []
materi_base_path = "MATERI/file-markdown-materi"

for course_num in range(1, 4):
    course_folder = f"course-{course_num}"
    course_path = os.path.join(materi_base_path, course_folder)
    
    if not os.path.exists(course_path):
        print(f"Warning: {course_path} does not exist")
        continue
    
    for lesson_num in range(1, 5):
        lesson_folder = f"lesson{course_num}-{lesson_num}"
        lesson_path = os.path.join(course_path, lesson_folder)
        
        if not os.path.exists(lesson_path):
            print(f"Warning: {lesson_path} does not exist")
            continue
        
        grammar_section_id = course_mapping[course_num]["lessons"][lesson_num]["grammar_section_id"]
        course_id = course_mapping[course_num]["course_id"]
        lesson_id = course_mapping[course_num]["lessons"][lesson_num]["lesson_id"]
        
        grammar_files = sorted([f for f in os.listdir(lesson_path) if f.startswith("grammar-") and f.endswith(".md")])
        
        for grammar_file in grammar_files:
            grammar_file_path = os.path.join(lesson_path, grammar_file)
            
            # Generate a unique UUID for grammar_id
            grammar_id = str(uuid.uuid4())
            
            # Extract title from markdown
            title = extract_title_from_markdown(grammar_file_path)
            
            # Construct S3 key: course_id/lesson_id/section_id/grammar_id.md
            s3_key = f"{course_id}/{lesson_id}/{grammar_section_id}/{grammar_id}.md"
            
            # Upload to S3
            print(f"Uploading {grammar_file_path} to S3 with key: {s3_key}")
            upload_result = upload_to_s3(grammar_file_path, s3_key)
            
            if upload_result:
                # Add to grammar data
                all_grammar_data.append({
                    "grammar_id": grammar_id,
                    "section_id": grammar_section_id,
                    "title": title,
                    "markdown_file_path": s3_key,
                })
                print(f"✓ Successfully processed: {title} (Course {course_num}, Lesson {lesson_num})")
            else:
                print(f"✗ Failed to upload {grammar_file_path}")

# Insert all grammar data into database
grammar_query = """
INSERT INTO grammars (grammar_id, section_id, title, markdown_file_path)
VALUES (%s, %s, %s, %s)
"""

for grammar in all_grammar_data:
    cursor.execute(
        grammar_query,
        (
            grammar["grammar_id"],
            grammar["section_id"],
            grammar["title"],
            grammar["markdown_file_path"],
        ),
    )
    print(f"✓ Inserted grammar: {grammar['title']} - S3 Key: {grammar['markdown_file_path']}")

print("\n=== VOCABULARY PROCESSING ===\n")

# English to Indonesian translation dictionary
translation_dict = {
    # Course 1 - Beginner
    "I": "Saya", "You": "Kamu/Anda", "He": "Dia (laki-laki)", "She": "Dia (perempuan)",
    "Hello": "Halo", "Name": "Nama", "Student": "Siswa/Pelajar", "Teacher": "Guru",
    "Friend": "Teman", "Happy": "Senang/Bahagia",
    "This": "Ini", "That": "Itu", "Book": "Buku", "Pen": "Pulpen",
    "Table": "Meja", "Chair": "Kursi", "My": "Milikku", "Your": "Milikmu",
    "His": "Miliknya (laki-laki)", "Her": "Miliknya (perempuan)",
    "Bag": "Tas", "Door": "Pintu", "Food": "Makanan", "House": "Rumah",
    "Phone": "Telepon", "Water": "Air",
    "Eat": "Makan", "Sleep": "Tidur", "Study": "Belajar", "Work": "Bekerja",
    "Play": "Bermain", "Every": "Setiap", "Day": "Hari", "Night": "Malam",
    "Morning": "Pagi", "Afternoon": "Siang/Sore",
    "Drink": "Minum", "Go": "Pergi", "Read": "Membaca", "Run": "Berlari", 
    "Walk": "Berjalan", "Write": "Menulis",
    "Big": "Besar", "Small": "Kecil", "Good": "Baik", "Bad": "Buruk",
    "Beautiful": "Cantik", "Beautifull": "Cantik", "Tall": "Tinggi", "Short": "Pendek", "Old": "Tua",
    "Young": "Muda", "New": "Baru", "Fast": "Cepat", "Slow": "Lambat",
    "Handsome": "Tampan", "Kind": "Baik hati", "Smart": "Pintar",
    
    # Course 2 - Intermediate
    "Yesterday": "Kemarin", "Last": "Terakhir", "Week": "Minggu", "Month": "Bulan",
    "Year": "Tahun", "Ago": "Yang lalu", "Was": "Adalah (lampau)", "Were": "Adalah (lampau jamak)",
    "Went": "Pergi (lampau)", "Came": "Datang (lampau)", "Bought": "Membeli (lampau)",
    "Forgot": "Lupa (lampau)", "Visited": "Mengunjungi (lampau)", "Received": "Menerima (lampau)",
    "Last week": "Minggu lalu", "Meeting": "Pertemuan", "Tired": "Lelah",
    "Will": "Akan", "Going": "Akan pergi", "Plan": "Rencana", "Future": "Masa depan",
    "Tomorrow": "Besok", "Next": "Berikutnya", "Soon": "Segera", "Later": "Nanti",
    "Promise": "Janji", "Hope": "Harapan", "Attend": "Hadir/Menghadiri", "Finish": "Selesai",
    "Join": "Bergabung", "Next month": "Bulan depan", "Probably": "Mungkin", "Tonight": "Malam ini",
    "Tonight ": "Malam ini", "Travel": "Bepergian",
    "Now": "Sekarang", "Currently": "Saat ini", "Right": "Benar/Tepat", "Moment": "Momen",
    "Busy": "Sibuk", "Watching": "Menonton", "Reading": "Membaca", "Writing": "Menulis",
    "Running": "Berlari", "Swimming": "Berenang",
    "At the moment": "Saat ini", "Cooking": "Memasak", "Driving": "Mengemudi",
    "Improving": "Meningkatkan", "Listening": "Mendengarkan", "Project": "Proyek",
    "Right now": "Sekarang juga", "Right now ": "Sekarang juga", "Waiting": "Menunggu",
    "Waiting ": "Menunggu", "Working": "Bekerja",
    "Better": "Lebih baik", "Worse": "Lebih buruk", "Bigger": "Lebih besar", "Smaller": "Lebih kecil",
    "Faster": "Lebih cepat", "Slower": "Lebih lambat", "Best": "Terbaik", "Worst": "Terburuk",
    "Biggest": "Terbesar", "Smallest": "Terkecil", "Than": "Daripada", "Most": "Paling",
    "Cheap": "Murah", "Difficult": "Sulit", "Easy": "Mudah", "Expensive": "Mahal",
    "Heavy": "Berat", "Important": "Penting",
    
    # Course 3 - Advanced
    "Already": "Sudah", "Yet": "Belum", "Since": "Sejak", "Recently": "Baru-baru ini",
    "Accomplished": "Tercapai", "Opportunity": "Kesempatan", "Duration": "Durasi", 
    "Deadline": "Tenggat waktu", "Consequence": "Konsekuensi", "Several": "Beberapa",
    "If": "Jika", "Would": "Akan", "Could": "Bisa", "Wish": "Berharap",
    "Dream": "Mimpi", "Imagine": "Membayangkan", "Suppose": "Anggaplah", "Reality": "Kenyataan",
    "Condition": "Kondisi", "Situation": "Situasi",
    "Made": "Dibuat", "Done": "Dilakukan", "Written": "Ditulis", "Spoken": "Diucapkan",
    "Built": "Dibangun", "Designed": "Dirancang", "Created": "Diciptakan", "Produced": "Diproduksi",
    "Published": "Diterbitkan", "Invented": "Diciptakan",
    "Must": "Harus", "Can't": "Tidak bisa", "Certain": "Pasti", "Impossible": "Mustahil",
    "Perhaps": "Mungkin", "Obviously": "Jelas", "Realize": "Menyadari", "Logic": "Logika",
    "Evidence": "Bukti", "Conclusion": "Kesimpulan", "Exhausted": "Kelelahan", 
    "Misunderstanding": "Kesalahpahaman",
}

# Function to get translation (fallback to word itself if not in dictionary)
def get_translation(word):
    # Check exact match first
    if word in translation_dict:
        return translation_dict[word]
    
    # Check case-insensitive match
    for key, value in translation_dict.items():
        if key.lower() == word.lower():
            return value
    
    # Fallback: return the word itself with note
    return f"{word} (perlu diterjemahkan)"

# Auto-generate vocabulary data from MATERI audio folder
all_vocabulary_data = []
audio_base_path = "MATERI/audio-materi/courses"

for course_num in range(1, 4):  # course-1, course-2, course-3
    course_folder = f"course-{course_num}"
    course_path = os.path.join(audio_base_path, course_folder)
    
    if not os.path.exists(course_path):
        print(f"Warning: {course_path} does not exist")
        continue
    
    for lesson_num in range(1, 5):  # lesson 1-4 for each course
        lesson_folder = f"lesson{course_num}-{lesson_num}"
        lesson_path = os.path.join(course_path, lesson_folder, "vocab")
        
        if not os.path.exists(lesson_path):
            print(f"Warning: {lesson_path} does not exist")
            continue
        
        # Get the vocabulary section_id for this lesson
        vocab_section_id = course_mapping[course_num]["lessons"][lesson_num]["vocab_section_id"]
        course_id = course_mapping[course_num]["course_id"]
        lesson_id = course_mapping[course_num]["lessons"][lesson_num]["lesson_id"]
        
        # Find all audio files in vocab folder
        vocab_files = sorted([f for f in os.listdir(lesson_path) if f.endswith(".mp3")])
        
        for vocab_file in vocab_files:
            vocab_file_path = os.path.join(lesson_path, vocab_file)
            
            # Generate a unique UUID for vocab_id
            vocab_id = str(uuid.uuid4())
            
            # Extract word from filename (remove .mp3 extension)
            word = os.path.splitext(vocab_file)[0]
            
            # Get translation
            translation = get_translation(word)
            
            # Construct S3 key: course_id/lesson_id/section_id/vocab_id.mp3
            s3_key = f"{course_id}/{lesson_id}/{vocab_section_id}/{vocab_id}.mp3"
            
            # Upload to S3
            print(f"Uploading {vocab_file_path} to S3 with key: {s3_key}")
            upload_result = upload_to_s3(vocab_file_path, s3_key)
            
            if upload_result:
                # Add to vocabulary data
                all_vocabulary_data.append({
                    "vocab_id": vocab_id,
                    "section_id": vocab_section_id,
                    "word": word,
                    "translation": translation,
                    "vocab_audio_path": s3_key,
                })
                print(f"✓ Successfully processed: {word} → {translation} (Course {course_num}, Lesson {lesson_num})")
            else:
                print(f"✗ Failed to upload {vocab_file_path}")

# Insert all vocabulary data into database
vocabulary_query = """
INSERT INTO vocabularies (vocab_id, section_id, word, translation, vocab_audio_path)
VALUES (%s, %s, %s, %s, %s)
"""

for vocab in all_vocabulary_data:
    cursor.execute(
        vocabulary_query,
        (
            vocab["vocab_id"],
            vocab["section_id"],
            vocab["word"],
            vocab["translation"],
            vocab["vocab_audio_path"],
        ),
    )
    print(f"✓ Inserted vocabulary: {vocab['word']} → {vocab['translation']} - S3 Key: {vocab['vocab_audio_path']}")

# Auto-generate speaking exercise data from MATERI audio folder (practice line)
all_speaking_data = []

for course_num in range(1, 4):  # course-1, course-2, course-3
    course_folder = f"course-{course_num}"
    course_path = os.path.join(audio_base_path, course_folder)
    
    if not os.path.exists(course_path):
        print(f"Warning: {course_path} does not exist")
        continue
    
    for lesson_num in range(1, 5):  # lesson 1-4 for each course
        lesson_folder = f"lesson{course_num}-{lesson_num}"
        lesson_path = os.path.join(course_path, lesson_folder, "practice line")
        
        if not os.path.exists(lesson_path):
            print(f"Warning: {lesson_path} does not exist")
            continue
        
        # Get the speaking section_id for this lesson
        speaking_section_id = course_mapping[course_num]["lessons"][lesson_num]["speaking_section_id"]
        course_id = course_mapping[course_num]["course_id"]
        lesson_id = course_mapping[course_num]["lessons"][lesson_num]["lesson_id"]
        
        # Find all audio files in practice line folder
        speaking_files = sorted([f for f in os.listdir(lesson_path) if f.endswith(".mp3")])
        
        for speaking_file in speaking_files:
            speaking_file_path = os.path.join(lesson_path, speaking_file)
            
            # Generate a unique UUID for speaking_id
            speaking_id = str(uuid.uuid4())
            
            # Extract sentence from filename (remove .mp3 extension)
            sentence = os.path.splitext(speaking_file)[0]
            
            # Construct S3 key: course_id/lesson_id/section_id/speaking_id.mp3
            s3_key = f"{course_id}/{lesson_id}/{speaking_section_id}/{speaking_id}.mp3"
            
            # Upload to S3
            print(f"Uploading {speaking_file_path} to S3 with key: {s3_key}")
            upload_result = upload_to_s3(speaking_file_path, s3_key)
            
            if upload_result:
                # Add to speaking data
                all_speaking_data.append({
                    "speaking_id": speaking_id,
                    "section_id": speaking_section_id,
                    "sentence": sentence,
                    "speaking_audio_path": s3_key,
                })
                print(f"✓ Successfully processed: {sentence} (Course {course_num}, Lesson {lesson_num})")
            else:
                print(f"✗ Failed to upload {speaking_file_path}")

# Insert all speaking exercise data into database
speaking_query = """
INSERT INTO speaking (speaking_id, section_id, sentence, speaking_audio_path)
VALUES (%s, %s, %s, %s)
"""

for speaking in all_speaking_data:
    cursor.execute(
        speaking_query,
        (
            speaking["speaking_id"],
            speaking["section_id"],
            speaking["sentence"],
            speaking["speaking_audio_path"],
        ),
    )
    print(f"✓ Inserted speaking exercise: {speaking['sentence']} - S3 Key: {speaking['speaking_audio_path']}")

connection.commit()