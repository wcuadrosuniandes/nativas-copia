user = {
            "id": "a016c592-9271-42a7-b6f3-64a63a2a1cef",
            "username": "earlene",
            "email": "paige.bergstrom72@gmail.com",
            "fullName": "mae sipes",
            "dni": "189",
            "phoneNumber": "3806416390",
            "status": "POR_VERIFICAR",
        }
post =  {
        "id": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "userId": "a016c592-9271-42a7-b6f3-64a63a2a1cef",
        "routeId": "2401f7e4-d03e-4fad-9328-1f0e1e2a5ece",
        "expireAt": "2024-03-05T15:02:53.498000",
        "createdAt": "2024-02-27T12:34:15.137646"
    }
post_alt =  {
        "id": "a016c592-9271-42a7-b6f3-64a63a2a1cef",
        "userId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "routeId": "2401f7e4-d03e-4fad-9328-1f0e1e2a5ece",
        "expireAt": "2024-03-05T15:02:53.498000",
        "createdAt": "2024-02-27T12:34:15.137646"
    }
route = {
    "id": "2401f7e4-d03e-4fad-9328-1f0e1e2a5ece",
    "flightId": "554",
    "sourceAirportCode": "BOG",
    "sourceCountry": "Colombia",
    "destinyAirportCode": "LGW",
    "destinyCountry": "Inglaterra",
    "bagCost": 603,
    "plannedStartDate": "2024-02-29T15:01:53.921000",
    "plannedEndDate": "2024-03-08T15:01:53.921000",
    "createdAt": "2024-02-27T12:34:14.751117"
}
offers= [
    {
        "id": "ccc4dd20-1434-49ec-a8bd-6f61c87af8c8",
        "postId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "description": "debitis tempora libero",
        "size": "LARGE",
        "fragile": False,
        "offer": 162.0,
        "createdAt": "2024-02-27T12:34:14.728826",
        "userId": "a016c592-9271-42a7-b6f3-64a63a2a1cef"
    },
    {
        "id": "f5ab144e-4239-4af6-b576-5f658bd10f4b",
        "postId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "description": "ut quia fugit",
        "size": "SMALL",
        "fragile": True,
        "offer": 343.0,
        "createdAt": "2024-02-27T12:34:14.728826",
        "userId": "a016c592-9271-42a7-b6f3-64a63a2a1cef"
    },
    {
        "id": "466d81e5-3895-4741-b51c-09a0cb4a8d28",
        "postId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "description": "sint tempora quaerat",
        "size": "LARGE",
        "fragile": True,
        "offer": 523.0,
        "createdAt": "2024-02-27T12:34:14.728826",
        "userId": "a016c592-9271-42a7-b6f3-64a63a2a1cef"
    }
]
scores = [
    {
        "id": "ccc4dd20-1434-49ec-a8bd-6f61c87af8c8",
        "offer": 162.0,
        "postId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "size": "LARGE",
        "bagCost": 603.0,
        "profit": -441.0
    },
    {
        "id": "f5ab144e-4239-4af6-b576-5f658bd10f4b",
        "offer": 343.0,
        "postId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "size": "SMALL",
        "bagCost": 603.0,
        "profit": 192.25
    },
    {
        "id": "466d81e5-3895-4741-b51c-09a0cb4a8d28",
        "offer": 523.0,
        "postId": "7d244df0-0370-4a0f-9fee-8cd89b991d41",
        "size": "LARGE",
        "bagCost": 603.0,
        "profit": -80.0
    }
]