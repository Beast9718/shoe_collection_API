shoes_prefix=f"/api/v1/shoes"

def test_get_all_shoes(test_client,fake_shoe_service,fake_session):
    response=test_client.get(
        url=f"{shoes_prefix}"
    )
    assert fake_shoe_service.get_all_shoes_called_once()
    assert fake_shoe_service.get_all_shoes_called_once_with(fake_session)