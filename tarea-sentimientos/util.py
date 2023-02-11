import random
import sys
from collections import Counter
from typing import Callable, Dict, List, Tuple

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]


def dotProduct(d1: Dict, d2: Dict) -> float:
    """
    @param dict d1: un vector de características representado por una asociación de característica (string) a peso (float).
    @param dict d2: igual que d1.
    @return float: el producto punto entre d1 y d2.
    """
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in list(d2.items()))


def increment(d1: Dict, scale: float, d2: Dict):
    """
    Implementa d1 += scale * d2 para vectores dispersos.
    @param dict d1: el vector de características que es modificado.
    @param float scale: factor de escalamiento.
    @param dict d2: un vector de características.
    """
    for f, v in list(d2.items()):
        d1[f] = d1.get(f, 0) + v * scale


def readExamples(path: str):
    """
    Lee un conjunto de ejemplos de entrenamiento.
    """
    examples = []
    for line in open(path, "rb"):
        line = line.decode("latin-1")
        y, x = line.split(" ", 1)
        examples.append((x.strip(), int(y)))
    print("Read %d examples from %s" % (len(examples), path))
    return examples


def evaluatePredictor(
    examples: Tuple[FeatureVector, int], predictor: Callable
) -> float:
    """
    predictor: una función que toma una x y regresa una predicción y.
    Dada una lista de ejemplos (x, y), hace predicciones basadas en |predict| y regresa la fracción
    de ejemplos mal clasificados.
    """
    error = 0
    for x, y in examples:
        if predictor(x) != y:
            error += 1
    return 1.0 * error / len(examples)


def outputWeights(weights: WeightVector, path: str):
    print("%d weights" % len(weights))
    out = open(path, "w", encoding="utf8")
    for f, v in sorted(list(weights.items()), key=lambda f_v: -f_v[1]):
        print("\t".join([f, str(v)]), file=out)
    out.close()


def verbosePredict(phi: FeatureVector, y: int, weights: WeightVector, out) -> int:
    yy = 1 if dotProduct(phi, weights) >= 0 else -1
    if y:
        print(
            "Truth: %s, Prediction: %s [%s]"
            % (y, yy, "CORRECT" if y == yy else "WRONG"),
            file=out,
        )
    else:
        print("Prediction:", yy, file=out)
    for f, v in sorted(
        list(phi.items()), key=lambda f_v1: -f_v1[1] * weights.get(f_v1[0], 0)
    ):
        w = weights.get(f, 0)
        print("%-30s%s * %s = %s" % (f, v, w, v * w), file=out)
    return yy


def outputErrorAnalysis(
    examples: Tuple[FeatureVector, int],
    featureExtractor: Callable,
    weights: WeightVector,
    path: str,
):
    out = open(path, "w", encoding="utf-8")
    for x, y in examples:
        print("===", x, file=out)
        verbosePredict(featureExtractor(x), y, weights, out)
    out.close()


def interactivePrompt(featureExtractor: Callable, weights: WeightVector):
    while True:
        print("> ", end=" ")
        x = sys.stdin.readline()
        if not x:
            break
        phi = featureExtractor(x)
        verbosePredict(phi, None, weights, sys.stdout)


############################################################


def generateClusteringExamples(
    numExamples: int, numWordsPerTopic: int, numFillerWords: int
) -> List:
    """
    Genera ejemplos artificiales inspirados por sentimientos para agrupamiento.
    Cada reseña tiene un sentimiento oculto (positivo o negativo) y un tema (la trama, la actuación o la música).
    La reseña en sí consiste de 2 palabras de sentimientos, 4 palabras de temas y 1 palabra de relleno, por ejemplo:

        good:1 great:1 plot1:2 plot7:1 plot9:1 plot11:1 filler0:1

    numExamples: Número de ejemplos a generar
    numWordsPerTopic: Número de palabras por tema
    numFillerWords: Número de palabras por relleno
    """
    sentiments = [
        ["bad", "awful", "worst", "terrible"],
        ["good", "great", "fantastic", "excellent"],
    ]
    topics = ["plot", "acting", "music"]

    def generateExample():
        x = Counter()
        # Elige 2 palabras de sentimiento
        sentimentWords = random.choice(sentiments)
        x[random.choice(sentimentWords)] += 1
        x[random.choice(sentimentWords)] += 1
        # Elige 4 palabras de temas
        topic = random.choice(topics)
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        x[topic + str(random.randint(0, numWordsPerTopic - 1))] += 1
        # Elige 1 palabra de relleno
        x["filler" + str(random.randint(0, numFillerWords - 1))] += 1
        return x

    random.seed(42)
    examples = [generateExample() for _ in range(numExamples)]
    return examples


def outputClusters(
    path: str, examples: List[Dict[str, float]], centers: List, assignments: List
):
    """
    Imprime los agrupamientos a la ruta dada.
    """
    print("Outputting clusters to %s" % path)
    out = open(path, "w", encoding="utf8")
    for j in range(len(centers)):
        print("====== Cluster %s" % j, file=out)
        print("--- Centers:", file=out)
        for k, v in sorted(list(centers[j].items()), key=lambda k_v: -k_v[1]):
            if v != 0:
                print("%s\t%s" % (k, v), file=out)
        print("--- Assigned points:", file=out)
        for i, z in enumerate(assignments):
            if z == j:
                print(" ".join(list(examples[i].keys())), file=out)
    out.close()
