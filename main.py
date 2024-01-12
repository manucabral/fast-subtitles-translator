import googletrans
import argparse


def show_progress_bar(progress, total, bar_length=50):
    percent = progress / total
    filled_length = int(percent * bar_length)
    empty_length = bar_length - filled_length
    bar = "[" + "█" * filled_length + " " * empty_length + "]"
    percent_text = f"{percent*100:.1f}%" if percent < 1 else "Done!"
    print(f"\r{bar} {percent_text}", end="", flush=True)


def translate_srt_file(source_language, dest_language, srt_file, chunk_size):
    available_languages = googletrans.LANGUAGES
    if dest_language not in available_languages:
        raise ValueError(
            f"Language {dest_language} not available. Please check the list of available languages in https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages"
        )
    if source_language is not None and source_language not in available_languages:
        raise ValueError(
            f"Language {source_language} not available. Please check the list of available languages in https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages"
        )

    if not srt_file.endswith(".srt"):
        raise ValueError(f"File {srt_file} is not a .srt file")

    output_file = srt_file.replace(".srt", f"_{dest_language}.srt")
    translator = googletrans.Translator()

    print(f"Reading {srt_file}...")
    with open(srt_file, "r", encoding="utf-8", errors="ignore") as file:
        text = file.read()

    if source_language is None:
        print("Detecting source language...")
        target_line = None
        for line in text.split("\n"):
            if "-->" in line or line.strip() == "" or line.isnumeric():
                continue
            target_line = line
            break

        detector = translator.detect(line)
        if type(detector.lang) == list:
            print("Found multiple possible source languages and confidence levels:")
            for lang, confidence in zip(detector.lang, detector.confidence):
                print(f"{lang}: {confidence}")
            while True:
                chosen_language = input("Please type the correct language code:")
                if chosen_language in detector.lang:
                    source_language = chosen_language
                    break
                print("Invalid language code. Please try again.")
        else:
            source_language = detector.lang

    print(f"Translating from {source_language} to {dest_language}...")
    lines = text.split("\n")
    total_lines = len(lines)
    translated_lines = []

    for i in range(0, total_lines, chunk_size):
        chunk = lines[i : i + chunk_size]
        translated_chunk = translator.translate(
            "\n".join(chunk), dest=dest_language, src=source_language
        )
        translated_chunk = translated_chunk.text.split("\n")
        translated_lines.extend(translated_chunk)
        show_progress_bar(i, total_lines)

    show_progress_bar(total_lines, total_lines)

    print(f"\nWriting {output_file}...")
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(translated_lines))

    print("Success!")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--src", help="Source language (optional)")
    ap.add_argument("-d", "--dest", required=True, help="Destination language")
    ap.add_argument("-f", "--file", required=True, help=".srt file to translate")
    ap.add_argument("-c", "--chunk", type=int, default=200, help="Chunk size")
    args = ap.parse_args()

    translate_srt_file(args.src, args.dest, args.file, args.chunk)
