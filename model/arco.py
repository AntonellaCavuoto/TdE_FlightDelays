from dataclasses import dataclass

from model.airport import Airport


@dataclass
class Arco:
    aeroportoP: Airport
    aeroportoD: Airport
    peso: int
