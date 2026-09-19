from rag import retrieve, generate_answer


def main():
    question = input("Ask a question: ")

    results = retrieve(question)

    print("\nChunks found:")
    
    for result in results:
        print(
            f"\n--- {result['filename']} "
            f"| chunk {result['chunk_id']} "
            f"| score: {result['score']:.3f} ---"
        )
    
        print(result["text"])


    answer = generate_answer(question, results)

    print("\nAnswer:")
    print(answer)


if __name__ == "__main__":
    main()