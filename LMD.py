# Xavier Linn
# MSE215, Fall 2017
# LAMMPS Molecualr Dynamics
import re
import numpy as np
import matplotlib.pyplot as plt

# PARTI, Question 1
def plotEnergies():
    # Process the LAMMPS std.out file
    stdOutFile = open("stdoutPd.txt", "r") # Open the file
    lines = stdOutFile.readlines() # Put all lines of the file into a list
    lines = lines[8:] # Remove the first 8 lines, they are part of the header
    lines = lines[:-19] # Remove the last 19 lines, not needed

    # Create arrays to hold desired data
    numberDataPoints = len(lines)
    steps = np.arange(numberDataPoints)
    temp = np.arange(numberDataPoints)
    totalEnergy = np.arange(numberDataPoints)
    potentialEnergy = np.arange(numberDataPoints)
    kineticEnergy = np.arange(numberDataPoints)

    # Store the LAMMPS data
    i = 0 # index, used to set data of data array's
    for line in lines:
        # Order of data in file: Step Temp TotalEnergy PotentialEnergy KineticEnergy
        m = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", line) # Python Regex, parse the input file for desired info
        steps[i] = float(m.group(1))
        temp[i] = float(m.group(2))
        totalEnergy[i] = float(m.group(3))
        potentialEnergy[i] = float(m.group(4))
        kineticEnergy[i] = float(m.group(5))
        i += 1

    # Plot total energy vs. steps
    plt.title("Total Energy (eV) vs. Steps")
    plt.xlabel("Steps")
    plt.ylabel("Total Energy")
    plt.grid('on')
    plt.plot(steps, totalEnergy)
    plt.savefig("TEvsStepsQ1.pdf")
    plt.close()
    # Plot potential energy vs. steps
    plt.title("Potential Energy (eV) vs. Steps")
    plt.xlabel("Steps")
    plt.ylabel("Potential Energy")
    plt.grid('on')
    plt.plot(steps, potentialEnergy)
    plt.savefig("PotenVsStepsQ1.pdf")
    plt.close()
    # Plot kinetic energy vs. steps
    plt.title("Kinetic Energy (eV) vs. Steps")
    plt.xlabel("Steps")
    plt.ylabel("Kinetic Energy")
    plt.grid('on')
    plt.plot(steps, kineticEnergy)
    plt.savefig("KineticVsStepQ1.pdf")
    plt.close()

# PARTII
def thermoProperties():

    # Create a dynamic list to hold pressure data
    pressure = None # For questions 2 and 3

    # Read the LAMMPS outfile file and return the Pressure data
    def storeLAMMPSData():
        print("Hello World from storeLAMMPSData")

    # Question 2
    def velocityDistribution():
        # Process the LAMMPS velocities.dump file
        velocitiesFile = open("velocitiesdump2.txt", "r") # Open the file
        lines2 = velocitiesFile.readlines() # Put all lines of the file into a list

        # Create a dynamic list to hold velocity data
        velocities = []

        # Store the LAMMPS data
        for line in lines2:
            # Order of data: id type vx vy vz
            m2 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", line)
            if (m2 is None): # Ignore if pattern doesn't match
                pass # Do nothing
            else: # Pattern matches, store the data
                velocities.append(float(m2.group(3))) # Take only group 3, the vx

        # Randomly select 10,000 data points from the velocity data to generare a distribution
        upperBound = len(velocities) # Upper bound for indexing into the array
        randomVel = np.arange(10000) # Create an array to hold the sample of 1000 velocities
        for i in range(0, 10000): # TODO: Should only be 100 data points, 10,000 looks better though. Need to remove eq. data?
            randomIndex = np.random.randint(0, upperBound)
            randomVel[i] = velocities[randomIndex]

        ## Plot experimental and exact distribution
        plt.hist(randomVel, 15)

        # Calcualte exact distribution
        # Relevant constants
        T = 600 # units of Kelvin
        kB = 8.6173303 * np.power(10.0, -5.0) # units of eV/K
        m = 0.0110284  # units of eVps^2/Angstrom^2
        velocitiesExact = np.arange(-10, 11, dtype=float)
        distn = np.arange(21, dtype=float)
        for vel in velocitiesExact: # vel has units of Angstroms/picosecond
            distn[vel] = 500.0 * np.power((m / (2.0 * np.pi * kB * T)), 1.0/2.0) * (4 * np.pi * np.power(vel, 2.0)) * np.exp((-1.0 * m * np.power(vel, 2.0)) / (2.0 * kB * T))
        plt.title("Maxwell Boltzman Distribution")
        plt.xlabel("Velocity (Angstrom / ps)")
        plt.ylabel("Density")
        plt.plot(velocitiesExact, distn, label='Exact')
        plt.legend()
        plt.savefig("velocityDistributionQ2.pdf")
        plt.grid('on')
        plt.close()

    # Question 3
    def caclulateTimeCorrelationFxn():
        print("Hello World from Correlation caclulateTimeCorrelationFxn")

        # Process the LAMMPS file with pressure
        pressureDataFile = open("stdoutPressurePd.txt", "r") # Open the file
        lines3 = pressureDataFile.readlines() # Put all lines of the file into a list

        # Create a dynamic list to hold pressure data
        pressures = []
        steps = []
        # Store the LAMMPS pressure data into pressures list
        for line in lines3:
            # Order of data: step pressure
            m3 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
            if (m3 is None): # Ignore if pattern doesn't match
                pass # Do nothing
            else: # Pattern matches, store the data
                steps.append(int(m3.group(1)))
                pressures.append(float(m3.group(2))) # Take only group 2, the pressure
        pressures = pressures[1000:] # Remove non-equilibrium data
        steps = steps[1000:]
        plt.title("Maxwell Boltzman Distribution")
        plt.xlabel("Velocity (Angstrom / ps)")
        plt.ylabel("Density")
        plt.plot(pressures)
        plt.grid('on')
        plt.savefig("pressureVsSteps.pdf")
        plt.close()

        # Calculate the correlation function
        averagePressure = np.average(pressures) # Calcualte avergae pressure
        correlationFunction = [] # List to hold correlation values
        for t in range(0, len(pressures)): # For each time dispalcement t..
            terms = []
            for t0 in range(0, len(pressures)): # For each time origin..
                if (t0 + t >= len(pressures)):
                    break;
                terms.append((pressures[t0 + t] - averagePressure) * (pressures[t0] - averagePressure))
            correlationFunction.append(np.average(terms))
        plt.title("Time-Displaced Correlation vs Steps")
        plt.xlabel("Steps")
        plt.ylabel("Correlation")
        plt.plot(correlationFunction)
        plt.grid('on')
        plt.savefig("correlationFunctionPressure.pdf")
        plt.close()

        # Take the semilog of the correlation function
        logCorrelationFunction = np.log(correlationFunction)
        plt.title("Semilog of Time-Displaced Correlation vs Steps")
        plt.xlabel("Steps")
        plt.ylabel("Correlation")
        plt.plot(logCorrelationFunction)
        plt.grid('on')
        plt.savefig("semiLogCorrelationFunctionPressure.pdf")
        plt.close()

        # Caculate the correlation time
        # Splice data to consider a regions that looks linear
        logCorrelationFunction = logCorrelationFunction[:150]
        logCorrelationFunction = logCorrelationFunction[50:]
        steps = steps[:150]
        steps = steps[50:]
        slope = np.polyfit(steps, logCorrelationFunction, 1)[0]
        # print("Slope of the semilog plot: ", slope[0])
        correlationTime = -1.0 / slope
        print("Correlation time: ", correlationTime)


    # Question 4
    def calculateEquilibriumLatticeParameter():
        print("Calculating equilibrium lattice parameter")

        # TODO: Calculate equilibirum pressures @ 600K for a = 3.90, 3.91, 3.92, 3.93, 3.94, 3.95
        avg_pressures = [] # average the pressure over each file
        for i in range(0, 6):
            # Process the LAMMPS files with pressure at each lattice parameter a
            fileName = "data4_9" + str(i) + ".txt"
            pressureDataFile = open(fileName, "r") # Open the file
            lines4 = pressureDataFile.readlines() # Put all lines of the file into a list

            temp = []
            # Store the LAMMPS pressure data into pressures list
            for line in lines4:
                # Order of data: step pressure
                m3 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)", line)
                if (m3 is None): # Ignore if pattern doesn't match
                    pass # Do nothing
                else: # Pattern matches, store the data
                    temp.append(float(m3.group(2))) # Take only group 2, the pressure
            avg_pressures.append(np.average(temp))
        volumes = [np.power(3.90, 3), np.power(3.91, 3), np.power(3.92, 3), np.power(3.93, 3), np.power(3.94, 3), np.power(3.95, 3)]
        plt.title("Average Equilibrium Pressure vs Unit Cell Volume")
        plt.xlabel("Volume (Angstrom^3)")
        plt.ylabel("Pressure (bars)")
        plt.grid('on')
        plt.plot(volumes, avg_pressures)
        plt.savefig("pressureVsVolumeQ4.pdf")
        plt.close()


    # Run the code for PARTII questions
    storeLAMMPSData()
    velocityDistribution()
    caclulateTimeCorrelationFxn()
    calculateEquilibriumLatticeParameter()




####RUN####
# plotEnergies() # PARTI, Question 1
thermoProperties() # PARTII, Questions 2, 3, 4, 5



# Scratch
# ##########PRACTICE############
# m2 = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", "ITEM: ATOMS id type vx vy vz")
# if (m2 is None):
#     print("NONE - NO MATCH")
# else:
#     print(m2.group(0), "ground(0)")
#     print(m2.group(1), "group(1)")
#     print(m2.group(2), "group(2)")
#     print(m2.group(3), "group(3)")
#     print(m2.group(4), "group(4)")
#     print(m2.group(5), "group(5)")

# ##########PRACTICE############
# # m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
# m = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", " 0         1112   -1874.2011    -1945.926    71.724903, physicist")
# print(m.group(0), "0")
# print(m.group(1), "1")
# print(m.group(2), "2")
# print(m.group(3), "3")
# print(m.group(4), "4")
# print(m.group(5), "5")

# ##########PRACTICE############
# # m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")
# m = re.match("(?:\s*)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s+)(-?[0-9]*\.?[0-9]*)(?:\s*)", " 0         1112   -1874.2011    -1945.926    71.724903, physicist")
# print(m.group(0), "0")
# print(m.group(1), "1")
# print(m.group(2), "2")
# print(m.group(3), "3")
# print(m.group(4), "4")
# print(m.group(5), "5")

# ##########PRACTICE############
# a = [5, 4, 3, 2, 1]
# b = [0, 1, 2, 3, 4]
#
# i = 0
# j = 5, 4, 3, 2, 1
# k = 5, 4, 3, 2, 1
#
# i = 1
# j = 4, 3, 2, 1
# k = 5, 4, 3, 2
#
# i = 2
# j = 3, 2, 1
# k = 5, 4, 3
#
# i = 3
# j = 2, 1--
# k = 5, 4
#
# i = 4
# j = 1
# k = 5

# data = [5, 4, 3, 2, 1]
# avg_data = np.average(data)
# corr_fxn = []
#
#
# for t in range(0, len(data)):
#     temps = []
#     print("t: ", t)
#     for t0 in range(0, len(data)):
#         print("t0: ", t0)
#         if (t0 + t >= len(data)):
#             break;
#         print("data[t0 + t]: ", data[t0 + t], " ", "data[t0]: ", data[t0])
#         temps.append((data[t0 + t] - avg_data) * (data[t0] - avg_data))
#     corr_fxn.append(np.average(temps))
# print(corr_fxn)



