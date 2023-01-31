import collections
import copy
import fundamentos

test_cases_3a = [
    {
        "input": "cual es la primera palabra en orden alfabético",
        "output": "alfabético",
    },
    {"input": "gato sol marciano", "output": "gato"},
    {"input": " ".join(str(x) for x in range(100000)), "output": "0"},
]


def test_3a():
    for test_case in test_cases_3a:
        output = fundamentos.find_alphabetically_first_word(test_case["input"])
        assert output == test_case["output"]

test_cases_3b = [{"inputs": ((1, 5), (4, 1)), "output": 5}]


def test_3b():
    for test_case in test_cases_3b:
        output = fundamentos.euclidean_distance(*test_case["inputs"])
        assert output == test_case["output"]

'''
test_cases_3c = [
    {"input": "a a a a a", "output": ["a a a a a"]},
    {"input": "el gato", "output": ["el gato"]},
    {
        "input": "el gato y el ratón",
        "output": [
            "y el gato y el",
            "el gato y el ratón",
            "el gato y el gato",
            "gato y el gato y",
        ],
    },
]


def test_3c():
    for test_case in test_cases_3c:
        output = fundamentos.mutate_sentences(test_case["input"])
        assert sorted(output) == sorted(test_case["output"])
'''

test_cases_3d = [
    {
        "inputs": (
            collections.defaultdict(float, {"a": 5}),
            collections.defaultdict(float, {"b": 2, "a": 3}),
        ),
        "output": 15,
    }
]


def test_3d():
    for test_case in test_cases_3d:
        output = fundamentos.sparse_vector_dot_product(*test_case["inputs"])
        assert output == test_case["output"]


test_cases_3e = [
    {
        "inputs": (
            collections.defaultdict(float, {"a": 5}),
            2,
            collections.defaultdict(float, {"b": 2, "a": 3}),
        ),
        "output": collections.defaultdict(float, {"a": 11, "b": 4}),
    }
]


def test_3e():
    for test_case in test_cases_3e:
        v = copy.deepcopy(test_case["inputs"][0])
        output = fundamentos.increment_sparse_vector(v, *test_case["inputs"][1:])
        assert v == test_case["output"]


test_cases_3f = [
    {
        "input": "el veloz zorro marrón salta sobre el zorro perezoso",
        "output": {"el", "zorro"},
    }
]


def test_3f():
    for test_case in test_cases_3f:
        output = fundamentos.find_nonsingleton_words(test_case["input"])
        assert output == test_case["output"]
