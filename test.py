import re
from pathlib import Path
from TTS.api import TTS

# Initialize the TTS model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.to("cpu")  # Explicitly set to CPU

# Define paths
base_dir = Path(r"c:\Macbook\Others\voicee\XTTS-v2")
input_file = base_dir / "script.txt"
output_dir = base_dir / "split_outputs"
output_dir.mkdir(exist_ok=True)

# Define speaker WAV files
speaker_wavs = [
    base_dir / "boy_1.wav",
    base_dir / "boy_2.wav",
    base_dir / "boy_3.wav",
    base_dir / "boy_4.wav",
    base_dir / "boy_5.wav",
]

# Read and parse the text file
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Extract paragraphs using regex
paragraphs = re.findall(r"Paragraph\s+(\d+):\s*(.*?)(?=Paragraph\s+\d+:|$)", content, re.DOTALL)
total_paragraphs = len(paragraphs)

# Helper function to split text into chunks
def split_text(text, max_length=400):
    words = text.split()
    chunks, current_chunk = [], []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 <= max_length:
            current_chunk.append(word)
            current_length += len(word) + 1
        else:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# Generate audio for each paragraph
for idx, (para_num, para_text) in enumerate(paragraphs, start=1):
    para_text = para_text.strip().replace('\n', ' ')
    chunks = split_text(para_text)

    for part_idx, chunk in enumerate(chunks, start=1):
        if len(chunks) > 1:
            file_name = f"Paragraph_{para_num} (part {part_idx}).wav"
        else:
            file_name = f"Paragraph_{para_num}.wav"

        output_path = output_dir / file_name
        print(f"Processing paragraph {idx}/{total_paragraphs} (Paragraph {para_num}, Part {part_idx}/{len(chunks)})...")
        
        tts.tts_to_file(
            text=chunk,
            file_path=str(output_path),
            speaker_wav=[str(wav) for wav in speaker_wavs],
            language="en",
            split_sentences=True
        )
        print(f"Generated: {output_path}\n")

print("All paragraphs have been processed.")
