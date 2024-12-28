import pytest
from main import BooksCollector

@pytest.fixture(scope="function")
def collector():
    return BooksCollector()
class TestBooksCollector:
    def test_add_new_book_one_book_added(self, collector):
        collector.add_new_book("Что делать, если ваш кот хочет вас убить")
        assert "Что делать, если ваш кот хочет вас убить" in collector.get_books_genre()

    def test_add_new_book_add_existing_book_not_added(self, collector):
        collector.add_new_book("Что делать, если ваш кот хочет вас убить")
        collector.add_new_book("Что делать, если ваш кот хочет вас убить")
        assert len(collector.get_books_genre()) == 1

    @pytest.mark.parametrize("name, genre", [
        ("Что делать, если ваш кот хочет вас убить", "Ужасы"),
        ("Автостопом по галактике", "Фантастика")
    ])
    def test_set_book_genre_listed_genre_updated(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    def test_set_book_genre_unlisted_genre_not_updated(self, collector):
        collector.add_new_book("Малыш и Карлсон")
        collector.set_book_genre("Малыш и Карлсон", "Детская литература")
        assert collector.get_book_genre("Малыш и Карлсон") == ""

    def test_get_book_genre_existing_book_with_genre_returned(self, collector):
        collector.add_new_book("Автостопом по галактике")
        collector.set_book_genre("Автостопом по галактике", "Фантастика")
        assert collector.get_book_genre("Автостопом по галактике") == "Фантастика"

    @pytest.mark.parametrize("name, genre, expected", [
        ("Что делать, если ваш кот хочет вас убить", "Ужасы", ["Что делать, если ваш кот хочет вас убить"]),
        ("Автостопом по галактике", "Фантастика", ["Автостопом по галактике"]),
        ("Шерлок Холмс", "Детективы", []),
    ])
    def test_get_books_with_specific_genre_list_returned(self, collector, name, genre, expected):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_books_with_specific_genre(genre) == expected

    def test_get_books_genre_one_book_dict_state(self, collector):
        collector.add_new_book("Автостопом по галактике")
        collector.set_book_genre("Автостопом по галактике", "Фантастика")
        assert collector.get_books_genre() == {"Автостопом по галактике": "Фантастика"}

    @pytest.mark.parametrize("name, genre, books_for_children", [
        ("Автостопом по галактике", "Фантастика", ["Автостопом по галактике"]),
        ("Что делать, если ваш кот хочет вас убить", "Ужасы", []),
        ("Незнайка на луне", "Мультфильмы", ["Мультфильмы"]),
        ("Шерлок Холмс", "Детективы", []),
    ])
    def test_get_books_for_children_restricted_books_not_added(self, collector, name, genre, books_for_children):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_books_for_children() == books_for_children

    def test_add_book_in_favorites_book_in_dict_added(self, collector):
        collector.add_new_book("Автостопом по галактике")
        collector.set_book_genre("Автостопом по галактике", "Фантастика")
        collector.add_book_in_favorites("Автостопом по галактике")
        assert "Автостопом по галактике" in collector.get_list_of_favorites_books()


    def test_delete_book_from_favorites_book_in_list_deleted(self, collector):
        collector.add_new_book("Автостопом по галактике")
        collector.set_book_genre("Автостопом по галактике", "Фантастика")
        collector.add_book_in_favorites("Автостопом по галактике")
        collector.delete_book_from_favorites("Автостопом по галактике")
        assert "Автостопом по галактике" not in collector.get_list_of_favorites_books()

    @pytest.mark.parametrize("name, genre, favorites", [
        ("Автостопом по галактике", "Фантастика", ["Автостопом по галактике"]),
        ("Что делать, если ваш кот хочет вас убить", "Ужасы", ["Что делать, если ваш кот хочет вас убить"]),
        ("Незнайка на луне", "Мультфильмы", ["Незнайка на луне"]),
    ])
    def test_get_list_of_favorites_books_favorites_list_returned(self, collector, name, genre, favorites):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        collector.add_book_in_favorites(name)
        assert collector.get_list_of_favorites_books() == favorites
