from typing import Optional, Any
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator, UUID4


class CustomerBaseResource(BaseModel):
    email: EmailStr = Field(
        default=...,
        description="Email of the customer.",
        examples=["henrik@gmail.com"]
    )

    phone_number: Optional[str] = Field(
        default=...,
        description="Phone number of the customer.",
        examples=["10203040"]
    )

    first_name: str = Field(
        default=...,
        description="First name of the customer.",
        examples=["Henrik"]
    )

    last_name: str = Field(
        default=...,
        description="Last name of the customer.",
        examples=["Henriksen"]
    )

    address: Optional[str] = Field(
        default=...,
        description="Address of the customer.",
        examples=["Randomgade nr. 10 4. tv."]
    )

    model_config = ConfigDict(from_attributes=True)



class CustomerCreateOrUpdateResource(CustomerBaseResource):

    @field_validator('email')
    def validate_email(cls, email: str) -> str:
        minimum_length_of_email = 8
        maximum_length_of_email = 100
        email_length = len(email)
        if email_length < minimum_length_of_email:
            raise ValueError(
                f"The given email {email} is too short, "
                f"it must be at least {minimum_length_of_email} characters long.")
        if email_length > maximum_length_of_email:
            raise ValueError(
                f"The given email {email} is {email_length - maximum_length_of_email} characters too long, "
                f"it can only be maximum {maximum_length_of_email} characters and not {email_length}.")
        return email

    @field_validator('phone_number')
    def validate_phone_number(cls, phone_number: Optional[str]) -> Optional[str]:
        minimum_length_of_phone_number = 8
        maximum_length_of_phone_number = 30
        maximum_length_of_phone_number_that_starts_with_plus = maximum_length_of_phone_number - 3
        if phone_number is not None:
            phone_number = phone_number.strip()
            length_of_phone_number = len(phone_number)
            if phone_number.startswith('+') and length_of_phone_number <= maximum_length_of_phone_number_that_starts_with_plus:
                length_of_phone_number -= 3
            if length_of_phone_number == 0:
                return None
            if length_of_phone_number < minimum_length_of_phone_number:
                raise ValueError(f"The given phone number {phone_number} is too short, "
                                 f"it must be at least {minimum_length_of_phone_number} characters long.")
            if length_of_phone_number > maximum_length_of_phone_number:
                raise ValueError(f"The given phone number {phone_number} is too long, "
                                 f"it can only be maximum {maximum_length_of_phone_number} characters long.")
            if ' ' in phone_number:
                raise ValueError(f"The given phone number {phone_number} contains whitespace.")
            if '+' in phone_number:
                if not phone_number.startswith('+') or '+' in phone_number[1:]:
                    raise ValueError(f"The given phone number {phone_number} can only contain digits after the +.")
            if not phone_number.isdigit() and not phone_number[1:].isdigit():
                raise ValueError(f"The given phone number {phone_number} can only contain digits.")
        return phone_number

    @field_validator('first_name')
    def validate_first_name(cls, first_name: str) -> str:
        minimum_length_of_first_name = 1
        maximum_length_of_first_name = 45
        first_name = first_name.strip()
        if len(first_name) < minimum_length_of_first_name:
            raise ValueError(f"The given first name {first_name} is too short, "
                             f"it must be at least {minimum_length_of_first_name} characters long.")
        if len(first_name) > maximum_length_of_first_name:
            raise ValueError(f"The given first name {first_name} is too long, "
                             f"it can only be maximum {maximum_length_of_first_name} characters long.")
        if '  ' in first_name:
            raise ValueError(f"The given first name {first_name} contains extra whitespaces.")
        if not all(part.isalpha() for part in first_name.replace('-', ' ').split()):
            raise ValueError(f"The given first name {first_name} can only contain alphabetic characters.")
        if first_name.startswith('-') or first_name.endswith('-'):
            raise ValueError(f"The given first name {first_name} starts or ends with a hyphen.")
        if ' -' in first_name or '- ' in first_name:
            raise ValueError(f"The given first name {first_name} contains whitespace before or after a hyphen.")
        return first_name.title()

    @field_validator('last_name')
    def validate_last_name(cls, last_name: str) -> str:
        minimum_length_of_last_name = 1
        maximum_length_of_last_name = 45
        last_name = last_name.strip()
        if len(last_name) < minimum_length_of_last_name:
            raise ValueError(f"The given last name {last_name} is too short, "
                             f"it must be at least {minimum_length_of_last_name} characters long.")
        if len(last_name) > maximum_length_of_last_name:
            raise ValueError(f"The given last name {last_name} is too long, "
                             f"it can only be maximum {maximum_length_of_last_name} characters long.")
        if ' ' in last_name:
            raise ValueError(f"The given last name {last_name} contains whitespace.")
        if not all(part.isalpha() for part in last_name.replace('-', ' ').split()):
            raise ValueError(f"The given last name {last_name} can only contain alphabetic characters.")
        if last_name.startswith('-') or last_name.endswith('-'):
            raise ValueError(f"The given last name {last_name} starts or ends with a hyphen.")
        return last_name.title()

    @field_validator('address')
    def validate_address(cls, address: Optional[str]) -> Optional[str]:
        minimum_length_of_address = 5
        maximum_length_of_address = 255
        if address is not None:
            address = address.strip()
            if len(address) == 0:
                return None
            if len(address) < minimum_length_of_address:
                raise ValueError(f"The given address {address} is too short, "
                                 f"it must be at least {minimum_length_of_address} characters long.")
            if len(address) > maximum_length_of_address:
                raise ValueError(f"The given address {address} is too long, "
                                 f"it can only be maximum {maximum_length_of_address} characters long.")
            if '  ' in address:
                raise ValueError(f"The given address {address} contains extra whitespace.")
        return address


class CustomerCreateResource(CustomerCreateOrUpdateResource):
    id: UUID4 = Field(
        default=...,
        description="ID of the customer to create.",
        examples=["a904021a-0777-485f-bb84-22146717602d"]
    )


class CustomerUpdateResource(CustomerCreateOrUpdateResource):
    email: EmailStr = Field(
        default=None,
        description="Updated email of the customer.",
        examples=["new@gmail.com"]
    )

    phone_number: Optional[str] = Field(
        default=None,
        description="Updated phone number of the customer.",
        examples=["10203040"]
    )

    first_name: str = Field(
        default=None,
        description="Updated first name of the customer.",
        examples=["New"]
    )

    last_name: str = Field(
        default=None,
        description="Updated last name of the customer.",
        examples=["Name"]
    )

    address: Optional[str] = Field(
        default=None,
        description="Updated address of the customer.",
        examples=["Randomgade nr. 10 4. tv."]
    )

    def get_updated_fields(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)


class CustomerReturnResource(CustomerBaseResource):
    id: str = Field(
        default=...,
        description="The UUID for the customer.",
        examples=["0ac1d668-55aa-46a1-898a-8fa61457facb"]
    )
