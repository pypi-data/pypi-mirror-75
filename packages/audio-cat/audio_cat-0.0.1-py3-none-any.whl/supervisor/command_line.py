import argparse 
import sys

from .utils import download_youtube_audio, dataset_from_segments


def main():

    parser = argparse.ArgumentParser(prog='audio-cat', 
        description ='manipulate audio.', 
        usage='%(prog)s [command]', 
        epilog='read the docs!', 
        allow_abbrev=False,
        add_help=True)

    parser.version= '0.0.1'


    subparsers = parser.add_subparsers(help='commands')

    dl_parser = subparsers.add_parser('download', help='download audio from youtube')
    dl_parser.add_argument('url', action='store', help='youtube video url')
    dl_parser.add_argument('title', action='store', help='stored title')
    dl_parser.add_argument('--des', action='store', help='destination default=audio', default='audio')
    dl_parser.add_argument('--split', action='store', help='split interval default=2500', type=int, default=2500)
    dl_parser.add_argument('--blurb', action='store', help='full audio storage default=FULL_AUDIO', default="FULL_AUDIO")
    dl_parser.add_argument('--dataset', action='store_true', help='create dataset for samples')
    dl_parser.add_argument('--dry', action='store_true', help='dry run to be used in debugging')


    ds_parser = subparsers.add_parser('dataset', help='create dataset from segments')
    ds_parser.add_argument('path', action='store', help='path to directory containing segments')
    ds_parser.add_argument('title', action='store', help='desired title of dataset')
    ds_parser.add_argument('--des', action='store', help='directory for datasets, will be created if non-existent default=datasets', default='datasets')
    ds_parser.add_argument('--dry', action='store_true', help='dry run to be used in debugging')



    parser.add_argument("--version", action='version', help="display program version")

    #quit if no args
    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    #parse args
    args = parser.parse_args()


    #dry run
    if args.dry is False:


        #download from youtube
        if sys.argv[1] == 'download':
            path = download_youtube_audio(url=args.url,
                                        title=args.title,
                                        destination=args.des,
                                        split=args.split,
                                        blurb=args.blurb)
            print(path)

            #creating dataset
            if args.dataset and args.split > 0:
                print(dataset_from_segments(path=path,
                                            title=args.title))


        if sys.argv[1] == 'dataset':
            print(dataset_from_segments(path=args.path,
                                        title=args.title,
                                        destination=args.des))


    else:
        print(args, "DRY")
