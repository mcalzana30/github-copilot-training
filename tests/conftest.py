import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app, MOCK_TASKS
from app.models import TaskStatus, DeveloperTask

_INITIAL_TASKS = {
    1: DeveloperTask(task_id=1, title="Refactor legacy service", status=TaskStatus.COMPLETE, hours_spent=8.5),
    2: DeveloperTask(task_id=2, title="Implement new user auth flow", status=TaskStatus.IN_PROGRESS, hours_spent=15.0),
    3: DeveloperTask(task_id=3, title="Write unit tests for checkout", status=TaskStatus.PENDING, hours_spent=0.0),
}


@pytest.fixture(autouse=True)
def reset_mock_tasks() -> None:
    MOCK_TASKS.clear()
    MOCK_TASKS.update(_INITIAL_TASKS)


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
