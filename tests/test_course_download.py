import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from datacamp_downloader.course_download import CourseDownloader
from datacamp_downloader.datacamp_utils import Datacamp
from datacamp_downloader.templates.course import Course
from datacamp_downloader.templates.exercise import Exercise


class FakeSession:
    def __init__(self, responses=None):
        self.responses = responses or {}
        self.started = False
        self.driver = SimpleNamespace(minimize_window=lambda: None)

    def start(self):
        self.started = True

    def get_json(self, url):
        for key, response in self.responses.items():
            if key in url:
                if isinstance(response, Exception):
                    raise response
                return response
        return {}


class FakeResponse:
    headers = {"content-length": "3"}
    content = b"new"

    def iter_content(self, chunk_size):
        return [self.content]


def course_with_chapter(dataset_url="https://example.test/data.csv"):
    return SimpleNamespace(
        id=42,
        slug="sample-course",
        title="Sample Course",
        datasets=[SimpleNamespace(asset_url=dataset_url)],
        chapters=[
            SimpleNamespace(
                id=7,
                number=1,
                slug="chapter-one",
                title="Chapter One",
                title_meta="Chapter One",
                slides_link="https://example.test/chapter1.pdf",
            )
        ],
    )


class CourseDownloadTests(unittest.TestCase):
    @patch("datacamp_downloader.course_download.print_progress")
    @patch("datacamp_downloader.helper.requests.get", return_value=FakeResponse())
    def test_materials_are_placed_in_course_order(self, _get, _progress):
        with tempfile.TemporaryDirectory() as directory:
            downloader = CourseDownloader(FakeSession())
            downloader.download(
                course_with_chapter(),
                Path(directory),
                datasets=True,
                slides=True,
            )

            self.assertTrue(
                (Path(directory) / "sample-course/datasets/data.csv").is_file()
            )
            self.assertTrue(
                (Path(directory) / "sample-course/chapter-one/chapter1.pdf").is_file()
            )

    @patch("datacamp_downloader.course_download.print_progress")
    @patch("datacamp_downloader.helper.requests.get", return_value=FakeResponse())
    def test_overwrite_controls_existing_materials(self, _get, _progress):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "sample-course/datasets/data.csv"
            target.parent.mkdir(parents=True)
            target.write_bytes(b"old")
            downloader = CourseDownloader(FakeSession())
            downloader.download(
                course_with_chapter(),
                Path(directory),
                datasets=True,
            )
            self.assertEqual(target.read_bytes(), b"old")
            downloader.download(
                course_with_chapter(), Path(directory), datasets=True, overwrite=True
            )

            self.assertEqual(target.read_bytes(), b"new")

    @patch("datacamp_downloader.course_download.print_progress")
    @patch("datacamp_downloader.course_download.save_text")
    def test_failed_exercise_does_not_stop_later_exercises(self, save_text, _progress):
        responses = {"/progress": [{"exercise_id": 1}, {"exercise_id": 2}]}
        downloader = CourseDownloader(FakeSession(responses))
        good_exercise = {
            "id": 2,
            "type": "NormalExercise",
            "data": {"id": 2, "type": "NormalExercise", "language": "python"},
            "version": "1",
        }
        with patch.object(
            downloader,
            "_get_exercise",
            side_effect=[
                None,
                Exercise(**good_exercise),
            ],
        ):
            with tempfile.TemporaryDirectory() as directory:
                downloader.download(
                    course_with_chapter(),
                    Path(directory),
                    exercises=True,
                )

        save_text.assert_called_once()

    def test_datacamp_resolves_cached_course_slug(self):
        session = FakeSession()
        datacamp = Datacamp(session)
        datacamp.loggedin = True
        datacamp.courses = [Course(id=42, title="Sample Course", slug="sample-course")]
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(datacamp.course_downloader, "download") as download:
                datacamp.download(["sample-course"], directory)

        self.assertTrue(session.started)
        download.assert_called_once()


if __name__ == "__main__":
    unittest.main()
