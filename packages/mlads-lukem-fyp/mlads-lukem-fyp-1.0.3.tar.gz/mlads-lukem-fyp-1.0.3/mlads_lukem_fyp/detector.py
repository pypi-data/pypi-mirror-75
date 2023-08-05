#!/usr/bin/env python

# Machine learning imports
from sklearn.metrics import confusion_matrix
import numpy as np
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
# Alerting imports
import urllib.request
import urllib.parse
import smtplib
# Other imports
from mlads_lukem_fyp.databaser import Databaser
from mlads_lukem_fyp import feature_extraction
import pickle
import os.path
from os.path import split, dirname, abspath, join


HOME = split(dirname(__file__))[0]
CSVDIR = abspath(join(HOME, 'csvs'))
SAVEDIR = abspath(join(HOME, 'model'))
DBDIR = abspath(join(HOME, 'sqlite'))
CONFIG_FILE = abspath(join(HOME, 'mlads.cfg'))
README_FILE = abspath(join(HOME, 'README.txt'))


def calc_results(tp, fp, tn, fn):
    """Calculate the scores of a machine learning algorithm.

    Based on the input parameters calculate the TPR, FPR, Overall Success Rate, Precision and F-Score.

    Parameters
    ----------
    tp : int
        The total number of true positives the algorithm produced
    fp : int
        The total number of false positives the algorithm produced
    tn : int
        The total number of true negatives the algorithm produced
    fn : int
        The total number of false negatives the algorithm produced
    """
    tpr = float(tp / (tp + fn)) * 100
    fpr = float(fp / (fp + tn)) * 100
    osr = float((tp + tn) / (tp + tn + fp + fn)) * 100
    prec = float(tp / (tp + fp)) * 100
    fscore = float((2 * prec * tpr) / (prec + tpr))

    return tpr, fpr, osr, prec, fscore


def read_csv(fname):
    """Read a CSV into a Numpy array.

    Parameters
    ----------
    fname : str
        The name of the file to be read
    """
    x = []

    if CSVDIR not in fname:
        fname = abspath(join(CSVDIR, fname))

    try:
        with open(fname, "r") as f:
            for line in f.readlines():
                data = line[:-1].split(",")
                x.append(data)
    except FileNotFoundError as err:
        print(err)

    x = np.array(x)
    return x


def pcap_to_csv(inpcap):
    """Convert a PCAP to a CSV.

    Convert a PCAP file to a CSV file and put them in the correct corresponding folders in the project directory.

    Parameters
    ----------
    inpcap : str
        The name/location of the file to be converted
    """
    outcsv = join(CSVDIR, split(inpcap)[-1].split('.')[0] + ".csv")  #  inpcap.split("/")[-1].split(".")[0]  # change the extension
    feature_extraction.convert(inpcap, outcsv)


class Detector:
    """A class used to interact with the machine learning algorithm.

    Attributes
    ----------
    db : databaser.Databaser
        A Databaser object to interact with the database
    classifier : sklearn.multiclass.OneVsOneClassifier
        The machine learning algorithm object
    label_encoder : [sklearn.preprocessing.LabelEncoder]
        A list of label encoder objects to encode and decode datasets
    model_file : str
        Location of the model when pickled
    le_file : str
        Location of the label encoder when pickled
    apikey : str
        API key used for SMS alerts
    username : str
        Username used for email alerts
    password : str
        Password used for email alerts
    knum : int
        Number of neighbours for KNN to utilise
    weights : str
        Weighting for KNN to utilise
    db_file : str
        The file in which the database is stored
    send_email_alerts : bool
        True or false depending on if emails can be sent with credentials in configuration file
    send_sms_alerts : bool
        True or false depending on if SMS can be sent with credentials in configuration file

    Methods
    -------
    __init__(model_file, label_encoder_file, train_data_file)
        Define initial values for various class attributes.
    train(x_train, y_train)
        Train the machine learning algorithm.
    cross_validate(x_test, y_test)
        Test the machine learning algorithm is well trained.
    predict(x)
        Make predictions for a given dataset.
    save(mod_file=None, le_file=None)
        Save model and label encoder objects.
    load(mod_file=None, le_file=None)
        Load model and label encoder objects.
    train_label_encoder(train_data_file)
        Train the label encoder.
    encode_data(input_data)
        Encode input datasets.
    decode_data(input_data_encoded, y_pred)
        Decode input datasets.
    generate_alert(x)
        Generate the message to be sent to contacts.
    get_contact()
        Get contact information from the database.
    read_config()
        Read the configuration file.
    send_sms(numbers, sender, message)
        Send SMS alerts.
    send_email(sender, recipients, subject, body)
        Send Email alerts.
    """

    def __init__(self, model_file=join(SAVEDIR, "mlads_model.sav"),
                 label_encoder_file=join(SAVEDIR, "mlads_label_encoder.sav"),
                 train_data_file=join(CSVDIR, "Xample_Training_Data.csv")):
        """Define initial values for various class attributes.

        Define the database object, attempt to load an existing trained algorithm, otherwise create and train a new one.

        Parameters
        ----------
        model_file : str
            Location of an existing model
        label_encoder_file : str
            Location of an existing label encoder
        train_data_file : str, None
            Location of training data"""
        # Read config settings
        self.apikey = None
        self.username = None
        self.password = None
        self.knum = None
        self.weights = None
        self.db_file = None
        self.send_email_alerts = False
        self.send_sms_alerts = False
        self.read_config()

        if self.db_file is None:
            self.db = Databaser()
        else:
            self.db = Databaser(self.db_file)
        self.classifier = None
        self.label_encoder = None
        self.model_file = model_file
        self.le_file = label_encoder_file

        # Attempt to load existing model and label encoder
        self.load(self.model_file, self.le_file)
        # If the classifier or label encoder didn't load and there is training data, create a new model
        if (self.classifier is None or self.label_encoder is None) and train_data_file is not None:
            # self.classifier = OneVsOneClassifier(LinearSVC(random_state=0, dual=False, max_iter=7500))
            self.classifier = KNeighborsClassifier(algorithm='auto', n_neighbors=self.knum, weights=self.weights,
                                                   n_jobs=-1)
            # Train the label encoder
            x, y = self.train_label_encoder(train_data_file)
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=5)
            # Train the model
            self.train(x_train, y_train)
            # print(self.cross_validate(x_test, y_test)
            self.save(self.model_file, self.le_file)
        # If there is no model/label encoder and no training data, exit the program
        elif (self.classifier is None or self.label_encoder is None) and train_data_file is None:
            # No save file, and no training data
            print("No model to load and no data to train on... Exiting...")
            exit()

    def train(self, x_train, y_train):
        """Train the machine learning algorithm.

        Parameters
        ----------
        x_train : numpy.array
            Data for the machine learning algorithm to use
        y_train : numpy.array
            The correct results for x_train data
        """
        self.classifier.fit(x_train, y_train)

    def cross_validate(self, x_test, y_test):
        """Test the machine learning algorithm is well trained.

        Make predictions on test data, compare this to correct results and then calculate TP, FP, TN and FN values.

        Parameters
        ----------
        x_test : numpy.array
            Data for the machine learning algorithm to use
        y_test : numpy.array
            The correct results for x_test data
        """
        # Make predictions for the test data
        y_pred = self.classifier.predict(x_test)

        # Compute TP, FP, TN and FN values
        tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
        # Before returning, calculate FPR, TPR, OSR, Precision and F-Score
        return calc_results(tp, fp, tn, fn)

    def predict(self, x):
        """Make predictions for a given dataset.

        Encode the dataset, give it to the machine learning algorithm, decide the result and generate an alert.

        Parameters
        ----------
        x : numpy.array
            The dataset on which predictions are to be made
        """
        x_enc = self.encode_data(x)
        y_pred = self.classifier.predict(x_enc)
        x_dec = self.decode_data(x_enc, y_pred)
        self.generate_alert(x_dec)

    def save(self, mod_file=None, le_file=None):
        """Save model and label encoder objects.

        Pickle the model and label encoder objects and then dump to files.

        Parameters
        ----------
        mod_file : str, None
            The name of the file to dump the model to
        le_file : str, None
            The name of the file to dump the label encoder to
        """
        if mod_file is not None:
            try:
                # Open the file in binary write mode (create if doesn't exist) and dump the model object
                model_pickle_out = open(mod_file, 'wb')
                pickle.dump(self.classifier, model_pickle_out)
                model_pickle_out.close()
            except IOError as e:
                print(e)
        if le_file is not None:
            try:
                # Open the file in binary write mode (create if doesn't exist) and dump the label encoder object
                le_pickle_out = open(le_file, 'wb')
                pickle.dump(self.label_encoder, le_pickle_out)
                le_pickle_out.close()
            except IOError as e:
                print(e)

    def load(self, mod_file=None, le_file=None):
        """Load model and label encoder objects.

        Load the pickled model and label encoder objects from files.

        Parameters
        ----------
        mod_file : str, None
            The name of the file to read from to fill the model object
        le_file : str, None
            The name of the file to read from to fill the label encoder object
        """
        if mod_file is not None and os.path.exists(mod_file):
            try:
                # Open the file in binary read mode and set the model equal to this pickled object
                loaded_model = pickle.load(open(mod_file, 'rb'))
                self.classifier = loaded_model
            except IOError as e:
                print(e)
        if le_file is not None and os.path.exists(le_file):
            try:
                # Open the file in binary read mode and set the label encoder equal to this pickled object
                label_encoder = pickle.load(open(le_file, 'rb'))
                self.label_encoder = label_encoder
            except IOError as e:
                print(e)

    def train_label_encoder(self, train_data_file):
        """Train the label encoder.

        Given a training data file, teach the label encoder how to encode each value it sees.

        Parameters
        ----------
        train_data_file : str
            Filename of the data file
        """
        x = []
        count_ddos = 0
        count_benign = 0
        max_datapoints = 3000  # Maximum 3000 data points each of benign and ddos - 6000 total

        # Read the file
        try:
            with open(train_data_file, "r") as f:
                for line in f.readlines():
                    # If we exceed the maximum, break
                    if count_ddos >= max_datapoints and count_benign >= max_datapoints:
                        break
                    # Add the data to x and increase counts
                    data = line[:-1].split(",")
                    if data[-1] != "BENIGN" and count_ddos < max_datapoints:
                        x.append(data)
                        count_ddos += 1
                    if data[-1] == "BENIGN" and count_benign < max_datapoints:
                        x.append(data)
                        count_benign += 1
        except IOError as err:
            print(err)
            print("No training data")

        x = np.array(x)
        # Train the label encoders
        self.label_encoder = []
        x_encoded = np.empty(x.shape)
        for i, item in enumerate(x[0]):
            # A new label encoder for each column
            self.label_encoder.append(preprocessing.LabelEncoder())
            x_encoded[:, i] = self.label_encoder[-1].fit_transform(x[:, i])

        # Convert encoded values to integers
        x = x_encoded[:, :-1].astype(int)
        y = x_encoded[:, -1].astype(int)
        return x, y

    def encode_data(self, input_data):
        """Encode input datasets.

        Given a dataset, encode it using the label encoder.

        Parameters
        ----------
        input_data : numpy.array
            An array of data points
        """
        fit_altered = False  # In case we encounter new values we haven't seen before
        input_data = np.array(input_data)  # Make sure it is indeed a numpy array
        input_data_encoded = np.empty(input_data.shape)  # To store the encoded values in

        for i in range(len(input_data[0])):
            try:
                # Try just encoding the values
                input_data_encoded[:, i] = self.label_encoder[i].transform(input_data[:, i])
            except ValueError:  # as e:
                # If that doesn't work, fit the label encoder to the new values
                input_data_encoded[:, i] = self.label_encoder[i].fit_transform(input_data[:, i])
                fit_altered = True
                # print(e)

        # If we had to adjust the fit, save the label encoder
        if fit_altered:
            self.save(le_file=self.le_file)

        input_data_encoded = input_data_encoded[:, :].astype(int)
        return input_data_encoded

    def decode_data(self, input_data_encoded, y_pred):
        """Decode input datasets.

        Given a dataset and a set of predictions, decode using the label encoder.

        Parameters
        ----------
        input_data_encoded : numpy.array
            An array of encoded data points
        y_pred : numpy.array
            The predicted values given by the machine
        """
        decoded_data = np.ndarray(input_data_encoded.shape)  # Empty array the size of input_data_encoded
        decoded_data_y = [[None]] * len(input_data_encoded)  # Empty array the size of y_pred
        decoded_data = np.append(decoded_data, decoded_data_y, axis=1)  # Combine the two

        for i in range(len(input_data_encoded[0])):
            decoded_data[:, i] = self.label_encoder[i].inverse_transform(input_data_encoded[:, i])
        decoded_data[:, -1] = self.label_encoder[-1].inverse_transform(y_pred[:])

        return decoded_data

    def generate_alert(self, x):
        """Generate the message to be sent to contacts.

        Given a decoded dataset including predictions, input values into the database and send an alert.

        Parameters
        ----------
        x : numpy.array
            A decoded dataset including predictions
        """
        to_email, to_phone = self.get_contact()  # Grab contact info from the database
        message = "The following Flow IDs have been detected as malicious:\n\n"
        sender = 'MLADS Alerts'
        subject = 'Alert Received'

        # We only want 1 alert for each malicious flow id
        for item in x:
            # If malicious and same flow id isn't already in the malicious list, add it
            if item[-1].lower() != 'benign' and item[0] not in message:
                # insert to alerts table in database - the [1] is to insert group 1 as the alerted group
                item = list([1]) + list(item)
                self.db.insert_row('alerts', item)
                # add the flow id to the message
                message += str(item[1]) + '\n'

        message += '\nMLADS'
        # Send the alerts
        if self.send_sms_alerts:
            for number in to_phone:
                self.send_sms(number, sender, message)
        if self.send_email_alerts:
            self.send_email(sender, to_email, subject, message)

    def get_contact(self):
        """Get contact information from the database.

        Get the email addresses, phone numbers and contact IDs of each contact the should be alerted."""
        # Search the database for each contact that should be alerted
        data = self.db.get_alertable_contacts()
        to_email, to_phone = [], []

        if data is not None:
            # Format the database results into the corresponding array
            for i, (email, phone) in enumerate(data):
                to_email.append(email)
                to_phone.append(phone)
        else:
            self.send_email_alerts = False
            self.send_sms_alerts = False

        return to_email, to_phone

    def read_config(self):
        """Read the configuration file.

        Read usernames, passwords, KNN configs and other data from config files."""
        try:
            with open(CONFIG_FILE, 'r') as f:
                for line in f.readlines():
                    if line.startswith('#'):  # skip comments
                        continue
                    if 'username' in line:
                        self.username = line.split("=")[1].strip()
                    if 'password' in line:
                        self.password = line.split("=")[1].strip()
                    if 'api' in line:
                        self.apikey = line.split("=")[1].strip()
                    if 'neighbour' in line:
                        self.knum = line.split("=")[1].strip()
                    if 'weight' in line:
                        self.weights = line.split("=")[1].strip()
                    if 'database' in line:
                        self.db_file = join(DBDIR, line.split("=")[1].strip())
        except FileNotFoundError as err:
            print(err)
            print('Configuration file error')

        if self.knum is None or not self.knum.isdigit():
            self.knum = 5
        else:
            self.knum = int(self.knum)
        if self.weights is None:
            self.weights = 'uniform'
        if self.username is not None and self.password is not None:
            self.send_email_alerts = True
        if self.apikey is not None:
            self.send_sms_alerts = True

    def send_sms(self, numbers, sender, message):
        """Send SMS alerts.

        Send SMS alerts with a predefined message to predefined mobile numbers using an online API.

        Parameters
        ----------
        numbers : str
            A string containing the mobile phone number
        sender : str
            The name of the sender of the message
        message : str
            The message to be sent in the SMS
        """
        # Function to send SMS alerts. Communicates with the API at www.textlocal.com (requires internet connection)
        data = urllib.parse.urlencode({'apikey': self.apikey, 'numbers': numbers,
                                       'message': message, 'sender': sender, })  # 'test': True})
        data = data.encode('utf-8')
        # Using www.textlocal.com API for sending SMS alerts from the Machine Learning Anomaly Detection System (MLADS).
        request = urllib.request.Request("https://api.txtlocal.com/send/?")
        f = urllib.request.urlopen(request, data)  # Form and send the complete POST request
        fr = f.read()
        return fr

    def send_email(self, sender, recipients, subject, body):
        """Send Email alerts.

        Send Email alerts with a predefined message to predefined email addresses using Google's SMTP services.

        Parameters
        ----------
        sender : str
            The name of the sender of the message
        recipients : [str]
            An array of strings containing Email addresses
        subject : str
            The subject of the Email
        body : str
            The message to be sent in the Email
        """
        # Format the email
        email_text = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (sender, ', '.join(recipients), subject, body)

        try:
            # Open connection to Google's SMTP server, login and send the email
            # This method requires the Google account has 'less secure app access' enabled
            with smtplib.SMTP_SSL('smtp.gmail.com') as server:
                server.login(self.username, self.password)
                server.sendmail(self.username, recipients, email_text)
                server.close()
        except smtplib.SMTPException as e:
            return e
