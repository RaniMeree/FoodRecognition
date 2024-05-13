import pydantic
from typing import Any
from pydantic import validator, Field, computed_field

class FoodCalories(pydantic.BaseModel):
    id: int
    name: str

class Calculation(pydantic.BaseModel):
    food_id: int
    intake_count: float

class FoodDetails(pydantic.BaseModel):
    name: str
    calories: float

class IntakeRes(pydantic.BaseModel):
    food: FoodDetails = Field(exclude=True)
    count: float
    date: Any

    @computed_field
    @property
    def food_calories(self) -> float:
        return self.food.calories
    
    @computed_field
    @property
    def food_name(self) -> str:
        return self.food.name
    
    class Config:
        fields_order =  ['food_name', 'food_calories', 'count', 'date']


    
