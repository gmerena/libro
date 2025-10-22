"""
Demonstrációs teszt - Fixture használat szemléltetése
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_fixture_demonstration(client: AsyncClient):
    """
    Ez a teszt megmutatja, hogy a client fixture hogyan működik.
    
    A 'client' paraméter AUTOMATIKUSAN kap egy AsyncClient-et
    a conftest.py-ból.
    """
    print("\n🎯 Teszt kezdődik")
    print(f"   Client típusa: {type(client)}")
    print(f"   Base URL: {client.base_url}")
    
    # Használjuk a client-et
    response = await client.get("/api/v1/members")
    
    print(f"   Status code: {response.status_code}")
    print("🎯 Teszt vége\n")
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_another_test_gets_new_client(client: AsyncClient):
    """
    Ez a teszt egy ÚJ client fixture-t kap!
    Minden teszt friss client-tel indul.
    """
    print("\n🎯 Második teszt - ÚJ client")
    print(f"   Client típusa: {type(client)}")
    
    response = await client.get("/api/v1/books")
    assert response.status_code == 200
    print("🎯 Második teszt vége\n")