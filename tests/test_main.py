import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_status(client: AsyncClient) -> None:
    response = await client.get("/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_get_all_tasks(client: AsyncClient) -> None:
    response = await client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) > 0
    assert all("task_id" in t and "title" in t and "status" in t for t in tasks)


@pytest.mark.asyncio
async def test_get_productivity_report(client: AsyncClient) -> None:
    response = await client.get("/report")
    assert response.status_code == 200
    report = response.json()
    assert "total_tasks" in report
    assert "completed_tasks" in report
    assert "total_hours_spent" in report
    assert "completion_rate" in report
    assert report["completed_tasks"] <= report["total_tasks"]


@pytest.mark.asyncio
async def test_log_task(client: AsyncClient) -> None:
    new_task = {"task_id": 0, "title": "Test task", "status": "pending", "hours_spent": 2.0}
    response = await client.post("/log_task", json=new_task)
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_get_task_status(client: AsyncClient) -> None:
    response = await client.get("/task/1/status")
    assert response.status_code == 200
    assert response.json() == {"task_id": 1, "status": "complete"}


@pytest.mark.asyncio
async def test_get_task_status_not_found(client: AsyncClient) -> None:
    response = await client.get("/task/999/status")
    assert response.status_code == 404
