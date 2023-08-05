# Machine Learning for Anomaly Detection in Network Traffic
## A Final Year Project by Luke Morris

### An overview

I will be attempting to create a solution including machine learning to detect anomalies in a given dataset of network traffic. This will involve picking apart a PCAP provided by the user or using (wire|t)shark / tcpdump to read packets directly from the network to provide the machine learning algorithm with data. The ML algorithm will then be able to 'learn' normal traffic sequences. This enables the algorithm to determine when an anomaly is detected and thus alert the owner of the network.

This project will be in the form of:
* A final report including a literature review
* This software
* A portfolio including meeting minutes, CV and a self review

The software provided in this project contains a database, a machine learning algorithm trained to detect anomalies in a PCAP file, and a system to alert users.

### Installing the software

This software is available on PyPI as mlads_lukem_fyp and can be installed using pip:
```
pip install mlads_lukem_fyp
```
### Running the software

To run the software and begin detecting anomalies, run the MLADS.py file from the mlads_lukem_fyp directory.

Alternatively:
```
>>> from mlads_lukem_fyp.MLADS import start_mlads
>>> start_mlads()
```

### Using MLADS
#### View Alerts

The page used to view previous alerts or detections by the software. Alerts can be searched through using the fields at the top of the page.

When an alert is highlighted, further details on the alert can be viewed.

#### Analyse PCAPs

PCAP files can be 'uploaded' to the software. The file is fed through a feature extractor into a CSV that is then used by the machine learning algorithm.

Alerts are generated and sent via SMS and email. These alerts can also be viewed in the 'View Alerts' page.

This page runs very slowly when loading a large file, please be patient.

#### Edit Contacts

The contacts to be alerted when the software detects anomalies are kept up to date here, and contacts stored in a database.

#### Live Capture

Coming soon...