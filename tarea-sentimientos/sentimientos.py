import random
from typing import Callable, Dict, List, Tuple, TypeVar

from util import *

FeatureVector = Dict[str, int]
WeightVector = Dict[str, float]
Example = Tuple[FeatureVector, int]


############################################################
# Problem 3: binary classification
############################################################

############################################################
# Problem 3a: feature extraction


def extractWordFeatures(x: str) -> FeatureVector:
    """
    Extrae características de palabras para una cadena x. Las palabras
    son delimitadas por espacios en blanco unicamente.
    @param string x:
    @return dict: representación en vector de características de x.
    Ejemplo: "I am what I am" --> {'I': 2, 'am': 2, 'what': 1}
    """
    # Inicio de tu código
    # Separamos por espacios
    words = x.split()
    # Definimos nuestro vector de caracteristicas como vacio
    feature_vector = {}
    for word in words:
        # Actualiza la letra en el vector de caracteristicas,
        # incrementandolo en 1 si ya existia en el diccionario,
        # o agregándolo con un valor de 1 si es la primera vez que aparece.
        feature_vector[word] = feature_vector.get(word, 0) + 1
    # Devolvemos el vector
    return feature_vector
    # Fin de tu código

############################################################
# Problem 3b: stochastic gradient descent


T = TypeVar("T")

def learnPredictor(
    trainExamples: List[Tuple[T, int]],
    validationExamples: List[Tuple[T, int]],
    featureExtractor: Callable[[T], FeatureVector],
    numEpochs: int,
    eta: float,
) -> WeightVector:
    """
    A partir de |trainExamples| y |validationExamples| (cada uno siendo una lista
    de parejas (x,y)), un |featureExtractor| para aplicar a x, y el número de
    épocas para entrenar |numEpochs|, el tamaño de paso |eta|, regresa el vector
    de pesos (vector de características disperas) aprendido.
    Debes implementar descenso de gradiente estocástico.
    Notas:
    - ¡Solo usa trainExamples para entrenar!
    - Debes llamar evaluatePredictor() sobre trainExamples y validationExamples para
    ver cómo te está llendo conforme aprendes después de cada época.
    - El predictor debe tener como salida +1 si el puntaje es precisamente 0.
    """
    weights = {}  # característica => peso
    # Inicio de tu código
    for epoch in range(numEpochs):
        for example, label in trainExamples:
            # vector de caracteristicas donde cada clave es una caracteristica
            # y cada valor es el peso asociado.
            features = featureExtractor(example)

            # activacion = w · phi(x)
            activation = dotProduct(weights, features)

            # Cuando el ejemplo de entrenamiento se clasifica incorrectamente actualiza los pesos.
            # Si la activación multiplicada por la etiqueta es mayor que cero, significa que el ejemplo se clasificó correctamente.
            if activation * label <= 0:
                increment(weights, eta * label, features)

        # Después de cada época de entrenamiento, se evalúa el desempeño,
        # sobre los datos de entrenamiento y validación.

        # En el primer parámetro pasamos los datos.
        # En el segundo parámetro si la función de articulación en la activación
        # (w · phi(x)) es mayor igual 0, significa que estamos clasificando
        # correctamente nuestra predicción por lo tanto devolvemos 1, de lo
        # contrario devolveremos -1.
        trainError = evaluatePredictor(trainExamples, lambda x: (
            1 if dotProduct(weights, featureExtractor(x)) >= 0 else -1))
        validationError = evaluatePredictor(validationExamples, lambda x: (
            1 if dotProduct(weights, featureExtractor(x)) >= 0 else -1))
    print(
        f"Epoch {epoch}: train error = {trainError:.10f}, validation error = {validationError:.10f}")
    # Fin de tu código
    return weights

############################################################
# Problem 3c: generate test case


def generateDataset(numExamples: int, weights: WeightVector) -> List[Example]:
    """
    Regresa un conjunto de ejemplos (phi(x), y) aleatoriamente que sean clasificados
    correctamente por |weights|.
    """
    random.seed(42)
    # Regresa un solo ejemplo (phi(x), y).
    # phi(x) debe ser un diccionario cuyas llaves sean un subconjunto de las
    # llaves en weights y los valores pueden ser cualquier cosa con un puntaje
    # para el vector de pesos dado.
    # y debe ser 1 o -1 como lo clasifica el vector de pesos.
    # y debe ser 1 si el puntaje es precisamente 0.

    # Nota que el vector de pesos puede ser arbitrario durante las pruebas.
    def generateExample() -> Tuple[Dict[str, int], int]:
        # Inicio de tu código
        phi = {}
        score = 0
        while score == 0:
            # Se selecciona un subconjunto aleatorio de las características en weights
            # y les asigna valores aleatorios.
            phi = {key: random.randint(-10, 10)
                   for key in weights.keys() if random.random() < 0.5}
            # Un margen mayor indica que el modelo de clasificación es más robusto.
            score = sum(weights[key] * phi[key] for key in phi)
        # Clasificación.
        y = 1 if score > 0 else -1
        # Fin de tu código
        return phi, y
    return [generateExample() for _ in range(numExamples)]

############################################################
# Problem 3d: character features


def extractCharacterFeatures(n: int) -> Callable[[str], FeatureVector]:
    """
    Regresa una función que tome una cadena |x| y regrese un vector de
    características disperso que consiste de todos los n-gramas de |x| sin
    espacios asociados a los conteos de n-gramas.
    EXAMPLE: (n = 3) "I like tacos" --> {'Ili': 1, 'lik': 1, 'ike': 1, ...
    Puedes suponer que n >= 1.
    """

    def extract(x: str) -> Dict[str, int]:
        # Inicio de tu código
        features = {}
        # Quitamos todos los espacios
        x = x.replace(" ", "")
        # El ciclo termina cuando ya no se puden crear mas n-gramas.
        # Ej. n = 3, x = "Holamundo" -> i < 7 -> Hol amu ndo
        for i in range(len(x) - n + 1):
            gram = x[i:i+n]
            # Actualiza el n-grama en el vector de caracteristicas,
            # incrementandolo en 1 si ya existia en el diccionario,
            # o agregándolo con un valor de 1 si es la primera vez que aparece.
            features[gram] = features.get(gram, 0) + 1
        return features
        # Fin de tu código
    return extract

############################################################
# Problem 3e:


def testValuesOfN(n: int):
    """
    Usa este código para probar distintos valores de n para extractCharacterFeatures
    Este código es exclusivo para las pruebas.
    Tu solución escrita completa debe estar en el archivo PDF.
    """
    trainExamples = readExamples("polarity.train")
    validationExamples = readExamples("polarity.dev")
    featureExtractor = extractCharacterFeatures(n)
    weights = learnPredictor(
        trainExamples, validationExamples, featureExtractor, numEpochs=20, eta=0.01
    )
    outputWeights(weights[0], "weights")
    outputErrorAnalysis(
        validationExamples, featureExtractor, weights[0], "error-analysis"
    )  # Usa esto para depurar
    trainError = evaluatePredictor(
        trainExamples,
        lambda x: (1 if dotProduct(featureExtractor(x), weights[0]) >= 0 else -1),
    )
    validationError = evaluatePredictor(
        validationExamples,
        lambda x: (1 if dotProduct(featureExtractor(x), weights[0]) >= 0 else -1),
    )
    print(
        (
            "Official: train error = %s, validation error = %s"
            % (trainError, validationError)
        )
    )
    return trainError, validationError


############################################################
# Problem 5: k-means
############################################################


def kmeans(
    examples: List[Dict[str, float]], K: int, maxEpochs: int
) -> Tuple[List, List, float]:
    """
    Realiza agrupamiento con K-medias sobre |examples|, donde cada ejemplo es un vector de
    características disperso.

    examples: lista de ejemplos, cada ejemplo es un diccionario string=>float representando un
              un vector disperso.
    K: número de grupos deseados. Supón que 0 < K <= |examples|.
    maxEpochs: máximo número de epocas para correr (debes terminar temprano solo si el algoritmo converge).
    Return: (lista de longitud K de centroides del agrupamiento,
             lista de asignaciones (es decir, si examples[i] pertenece a centers[j], entonces assignments[i] = j),
             pérdida final)
    """
    # Inicio de tu código
    
    # Inicializar los K centros aleatoriamente
    centers = random.sample(examples, K)
    # Producto punto entre cada ejemplo y cada centro
    products = [[sum([x*y for x, y in zip(example.values(), center.values())]) for center in centers] for example in examples]
    # Inicializar las asignaciones
    assignments = len(examples)
    # Inicializar la pérdida
    loss = float('inf')
    
    # Iterar hasta que se alcance la convergencia o se llegue al máximo número de épocas
    for _ in range(maxEpochs):
        
        # Asignar cada ejemplo al centro más cercano
        for i in examples:
            distances = products[i]
            assignments[i] = min(range(K), key=lambda j: distances[j])
        
        # Recalcular los centros como el promedio de los ejemplos asignados a cada grupo
        new_centers = []
        for j in range(K):
            members = [examples[i] for i in range(len(examples)) if assignments[i] == j]
            if members:
                new_center = Counter()
                for member in members:
                    new_center += member
                new_center = {k: v/len(members) for k, v in new_center.items()}
                new_centers.append(new_center)
            else:
                new_centers.append(centers[j])
        
        # Producto punto entre cada ejemplo y cada nuevo centro
        products = [[sum([x*y for x, y in zip(example.values(), center.values())]) for center in new_centers] for example in examples]
        # Calcular la nueva pérdida como la suma de las distancias al centro de cada ejemplo
        new_loss = sum([products[i][assignments[i]] for i in range(len(examples))])
        
        # Si la pérdida no ha cambiado mucho, terminar
        if abs(new_loss - loss) < 1e-6:
            break
        else:
            loss = new_loss
            centers = new_centers
    
    # Centroides finales, asignaciones y la pérdida final
    return centers, assignments, loss
    # Fin de tu código