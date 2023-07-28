import googletrans
import argparse

def show_progress_bar(progress, total, bar_length=50):
    percent = progress / total
    filled_length = int(percent * bar_length)
    empty_length = bar_length - filled_length
    bar = "[" + "█" * filled_length + " " * empty_length + "]"
    percent_text = f"{percent*100:.1f}%" if percent < 1 else "Done!"
    print(f"\r{bar} {percent_text}", end="", flush=True)

def translate_srt_file(dest_language, srt_file):
    available_languages = googletrans.LANGUAGES
    if dest_language not in available_languages:
        raise ValueError(f"Language {dest_language} not available. Please check the list of available languages in https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages")
    
    if not srt_file.endswith(".srt"):
        raise ValueError(f"File {srt_file} is not a .srt file")
    
    output_file = srt_file.replace(".srt", f"_{dest_language}.srt")
    translator = googletrans.Translator()
    
    print(f"Reading {srt_file}...")
    with open(srt_file, 'r', encoding='utf-8') as file:
        text = file.read()
    
    print(f"Translating to {dest_language}...")
    lines = text.split("\n")
    total_lines = len(lines)
    chunk_size = 500
    translated_lines = []
    
    for i in range(0, total_lines, chunk_size):
        chunk = lines[i:i + chunk_size]
        translated_chunk = translator.translate("\n".join(chunk), dest=dest_language)
        translated_chunk = translated_chunk.text.split("\n")
        translated_lines.extend(translated_chunk)
        show_progress_bar(i, total_lines)
    
    show_progress_bar(total_lines, total_lines)
    
    print(f"\nWriting {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("\n".join(translated_lines))
    
    print("Success!")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--dest", required=True, help="Destination language")
    ap.add_argument("-f", "--file", required=True, help=".srt file to translate")
    args = ap.parse_args()

    translate_srt_file(args.dest, args.file)
