# CroppyPlanning
# Michael Siegmund
# V0.0 25 Feb 2022
# WE ARE!

# This program is designed to facilitate planting, seeding, and harvesting planning
#     for a small scale vegitable farm. I hope it helps!

from datetime import date, timedelta
from math import ceil


print('mmmmmmmmmmmmmm doughnuts.. I mean veggies........')


class cropObj(object):
    ''' The Basic object of CroppyPlanning. A cropObj holds all the information about a specific crop on the farm
    A 'Crop' refers to all plans of that type. So all left-handed striped tomatoes are considered one crop, but 
    clockwise turnips and counterclockwise turnips are considered separate crops. The same variety planted in two different
    seasons is considered the same crop, with two different plantings'''

    def __init__ (self, crop, variety, days2transplant=0,days2maturity=0,control='Harvest',germRate=1.0,seedTray=128,rePot=True,rePotSize=72,source='savedSeed',method="directSeed"):
        self.crop = crop 
        self.variety = variety
        self.control = control
        self.days2transplant = days2transplant
        self.days2maturity = days2maturity
        self.germRate = germRate  #Germination Rate (Fraction. 1.0, or 0.9, or 0.7, etc.)
        self.seedTray = seedTray  #Size of the seed tray used
        self.rePot = rePot #Does this crop get repotted before transplanting? Bool
        self.repotSize = rePotSize #Size of the trays used for the repotting
        self.source = source #Source (Johnny's, Kitazawa, Lowes, Saved Seed, etc...)
        self.method = method #Planting method: 'directSeed','seedStart', or 'transplant'. 

    def seedingInfo(self,needs,controlDate):
        '''Calculates what is needed for the seeding of the plant
        inputs
            needs       -   How many plants are needed for transplanting
            controlDate -   Either the known seeding date (if seeding controls this crop) or the known plantingDate [datetime.date]
            
        returns
            seedingDate     -   Date to seed [datetime.date]
            repotDate       -   Date to repot [datetime.date]
            plantingDate    -   Date to transplant [datetime.date]
            nTrays          -   Number of seed trays required
            nSeeds          -   Number of seeds planted
            nRePot          -   Number of trays needed for a re-potting'''

        if self.control == 'Seeding':
            seedingDate = controlDate
            plantingDate = seedingDate + timedelta(days=self.days2transplant)
        else:
            plantingDate = controlDate
            seedingDate = plantingDate - timedelta(days=self.days2transplant)

        minSeeds = needs/self.germRate #Minimum number of seeds planted at the given germination rate to get the required amount of plants
        nTrays = ceil(minSeeds/self.seedTray) #Number of trays. Assume you always use a full tray, so round up
        nSeeds = nTrays*self.seedTray #Assuming a full tray is planted, how many seeds will you actually plant
        if self.rePot:
            nRePot = ceil(nSeeds*self.germRate/self.repotSize) #How many repotting trays will you need if the seeds germinate at the expected rate
        else:
            nRePot = 0
            
        return(seedingDate,plantingDate,nTrays,nSeeds,nRePot)


    def successionPlanting(self,interval,firstPlantDate,lastPlantDate=date(1,1,1),lastHarvestDate=date(1,1,1)):
        '''Calculates every planting and harvesting date for succession planting
        
        Inputs:
            interval        -   Weeks between successive plantings
            firstPlantDate  -   First planting date [datetime.date]
            lastPlantDate   -   Last possible planting date [datetime.date, optional]
            lastHarvestDate -   Last possible harvest date [datetime.date, optional]  
            
        Returns:
            plantingDates       -   Array of all planting dates [1D array of datetime.date]
            transplantgDates    -   Array of all transplant dates, if crop is started as seed and then transplanted [1D array of datetime.date]
            harvestDates        -   Array of all harvest dates [1D array of datetime.date]
            nPlantings          -   Total number of plantings'''


        # Check that at least one of lastPlantDate or lastHarvestDate has been set
        if lastPlantDate.year < 2 and lastHarvestDate.year < 2:
            raise ValueError('Error! You must define the last planting date or the last harvest date for successionPlanting')
        elif lastPlantDate.year < 2:
            # Calculate last planting date from last harvest date
            lastPlantDate = lastHarvestDate - timedelta(days=self.days2maturity)
        elif lastHarvestDate.year < 2:
            # Calculate last harvest date from last planting date
            lastHarvestDate = lastPlantDate + timedelta(days=self.days2maturity)


        plantingDates = [firstPlantDate]
        harvestDates = [firstPlantDate + timedelta(days=self.days2maturity)]
        if self.method == 'seedStart':
            # We only need to know transplant dates if the crop is started as seed and then transplanted
            transplantDates = [firstPlantDate + timedelta(days=self.days2transplant)]
        else:
            transplantDates = []

        cDate = firstPlantDate
        ind = True
        while ind:
            nextPlant = plantingDates[-1] + timedelta(weeks=interval)
            nextHarvest = harvestDates[-1] + timedelta(weeks=interval)
            if nextPlant > lastPlantDate or nextHarvest > lastHarvestDate:
                ind = False
            else:
                plantingDates.append(nextPlant)
                harvestDates.append(nextHarvest)

                if self.method == 'seedStart':
                    transplantDates.append(nextPlant + timedelta(days=self.days2transplant))



        nPlantings = len(plantingDates)

        return(plantingDates,transplantDates,harvestDates,nPlantings)


print('ALL DONE!')