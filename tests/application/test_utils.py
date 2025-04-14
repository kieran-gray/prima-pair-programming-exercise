from src.application.utils import chunk_list


def test_chunk_list_returns_single_person_id():
    person_ids = ["test"]
    batches = chunk_list(list=person_ids, chunk_size=1)
    for batch in batches:
        assert batch == person_ids


def test_chunk_list_returns_multiple_person_ids():
    person_ids = ["test", "test1", "test2"]
    batches = chunk_list(list=person_ids, chunk_size=1)
    seen_person_ids = []
    for batch in batches:
        assert len(batch) == 1
        assert batch[0] not in seen_person_ids
        seen_person_ids.append(batch[0])


def test_chunk_list_doesnt_key_error_on_large_chunk_size():
    person_ids = ["test", "test1", "test2"]
    batches = chunk_list(list=person_ids, chunk_size=100)
    for batch in batches:
        batch == person_ids