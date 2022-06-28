from dmt import *
import random


"""import googlemaps

# Add API Key here
gmaps = googlemaps.Client(key='AIzaSyBUHfShaosJaSUneB0rGj-lKl9nW5NMXZk')

"""
class gmaps:
    @staticmethod
    def directions(start, end):

        # Set a random seed based on the combination of the start + end string
        random.seed(hash(start + end))

        # Return the distance format as the google maps directions
        return [{'legs': [{'distance': {'value': random.randint(1e4, 1e5)}}]}]


class AddressError(Exception):
    """Invalid address when generating distances"""
    def __init__(self, start, end):
        print(f"(factory={start}, customer={end}) not found")


class FormatError(Exception):
    """Error when Formatting the distance matrix"""
    def __init__(self):
        print("Error when formatting distance matrix")
        

class SaveError(Exception):
    """Error when saving excel file"""
    def __init__(self):
        print("Error while saving Excel file")


class DistanceMatrix:
    """Everything distance matrix"""

    filepath = "C:\\Users\\monty.minh\\Documents\\Distance-Matrix-Tool\\Address Inputs\\Address Input.xlsx"

    @classmethod
    def collect_address(cls):
        """
        Collect the list of factory-customer 
        addresses from uploaded file
        
        """

        # Collect Factory Addresses
        df = pd.read_excel(cls.filepath, sheet_name="Factory Address")
        cls.factory_id, cls.factory_address = list(
            df['Factory ID']), df['Address']
        cls.factory_len = len(cls.factory_address)

        # Collect Customer Addresses
        df = pd.read_excel(cls.filepath, sheet_name="Customer Address")
        cls.customer_id, cls.customer_address = list(
            df['Customer ID']), df['Address']
        cls.customer_prov = list(df['Province'])
        cls.customer_len = len(cls.customer_address)

        del df

    @classmethod
    def collect_distance(cls):
        """
        Generate distance matrix from list 
        of factory-customer address
        """
        cls.distance_list = []
        cls.completion = False

        for factory in cls.factory_address:

            for customer in cls.customer_address:

                try:  # Try to get distance
                    distance = gmaps.directions(
                        origin=factory,
                        destination=customer)[0]['legs'][0]['distance']['value']
                    cls.distance_list = np.append(cls.distance_list, distance)

                except:  # If not working, break, return the (fac, cus)
                    factory_index = len(cls.distance_list) // cls.customer_len
                    customer_index = len(cls.distance_list) % cls.customer_len

                    print(f"{factory_index=}, {customer_index=}")

                    raise AddressError(cls.factory_address[factory_index],
                                       cls.customer_address[customer_index])

            cls.completion = True

    @classmethod
    def format_distance(cls):
        """Format the distance list into the distance matrix dataframe"""

        if cls.completion:
            cls.distance_matrix = cls.distance_list.reshape(
                cls.customer_len, cls.factory_len)

            cls.distance_df = pd.DataFrame(data=cls.distance_matrix,
                                           columns=cls.factory_id)

            # Inser info columns into sheet
            cls.distance_df.insert(0, 'Customer ID', cls.customer_id)
            cls.distance_df.insert(1, 'Province', cls.customer_prov)

        else:
            raise FormatError()

    @classmethod
    def save_output(cls):
        """Save outputs to Excel file"""

        try:
            cls.distance_df.to_excel("C:\\Users\\monty.minh\\Documents\\Distance-Matrix-Tool\\Distance.xlsx",
                                     "Factory-Customer Distances",
                                     index=False,
                                     header=True,
                                     startrow=0,
                                     startcol=0)
        except:
            raise SaveError()
            
    
    @classmethod
    def generate_distances(cls):
        """Run all methods in the class"""

        cls.collect_address()
        cls.collect_distance()
        cls.format_distance()
        cls.save_output()
