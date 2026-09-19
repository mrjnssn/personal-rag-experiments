from rag import retrieve, generate_answer


def main():
    question = input("Ask a question: ")

    results = retrieve(question)

    answer = generate_answer(question, results)

    print("\nAnswer:")
    print(answer)

    print("\nSources:")
    
    for result in results:
        print(
            f"- {result['filename']} "
            f"(score: {result['score']:.3f})"
        )


if __name__ == "__main__":
    main()