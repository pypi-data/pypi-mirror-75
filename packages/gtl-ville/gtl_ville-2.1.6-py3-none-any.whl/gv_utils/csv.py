#!/usr/bin/env python3

import io
import os

from gv_utils import enums

ENCODING = 'utf8'
CSVSEP = ';'
TEMPCSVSEP = ','

SAMPLES = enums.CsvData.samples
TIMESTAMP = enums.CsvData.timestamp


def dumps_indicators(dictdata):
    csvbuffer = io.BytesIO()
    timestamp, samples = dictdata[TIMESTAMP], dictdata[SAMPLES]
    metrics = None
    for sampleid, sample in samples.items():
        if metrics is None:
            metrics = list(sample.keys())
            headers = [str(timestamp), ] + metrics
            csvbuffer.write(CSVSEP.join(headers).encode(ENCODING))
        csvbuffer.write(os.linesep.encode(ENCODING))
        values = [str(sampleid), ]
        for metric in metrics:
            value = sample.get(metric, -1)
            if isinstance(value, float):
                value = round(value)
            values.append(str(value))
        csvbuffer.write(CSVSEP.join(values).encode(ENCODING))
    return csvbuffer


def loads_indicators(csvbuffer):
    header = _get_line(csvbuffer.readline())
    dictdata = {TIMESTAMP: int(header.pop(0))}
    samples = {}
    for line in csvbuffer.readlines():
        line = _get_line(line)
        sampleid = line.pop(0)
        sample = {}
        for i in range(len(header)):
            value = line[i]
            try:
                value = int(value)
            except ValueError:
                pass
            sample[header[i]] = value
        samples[sampleid] = sample
    dictdata[SAMPLES] = samples
    return dictdata


def _get_line(line):
    line = bytes.decode(line, ENCODING).strip(os.linesep)
    if CSVSEP not in line:
        line = line.split(TEMPCSVSEP)
    else:
        line = line.split(CSVSEP)
    return line


def dumps_travel_times(dictdata, timestamp):
    csvbuffer = io.BytesIO()
    csvbuffer.write(CSVSEP.join([str(timestamp), 'tozonepointeid', 'traveltime', 'path']).encode(ENCODING))
    for fromzpeid, traveltimes in dictdata.items():
        csvbuffer.write(os.linesep.encode(ENCODING))
        for tozpeid, traveltime in traveltimes.items():
            traveltime, path = traveltime
            values = [str(fromzpeid), str(tozpeid)]
            if isinstance(traveltime, float):
                traveltime = round(traveltime)
            values.append(str(traveltime))
            values.append(path)
            csvbuffer.write(CSVSEP.join(values).encode(ENCODING))
    return csvbuffer
