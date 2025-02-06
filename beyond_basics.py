import instructor
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

# -----------------------------------------------------------------------------
# Dynamic prompting
# -----------------------------------------------------------------------------
from pydantic import Field
from typing import Optional


# define the data model
class Ingredient(BaseModel):
    name: str
    quantity: int
    unit: Optional[str] = Field(
        default=None,
        description="The unit of measurement. It should always be singular",
    )


class Recipe(BaseModel):
    name: str = Field(
        description="The name of the recipe. It should be creative like a title of a movie or a song"
    )
    ingredients: list[Ingredient] = Field(
        default_factory=list,
        description="A list of ingredients",
    )
    steps: list[str]


# patch the openai client with instructor
client = instructor.from_openai(OpenAI())

recipe = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=Recipe,
    messages=[{"role": "user", "content": "Make me a recipe for a lasagna."}],
)

print(recipe.name)
pprint(recipe.ingredients)
pprint(recipe.steps)


def get_recipe(ingredients: str) -> Recipe:
    prompt = f"Create a recipe using the following ingredient: {ingredients}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=1.0,
        response_model=Recipe,
        messages=[{"role": "user", "content": prompt}],
    )
    return response


recipe = get_recipe("rice, beans, tomato, onion")
print(recipe.name)
pprint(recipe.ingredients)
pprint(recipe.steps)

# -----------------------------------------------------------------------------
# Routing with Conditional Logic
# -----------------------------------------------------------------------------

from typing import Literal, Any, Type


class Intent(BaseModel):
    type: Literal["weather", "stocks", "generic"] = Field(default="generic")
    query: str


class WeatherInfo(BaseModel):
    city: str
    temperature: float
    condition: str
    intent: Intent


class StockInfo(BaseModel):
    ticker: str
    price: float
    daily_change: float
    intent: Intent


class GenericResponse(BaseModel):
    response: str
    intent: Intent


client = instructor.from_openai(OpenAI())


def get_intent(query: str) -> Intent:
    prompt = f"Determine the intent of the following query: {query}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Intent,
        messages=[{"role": "user", "content": prompt}],
        max_retries=0,
    )
    return response


intent = get_intent("What is the weather in Tokyo?")
print(intent.type)
print(intent.query)

intent = get_intent("What is the stock price of Apple?")
print(intent.type)
print(intent.query)


# helper function to route the intent
def process_user_query(query: str) -> Any:
    intent = get_intent(query)
    if intent.type == "weather":
        return get_completion(query=query, response_model=WeatherInfo)
    elif intent.type == "stocks":
        return get_completion(query=query, response_model=StockInfo)
    else:
        return get_completion(query=query, response_model=GenericResponse)


# helper function to get the completion
def get_completion(
    query: str,
    response_model: Type[BaseModel],
    model: str = "gpt-4o-mini",
) -> Any:
    return client.chat.completions.create(
        model=model,
        response_model=response_model,
        messages=[{"role": "user", "content": query}],
    )


response = process_user_query("What is the weather in Tokyo?")
print(response.intent.type)
print(response.city)
print(response.temperature)
print(response.condition)

response = process_user_query("What is the stock price of Apple?")
print(response.intent.type)
print(response.ticker)
print(response.price)
print(response.daily_change)

response = process_user_query("Tell me a bear joke")
print(response.intent.type)
print(response.response)
