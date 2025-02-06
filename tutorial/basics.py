import instructor
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# -----------------------------------------------------------------------------
# Extract structured data from a text
# -----------------------------------------------------------------------------

# load the environment variables
load_dotenv()


# define the schema
class UserInfo(BaseModel):
    name: str
    age: int


# initialize the client
client = instructor.from_openai(OpenAI())

# extract structured data
user_info = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo,
    messages=[{"role": "user", "content": "Hey, I'm John Doe. I'm 30 years old."}],
)

print(user_info.name)
print(user_info.age)

# -----------------------------------------------------------------------------
# Field Validation
# -----------------------------------------------------------------------------

from pydantic import PositiveInt


class UserInfo2(BaseModel):
    name: str
    age: PositiveInt


# this will raise an error because the age is negative.
user_info = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo2,
    messages=[{"role": "user", "content": "Hey, I'm John Doe. I'm -10 years old."}],
    max_retries=0,
)

print(user_info.name)
print(user_info.age)

# -----------------------------------------------------------------------------
# Custom Validation
# -----------------------------------------------------------------------------

from pydantic import field_validator


class UserInfo3(BaseModel):
    name: str
    age: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, value: int):
        if not (0 < value > 18):
            raise ValueError("Age must be between 0 and 18")
        return value


# this will raise an error because the age is not between 0 and 18.
user_info = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo3,
    messages=[{"role": "user", "content": "Hey, I'm John Doe. I'm 12 years old."}],
    max_retries=0,
)

print(user_info.name)
print(user_info.age)

# -----------------------------------------------------------------------------
# Handling Nested Data
# -----------------------------------------------------------------------------

from typing import Optional


class Address(BaseModel):
    street: Optional[str]
    city: str
    state: str


class UserInfo4(BaseModel):
    name: str
    age: int
    address: Address


user_info = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=UserInfo4,
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant that extracts user information from a text. \
                Do not make up any information. Only use the information provided in the text. \
                The only thing you can infer is the state, based on the city name.",
        },
        {
            "role": "user",
            "content": "Hey, I'm John Doe. I live in New York city.",
        },
    ],
    max_retries=0,
)

print(user_info.name)
print(user_info.age)
print(user_info.address)
