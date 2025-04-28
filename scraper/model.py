from dataclasses import dataclass
import pydash
from scraper.enums import *


@dataclass
class PropertyRecord:
    """Data class representing a real estate property"""
    
    propertyId: int
    localityName: str
    postalCode: int
    typeOfProperty: int
    subtypeOfProperty: int
    price: int
    typeOfSale: int
    numberOfRooms: int
    livingArea: int
    equippedKitchen: int
    furnished: int
    openFire: int
    
    garden: int
    surfaceOfGood: int
    numberOfFacades: int
    swimmingPool: int
    stateOfBuilding: int
    latitude: float
    longitude: float
    terraceSurface: int
    hasBasement: int
    hasDressingRoom: int 
    hasDisabledAccess: int 
    hasLift: int
    hasLaundryRoom : int
    gardenOrientation : int
    streetFacadeWidth : int
    livingRoomSurface: int
    streetFacadeWidth : int
    electricalInstallationCertificate : int
    gScore : int
    heatingType : int
    hasHeatPump: int
    hasPhotovoltaicPanels : int
    hasThermicPanels : int
    hasCollectiveWaterHeater : int
    hasDoubleGlazing : int
    epcScore : int
    primaryEnergyConsumptionPerSqm : int
    renovationObligation : int
    cadastralIncome : int
    parkingCountIndoor : int
    parkingCountOutdoor : int
    parkingCountClosedBox: int

    @classmethod
    def from_json(self, json_object):
        """Create a PropertyRecord from a JSON object."""
        
        property = json_object['property']

        room_count = property['roomCount'] if property.get('roomCount') else (
            (property.get('bedroomCount') or 0) +
            (property.get('bathroomCount') or 0) +
            (1 if (property.get('kitchen')) else 0) +
            (1 if (property.get('hasDressingRoom')) else 0) +
            (1 if (property.get('hasDiningRoom')) else 0) +
            (1 if (property.get('hasLaundryRoom')) else 0) +
            (1 if (property.get('hasLivingRoom')) else 0)
        )

        return self(
            propertyId=json_object['id'],
            localityName=pydash.get(property, "location.locality") or "UNKNOWN",
            postalCode=pydash.get(property, "location.postalCode") or -1,
            typeOfProperty=PropertyType[property['type'] or "UNKNOWN"].value,
            subtypeOfProperty=PropertySubtype[property['subtype'] or "UNKNOWN"].value,
            price=self.price_value(json_object),
            typeOfSale=TypeOfSale[pydash.get(json_object, "price.type") or "UNKNOWN"].value, #je ne suis pas sûr de ça
            numberOfRooms=room_count,
            livingArea=self.livingarea_value(json_object),
            equippedKitchen=EquipedKitchen[pydash.get(property, "kitchen.type") or "UNKNOWN"].value,
            furnished=self.true_false_nan(json_object, 'transaction.sale.isFurnished'),
            openFire=self.true_false_nan(property, 'fireplaceExists'),
            garden= pydash.get(property, 'gardenSurface') or -1,
            gardenOrientation = GardenOrientation[pydash.get(property, 'gardenOrientation') or "UNKNOWN"].value,
            surfaceOfGood=pydash.get(property, "land.surface") or -1,
            numberOfFacades=pydash.get(property, "building.facadeCount") or -1,
            swimmingPool=self.true_false_nan(property, 'hasSwimmingPool'),
            stateOfBuilding=StateOfBuilding[pydash.get(property, "building.condition") or "UNKNOWN"].value,
            latitude=pydash.get(property, 'location.latitude') or -1,
            longitude=pydash.get(property, 'location.longitude') or -1,
            terraceSurface= pydash.get(property, 'terraceSurface') or -1,
            hasBasement=self.true_false_nan(property, 'hasBasement'),
            hasDressingRoom= self.true_false_nan(property, 'hasDressingRoom'),
            hasDisabledAccess= self.true_false_nan(property, 'hasDisabledAccess'), 
            hasLift= self.true_false_nan(property, 'hasLift'),
            hasLaundryRoom= self.true_false_nan(property, 'hasLaundryRoom'),
            livingRoomSurface = pydash.get(property, 'livingRoom.surface') or -1, 
            streetFacadeWidth = pydash.get(property, 'building.streetFacadeWidth') or -1,
            electricalInstallationCertificate = self.true_false_nan(property, 'propertyCertificates.hasElectricalInstallationComplianceCertificate'),
            gScore = GScore[pydash.get(property, 'constructionPermit.gScore') or "UNKNOWN"].value,
            heatingType = HeatingType[pydash.get(property, 'energy.heatingType') or "UNKNOWN"].value,
            hasHeatPump = self.true_false_nan(property, 'energy.hasHeatPump'), 
            hasPhotovoltaicPanels = self.true_false_nan(property, 'energy.hasPhotovoltaicPanels'),
            hasThermicPanels = self.true_false_nan(property, 'energy.hasThermicPanels'),
            hasCollectiveWaterHeater = self.true_false_nan(property, 'energy.hasCollectiveWaterHeater'),
            hasDoubleGlazing = self.true_false_nan(property, 'energy.hasDoubleGlazing'),
            epcScore = EPCScore.from_string(pydash.get(json_object, 'transaction.certificates.epcScore')).value,
            primaryEnergyConsumptionPerSqm = pydash.get(json_object, 'transaction.certificates.primaryEnergyConsumptionPerSqm') or -1,
            renovationObligation = self.true_false_nan(json_object, 'transaction.certificates.renovationObligation'),
            cadastralIncome = pydash.get(json_object, 'transaction.sale.cadastralIncome') or -1, 
            parkingCountIndoor = pydash.get(property, 'parkingCountIndoor') or -1,
            parkingCountOutdoor = pydash.get(property,'parkingCountOutdoor') or -1,
            parkingCountClosedBox = pydash.get(property, 'parkingCountClosedBox') or -1,
        )

    @classmethod
    def true_false_nan(self, obj, elem) -> int:
        value = pydash.get(obj, elem)
        if value is None:
            return -1
        elif value is True: 
            return 1
        else: 
            return 0
    
    @classmethod
    def price_value(self, json_object) -> int:
        """Get the price value, if none, then try to get the middle price value"""

        value = pydash.get(json_object, 'price.mainValue')

        if value is None: 
            try:
                value = int(pydash.get(json_object, 'cluster.maxPrice', 0) + pydash.get(json_object, 'cluster.minPrice', 0) / 2)
            except Exception:
                value = -1
    
        return value
    
    @classmethod
    def livingarea_value(self, json_object) -> int:
        """Get the surface value, if none, then try to get the middle surface value"""

        value = pydash.get(json_object, 'property.netHabitableSurface')

        if value is None: 
            try:
                value = int(pydash.get(json_object, 'cluster.maxSurface', 0) + pydash.get(json_object, 'cluster.minSurface', 0) / 2)
            except Exception:
                value = -1
    
        return value
    
    def __str__(self) -> str:
        """Return a string representation of the Property."""
        return f"ID-{self.propertyId} : {self.localityName}({self.postalCode}) - {self.price}€" 