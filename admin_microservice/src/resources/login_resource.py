from pydantic import BaseModel, Field
class EmployeeLoginResource(BaseModel):
    email: str = Field(
        default=...,
        description="Email of the employee to login as.",
        examples=["hans@gmail.com"]
    )
    password: str = Field(
        default=...,
        description="Password of the employee to login as.",
        examples=["hans123"]
    )
