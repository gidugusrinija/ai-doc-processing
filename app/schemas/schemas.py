from typing import Optional, Union
from pydantic import BaseModel, Field


class NetworkBenefit(BaseModel):
    copay: Optional[Union[float, str]] = None
    coinsurance: Optional[Union[float, str]] = None


class ServiceBenefit(BaseModel):
    service_name: str

    preferred_network: NetworkBenefit = Field(
        default_factory=NetworkBenefit
    )

    standard_network: NetworkBenefit = Field(
        default_factory=NetworkBenefit
    )

    non_participating: NetworkBenefit = Field(
        default_factory=NetworkBenefit
    )


class BenefitExtraction(BaseModel):
    benefit_category: str

    services: list[ServiceBenefit] = Field(
        default_factory=list
    )

    currency: str = "USD"

    notes: list[str] = Field(
        default_factory=list
    )

    additional_detail: Optional[str] = None