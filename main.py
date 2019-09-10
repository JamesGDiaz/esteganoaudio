import argparse
import esteganoacoustics


def main(*args):
    parser = argparse.ArgumentParser(
        description='Hide a message inside an audio file')
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('-r', '--read', action="store_true",
                      help="Read a message inside a file.")
    mode.add_argument('-w', '--write', action="store_true",
                      help="Write a message inside a file.")

    parser.add_argument("INPUT")
    parser.add_argument('-n', action="store", dest="msgLen", type=int,
                        help="Specify the size of the message to be read. If not specified, will read the entire file and a lot of gibberish might be read too.")
    parser.add_argument('-sr', '--sample-rate', action="store", dest="sr",
                        type=int, help="""Specify desired sample rate of the encoding. If not specified, an automatic value will be used.
                                          If this exceeds the maximum allowed, the program will fail.""")
    input_from = parser.add_mutually_exclusive_group()
    input_from.add_argument('-f', '--read-from-file', action="store", default=None,
                            dest="textfile", help="Read message from a plaintext file")
    input_from.add_argument("MESSAGE", nargs='?')
    parser.add_argument('-o', action="store", dest="oFile",  default=None,
                        help="Specify output filename without extension.")

    args = parser.parse_args()
    # print(args)
    if (args.write):
        if (args.MESSAGE is None and args.textfile is None):
            parser.error(
                "Write mode requires a MESSAGE or an text file to read the message from")
        print("Writing...")
        if (args.oFile is None):
            args.oFile = "output"
        if (args.textfile):
            with open(args.textfile, mode="r",encoding="utf8") as text:
                message = text.read()
                text.close()
                esteganoacoustics.write(
                    args.INPUT, message, args.sr, args.oFile)
        elif (args.MESSAGE):
            esteganoacoustics.write(
                args.INPUT, args.MESSAGE, args.sr, args.oFile)

    elif (args.read):
        print(f"Reading file {args.INPUT}")
        if (args.msgLen is None and args.sr is None):
            parser.error(
                "You must specify at least one of the secret message length or the sample rate of the encoded data.")
        esteganoacoustics.read(args.INPUT, args.sr,
                               args.msgLen, args.oFile)

    
if __name__ == "__main__":
    main()
    print("\n\n-// FI UNAM 2019 \\\\-")
