#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import asyncio
from concurrent.futures import ProcessPoolExecutor
import json
import io

import shapely.wkt

from gv_proto.proto.archivist_pb2 import DataQuality, Indicators, TravelTimes
from gv_proto.proto.geographer_pb2 import FreeflowSpeeds, Locations, Mapping
from gv_utils import csv, enums, geometry


ATT = enums.AttId.att
DATATYPE_EID = enums.AttId.datatypeeid
EID = enums.AttId.eid
GEOM = enums.AttId.geom
WEBATT = enums.AttId.webatt


async def encode_indicators(indicators):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        pbindicators = await loop.run_in_executor(executor, _csv_dumps_bytes, indicators)
    return Indicators(indicators=pbindicators)


def _csv_dumps_bytes(data):
    try:
        csvbuffer = csv.dumps(data)
        bdata = csvbuffer.getvalue()
        csvbuffer.close()
    except:
        bdata = b''
    return bdata


def sync_decode_indicators(pbindicators):
    return _csv_loads_bytes(pbindicators.indicators)


async def decode_indicators(pbindicators):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        data = await loop.run_in_executor(executor, _csv_loads_bytes, pbindicators.indicators)
    return data


def _csv_loads_bytes(indicators):
    try:
        csvbuffer = io.BytesIO(indicators)
        data = csv.loads(csvbuffer)
        csvbuffer.close()
    except:
        data = {}
    return data


async def encode_data_quality(dataquality):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        bdata = await loop.run_in_executor(executor, _encode_data_quality, dataquality)
    return DataQuality(dataquality=bdata)


def _encode_data_quality(dataquality):
    try:
        bdata = json.dumps(dataquality).encode(csv.ENCODING)
    except:
        bdata = b''
    return bdata


async def decode_data_quality(pbdataquality):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        data = await loop.run_in_executor(executor, _decode_data_quality, pbdataquality)
    return data


def sync_decode_data_quality(pbdataquality):
    return _decode_data_quality(pbdataquality)


def _decode_data_quality(pbdataquality):
    return json.loads(pbdataquality.dataquality.decode(csv.ENCODING))


async def encode_travel_times(traveltimes):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        bdata = await loop.run_in_executor(executor, _encode_travel_times, traveltimes)
    return TravelTimes(traveltimes=bdata)


def _encode_travel_times(traveltimes):
    try:
        bdata = json.dumps(traveltimes).encode(csv.ENCODING)
    except:
        bdata = b''
    return bdata


async def decode_travel_times(pbtraveltimes):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        data = await loop.run_in_executor(executor, _decode_travel_times, pbtraveltimes)
    return data


def sync_decode_travel_times(pbtraveltimes):
    return _decode_travel_times(pbtraveltimes)


def _decode_travel_times(pbtraveltimes):
    return json.loads(pbtraveltimes.traveltimes.decode(csv.ENCODING))


async def encode_locations(locations):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        pblocations = await loop.run_in_executor(executor, _encode_locations, locations)
    return pblocations


def _encode_locations(locations, pblocations=None):
    if pblocations is None:
        pblocations = Locations()
    for eid, loc in locations.items():
        geom = loc[GEOM]
        if isinstance(geom, str):
            geom = shapely.wkt.loads(geom)
        pblocations.locations[eid].geom = geom.wkb
        pblocations.locations[eid].att.FromJsonString(json.dumps(loc.get(ATT, {})))
        pblocations.locations[eid].webatt.FromJsonString(json.dumps(loc.get(WEBATT, {})))
        pblocations.locations[eid].datatype = loc.get(DATATYPE_EID, '')
    return pblocations


def sync_decode_locations(response):
    return _decode_locations(response.locations)


async def decode_locations(pblocations):
    loop = asyncio.get_event_loop()
    locations = await loop.run_in_executor(None, _decode_locations, pblocations.locations)
    return locations


def _decode_locations(pblocations):
    locations = {}
    for eid in pblocations:
        loc = pblocations[eid]
        locations[eid] = {EID: eid, GEOM: geometry.decode_geometry(loc.geom),
                          ATT: json.loads(loc.att.ToJsonString()), WEBATT: json.loads(loc.webatt.ToJsonString()),
                          DATATYPE_EID: loc.datatype}
    return locations


async def encode_mapping(mapping, validat):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        pbmapping = await loop.run_in_executor(executor, _encode_mapping, mapping, validat)
    return pbmapping


def _encode_mapping(mapping, validat):
    pbmapping = Mapping()
    for fromeid, toeidsorlocations in mapping.items():
        if not isinstance(toeidsorlocations, dict):
            pbmapping.mapping[fromeid].eids.eids.extend(toeidsorlocations)
        else:
            _encode_locations(toeidsorlocations, pbmapping.mapping[fromeid].locations)
    pbmapping.validat.FromSeconds(validat)
    return pbmapping


async def decode_mapping(pbmapping):
    loop = asyncio.get_event_loop()
    mapping = await loop.run_in_executor(None, _decode_mapping, pbmapping.mapping)
    return mapping, pbmapping.validat.ToSeconds()


def _decode_mapping(pbmapping):
    mapping = {}
    for eid in pbmapping:
        if pbmapping[eid].HasField('eids'):
            mapping[eid] = pbmapping[eid].eids.eids
        else:
            mapping[eid] = _decode_locations(pbmapping[eid].locations.locations)
    return mapping


async def encode_ffspeeds(eidsffspeeds):
    return FreeflowSpeeds(freeflowspeeds=eidsffspeeds)


async def decode_ffspeeds(pbffspeeds):
    return dict(pbffspeeds.freeflowspeeds)
