from enum import Enum

class PropertyType(Enum):
    """Enumeration of property types."""
    UNKNOWN = -1
    HOUSE = 0
    APARTMENT = 1
    HOUSE_GROUP = 2
    APARTMENT_GROUP = 3

class PropertySubtype(Enum):
    """Enumeration of property subtypes."""
    UNKNOWN = -1
    HOUSE = 0
    APARTMENT = 1
    HOUSE_GROUP = 2
    APARTMENT_GROUP = 3
    BUNGALOW = 4
    CHALET = 5
    CASTLE = 6
    FARMHOUSE = 7
    COUNTRY_COTTAGE = 8
    EXCEPTIONAL_PROPERTY = 9
    APARTMENT_BLOCK = 10
    MIXED_USE_BUILDING = 11
    TOWN_HOUSE = 12
    MANSION = 13
    VILLA = 14
    OTHER_PROPERTY = 15
    MANOR_HOUSE = 16
    PAVILION = 17
    GROUND_FLOOR = 18
    DUPLEX = 19
    TRIPLEX = 20
    FLAT_STUDIO = 21
    PENTHOUSE = 22
    LOFT = 23
    KOT = 24
    SERVICE_FLAT = 25

class StateOfBuilding(Enum):
    """Enumeration of building states."""
    UNKNOWN = -1
    TO_BE_DONE_UP = 0
    GOOD = 1
    AS_NEW = 2
    TO_RENOVATE = 3
    JUST_RENOVATED = 4
    TO_RESTORE = 5
    
class TypeOfSale(Enum):
    """Enumeration of the type of sale."""
    UNKNOWN = -1
    residential_sale = 0
    group_sale = 1
    
class EquipedKitchen(Enum):
    """Enumeration of equiped kitchen"""
    UNKNOWN = -1 
    NOT_INSTALLED = 0

    INSTALLED = 1
    SEMI_EQUIPPED = 2
    HYPER_EQUIPPED = 3
    
    USA_UNINSTALLED = 4
    USA_INSTALLED = 5
    USA_SEMI_EQUIPPED = 6
    USA_HYPER_EQUIPPED = 7

class GardenOrientation(Enum):
    """Enumeration of the garden orientation"""
    UNKNOWN = -1 
    NORTH = 0
    SOUTH = 1

    NORTH_WEST = 2
    WEST = 3
    SOUTH_WEST = 4

    NORTH_EAST = 5
    EAST = 6
    SOUTH_EAST = 7    
    
class GScore(Enum):
    """
    Risks of flooding:

    A : No risk of flooding
    B : small risk of flooding by 2050
    C : small risk of flooding
    D : Medium risk of flooding
    """ 
    UNKNOWN = -1 
    A = 0
    B = 1
    C = 2
    D = 3
    
class HeatingType(Enum):
    """Enumeration of heating types."""
    UNKNOWN = -1
    GAS = 0
    FUELOIL = 1
    WOOD = 2
    ELECTRIC = 3
    PELLET = 4
    SOLAR = 5
    CARBON = 6

class EPCScore(Enum):
    """
    Le score Parcelle et le score Bâtiment sont répartis en 4 classes de A à D et en fonction de la source d'inondation (pluie, mer ou rivières) :
    Classe A : Aucune inondation modélisée
    classe B : faible probabilité d'inondation sous l'effet du changement climatique (sc2050) ;
    classe C : faible risque d'inondation dans le climat actuel ;
    classe D : probabilité d'inondation moyenne dans le climat actuel.
    """

    UNKNOWN = -1 
    A_PLUS = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6

    @classmethod
    def from_string(self, value):
        """convert a string from the data into an EPCscore enumeration"""
        mapping = {
            "A+" : self.A_PLUS,
            "A" : self.A,
            "B" : self.B,
            "C" : self.C, 
            "D" : self.D,
            "E" : self.E, 
            "F" : self.F
        }

        return mapping.get(value, self.UNKNOWN)
