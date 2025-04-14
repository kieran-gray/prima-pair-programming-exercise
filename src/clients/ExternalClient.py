from dataclasses import dataclass


class APIException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


@dataclass
class OwnedVehicle:
    person_id: str
    vehicle_id: str


class ExternalApiClient:
    async def _get_data(self) -> list[OwnedVehicle]:
        return []

    async def get_owned_vehicles(
        self, person_ids: list[str]
    ) -> list[OwnedVehicle]:
        data = await self._get_data()
        return [vehicle for vehicle in data if vehicle.person_id in person_ids]
