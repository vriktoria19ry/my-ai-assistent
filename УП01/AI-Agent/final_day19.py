import json
from sentence_transformers import SentenceTransformer

def main():

    chunks = []
    try:
        with open('chunks.jsonl', 'r', encoding='utf-8') as f:
            for line in f:
                if len(chunks) >= 10:
                    break
                chunks.append(json.loads(line.strip()))
    except FileNotFoundError:
        print("Ошибка: файл chunks.jsonl не найден.")
        return

    print(f"Корпус загружен. Обрабатывается {len(chunks)} чанков.\n")

    model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = model.encode(texts)

    output_data = []
    for i, chunk in enumerate(chunks):
        output_data.append({
            "source": chunk["source"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            
            "embedding": chunk_embeddings[i].tolist() 
        })

    with open('chunks_with_embeddings.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
        
    print("Embeddings сохранены в файл chunks_with_embeddings.json\n")

    for search_round in range(3):
        print("-" * 60)
        print(f"ПОИСК #{search_round + 1} ИЗ 3")
        print("-" * 60)

        query = input("Введите ваш вопрос: ")
        query_embedding = model.encode(query)
        scores = model.similarity(query_embedding, chunk_embeddings)[0].tolist()

        THRESHOLD = 0.55 
        best_score = max(scores)

        if best_score < THRESHOLD:
            print("\nПодходящий фрагмент не найден (score ниже порога).")
            print("-" * 60 + "\n")
            continue 

        results = []
        for i in range(len(chunks)):
            results.append({"index": i, "score": scores[i]})
        
        results = sorted(results, key=lambda item: item["score"], reverse=True)

        print("\n--- ТОП-3 РЕЗУЛЬТАТА ---")
        for rank in range(3):
            idx = results[rank]["index"]
            score = results[rank]["score"]
            chunk = chunks[idx]
            
            print(f"\n{rank + 1}. Score: {score:.4f}")
            print(f"   Источник: {chunk['source']}")
            print(f"   ID чанка: {chunk['chunk_id']}")
            print(f"   Текст: {chunk['text']}")

        print("-" * 60 + "\n")

if __name__ == "__main__":
    main()