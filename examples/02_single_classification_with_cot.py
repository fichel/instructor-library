from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv
import instructor
from typing import Literal

load_dotenv()

# patch the openai client with instructor
client = instructor.from_openai(OpenAI())


# define the data model
class ClassificationResponse(BaseModel):
    """
    A few-shot example of a spam detector.

    Examples:
    - "Buy cheap tickets to any game!": SPAM
    - "Meeting at 10am tomorrow in the conference room.": NOT_SPAM
    - "Get rich quick! Work from home!": SPAM
    - "Can you review this document by EOD?": NOT_SPAM
    - "CONGRATULATIONS! You've won $1,000,000!!!": SPAM
    - "The project deadline has been extended to Friday": NOT_SPAM
    """

    chain_of_thought: str = Field(
        ..., description="The chain of thought that led to the classification"
    )
    label: Literal["SPAM", "NOT_SPAM"] = Field(
        ..., description="The predicted class label"
    )


def classify(data: str) -> ClassificationResponse:
    """Perform single-label classification on the input data."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=ClassificationResponse,
        messages=[
            {
                "role": "user",
                "content": f"Classify the following message: {data}",
            }
        ],
    )
    return response


if __name__ == "__main__":
    for data, label in [
        ("Click here to claim your free iPhone 13!", "SPAM"),
        ("The quarterly report is ready for your review.", "NOT_SPAM"),
        ("URGENT: Your account will be suspended unless you verify now!", "SPAM"),
        ("Could you send me the meeting notes from yesterday?", "NOT_SPAM"),
    ]:
        prediction = classify(data)
        assert prediction.label == label, f"Expected {label} but got {prediction.label}"
        print(f"Text: {data} -- Prediction Label: {prediction.label}\n")
