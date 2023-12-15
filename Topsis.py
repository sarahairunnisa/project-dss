from math import sqrt
import re

class Topsis:
    def __init__(self, data, weights, impacts) -> None:
        self.data = data
        self.features = {
            'Processor': 'Processor',
            'Screen': 'Screen',
            'InternalMemory': 'InternalMemory',
            'TotalStorage': 'TotalStorage',
            'Weight': 'Weight',
            'BatteryCells': 'BatteryCells',
        }
        self.weights = weights
        self.impacts = impacts
        self.ideal = {}
        self.negativeIdeal = {}

    def euclideanDistance(self, data) -> float:
        return sqrt(sum([i ** 2 for i in data]))

    def normalize(self) -> None:
        for key, value in self.features.items():
            self.data[value + 'Normalized'] = self.data[key] / self.euclideanDistance(self.data[key])
            self.data[value + 'Normalized'] *= self.weights[list(self.features.keys()).index(key)]

    def idealNegativeSolution(self) -> None:
        for key, value in self.features.items():
            if self.impacts[list(self.features.keys()).index(key)] == 1:
                self.ideal[value] = self.data[value + 'Normalized'].max()
                self.negativeIdeal[value] = self.data[value + 'Normalized'].min()
            elif self.impacts[list(self.features.keys()).index(key)] == 0:
                self.ideal[value] = self.data[value + 'Normalized'].min()
                self.negativeIdeal[value] = self.data[value + 'Normalized'].max()
    
    def separationMeasures(self) -> None:
        for _, value in self.features.items():
            self.data[value + 'SeparationMeasureIdeal'] = pow(self.data[value + 'Normalized'] - self.ideal[value], 2)
            self.data[value + 'SeparationMeasureNegativeIdeal'] = pow(self.data[value + 'Normalized'] - self.negativeIdeal[value], 2)
        
        self.data['SeparationMeasureIdeal'] = self.data[[f'{value}SeparationMeasureIdeal' for value in self.features.values()]].sum(axis=1)
        self.data['SeparationMeasureNegativeIdeal'] = self.data[[f'{value}SeparationMeasureNegativeIdeal' for value in self.features.values()]].sum(axis=1)

        self.data['SeparationMeasureIdeal'] = self.data['SeparationMeasureIdeal'].apply(sqrt)
        self.data['SeparationMeasureNegativeIdeal'] = self.data['SeparationMeasureNegativeIdeal'].apply(sqrt)

    def performanceScore(self) -> None:
        self.data['totalRelativeCloseness'] = self.data['SeparationMeasureNegativeIdeal'] / (self.data['SeparationMeasureIdeal'] + self.data['SeparationMeasureNegativeIdeal'])

    def rank(self) -> None:
        self.data = self.data.sort_values(by=['totalRelativeCloseness'], ascending=False)

    def run(self) -> None:
        self.normalize()
        self.idealNegativeSolution()
        self.separationMeasures()
        self.performanceScore()
        self.rank()

    #def getName(self) -> None:
        #regex = re.compile(r'https://www.laptoparena.net/product/(\w+)')
        #embed = []
        #for i in range(1):
            #embed.append(regex.sub(self.data['Name'].iloc[i], self.data['Name'].iloc[i]))
        #return embed

    def getEmbed(self) -> None:
        regex = re.compile(r'https://www.laptoparena.net/product/(\w+)')
        embed = []
        for i in range(15):
            embed.append(regex.sub(r'https://www.laptoparena.net/images/tmb/\1', self.data['ImageURLs'].iloc[i]))
        return embed
    
    def getPercentage(self) -> None:
        return self.data['totalRelativeCloseness'].iloc[0:15]