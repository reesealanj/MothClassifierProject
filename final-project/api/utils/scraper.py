# Web scraper to collect images from Discover Life
import argparse
from bs4 import BeautifulSoup, SoupStrainer
from conditional import conditional
from datetime import datetime
import getpass
import io
from interruptingcow import timeout
import logging
import multiprocessing as mp
import os
from PIL import Image
import platform
import re
import requests
import sys
from tqdm import tqdm
import tempfile
import urllib3

from api_keys import AUTH_KEY
from constants import API_URL, AUTH_URL, DISCOVER_LIFE_URL, IMAGE_ROOT


ALBUM_URL = f'{DISCOVER_LIFE_URL}/mp/20p?edit='
SPECIES_URL = f'{DISCOVER_LIFE_URL}/moth/data/table2_33.9_-83.3.html'
SPECIES_LIST_FILE = 'species_list.txt'

FIELD_MAP = {
    'title': 'db_field0',
    'country': 'db_field15',
    'region': 'db_field16',
    'county': 'db_field17',
    'city': 'db_field18',
    'street': 'db_field19',
    'lat': 'db_field21',
    'lng': 'db_field22',
}
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

VALID_RES = [80, 120, 240, 320, 640]
UNKNOWNS = [
    'moth',
]

TIMEOUT = 30

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
fh = logging.FileHandler('scraper.log')
fh.setLevel(logging.ERROR)
logger.addHandler(fh)


class ScrapeMultiProcessHandler:
    """
    A class used to handle the tasks related to multi-processing

    Attributes
    ----------
    num_processes : int
        The number of processes to create

    Methods
    -------
    handle(email, album, **kwargs)
        Creates all the processes and handles tasks relating to them
    monitor_progress(progress_bar)
        Updates the progress of the progress bar for all the processes
    increment_counter()
        Increments the progress bar counter
    """

    def __init__(self, num_processes):
        """
        Parameters
        ----------
        num_processes : int
            The number of processes to create
        """

        self.num_processes = num_processes
        self.counter = mp.Value('i', 0)
        self.cond = mp.Condition()

    def handle(self, email, password, album, start=1, end=1, step=1, res=240):
        """
        Creates all the processes and handles tasks relating to them

        Parameters
        ----------
        email\ : str
            The email of the user who is posting these images to the Moth Classifier API
        album : str
            The album that holds all the photos to be scraped
        **kwargs : dict
            Keyword arguments for optional parameters to the post_images() method
        """

        progress_bar = tqdm(range(start, end + 1), ncols=100, leave=True)

        # Create all the processes and have them execute post_images()
        process_list = []
        for i in range(self.num_processes):
            process_list.append(
                mp.Process(
                    target=post_images,
                    args=(email, password, album),
                    kwargs={
                        'start': start + i,
                        'end': end,
                        'step': self.num_processes,
                        'res': res,
                        'handler': self,
                    },
                )
            )

        # Run the processes
        for process in process_list:
            process.start()

        self.monitor_progress(progress_bar)

        # End the processes
        for process in process_list:
            process.join()

    def monitor_progress(self, progress_bar):
        """
        Updates the progress of the progress bar

        Parameters
        ----------
        progress_bar : object
            A tqdm.tqdm() object that represents the progress bar
        """

        prev = 0
        self.cond.acquire()
        while self.counter.value <= progress_bar.total:
            if self.counter.value > prev:
                progress_bar.update(self.counter.value - prev)
                prev = self.counter.value

            if self.counter.value == progress_bar.total:
                break

            self.cond.wait()
        self.cond.release()

    def increment_counter(self):
        """
        Increments the progress bar counter
        """

        self.cond.acquire()
        self.counter.value += 1
        self.cond.notify()
        self.cond.release()


def log_image_fail(image):
    """
    Logs images that fail to upload to the Moth Classifier API

    Parameters
    ----------
    image: str
        The image that failed to upload
    """

    logger.error(f'ERROR: {datetime.now().strftime("%m/%d/%Y %H:%M:%S")} {image}')


def user_auth(session, email, password):
    """
    Authorizes the user and retrieves his/her uid and authorization token

    Parameters
    ----------
    session: object
        The current Session() object from the requests module
    email: str
        The user's email
    password: str
        The user's password

    Raises
    ------
    requests.exceptions.HTTPError
        If the authorization fails due to invalid credentials

    Returns
    -------
    tuple
        A tuple of the user's id and authorization token
    """

    auth_data = {
        'email': email,
        'password': password,
        'returnSecureToken': True,
    }
    r = session.post(f'{AUTH_URL}?key={AUTH_KEY}', data=auth_data)

    if r.status_code != 200:
        r.raise_for_status()

    data = r.json()

    return data.get('localId'), data.get('idToken')


def request_species():
    """
    Scrapes the Discover Life website for a list of moth species
    """

    # Get the data from the web page
    page = requests.get(SPECIES_URL, headers=HEADERS, verify=False)
    species = BeautifulSoup(
        page.content,
        'html.parser',
        parse_only=SoupStrainer('a', href=re.compile(r'search=[A-z]+')),
    )

    # Write the species names into a text file
    # Create a folder for each species if one does not exist
    with open(SPECIES_LIST_FILE, 'w') as outfile:
        for item in species:
            name = item.text.strip()
            if not name:  # Skip if name is just whitespace
                continue

            outfile.write(f'{name}\n')


def post_images(email, password, album, start=1, end=1, step=1, res=240, handler=None):
    """
    Scrapes the Discover Life website for pictures in the specified album
    and then uploads them to the Moth Classifier API

    mp is optional with this function

    Parameters
    ---------
    email : str
        The email of the user who is posting these images to the Moth Classifier API
    album : str
        The album that holds all the photos to be scraped
    start : int, optional
        The index (inclusive) of the first picture to be scraped in the album (default is 1)
    end : int, optional
        The index (inclusive) of the last picture to be scraped in the album (default is 1)
    step : int, optional
        The step size for the iteration (default is 1)
    res : int, optional
        The resolution of the picture which must be a valid resolution in the album (default is 240)
    handler : object, optional
        The ScrapeMultiProcessHandler that is handling this method (default is None).
        Can be None if the method is not being multi-processed
    """

    # Validate function arguments
    if (
        start < 1
        or end < 1
        or step < 1
        or res not in VALID_RES
        or not email
        or not album
        or handler is not None
        and not isinstance(handler, ScrapeMultiProcessHandler)
    ):
        raise ValueError

    session = requests.Session()
    session.headers.update(HEADERS)

    # Attempt to authorize the user
    uid, token = user_auth(session, email, password)

    # Get the user from the Moth Classifier API
    r = session.get(
        f'{API_URL}/users/{uid}/', headers={'Authorization': f'Bearer {token}'}
    )

    user = r.json()

    with open(SPECIES_LIST_FILE, 'r') as infile:
        species = [line.strip() for line in infile if line.strip() != '']

    # Scrape the data for each image
    for i in range(start, end + 1, step):
        try:
            # The interruptingcow module does not work on Windows
            with conditional(
                platform.system() != 'Windows', timeout(TIMEOUT, exception=RuntimeError)
            ):
                page = session.get(f'{ALBUM_URL}{album}{i}', verify=False)
                soup = BeautifulSoup(page.content, 'html.parser')

                # Find the HTML fields that contain the relevant data for the Moth Classifier API
                data = soup.find_all('input', attrs={'name': FIELD_MAP.values()})
                image_data = soup.find('img', src=re.compile(f'img={album}'))

                # Quiety fail
                if image_data is None or data is None:
                    log_image_fail(f'{album}{i} -- NO DATA FOUND')
                    handler.increment_counter()
                    continue

                # Build the image url
                image_url = DISCOVER_LIFE_URL + re.sub(
                    'res=[0-9]+', f'res={res}', image_data.get('src')
                )

                data_dict = {}
                for item, key in zip(data, FIELD_MAP.keys()):
                    data_dict[key] = item.get('value')

                # Only get the species names from the title field
                idx = data_dict['title'].find(',')
                if idx > 0:
                    data_dict['title'] = data_dict['title'][:idx]

                # Check to see if the title corresponds to a valid moth species
                # If the title is valid, upload the picture to the Moth Classifier API
                if data_dict['title'] in species or data_dict['title'] in UNKNOWNS:
                    data_dict['is_training'] = data_dict['title'] in species
                    r = session.get(image_url, verify=False)

                    # Write the image on the Discover Life website into a temp file
                    with tempfile.NamedTemporaryFile(
                        prefix=f'{album}{i}-', suffix='.jpg'
                    ) as temp:
                        temp.write(r.content)
                        temp.flush()

                        width, height = Image.open(temp).size
                        data_dict['width'] = width
                        data_dict['height'] = height
                        temp.seek(0)

                        r = session.post(
                            user.get('images'),
                            data=data_dict,
                            files={'file': temp},
                            headers={'Authorization': f'Bearer {token}'},
                        )

                    if r.status_code == 401:  # Reauthorize the user and try again
                        uid, token = user_auth(session, email, password)
                        r = session.post(
                            user.get('images'),
                            data=data_dict,
                            files={'file': temp},
                            headers={'Authorization': f'Bearer {token}'},
                        )
                    elif r.status_code != 201:
                        log_image_fail(f'{album}{i} -- UNABLE TO UPLOAD')
                        handler.increment_counter()
                        continue

                    image_json = r.json()

                    # Upload the classification for this picture if there is one
                    if data_dict['title'] in species:
                        classification = {
                            'species': data_dict['title'],
                            'accuracy': 100.00,
                            'is_automated': False,  # Manual classification by Discover Life researcher
                        }

                        r = session.put(
                            image_json.get('classification'),
                            data=classification,
                            headers={'Authorization': f'Bearer {token}'},
                        )

                        if r.status_code == 401:  # Reauthorize the user and try again
                            uid, token = user_auth(session, email, password)
                            r = session.put(
                                image_json.get('classification'),
                                data=classification,
                                headers={'Authorization': f'Bearer {token}'},
                            )

                handler.increment_counter()
        except RuntimeError:
            log_image_fail(f'{album}{i} -- TIMED OUT')
            handler.increment_counter()
        except KeyboardInterrupt:
            pass
        except:  # Try again if an error occurs
            i -= 1


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    # Create a command line argument parser for this web scraper
    parser = argparse.ArgumentParser(description='Discover Life web scraper')
    parser.add_argument(
        '-u',
        '--email',
        required='--request-species' not in sys.argv,
        help='Email for Moth Classifier API (Required if --request-species is not specified)',
    )
    parser.add_argument(
        '-p',
        '--password',
        help='Password for Moth Classifier API. If not specified, a prompt will appear. (Required if --request-species is not specified)',
    )
    parser.add_argument(
        '--album',
        required='--request-species' not in sys.argv,
        help='Album on Discover Life to scrape (Required if --request-species is not specified)',
    )
    parser.add_argument(
        '--range',
        help='Range of images to search in the album',
        nargs=2,
        type=int,
        default=[1, 1],
    )
    parser.add_argument(
        '--res',
        help='Resolution of image to scrape',
        dest='res',
        choices=VALID_RES,
        default=240,
    )
    parser.add_argument(
        '--cpus',
        help='Number of CPUs to use for this utility. -1 permits all cores to be used',
        dest='cpus',
        choices=[-1] + [i for i in range(1, os.cpu_count() + 1)],
        type=int,
        default=-1,
    )
    parser.add_argument(
        '--request-species',
        help='Scrapes the Discover Life website for a list of moth species',
        action='store_true',
    )

    args = parser.parse_args()

    if args.request_species:
        request_species()
    else:
        # Request password if not specified
        if not args.password:
            args.password = getpass.getpass()

        # Validate user credentials
        user_auth(requests.Session(), args.email, args.password)

        # Multi-process post_images
        if args.cpus == -1:
            args.cpus = os.cpu_count()

        handler = ScrapeMultiProcessHandler(args.cpus)
        handler.handle(
            args.email,
            args.password,
            args.album,
            start=args.range[0],
            end=args.range[1],
            res=args.res,
        )


if __name__ == '__main__':
    main()
