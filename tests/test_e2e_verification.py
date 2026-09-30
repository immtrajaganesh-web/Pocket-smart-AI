import httpx

def test_full_pipeline():
    client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=30.0)

    # 1. Health check
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    print("[OK] Health check passed")

    # 2. Register & Login
    email = "pipeline_test@pocketsmart.ai"
    reg = client.post("/api/auth/register", json={
        "name": "Pipeline Tester",
        "email": email,
        "password": "password123"
    })
    assert reg.status_code in (201, 409)

    login = client.post("/api/auth/login", json={
        "email": email,
        "password": "password123"
    })
    assert login.status_code == 200
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("[OK] Auth & JWT token issuance passed")

    # 3. Session info
    sess = client.get("/api/session-info", headers=headers)
    assert sess.status_code == 200
    assert sess.json()["authenticated"] is True
    print("[OK] Session info passed")

    # 4. Generate Home plan
    home_res = client.post("/api/generate-home", headers=headers, json={
        "budget": 45000,
        "currency": "INR",
        "rooms": ["Living Room", "Dining Area"],
        "items": {"lights": 4, "ceiling_fans": 2, "dining_tables": 1},
        "style": "Scandinavian Modern",
        "priorities": ["Energy Efficient BLDC", "High Durability"]
    })
    assert home_res.status_code == 200
    data = home_res.json()
    assert "allocations" in data
    assert len(data["allocations"]) > 0
    assert len(data["recommendations"]) > 0
    rec_id = data.get("recommendation_id")
    assert rec_id is not None
    print(f"[OK] Home plan generated (id={rec_id}, mode={data.get('source_mode')})")

    # 5. History & Details
    hist = client.get("/api/history", headers=headers)
    assert hist.status_code == 200
    assert len(hist.json()) >= 1
    print(f"[OK] History check passed ({len(hist.json())} plans found)")

    detail = client.get(f"/api/recommendations-details/{rec_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["id"] == rec_id
    print("[OK] Recommendation detail fetch passed")

    # 6. HTML page views
    pages = ["/", "/planner/home", "/planner/party", "/planner/jewelry", "/dashboard", "/login", "/register"]
    for p in pages:
        r = client.get(p)
        assert r.status_code == 200
        assert "PocketSmart" in r.text
    print(f"[OK] All {len(pages)} frontend HTML routes served successfully")

if __name__ == "__main__":
    test_full_pipeline()
    print("\nALL E2E PIPELINE TESTS PASSED SUCCESSFULLY!")
