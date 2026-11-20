from pathlib import Path
import csv

def split_with_overlap(text, chunk_size, overlap, minimum_length=20):
    if chunk_size <= 0:
        raise ValueError("chunk_size должен быть больше 0")
    if overlap < 0:
        raise ValueError("overlap не может быть отрицательным")
    if overlap >= chunk_size:
        raise ValueError("overlap должен быть меньше chunk_size")

    step = chunk_size - overlap
    chunks = []

    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if chunk and len(chunk) >= minimum_length:
            chunks.append(chunk)
    return chunks

source_dir = Path("normalized")
files = list(source_dir.glob("*.txt"))

chunks_dir = Path("chunks")
chunks_dir.mkdir(exist_ok=True)

all_chunks = []

for file_path in files:
    text = file_path.read_text(encoding="utf-8")
    chunks = split_with_overlap(text, chunk_size=200, overlap=40)

    for chunk_id, chunk in enumerate(chunks):
        all_chunks.append({
            "source": file_path.name,   
            "chunk_id": chunk_id,      
            "length": len(chunk),      
            "text": chunk,
        })
        (chunks_dir / f"{file_path.stem}_chunk_{chunk_id}.txt").write_text(chunk, encoding="utf-8")

with open("chunks_summary.csv", "w", encoding="utf-8", newline="") as f_out:
    writer = csv.writer(f_out)
    writer.writerow(["source", "chunk_id", "length"])
    for c in all_chunks:
        writer.writerow([c["source"], c["chunk_id"], c["length"]])

total_length = sum(c["length"] for c in all_chunks)
print("Документов:", len(files))
print("Всего чанков:", len(all_chunks))
if all_chunks:
    print("Средняя длина чанка:", round(total_length / len(all_chunks), 1))
