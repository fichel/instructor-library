# A common use case for a recursive schema is a comment tree, where each comment can have subcomments

from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import instructor

load_dotenv()


# define the data model
class Comment(BaseModel):
    text: str
    subcomments: list["Comment"] = Field(default_factory=list)


# patch the openai client with instructor
client = instructor.from_openai(OpenAI())


# helper function to get the comment tree
def get_comment_tree(query: str) -> Comment:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Comment,
        messages=[{"role": "user", "content": query}],
    )
    return response


# helper function to print the comment tree
def print_comment_tree(comment: Comment, level: int = 0):
    print("  " * level + "- " + comment.text)
    for subcomment in comment.subcomments:
        print_comment_tree(subcomment, level + 1)


if __name__ == "__main__":
    query = """Lakers defeat Warriors 124-120 in an absolute thriller! LeBron (35pts/12ast/8reb) and Curry (42pts/8ast) both went OFF but Lakers' defense came up clutch in the final minutes.
        • That block by AD on Wiggins with 45 seconds left was INSANE. Completely changed the momentum.
            • AD's defensive positioning was perfect but let's be real, Wiggins should've pump faked there
                • Kerr should've called a timeout before that possession, Warriors offense was completely stagnant
                • Nah, you want your players to play through it in crunch time. That's how you build experience.
        • Curry was absolutely cooking in the 3rd quarter. That stretch of 4 straight threes was vintage Chef
            • Yeah but where was that same energy in the 4th? Only 2 points in the final 6 minutes
                • Lakers' adjustment to put Reaves on him and double off screens worked perfectly
                    • Reaves is so underrated defensively, his footwork is elite
        • LeBron haters real quiet tonight 👀 35/12/8 at age 39 is ridiculous
            • Curry had better efficiency though. 42 points on 65% TS% vs LeBron's 54% TS%
                • Raw TS% doesn't tell the whole story, LeBron was creating for others and controlling pace
                    • Facts. LeBron had 12 assists to Curry's 8, and 6 of those came in clutch time
            • Both GOATs in their own right, we should appreciate watching them battle
                • Exactly, we're witnessing history. These matchups will be legendary in 20 years"""
    comment = get_comment_tree(query)
    print_comment_tree(comment)
