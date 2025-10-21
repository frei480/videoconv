import subprocess
from pathlib import Path

from checks import Setup


def main():
    """
    This script extract soundtrack from video files using FFmpeg.
    It finds video files in an 'input' folder, and saves mp3 to an 'output' folder.
    """
    current_path = Path(__file__).parent.resolve()
    setup = Setup(current_path)
    setup.prerun_checks()
    input_folder, output_folder, ffmpeg_path = setup.get_folders()

    # Get a list of files to process
    files_to_process = [f for f in input_folder.glob("*.webm") if f.is_file()]

    if not files_to_process:
        print(f"No files found in the '{input_folder.name}' folder.")
        print("Please add video files to the input folder and run the script again.")
        input("Press Enter to exit...")
        return
    for file_path in files_to_process:
        print("\n" + "-" * 12 + " Starting next file " + "-" * 12)
        print(f"Processing: {file_path.name}")
        # Change extension (container type)
        output_file_path = str(output_folder / file_path.stem) + "_sound.opus"

        args = [
            str(ffmpeg_path),
            "-i",
            str(file_path),
            "-vn",
            "-acodec",
            "copy",
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
