# Xavier Linn
# MSE 215, Project 3
# A Monte Carlo Problem
# Metropolis algorithm to compute the properties of a 2D Ising models.

# Import statements
import numpy as np # Library for providing array and functions to calculate values
import matplotlib.pyplot as plt # Library for plotting

# TwoDArray is a class that provides a 2D lattice for the Monte Carlo simulation,
# with features for changing the state at a given site, and indexing functions for
# implementing periodic boundary conditions.
class TwoDArray:

    # Instantiate a 2D array
    def __init__(self, size):
        self.size = size # 2D array is a square with length size. 0, 1, ... size - 1
        self.alloy = np.arange(size * size).reshape(size, size) # Generate a 2D Array
        self.populateTwoDArray() # Populate the array randomly with -1's and 1's

    # Populate alloy randomly with 1's an -1's
    def populateTwoDArray(self):
        # Iterate through all the 2D array and put a -1 or 1 based on random number
        # Generate a random number between 1 and 10, if <= 5 populate with -1
        for i in range(0, self.size):
            for j in range(0, self.size):
                spin = 1
                randomValue = np.random.randint(1,11)
                if (randomValue <= 5):
                    spin = -1
                self.alloy[i][j] = spin

    # Prints the 2D array
    # used primarily for testing and debugging
    def printArray(self):
        print("Printing the 2D array")
        print(self.alloy)


    # Retrieve the state at index i
    # implements periodic boundary conditions
    def stateAtIndexI(self, i, j):
        if (i == -1):
            return self.alloy[self.size - 1][j]
        elif (i == self.size):
            return self.alloy[0][j]
        else:
            return self.alloy[i][j]

    # Retrieve the state at index j
    # implements periodic boundary conditions
    def stateAtIndexJ(self, i, j):
        if (j == -1):
            return self.alloy[i][self.size - 1]
        elif (j == self.size):
            return self.alloy[i][0]
        else:
            return self.alloy[i][j]

    # Change state at index i, j
    # changes state from 1 to -1 and vice-versa
    def changeState(self, site):
        i = site[0]
        j = site[1]
        currentState = self.alloy[i][j]
        if currentState == 1:
            self.alloy[i][j] = -1
        else:
            self.alloy[i][j] = 1

# Class for running the MonteCaro Simulation, with features for
# calculating experimental and exact values. A Monte Carlo time
# step is defined to be L^2 spin flip attempts. For this simulation
# J = 1, and H = 0.
class MonteCarlo:

    # Instantiate a  Monte Carlo Simulation
    def __init__(self, s, temp):
        self.twoDArray = TwoDArray(s)
        self.totalEnergy = 0
        self.size = s
        self.time = 0
        self.temperature = temp
        self.avgMagArray = np.array
        self.magneticMomentArray = np.array
        self.energyArray = np.array
        self.heatCapacityPerSite = np.array
        self.exactMagArray = np.array
        self.exactHeatCapacity = np.array
        self.exactTemps = np.array
        self.steps = 0
        self.ntrials = 0
        self.correlationTime = 0
        self.correlationFxn = np.array
        self.calculateInitialTotalEnergy() # Calculates the total energy before any spin flip attempts

    # Plot total energy vs time
    # used primarily for testing and debugging
    def totalEnergyVsTime(self):
        plt.plot(self.energyArray)
        plt.title("ENERGY VS TIME")
        plt.show()

    # Plot avg mag vs time
    # used primarily for testing and debugging
    def magVsTime(self):
        plt.plot(self.avgMagArray)
        plt.title("MAG VS TIME")
        plt.show()

    # Calculate the initial total energy, before any spins have been flipped
    def calculateInitialTotalEnergy(self):
        for i in range(0, self.size):
            for j in range(0, self.size):
                self.totalEnergy += self.twoDArray.alloy[i][j]*(self.twoDArray.stateAtIndexI(i + 1, j) + self.twoDArray.stateAtIndexJ(i, j + 1))
        self.totalEnergy *= (-1)

    # Returns a random site as a tuple (i, j)
    def generateRandomSite(self):
        i = np.random.randint(0, self.size)
        j = np.random.randint(0, self.size)
        return (i, j)

    # Calculates the energy contribution at a given site, by
    # summing up the iteractions of a site and it's four neighbors
    def energyContributionAtSite(self, site):
        i = site[0]
        j = site[1]
        energyContribution = (-1) * self.twoDArray.alloy[i][j] * (self.twoDArray.stateAtIndexI(i + 1, j) + self.twoDArray.stateAtIndexJ(i, j + 1) + self.twoDArray.stateAtIndexI(i - 1, j) + self.twoDArray.stateAtIndexJ(i, j - 1))
        return energyContribution

    # Calculates and returns the energy after a Monte Carlo time step
    def calculateTotalEnergyAfterSpinFlip(self, site):
        initialEnergy = self.totalEnergy
        energyContributionAtSiteBeforeFlip = self.energyContributionAtSite(site)
        self.twoDArray.changeState(site)
        energyContributionAtSiteAfterFlip = self.energyContributionAtSite(site)
        finalEnergy = initialEnergy - energyContributionAtSiteBeforeFlip + energyContributionAtSiteAfterFlip
        return finalEnergy

    # Decides whether to accept a spin flip or not, by calculating
    # the boltzman factor and comparing it to a random number between 0 and 1.
    # Returns true for flipping the spin and false to not flip the spin
    def acceptFlipOrNot(self, newEnergy):
        energyChange = newEnergy - self.totalEnergy
        if (energyChange <= 0):
            return True
        else:
            boltzman = np.exp(-1 * (1.0 / self.temperature) * energyChange)
            eta = np.random.random_sample()
            if (eta < boltzman): # If eta < boltzman factor, ACCEPT
                return True
            else: # If eta >= boltzman factor, REJECT
                return False

    # Calculates and returns the average magnetization per site using
    def calculateAvgMagnetization(self):
        #avg = abs((np.sum(self.twoDArray.alloy, None, float) + 0.0) / np.power(self.size, 2))
        avg = abs(np.average(self.avgMagArray))
        return avg

    # Calculates the returns the magnetic moment
    def calculateMagneticMoment(self):
        return np.sum(self.twoDArray.alloy, None, float)

    # Metropolis Alogrithm for the 2D Ising Model
    def metropolisAlgorithm(self, steps):
        # Set or reset the time to zero
        self.time = 0
        # Setup data structures for collecting experimental data
        numSpin = self.size * self.size # By convention one "time" step is L^2 spin flip attempts
        initialNumDataPoints = int(steps / numSpin)
        self.avgMagArray = np.zeros(initialNumDataPoints, dtype=np.float)
        self.magneticMomentArray = np.zeros(initialNumDataPoints, dtype=np.float)
        self.energyArray = np.zeros(initialNumDataPoints, dtype=np.float)
        self.heatCapacityPerSite = np.zeros(initialNumDataPoints, dtype=np.float)
        # Take the system to equilibrium and record data every L^2 spin flip attempts
        for i in range(0, steps):
            site = self.generateRandomSite() # Select a random site
            totalEnergyAfterSpinFlip = self.calculateTotalEnergyAfterSpinFlip(site) # Calculate the energy after a random spin is flipped
            # Accept or reject the spin flip
            flip = self.acceptFlipOrNot(totalEnergyAfterSpinFlip)
            if (flip):
                self.totalEnergy = totalEnergyAfterSpinFlip
            else:
                self.twoDArray.changeState(site)
            # Store energy and magnetization while system reaches equilibrium
            if (i % numSpin == 0): # Record data every L^2 spin flip attempts
                if (i / numSpin == initialNumDataPoints):
                    break
                #self.avgMagArray[self.time] = self.calculateAvgMagnetization()
                #self.magneticMomentArray[self.time] = self.calculateMagneticMoment()
                self.avgMagArray[self.time] = np.absolute((float(self.totalEnergy)) / (self.size * self.size))/2
                self.magneticMomentArray[self.time] = self.totalEnergy
                self.energyArray[self.time] = self.totalEnergy
                self.heatCapacityPerSite[self.time] = self.calculateHeatCapcaityPerSite()
                self.time += 1

        # Determine the correlation time.
        self.correlationFxn = self.estimated_autocorrelation(self.avgMagArray)
        self.correlationTime = self.integrateCorrelation(self.correlationFxn)
        # Remove non-equilibrium data using correlation time.
        scaledCorrelationTime = int(1 * self.correlationTime)
        self.avgMagArray = self.avgMagArray[scaledCorrelationTime:]
        self.energyArray = self.energyArray[scaledCorrelationTime:]
        self.magneticMomentArray = self.magneticMomentArray[scaledCorrelationTime:]
        self.heatCapacityPerSite = self.heatCapacityPerSite[scaledCorrelationTime:]

    # Calculate the correlation data, returns a correlation function
    def estimated_autocorrelation(self, x):
        n = len(x)
        variance = x.var()
        x = x-x.mean()
        r = np.correlate(x, x, mode = 'full')[-n:]
        result = r/(variance*(np.arange(n, 0, -1)))
        return result

    # Approximate and returns the index where the correlation function crosses the x-axis
    def findZeroIndex(self, x):
        i = 0
        j = 1
        for v in x: # Finds the two points where the value changes from (+) to (-)
            if x[i] > 0 and x[j] < 0:
                return j
            i += 1
            j += 1

    # Calculates and returns the correlation time using the trapezoid method integrate
    # the correlation function from 0 to where to first intersects the x-axis
    def integrateCorrelation(self, correlationFxn):
        index = self.findZeroIndex(correlationFxn)
        correlationFxn = correlationFxn[:index + 1]
        correlationTime = np.trapz(correlationFxn)
        return correlationTime

    # Calculates the number of independent trials using the correlation time
    def calculateNumberOfIndpTrials(self):
        #print(self.avgMagArray.size)
        self.ntrials = int(self.avgMagArray.size / (2 * self.correlationTime))

    # Calculates the and returns the uncertainty using Bootstrapping method
    def bootStrappingMethod(self, data):
        self.calculateNumberOfIndpTrials()
        p = np.arange(self.ntrials, dtype='f')
        avgSampleArray = np.arange(1000, dtype='f')
        for i in range(0, 1000):
            for j in range(0, int(self.ntrials)):
                index = np.random.randint(1, data.size)
                p[j] = data[index]
            avgSample = p.mean()
            avgSampleArray[i] = avgSample
        avp = np.sqrt(np.var(avgSampleArray))
        return avp

    # Calculates the the variance
    def calculateHeatCapcaityPerSite(self):
        # Cv = (1 / (Kb * T^2 * L^2)) * (<E^2> - <E>^2)
        var = np.var(self.energyArray)
        Cv = (1.0 / (np.power(self.size, 2) * np.power(self.temperature, 2))) * var
        return Cv

    # Caclulates the magnetic susceptibility per site
    def calculateMagneticSusceptibilityPerSite(self):
        # x = beta * (1 / L^2) (<m^2> - <m>^2), beta = 1 / T
        var = np.var(self.magneticMomentArray)
        #var = np.var(self.avgMagArray)
        x = (1.0 / self.temperature) * (1.0 / np.power(self.size, 2 )) * var
        return x

    # Calculates the exact solution for the magnetic susceptibility
    def calculateExactAvgMagneticPerSite(self, temp):
        avg_x = np.power((1 - np.power(np.sinh(2 * (1.0 / temp) * 1), -4)), 1.0/8.0)
        return avg_x

    # Calculates the critical temperature
    def calcuateExactCriticalTemperature(self):
        return (2.0 / np.log(1.0 + np.sqrt(2)))

    # Calculates the exact heat capacity per spin
    def calculateExactHeatCapacity(self, temp):
        Tc = self.calcuateExactCriticalTemperature()
        val = (2.0 / np.pi) * np.power((2.0 / Tc), 2) * (-1 * np.log(1 - (temp + 0.0) / Tc) + np.log(Tc / 2.0) - (1 + (np.pi + 0.0)/ 4.0))
        return val

    # Calcuates the exact values for mag. sus., heat cap., avg mag. over a range of temperatures
    def calculateExactValues(self):
        # Create an array of temperatures, with very small steps near Tc
        criticalTemp = self.calcuateExactCriticalTemperature()
        dT = 0.00001
        numTemps = int(criticalTemp / dT)
        self.exactTemps = np.zeros(numTemps)
        self.exactTemps[0] = 1.0
        for i in range(1, numTemps):
            self.exactTemps[i] = self.exactTemps[i - 1] + dT
        # Create an arary's for the exact data
        self.exactMagArray = np.zeros(numTemps)
        self.exactHeatCapacity = np.zeros(numTemps)
        for i in range(0, numTemps):
            self.exactMagArray[i] = self.calculateExactAvgMagneticPerSite(self.exactTemps[i])
            self.exactHeatCapacity[i] = self.calculateExactHeatCapacity(self.exactTemps[i])

# Function for running the simulation over a range of system sizes each over
# a range of temperatures. Plot's data to file.
def simulation():
    # Create an array of temperatures
    # Choose a step size for the temperature, dT = 0.1
    numTemps = int(3 / 0.1)
    temps = np.zeros(numTemps)
    temps[0] = 1.0
    numTemps = len(temps)
    dT = 0.1
    for i in range(1, numTemps):
        temps[i] = temps[i - 1] + dT
    # Create array's for the experimental data
    avgMagArray = np.zeros(numTemps)
    magneticSusceptibilityArray = np.zeros(numTemps)
    heatCapacityArray = np.zeros(numTemps)
    # Create array's for the uncertainties
    uncertMagArrray = np.zeros(numTemps)
    uncertMagSusArray = np.zeros(numTemps)
    uncertHeatCapArray = np.zeros(numTemps)
    # For a series of system sizes and temperatures run the simulation
    sizes = [4, 8]
    for L in sizes:
        # Create a new Monte Carlo
        temp = MonteCarlo(L, 1.0)
        for i in range(0, numTemps):
            temp.temperature = temps[i]
            temp.metropolisAlgorithm(500000)
            # Calcultate experimental data for given temperature
            avgMagArray[i] = temp.calculateAvgMagnetization()
            magneticSusceptibilityArray[i] = temp.calculateMagneticSusceptibilityPerSite()
            heatCapacityArray[i] = temp.calculateHeatCapcaityPerSite()
            # Caclulate uncertainties for experimental values
            uncertMagArrray[i] = temp.bootStrappingMethod(temp.avgMagArray)
            uncertMagSusArray[i] = temp.bootStrappingMethod(magneticSusceptibilityArray)
            uncertHeatCapArray[i] = temp.bootStrappingMethod(temp.heatCapacityPerSite)
        # Calculate the exact values
        temp.calculateExactValues()
        # Plot data to files as pdf's
        plt.errorbar(temps, avgMagArray, uncertMagArrray)
        plt.plot(temp.exactTemps, temp.exactMagArray)
        plt.title("Average Magnetization Per Site vs. Temperature")
        plt.xlabel("T")
        plt.ylabel("<|m|>")
        fileName = str(L) + "x" + str(L) + "AvgMag.pdf"
        plt.savefig(fileName)
        plt.close()
        plt.errorbar(temps, magneticSusceptibilityArray, uncertMagSusArray)
        plt.title("Magnetic Susceptibility Per Site vs. Temperature")
        plt.xlabel("T")
        plt.ylabel("x")
        fileName = str(L) + "x" + str(L) + "MagSuscept.pdf"
        plt.savefig(fileName)
        plt.close()
        plt.errorbar(temps, heatCapacityArray, uncertHeatCapArray)
        plt.plot(temp.exactTemps, temp.exactHeatCapacity)
        plt.title("Heat Capacity Per Site vs. Temperature")
        plt.xlabel("T")
        plt.ylabel("Cv")
        fileName = str(L) + "x" + str(L) + "HeatCapacity.pdf"
        plt.savefig(fileName)
        plt.close()


# Run the simulation
simulation()


#print("The correlation time is: ", temp.correlationTime)
#print("avgMagArray: ", avgMagArray)
#print("magneticSusceptibilityArray: ", magneticSusceptibilityArray)
#print("heatCapacityArray: ", heatCapacityArray)
#print("uncertaintyArrary: ", uncertMagArrray)
#print("uncertMagSusArray: ", uncertMagSusArray)
#print("uncertHeatCapArray: ", uncertHeatCapArray)