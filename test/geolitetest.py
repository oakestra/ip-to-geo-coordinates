import unittest
from geolite.geolitedb import Geolite


def test_location_single():
    # SETUP
    geo = Geolite(location="test_db.csv")

    # EXEC
    results = geo.query_geolocation_for_ips(['112.210.112.0'])

    # ASSERT
    assert results['112.210.112.0'] == {"lat": "14.5448", "long": "120.9900"}

def test_location_multi_1():
    # SETUP
    geo = Geolite(location="test_db.csv")

    # EXEC
    results = geo.query_geolocation_for_ips(['112.210.112.0', '112.210.128.0', '188.96.90.128'])

    # ASSERT
    assert results['112.210.112.0'] == {"lat": "14.5448", "long": "120.9900"}
    assert results['112.210.128.0'] == {"lat": "14.4340", "long": "120.9376"}
    assert results['188.96.90.128'] == {"lat": "48.9091", "long": "9.2195"}


def test_location_not_existing():
    # SETUP
    geo = Geolite(location="test_db.csv")

    # EXEC
    results = geo.query_geolocation_for_ips(['112.210.112.0', '112.210.128.0', '199.96.90.128'])

    # ASSERT
    assert results['112.210.112.0'] == {"lat": "14.5448", "long": "120.9900"}
    assert results['112.210.128.0'] == {"lat": "14.4340", "long": "120.9376"}
    assert results['199.96.90.128'] == {"lat": "0", "long": "0"}


def test_location_double_init():
    # SETUP
    geo = Geolite(location="test_db.csv")
    Geolite()
    geo = Geolite()

    # EXEC
    results = geo.query_geolocation_for_ips(['112.210.112.0', '254.210.128.0', '199.96.90.128'])

    # ASSERT
    assert results['112.210.112.0'] == {"lat": "14.5448", "long": "120.9900"}
    assert results['254.210.128.0'] == {"lat": "0", "long": "0"}
    assert results['199.96.90.128'] == {"lat": "0", "long": "0"}

def test_location_use_cols_no_default():
    # SETUP
    geo = Geolite(location="test_db_nocols.csv",
                  columns='ip_range_start,ip_range_end,country_code,state1,state2,city,postcode,latitude,longitude,timezone')

    # EXEC
    results = geo.query_geolocation_for_ips(['112.210.112.0', '254.210.128.0', '199.96.90.128'])

    # ASSERT
    assert results['112.210.112.0'] == {"lat": "14.5448", "long": "120.9900"}
    assert results['254.210.128.0'] == {"lat": "0", "long": "0"}
    assert results['199.96.90.128'] == {"lat": "0", "long": "0"}
