import sys
from pathlib import Path


class Setup:
    def __init__(self, current_path: Path):
        self.input_folder = current_path / "input"
        self.output_folder = current_path / "output"
        self.ffmpeg_path = self._which_ffmpeg(current_path)

    def _which_ffmpeg(self, path: Path) -> Path:
        # Check OS to determine the correct ffmpeg executable name
        ffmpeg_executable = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
        return path / "ffmpeg" / ffmpeg_executable

    def get_folders(self) -> tuple[Path, Path, Path]:
        return self.input_folder, self.output_folder, self.ffmpeg_path

    def prerun_checks(self):
        """Pre-run Checks"""

        if not self.ffmpeg_path.is_file():
            print(f"Error: FFmpeg executable not found at '{self.ffmpeg_path}'")
            print("Please ensure ffmpeg is located in a 'ffmpeg' subfolder.")
            input("Press Enter to exit...")
            sys.exit(1)

        # 2. Create output folder if they don't exist
        if not self.output_folder.exists():
            print(f"Creating output folder at: {self.output_folder}")
            self.output_folder.mkdir()
