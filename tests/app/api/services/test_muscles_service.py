import pytest

from app.api.services import MuscleService


@pytest.mark.asyncio
async def test_create_muscle(muscle_schema):
    muscle_new = await MuscleService.create(muscle_schema)

    assert muscle_new.name == muscle_schema.name
    assert muscle_new.id == 1


@pytest.mark.asyncio
async def test_create_muscle_with_exercises(exercise, muscle_schema):
    muscle_schema.exercises_id = [exercise.id]
    muscle_new = await MuscleService.create(muscle_schema)

    assert muscle_new.name == muscle_schema.name
    assert muscle_new.exercises
    assert len(muscle_new.exercises) == 1
    assert muscle_new.exercises[0].name == exercise.name


@pytest.mark.asyncio
async def test_get_muscle_by_id(muscle):
    muscle_found = await MuscleService.find_by_id(muscle.id)

    assert muscle_found
    assert muscle_found.id == muscle.id
    assert muscle_found.name == muscle.name


@pytest.mark.asyncio
async def test_get_muscle_by_name(muscle):
    muscle_found = await MuscleService.find_by_name(muscle.name)

    assert muscle_found
    assert muscle_found.id == muscle.id
    assert muscle_found.name == muscle.name


@pytest.mark.asyncio
async def test_update(exercise, muscle, muscle_schema):
    muscle_schema.exercises_id = [exercise.id]

    msl_upd = await MuscleService.update(muscle.id, muscle_schema)

    assert msl_upd
    assert msl_upd.name == muscle_schema.name


@pytest.mark.asyncio
async def test_fetch_muscles_empty():
    muscles = await MuscleService.find_all()

    assert len(muscles) == 0


@pytest.mark.asyncio
async def test_fetch_multiple_muscles(muscle_branch):
    muscles = await MuscleService.find_all()

    assert len(muscles) == len(muscle_branch)
    assert muscles[0].name == muscle_branch[0].name
