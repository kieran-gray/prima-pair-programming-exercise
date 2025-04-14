import asyncio
import logging

from src.application.dtos import UpsellOpportunity, Policy
from src.application.utils import chunk_list
from src.clients.ExternalClient import (
    APIException,
    ExternalApiClient,
    OwnedVehicle,
)

log = logging.getLogger(__name__)


class UpsellService:
    def __init__(self, external_api_client: ExternalApiClient | None = None):
        self._api_client: ExternalApiClient = (
            external_api_client or ExternalApiClient()
        )

    def _upsells_from_owned_vehicles(
        self,
        owned_vehicles: list[OwnedVehicle],
        vehicles_with_policies: set[str],
    ) -> list[UpsellOpportunity]:
        upsells = []
        for owned_vehicle in owned_vehicles:
            if owned_vehicle.vehicle_id not in vehicles_with_policies:
                upsells.append(
                    UpsellOpportunity(
                        person_id=owned_vehicle.person_id,
                        vehicle_id=owned_vehicle.vehicle_id,
                    )
                )
        return upsells

    async def _get_vehicles_for_batch(
        self, person_ids: list[str]
    ) -> list[OwnedVehicle] | None:
        try:
            return await self._api_client.get_owned_vehicles(
                person_ids=person_ids
            )
        except APIException as err:
            # Would likely be better to let it error for alerting purposes
            log.critical(
                f"Error fetching owned vehicles for ids {person_ids}: {err}"
            )
            return None

    async def find_potential_upsells(
        self, policies: list[Policy]
    ) -> list[UpsellOpportunity]:
        person_ids: set[str] = set()
        vehicles_with_policies: set[str] = set()

        for policy in policies:
            person_ids.add(policy.person_id)
            vehicles_with_policies.add(policy.vehicle_id)

        upsells = []
        tasks = [
            self._get_vehicles_for_batch(batch)
            for batch in chunk_list(list=list(person_ids))
        ]
        results = await asyncio.gather(*tasks)
        for batch in results:
            if not batch:
                continue
            upsells.extend(
                self._upsells_from_owned_vehicles(
                    owned_vehicles=batch,
                    vehicles_with_policies=vehicles_with_policies,
                )
            )
        return upsells
