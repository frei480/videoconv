import subprocess
import sys
from pathlib import Path


def main():
    """
    This script add soundtrack to video files using FFmpeg.
    It finds video files in an 'input' folder, add mp3 file
    while copying the audio stream, and saves them to an 'output' folder.
    """

    current_path = Path(__file__).parent.resolve()

    input_folder = current_path / "input"
    output_folder = current_path / "output"

    # Check OS to determine the correct ffmpeg executable name
    if sys.platform == "win32":
        ffmpeg_executable = "ffmpeg.exe"
    else:  # Linux, macOS, etc.
        ffmpeg_executable = "ffmpeg"

    ffmpeg_path = current_path / "ffmpeg" / ffmpeg_executable

    # --- Pre-run Checks ---

    # 1. Check if the ffmpeg executable exists
    if not ffmpeg_path.is_file():
        print(f"Error: FFmpeg executable not found at '{ffmpeg_path}'")
        print("Please ensure ffmpeg is located in a 'ffmpeg' subfolder.")
        input("Press Enter to exit...")
        sys.exit(1)

    # 2. Create output folder if they don't exist
    if not output_folder.exists():
        print(f"Creating output folder at: {output_folder}")
        output_folder.mkdir()

    # 3. Get a list of files to process
    files_to_process = [f for f in input_folder.glob("*.webm") if f.is_file()]

    if not files_to_process:
        print(f"No files found in the '{input_folder.name}' folder.")
        print("Please add video files to the input folder and run the script again.")
        input("Press Enter to exit...")
        return

    # Iterate over each file in the input folder
    for file_path in files_to_process:
        print("\n" + "-" * 12 + " Starting next file " + "-" * 12)
        print(f"Processing: {file_path.name}")
        # Change extension (container type)
        output_file_path = str(output_folder / file_path.stem) + ".mp4"
        add_soundtrack = str(input_folder / file_path.stem) + ".mp3"
        args = [
            str(ffmpeg_path),
            "-i",
            str(file_path),
            "-i",
            add_soundtrack,
            "-c",
            "copy",
            "-map",
            "0:0",
            "-map",
            "0:1",
            "-map",
            "1:0",
            output_file_path,
        ]

        try:
            result = subprocess.run(args, check=True, capture_output=True, text=True)
            print(f"Successfully converted '{file_path.name}'")
            print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"Error converting {file_path.name}:")
            print(e.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    print("\n" + "=" * 40)
    print("All files have been processed.")

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
