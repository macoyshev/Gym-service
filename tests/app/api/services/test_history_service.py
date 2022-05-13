import pytest

from app.api.services import HistoryService


@pytest.mark.asyncio
async def test_add_train(user, train):
    await HistoryService.add_train(user.id, train.id)
    history = await HistoryService.find_user_history(user.id)

    assert history
    assert history.train_days
    assert len(history.train_days) == 1
    assert history.train_days
    assert history.train_days[0].train_counts
    assert history.train_days[0].train_counts[0].train.name == train.name
