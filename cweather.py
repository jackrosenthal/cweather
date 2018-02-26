#!/usr/bin/python3
import requests
import argparse
import sys
import os
__version__ = '0.0.1'

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--api-key',
        type=str,
        # I have no idea whose API key this is... but I've used it for
        # a long time and it has not failed me (yet)
        # ... perhaps if you are a reasonable person you will get your
        #     own key and use that
        default=os.getenv('WUNDERGROUND_API_KEY') or 'e4766f93abf302cd'[::-1],
        help="Wunderground API key, defaults to WUNDERGROUND_API_KEY "
             "in your environment, or some random one that might work "
             "if unset")
    parser.add_argument('--timeout',
        type=float, default=1.5,
        help="Timeout for connection")
    parser.add_argument('--no-color',
        action="store_true", default=(os.getenv("TERM") == 'vt100'),
        help="No colors, default if TERM is vt100")
    parser.add_argument('location',
        type=str,
        nargs='?',
        # Golden is a pretty reasonable deafult.
        default=(os.getenv('LOCATION') or '80401'),
        help="Location or postal code, defaults to LOCATION environment "
             "variable, or 80401 (Golden, CO) if unset")
    args = parser.parse_args()

    try:
        r = requests.get(
            'http://api.wunderground.com/api/{}/conditions/q/{}.json'
            .format(args.api_key, args.location),
            timeout=args.timeout)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    if not r.ok:
        print(
            "Something went wrong! Got status {}.".format(r.status_code),
            file=sys.stderr)
        sys.exit(1)

    obs = r.json().get('current_observation')
    if not obs:
        print("I don't know where that is!", file=sys.stderr)
        sys.exit(2)

    colors = {
        # (Background, Foreground)
        'Clear': (44, 33),
        'Scattered Clouds': (44, 37),
        'Partly Cloudy': (47, 34),
        'Mostly Cloudy': (47, 90),
        'Overcast': (100, 37),
    }

    # nasty formatting stuff follows!
    c = ("\033[{}m" * 2).format(*colors.get(obs['weather'], (0, 0)))
    if args.no_color:
        c = ""
    print(c, "Weather for \033[4m{:<31} \033[0m".format(obs['display_location']['full'] + '\033[24m:'))
    print(c, "  Conditions: \033[1m{:>24} \033[0m".format(obs['weather']))
    print(c, "  Temperature: \033[1m{:>23} \033[0m".format(obs['temperature_string']))
    print(c, "  Feels Like: \033[1m{:>24} \033[0m".format(obs['feelslike_string']))
    wind, p, gust = obs['wind_string'].partition(' Gusting')
    print(c, "  Wind: \033[1m{:>30} \033[0m".format(wind))
    if p:
        print(c, "\033[1m{:>38} \033[0m".format(p + gust))

if __name__ == '__main__':
    main()
