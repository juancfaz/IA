import string
import util
import random
import sentimientos


test_cases_3a = [
    {"input": "a b a", "output": {"a": 2, "b": 1}},
]


def test_3a():
    for test_case in test_cases_3a:
        output = sentimientos.extractWordFeatures(test_case["input"])
        assert output == test_case["output"]


test_cases_3b = [
    {
        "trainExamples": (("hello world", 1), ("goodnight moon", -1)),
        "testExamples": (("hello", 1), ("moon", -1)),
        "numEpochs": 20,
        "eta": 0.01,
        "greaterThanKey": "hello",
        "lessThanKey": "moon",
    },
    {
        "trainExamples": (("hi bye", 1), ("hi hi", -1)),
        "testExamples": (("hi", -1), ("bye", 1)),
        "numEpochs": 20,
        "eta": 0.01,
        "greaterThanKey": "bye",
        "lessThanKey": "hi",
    },
]


def test_3b():
    featureExtractor = sentimientos.extractWordFeatures
    for test_case in test_cases_3b:
        weights = sentimientos.learnPredictor(
            test_case["trainExamples"],
            test_case["testExamples"],
            featureExtractor,
            test_case["numEpochs"],
            test_case["eta"],
        )
        assert weights[test_case["greaterThanKey"]] > 0
        assert weights[test_case["lessThanKey"]] < 0


def test_3b2():
    trainExamples = readExamples("polarity.train")
    validationExamples = readExamples("polarity.dev")
    featureExtractor = sentimientos.extractWordFeatures
    weights = sentimientos.learnPredictor(
        trainExamples, validationExamples, featureExtractor, numEpochs=20, eta=0.01
    )
    outputWeights(weights, "weights")
    outputErrorAnalysis(
        validationExamples, featureExtractor, weights, "error-analysis"
    )  # Para depurar
    trainError = evaluatePredictor(
        trainExamples,
        lambda x: (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1),
    )
    validationError = evaluatePredictor(
        validationExamples,
        lambda x: (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1),
    )
    print(
        (
            "Official: train error = %s, validation error = %s"
            % (trainError, validationError)
        )
    )
    assert trainError < 0.04
    assert validationError < 0.30


def test_3c0():
    weights = {"hello": 1, "world": 1}
    data = sentimientos.generateDataset(5, weights)
    for datapt in data:
        assert (util.dotProduct(datapt[0], weights) >= 0) == (datapt[1] == 1)


def test_3c1():
    weights = {}
    for _ in range(100):
        k = "".join(random.choice(string.ascii_lowercase) for _ in range(5))
        v = random.uniform(-1, 1)
        weights[k] = v
    data = sentimientos.generateDataset(100, weights)
    for phi, y in data:
        assert (util.dotProduct(phi, weights) >= 0) == (y == 1)


def test_3d0():
    fe = sentimientos.extractCharacterFeatures(3)
    sentence = "hello world"
    ans = {
        "hel": 1,
        "ell": 1,
        "llo": 1,
        "low": 1,
        "owo": 1,
        "wor": 1,
        "orl": 1,
        "rld": 1,
    }
    assert ans == fe(sentence)
