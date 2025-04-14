from dataclasses import dataclass


@dataclass
class Policy:
    person_id: str
    vehicle_id: str


@dataclass
class UpsellOpportunity:
    person_id: str
    vehicle_id: str
