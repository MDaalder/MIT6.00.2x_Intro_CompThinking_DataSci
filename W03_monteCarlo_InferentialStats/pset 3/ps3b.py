# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab
random.seed(0)
''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

#    def __init__(self):
#        print('No child was made')

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        num = random.random()
        
        if num < self.clearProb:
            return True
        else:
            return False
        
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
                
        reproduceProb = self.maxBirthProb * (1 - popDensity)
        
        if random.random() >= (1-reproduceProb):
            return SimpleVirus(self.getMaxBirthProb(), self.getClearProb())
#            return self.__init__(self.getMaxBirthProb(), self.getClearProb())
        
        raise NoChildException
        


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop
        self.popDens = len(self.viruses)/float(self.maxPop)

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses[:]
        

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop


    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        virusList = []
                
        for virus in self.getViruses():
            if not virus.doesClear():
                virusList.append(virus)
#            elif virus.doesClear() == False:
                
        self.popDens = self.getTotalPop()/float(self.getMaxPop())
        
        if self.popDens <= 1:
            for virus in virusList[:]:
                try:
                    virusList.append(virus.reproduce(self.popDens))
                except NoChildException:
                    pass
        
        self.viruses = virusList[:]
            
        return len(self.viruses)
#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    timeSteps = 300
    trialsData = []
    avgData = []
    
    for step in range(timeSteps):
        trialsData.append([])
    
    for trial in range(numTrials):
        step = 0
        virusList = []
        
        for num in range(numViruses):
            virusList.append(SimpleVirus(maxBirthProb, clearProb))
        
        person = Patient(virusList, maxPop)
        
        
        while step < timeSteps:
            trialsData[step].append(person.update())      
            step += 1
            
    
    for step in range(timeSteps):
        avgStep = (sum(trialsData[step])/len(trialsData[step]))
        avgData.append(avgStep)
    
    xVals = range(timeSteps)
    yVals = avgData
    
    pylab.plot(xVals, yVals, label = "SimpleVirus")
    pylab.title("SimpleVirus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()
    

#numTrials = 100
#numViruses = 100
#maxPop = 1000
#maxBirthProb = 0.1
#clearProb = 0.05
#simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials)


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        
        try:
            return self.resistances[drug]
        except:
            pass


    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        
        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException
        
        childResistance = {}
        num = random.random()
        reproduceProb = self.maxBirthProb * (1 - popDensity)
        
        
        
        if num >= (1-reproduceProb):
            
            for drug in self.resistances.keys():
                # if the parent is resistant to a drug, then the child has 1-mutprob of keeping the resistance
                if self.isResistantTo(drug):
                    if num < 1-self.getMutProb():
                        childResistance[drug] = True
                    else:
                        childResistance[drug] = False         
                # if the parent is not resistant to a drug, then the child has mutprob of being resistant to the drug
                else:
                    if num < self.getMutProb():
                        childResistance[drug] = True
                    else:
                        childResistance[drug] = False
                    
            return ResistantVirus(self.getMaxBirthProb(), self.getClearProb(), childResistance, self.getMutProb())
        
        raise NoChildException
  
    
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        
        # a list of strings: drugs being administered to the patient
        self.drugList = []
        
         # from the Patient(object) class
#        self.viruses = viruses
#        self.maxPop = maxPop
#        self.popDens = len(self.viruses)/float(self.maxPop)



    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        # if the newDrug is already being administered, do nothing
        # else, add the drug to the list of drugs being administered to the patient
        if newDrug in self.drugList:
            pass
        else:
            self.drugList.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # returns a copy of the list of strings of drugs being administered to the patient
        return self.drugList[:]


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        
        if len(drugResist) == 0:
            pass
        
        # initiate a list to store viruses that are resistant to the drugs list in drugResist
        resistantPop = []
        
        # iterate down the total virus population
        for virus in self.getViruses():
            
            # set dummy variable to True
            resistant = True
            # iterate down drugs in drugResist
            for drug in drugResist:
                # if the virus in the total population is not resistant to a drug
                # set the resistant dummy variable to False
                if not virus.isResistantTo(drug):
                    resistant = False
            
            # all viruses that are resistant to the drugs in drugResist get stored in the list
            if resistant == True:
                resistantPop.append(virus)
        
        # returns the population of drug resistant viruses
        return len(resistantPop)
                    


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        
        virusList = []
        
        # checks to see if a virus survives randomly, and stores it
        for virus in self.getViruses():
            if not virus.doesClear():
                virusList.append(virus)
        
        # updates the virus population list
        self.viruses = virusList[:]
        
        # calculates the current population density
        self.popDens = self.getTotalPop()/float(self.getMaxPop())
        
        # if the population has not met saturation
        if self.popDens < 1:
            for virus in virusList[:]:
                # determine if the virus reproduces, and add it to the list of the virus population
                # we now include drugs being administered to the patient
                try:
                    virusList.append(virus.reproduce(self.popDens, self.getPrescriptions()))
                # if the virus does not reproduce, raise the error 'NoChildException'
                except NoChildException:
                    pass
        
        # update the virus population list
        self.viruses = virusList[:]
        
        # returns the population as an integer
        return len(self.viruses)
        
#
# PROBLEM 4
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    #update these parameters based on desired outcome
    timeSteps = 300
    timePrescription = timeSteps/2
    
    if len(resistances) > 0:
        checkResistance = [*resistances]
    else:
        checkResistance = ['0']
    
    trialsData = []
    trialsResistantData = []
    avgData = []
    avgResistantData = []
    
    # populate the trialsData list with empty lists the length of timesteps
    # each sub-list will be populated with all of the trials worth of virus population data
    # for the respective timestep. This will be used to calculate the average virus population at each timestep.
    # i.e. trialsData[10] = [data from all trials at timestep 10]
    for step in range(timeSteps):
        trialsData.append([])
        trialsResistantData.append([])
    
    # will complete x number of timesteps, for x number of trials
    for trial in range(numTrials):
        # tracks the timesteps taken, up to a max of timeSteps initiated above
        step = 0
        # empty list to be populated with the virus population at every timestep for the given trial
        virusList = []
        
        # initiates the first list of numViruses viruses in the patient
        for __ in range(numViruses):
            virusList.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))
        
        # initiates an instance of TreatedPatient
        person = TreatedPatient(virusList, maxPop)
        
        # while there is still time to simulate, update the virus population and the rsistant virus population
        # store the population in the corresponding list for the current trial
        # using timestep/2 in this instance
        while step < timeSteps:
            # introduce drugs to the patient at specific timestep
            if step == timePrescription:
                person.addPrescription('guttagonol')
#                person.addPrescription('srinol')
                
            trialsData[step].append(person.update())
            trialsResistantData[step].append(person.getResistPop(checkResistance))
#            trialsResistantData[step].append(person.getResistPop([*resistances]))
            
            step += 1
                                               
    # this calculates and stores the average virus and resistant virus populations from all trials at timestep step
    for step in range(timeSteps):
        avgStep = (sum(trialsData[step])/len(trialsData[step]))
        avgData.append(avgStep)
        avgResistantStep = (sum(trialsResistantData[step])/len(trialsResistantData[step]))
        avgResistantData.append(avgResistantStep)
    

    xVals = range(timeSteps)
    yVals = avgData
    yValsResistant = avgResistantData
    
    pylab.plot(xVals, yVals, label = "Total Virus Pop")
    pylab.plot(xVals, yValsResistant, label = 'Resistant Virus Pop')
    pylab.title("Resistant Virus simulation")
    pylab.xlabel("Time Steps")
    pylab.ylabel("Average Virus Population")
    pylab.legend(loc = "best")
    pylab.show()



numTrials = 10
numViruses = 100
maxPop = 1000
maxBirthProb = 0.1
clearProb = 0.05
mutProb = 0.005
resistances = {'guttagonol': False}#, 'srinol': True}
simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials)