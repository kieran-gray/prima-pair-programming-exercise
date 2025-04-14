from unittest.mock import AsyncMock
from src.application.upsell_service import UpsellService
from src.clients.ExternalClient import APIException, ExternalApiClient, OwnedVehicle
from src.application.dtos import UpsellOpportunity, Policy


async def test_find_potential_upsells_no_data():
    client = ExternalApiClient()

    policies = [
        Policy(person_id="P1", vehicle_id="V8"),
        Policy(person_id="P2", vehicle_id="V6"),
    ]

    upsell_service = UpsellService(external_api_client=client)
    upsells = await upsell_service.find_potential_upsells(policies=policies)
    assert upsells == []


async def test_find_potential_upsells_with_example():
    client = ExternalApiClient()
    client._get_data = AsyncMock(
        return_value=[
            OwnedVehicle(person_id="P1", vehicle_id="V8"),
            OwnedVehicle(person_id="P2", vehicle_id="V6"),
            OwnedVehicle(person_id="P1", vehicle_id="V3"),
        ]
    )

    policies = [
        Policy(person_id="P1", vehicle_id="V8"),
        Policy(person_id="P2", vehicle_id="V6"),
    ]

    upsell_service = UpsellService(external_api_client=client)
    upsells = await upsell_service.find_potential_upsells(policies=policies)
    assert upsells == [UpsellOpportunity(person_id="P1", vehicle_id="V3")]


async def test_find_potential_upsells_no_upsells():
    client = ExternalApiClient()
    client._get_data = AsyncMock(
        return_value=[
            OwnedVehicle(person_id="P1", vehicle_id="V8"),
            OwnedVehicle(person_id="P2", vehicle_id="V6"),
        ]
    )

    policies = [
        Policy(person_id="P1", vehicle_id="V8"),
        Policy(person_id="P2", vehicle_id="V6"),
    ]

    upsell_service = UpsellService(external_api_client=client)
    upsells = await upsell_service.find_potential_upsells(policies=policies)
    assert upsells == []


async def test_find_potential_upsells_more_than_one():
    client = ExternalApiClient()
    client._get_data = AsyncMock(
        return_value=[
            OwnedVehicle(person_id="P1", vehicle_id="V8"),
            OwnedVehicle(person_id="P2", vehicle_id="V6"),
            OwnedVehicle(person_id="P1", vehicle_id="V3"),
            OwnedVehicle(person_id="P1", vehicle_id="V4"),
        ]
    )

    policies = [
        Policy(person_id="P1", vehicle_id="V8"),
        Policy(person_id="P2", vehicle_id="V6"),
    ]

    upsell_service = UpsellService(external_api_client=client)
    upsells = await upsell_service.find_potential_upsells(policies=policies)
    assert upsells == [
        UpsellOpportunity(person_id="P1", vehicle_id="V3"),
        UpsellOpportunity(person_id="P1", vehicle_id="V4"),
    ]


async def test_find_potential_upsells_more_than_one_policy():
    client = ExternalApiClient()
    client._get_data = AsyncMock(
        return_value=[
            OwnedVehicle(person_id="P1", vehicle_id="V8"),
            OwnedVehicle(person_id="P2", vehicle_id="V6"),
            OwnedVehicle(person_id="P1", vehicle_id="V3"),
        ]
    )

    policies = [
        Policy(person_id="P1", vehicle_id="V8"),
        Policy(person_id="P1", vehicle_id="V3"),
        Policy(person_id="P2", vehicle_id="V6"),
    ]

    upsell_service = UpsellService(external_api_client=client)
    upsells = await upsell_service.find_potential_upsells(policies=policies)
    assert upsells == []


async def test_find_potential_upsells_api_exception():
    client = ExternalApiClient()
    client._get_data = AsyncMock(side_effect=APIException("API connection failed"))
    
    policies = [
        Policy(person_id="P1", vehicle_id="V8"),
        Policy(person_id="P2", vehicle_id="V6"),
    ]
    
    upsell_service = UpsellService(external_api_client=client)
    
    upsells = await upsell_service.find_potential_upsells(policies=policies)
    assert upsells == []
