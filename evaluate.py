import json

from rag import retrieve


def load_test_questions():
    with open("tests/questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

def evaluate():
    tests = load_test_questions()

    correct = 0

    for test in tests:
        question = test["question"]
        expected_source = test["expected_source"]

        results = retrieve(question)

        if results:
            found_source = results[0]["filename"]
        else:
            found_source = None

        is_correct = found_source == expected_source

        if is_correct:
            correct += 1
            symbol = "v"
        else:
            symbol = "x"

        print(
            f"{symbol} {question}\n"
            f"   expected: {expected_source}\n"
            f"   found:    {found_source}"
        )

    total = len(tests)

    print(f"\nScore: {correct}/{total}")

if __name__ == "__main__":
    evaluate()