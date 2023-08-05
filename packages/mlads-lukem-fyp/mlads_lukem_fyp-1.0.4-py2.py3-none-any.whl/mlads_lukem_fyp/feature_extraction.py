#!/usr/bin/env python

# PCAP imports
from scapy.all import *

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80


def full_duplex(p):
    """Consolidate groups of streams of differing directions.

    Adapted from https://gist.github.com/MarkBaggett/d8933453f431c111169158ce7f4e2222#file-scapy_helper-py
    and https://www.sans.org/blog/scapy-full-duplex-stream-reassembly/

    Parameters
    ----------
    p : scapy.layers.l2.Ether, scapy.layers.l2.Dot3
        A single packet on which calculations are made
    """
    sess = "Other"
    if 'Ether' in p:
        if 'IP' in p:
            if 'TCP' in p:
                sess = str(sorted(["TCP", [p['IP'].src, p['TCP'].sport], [p['IP'].dst, p['TCP'].dport]], key=str))
            elif 'UDP' in p:
                sess = str(sorted(["UDP", [p['IP'].src, p['UDP'].sport], [p['IP'].dst, p['UDP'].dport]], key=str))
            elif 'ICMP' in p:
                sess = str(
                    sorted(["ICMP", p['IP'].src, p['IP'].dst, p['ICMP'].code, p['ICMP'].type, p['ICMP'].id], key=str))
            else:
                sess = str(sorted(["IP", p['IP'].src, p['IP'].dst, p['IP'].proto], key=str))
        elif 'ARP' in p:
            sess = str(sorted(["ARP", p['ARP'].psrc, p['ARP'].pdst]))
        else:
            sess = p.sprintf("Ethernet type=%04xr,Ether.type%")
    return sess


def convert(finname, foutname):
    """Convert streams contained in a PCAP file to CSV.

    Print to a file the streams in full duplex after extracting important features.

    Parameters
    ----------
    finname : str
        Input file name (PCAP)
    foutname : file
        Output file name (CSV)
    """
    # cols = "flowid,fwd_pkt_len_std,bwd_pkt_len_std,fwd_pkt_len_max,fwd_pkt_len_min,bwd_pkt_len_max,bwd_pkt_len_min," \
    #       "fwd_pkt_len_mean,bwd_pkt_len_mean,timestamp,srcip,dstip,proto,sport,dport"


    fout = open(foutname, "w")
    # fout.write(cols + '\n')

    try:
        f = rdpcap(finname)  # read the pcap file
    except FileNotFoundError as err:
        print(err)
        return
    sessions = f.sessions(full_duplex)  # extract full sessions (bidirectional as opposed to unidirectional)

    for k, ps in sessions.items():
        flowid = []
        fwdip = ''

        if 'TCP' in k or 'UDP' in k:
            for word in k.split(','):
                # append each item in the flow id, remove any unwanted characters
                flowid.append(re.sub(r"['\[\], ]", "", word))

            try:
                if int(flowid[2]) > int(flowid[4]):
                    fwdip = flowid[1]
                    flowid = flowid[1] + ':' + flowid[2] + '->' + flowid[3] + ':' + flowid[4] + ' ' + flowid[0]
                else:
                    fwdip = flowid[3]
                    flowid = flowid[3] + ':' + flowid[4] + '->' + flowid[1] + ':' + flowid[2] + ' ' + flowid[0]
            except ValueError as err:
                flowid = flowid[1] + ':' + flowid[2] + '->' + flowid[3] + ':' + flowid[4] + ' ' + flowid[0]
                print(err)
        else:
            # We only want to see TCP and UDP streams
            continue

        # reset the features dictionary so calculations are accurate for each session
        features = {"flowid": flowid, "num_fwd_pkts": 0, "num_bwd_pkts": 0, "tot_len_fwd_pkts": 0,
                    "tot_len_bwd_pkts": 0, "fwd_pkt_len_std": 0, "bwd_pkt_len_std": 0, "fwd_pkt_len_max": 0,
                    "fwd_pkt_len_min": 0, "bwd_pkt_len_max": 0, "bwd_pkt_len_min": 0, "fwd_pkt_len_mean": 0,
                    "bwd_pkt_len_mean": 0}

        # calculate min, max and mean packet lengths
        for p in ps:
            if 'IP' in p:
                if fwdip == '':
                    fwdip = p['IP'].src

                if p['IP'].src == fwdip:
                    if features["num_fwd_pkts"] == 0:
                        features["fwd_pkt_len_max"] = features["fwd_pkt_len_min"] = len(p)

                    # count total packets seen and total length so we can calculate mean and std
                    features["num_fwd_pkts"] += 1
                    features["tot_len_fwd_pkts"] += len(p)
                    # find max and min fwd packet lengths
                    if len(p) > features["fwd_pkt_len_max"]:
                        features["fwd_pkt_len_max"] = len(p)
                    if len(p) < features["fwd_pkt_len_min"]:
                        features["fwd_pkt_len_min"] = len(p)

                else:
                    if features["num_bwd_pkts"] == 0:
                        features["bwd_pkt_len_max"] = features["bwd_pkt_len_min"] = len(p)

                    # count total packets seen and total length so we can calculate mean and std
                    features["num_bwd_pkts"] += 1
                    features["tot_len_bwd_pkts"] += len(p)
                    # find max and min bwd packet lengths
                    if len(p) > features["bwd_pkt_len_max"]:
                        features["bwd_pkt_len_max"] = len(p)
                    if len(p) < features["bwd_pkt_len_min"]:
                        features["bwd_pkt_len_min"] = len(p)

        if features["num_fwd_pkts"] > 0:
            features["fwd_pkt_len_mean"] = features["tot_len_fwd_pkts"] / features["num_fwd_pkts"]
        else:
            features["fwd_pkt_len_mean"] = 0
        if features["num_bwd_pkts"] > 0:
            features["bwd_pkt_len_mean"] = features["tot_len_bwd_pkts"] / features["num_bwd_pkts"]
        else:
            features["bwd_pkt_len_mean"] = 0

        # calculate std deviation in packet lengths
        for p in ps:
            if 'IP' in p:
                if p['IP'].src == fwdip:
                    features["fwd_pkt_len_std"] += ((len(p) - features["fwd_pkt_len_mean"]) ** 2)
                else:
                    features["bwd_pkt_len_std"] += ((len(p) - features["bwd_pkt_len_mean"]) ** 2)
        if features["num_fwd_pkts"] > 0:
            features["fwd_pkt_len_std"] = math.sqrt(features["fwd_pkt_len_std"] / features["num_fwd_pkts"])
        else:
            features["fwd_pkt_len_std"] = 0
        if features["num_bwd_pkts"] > 0:
            features["bwd_pkt_len_std"] = math.sqrt(features["bwd_pkt_len_std"] / features["num_bwd_pkts"])
        else:
            features["bwd_pkt_len_std"] = 0

        # find all the individual stuff + output to file
        for p in ps:
            features['timestamp'] = time.strftime("%d/%m/%y %H:%M:%S", time.gmtime(p.sent_time))
            if 'IP' in p:
                features["srcip"] = p['IP'].src
                features["dstip"] = p['IP'].dst
                features["proto"] = p['IP'].proto
                if 'TCP' in p:
                    features["sport"] = p['TCP'].sport
                    features["dport"] = p['TCP'].dport

                elif 'UDP' in p:
                    features["sport"] = p['UDP'].sport
                    features["dport"] = p['UDP'].dport

            write_data = ""
            for key in features.keys():
                if key in ["num_fwd_pkts", "num_bwd_pkts", "tot_len_fwd_pkts", "tot_len_bwd_pkts"]:
                    continue
                else:
                    write_data = write_data + ',' + str(features[key])
            fout.write(write_data[1:] + '\n')
    fout.close()
