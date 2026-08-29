import sys
from pathlib import Path

from .constants import EXERCISE_DETAILS_API, LANGMAP, PROGRESS_API, VIDEO_DETAILS_API
from .helper import (
    Logger,
    correct_path,
    download_file,
    print_progress,
    save_text,
)
from .templates.course import Chapter
from .templates.exercise import Exercise
from .templates.video import Video


class CourseDownloader:
    """Download one Course through a session-like object."""

    def __init__(self, session) -> None:
        self.session = session
        self.overwrite = False

    def download(self, course, path: Path, index="", **kwargs):
        self.overwrite = bool(kwargs.get("overwrite"))
        download_path = path / (
            index + correct_path(course.slug or course.title.lower().replace(" ", "-"))
        )
        if kwargs.get("datasets") and course.datasets:
            for i, dataset in enumerate(course.datasets, 1):
                print_progress(i, len(course.datasets), "datasets")
                if dataset.asset_url:
                    download_file(
                        dataset.asset_url,
                        download_path
                        / "datasets"
                        / correct_path(dataset.asset_url.split("/")[-1]),
                        False,
                        overwrite=self.overwrite,
                    )
            sys.stdout.write("\n")
        for chapter in course.chapters:
            cpath = download_path / self._get_chapter_name(chapter)
            if kwargs.get("slides") and chapter.slides_link:
                download_file(
                    chapter.slides_link,
                    cpath / correct_path(chapter.slides_link.split("/")[-1]),
                    overwrite=self.overwrite,
                )
            if (
                kwargs.get("exercises")
                or kwargs.get("videos")
                or kwargs.get("audios")
                or kwargs.get("scripts")
            ):
                self._download_others(course.id, chapter, cpath, **kwargs)

    def _download_others(self, course_id, chapter: Chapter, path: Path, **kwargs):
        exercises = kwargs.get("exercises")
        videos = kwargs.get("videos")
        audios = kwargs.get("audios")
        scripts = kwargs.get("scripts")
        subtitles = kwargs.get("subtitles")
        last_attempt = kwargs.get("last_attempt")
        ids = self._get_exercises_ids(course_id, chapter.id)
        last_attempts = self._get_exercises_last_attempt(course_id, chapter.id)
        exercise_counter = 1
        video_counter = 1
        for i, exercise_id in enumerate(ids, 1):
            print_progress(i, len(ids), f"chapter {chapter.number}")
            exercise = self._get_exercise(exercise_id)
            if not exercise:
                continue
            exercise.last_attempt = last_attempts.get(exercise_id)
            if exercises and not exercise.is_video:
                self._download_normal_exercise(
                    exercise,
                    path / "exercises" / f"ex{exercise_counter}.md",
                    bool(last_attempt),
                )
                exercise_counter += 1
            if exercise.is_video:
                video = self._get_video(exercise.data.get("projector_key"))
                if not video:
                    continue
                video_path = path / "videos" / f"ch{chapter.number}_{video_counter}"
                if videos and video.video_mp4_link:
                    download_file(
                        video.video_mp4_link,
                        video_path.with_suffix(".mp4"),
                        overwrite=self.overwrite,
                    )
                if audios and video.audio_link:
                    download_file(
                        video.audio_link,
                        path / "audios" / f"ch{chapter.number}_{video_counter}.mp3",
                        False,
                        overwrite=self.overwrite,
                    )
                if scripts and video.script_link:
                    download_file(
                        video.script_link,
                        path / "scripts" / (video_path.name + "_script.md"),
                        False,
                        overwrite=self.overwrite,
                    )
                if subtitles and video.subtitles:
                    for subtitle_language in subtitles:
                        subtitle = self._get_subtitle(subtitle_language, video)
                        if subtitle:
                            download_file(
                                subtitle.link,
                                video_path.parent
                                / (video_path.name + f"_{subtitle_language}.vtt"),
                                False,
                                overwrite=self.overwrite,
                            )
                video_counter += 1
            print_progress(i, len(ids), f"chapter {chapter.number}")
        sys.stdout.write("\n")

    def _download_normal_exercise(
        self, exercise: Exercise, path: Path, include_last_attempt: bool = False
    ):
        save_text(path, str(exercise), self.overwrite)
        if include_last_attempt and exercise.is_python and exercise.last_attempt:
            save_text(
                path.parent / (path.name[:-3] + ".py"),
                exercise.last_attempt,
                self.overwrite,
            )
        if exercise.data.subexercises:
            for i, subexercise in enumerate(exercise.data.subexercises, 1):
                sub = self._get_exercise(subexercise)
                if sub:
                    self._download_normal_exercise(
                        sub, path.parent / (path.name[:-3] + f"_sub{i}.md")
                    )

    def _get_exercises_last_attempt(self, course_id, chapter_id):
        try:
            data = self.session.get_json(
                PROGRESS_API.format(course_id=course_id, chapter_id=chapter_id)
            )
            if "error" in data:
                raise ValueError(
                    f"Cannot get exercises for course {course_id}, chapter {chapter_id}."
                )
            return {e["exercise_id"]: e.get("last_attempt") for e in data}
        except Exception as error:
            Logger.error(error)
            return {}

    def _get_exercises_ids(self, course_id, chapter_id):
        try:
            data = self.session.get_json(
                PROGRESS_API.format(course_id=course_id, chapter_id=chapter_id)
            )
            if "error" in data:
                raise ValueError(
                    f"Cannot get exercises for course {course_id}, chapter {chapter_id}."
                )
            return [exercise["exercise_id"] for exercise in data]
        except Exception as error:
            Logger.error(error)
            return []

    def _get_exercise(self, exercise_id):
        try:
            if not exercise_id:
                raise ValueError("ID tag not found.")
            data = self.session.get_json(EXERCISE_DETAILS_API.format(id=exercise_id))
            if "error" in data:
                raise ValueError(f"Cannot get exercise with id: {exercise_id}.")
            return Exercise(**data)
        except Exception as error:
            Logger.error(error)
            return None

    def _get_video(self, video_id):
        try:
            if not video_id:
                raise ValueError("ID tag not found.")
            data = self.session.get_json(VIDEO_DETAILS_API.format(hash=video_id))
            if "error" in data:
                raise ValueError()
            return Video(**data)
        except Exception as error:
            Logger.error(error)
            return None

    def _get_subtitle(self, language, video: Video):
        language = LANGMAP.get(language)
        if not language:
            return
        for subtitle in video.subtitles:
            if subtitle.language == language:
                return subtitle

    def _get_chapter_name(self, chapter: Chapter):
        if chapter.title and chapter.title_meta:
            return correct_path(chapter.slug)
        if chapter.title:
            return correct_path(
                f"chapter-{chapter.number}-{chapter.title.replace(' ', '-').lower()}"
            )
        return f"chapter-{chapter.number}"
