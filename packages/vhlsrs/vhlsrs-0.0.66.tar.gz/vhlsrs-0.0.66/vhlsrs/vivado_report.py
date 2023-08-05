"""
Parse vivado hls report
"""

from itertools import dropwhile
from pathlib import Path
import re
from xml.dom import minidom

def __getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def parse_syn_report(synth_report_file):
    synth_rpt = Path(synth_report_file)
    res = {}
    with synth_rpt.open("r") as rpt:
        tree = minidom.parse(rpt)
    version = tree.getElementsByTagName('Version')[0]
    res['Vivado_HLS_Version'] = __getText(version.childNodes)
    estimated_clk = tree.getElementsByTagName('EstimatedClockPeriod')[0]
    res['estimated_period'] = __getText(estimated_clk.childNodes)
    try:
        pipeline_depth = tree.getElementsByTagName('Worst-caseLatency')[0]
        res['worst_case_latency'] = __getText(pipeline_depth.childNodes)
    except (KeyError, IndexError, ValueError):
        res['worst_case_latency'] = '0'
    try:
        pipeline_II = tree.getElementsByTagName('PipelineInitiationInterval')[0]
        res['II'] = __getText(pipeline_II.childNodes)
        res['pipelined'] = True
    except (KeyError, IndexError, ValueError):
        res['II'] = '0'
        res['pipelined'] = False
    return res

def _parse_timing(line):
    pattern = '(?P<val>[0-9]+\.[0-9]+)ns'
    match = re.search(pattern, line)
    return match.group('val')

def parse_impl_report(impl_report_file, timing_report_file):
    impl_file = Path(impl_report_file)
    res = {}
    with impl_file.open("r") as impl:
        tree = minidom.parse(impl)
    resources = tree.getElementsByTagName('Resources')[0]
    res["LUT"] = __getText(resources.getElementsByTagName('LUT')[0].childNodes)
    res["FF"] = __getText(resources.getElementsByTagName('FF')[0].childNodes)
    res["DSP"] = __getText(resources.getElementsByTagName('DSP')[0].childNodes)
    res["BRAM"] = __getText(resources.getElementsByTagName('BRAM')[0].childNodes)
    res["SRL"] = __getText(resources.getElementsByTagName('SRL')[0].childNodes)
    timing_report_path = Path(timing_report_file)
    line_filter = lambda x : not x.startswith('Max Delay Paths')
    with timing_report_path.open('r') as timing_report:
        for line in dropwhile(line_filter,  timing_report):
            if line.strip().startswith('Data Path Delay:'):
                res['timing'] = _parse_timing(line)
                return res
    return res

