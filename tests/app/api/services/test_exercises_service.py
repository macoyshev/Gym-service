import pytest

from app.api.services import ExercisesService


@pytest.mark.asyncio
async def test_create_without_muscles_exercise(exercise_schema):
    exercise_new = await ExercisesService.create(exercise_schema)

    assert exercise_new.name == exercise_schema.name
    assert exercise_new.video_link == exercise_schema.video_link
    assert exercise_new.description == exercise_schema.description


@pytest.mark.asyncio
async def test_create_with_muscles_exercise(muscle, exercise_schema):
    exercise_schema.muscles_id = [muscle.id]
    exercise_new = await ExercisesService.create(exercise_schema)

    assert exercise_new.name == exercise_schema.name
    assert exercise_new.muscles
    assert len(exercise_new.muscles) == 1
    assert exercise_new.muscles[0].name == muscle.name


@pytest.mark.asyncio
async def test_find_exercise_by_id(exercise):
    exercise_found = await ExercisesService.find_by_id(exercise.id)

    assert exercise_found
    assert exercise_found.id == exercise.id
    assert exercise_found.name == exercise.name


@pytest.mark.asyncio
async def test_find_non_existing_exercise_by_id():
    exercise = await ExercisesService.find_by_id(10)

    assert exercise is None


@pytest.mark.asyncio
async def test_fetch_exercise_empty():
    exercises = await ExercisesService.find_all()

    assert len(exercises) == 0


@pytest.mark.asyncio
async def test_fetch_all_exercise(exercise_batch):
    exercises = await ExercisesService.find_all()

    assert len(exercises) == len(exercise_batch)
    assert exercises[0].name == exercise_batch[0].name


@pytest.mark.asyncio
async def test_fetch_limit_offset_exercise(exercise_batch):
    exercises = await ExercisesService.find_all(limit=5, offset=5)

    assert len(exercises) == 5
    assert exercises[0].name == exercise_batch[5].name


@pytest.mark.asyncio
async def test_delete_exercise(exercise):
    await ExercisesService.delete(exercise.id)

    exercise_deleted = await ExercisesService.find_by_id(exercise.id)

    assert exercise_deleted is None


@pytest.mark.asyncio
async def test_update(exercise, muscle, exercise_schema):
    exercise_schema.muscles_id = [muscle.id]
    exr_upd = await ExercisesService.update(exercise.id, exercise_schema)

    assert exr_upd.muscles
    assert len(exr_upd.muscles) == 1
    assert exr_upd.muscles[0].name == muscle.name
    assert exr_upd.muscles[0].id == muscle.id
