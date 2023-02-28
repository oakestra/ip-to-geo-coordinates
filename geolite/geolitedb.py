import ipaddress
import pandas as pd
import time
import logging
from decorators.singleton import singleton


@singleton
class Geolite:
    instance = None

    def __init__(self, location=None, columns=None):
        logging.debug("Start building GeoLite2 dataframe...")
        self.df = None
        self.location = location
        if location is not None:
            start = time.time()
            column_list = None
            header = 'infer'
            if columns is not None:
                column_list = columns.split(',')
                header = None
            self.df = pd.read_csv(
                self.location,
                names=column_list,
                header=header,
                dtype={'ip_range_start': str, 'ip_range_end':str, 'latitude': str, 'longitude': str},
            )

            #remove ipv6 addresses
            self.df = self.df[self.df['ip_range_start'].apply(lambda x: isinstance(ipaddress.ip_address(x), ipaddress.IPv4Address))]

            # sort dataframe by start_int column in ascending order
            self.df['start_int'] = self.df['ip_range_start'].apply(lambda x: int(ipaddress.IPv4Address(x)))
            self.df['end_int'] = self.df['ip_range_end'].apply(lambda x: int(ipaddress.IPv4Address(x)))
            self.df = self.df.sort_values('start_int', ascending=True)

            end = time.time()
            logging.debug(f"...done building the dataframe. Took {end - start}s")
            logging.debug(self.df)

    def query_geolocation_for_ips(self, ip_addresses):
        if self.df is None:
            return []

        ip_addresses = [ipaddress.ip_address(ip) for ip in ip_addresses]
        ip_locations = {}

        for query_ip in ip_addresses:
            logging.info(f"Lookup: {query_ip}")

            # default lat == lon == 0
            ip_locations[str(query_ip)] = {"lat": '0', "long": '0'}

            # convert input address to integer representation
            network_int = int(ipaddress.IPv4Address(query_ip))

            # perform binary search for matching row
            low = 0
            high = len(self.df) - 1

            while low <= high:
                mid = (low + high) // 2
                if self.df.iloc[mid]['start_int'] <= network_int <= self.df.iloc[mid]['end_int']:
                    ip_locations[str(query_ip)] = {"lat": str(self.df.iloc[mid]['latitude']),
                                                   "long": str(self.df.iloc[mid]['longitude'])}
                    break
                elif network_int < self.df.iloc[mid]['start_int']:
                    high = mid - 1
                else:
                    low = mid + 1

        return ip_locations

