import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--chennelid', type=str, help='The channel ID')
    parser.add_argument('-k', 'key', type=str, help='API key')
    args = parser.parse_args()


if __name__ == '__main__':
    main()
