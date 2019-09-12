import scipy.io.wavfile as wavfile
import numpy as np
from unidecode import unidecode
from graph import plot2signals


def write(filename, message, selectedSampleRate=None, outputFilename="output"):
    """
    Write a hidden text message in an audio WAV file
    """

    fileSampleRate, wavData = wavfile.read(filename)
    origWavData = np.array(wavData)
    wavData = np.array(wavData)  # To be able to write this numpy array

    secretMessage = np.frombuffer(
        unidecode(message).encode(), dtype=np.uint8)

    # Sample rate to hide the message in
    DURATION = int(len(wavData)/fileSampleRate)  # [sec]
    MIN_SR = int(len(secretMessage)/DURATION)+1  # maximum sample rate in Hz
    if (selectedSampleRate is None):
        print("Detecting auto sample rate")
        selectedSampleRate = MIN_SR
    elif (selectedSampleRate < MIN_SR):
        print(
            f"Selected sample rate is lower than supported ({MIN_SR}Hz). Please specify a higher sample rate.")
        return
    elif(selectedSampleRate > fileSampleRate):
        print(f"The message you are trying to hide is too long for the audio file, please specify a shorter message or a long enough file")
        return
    elif(selectedSampleRate > (fileSampleRate/2)):
        ask_user("The message you are trying to hide is very long and \nthe audio might not be recognizable, do you wish to continue?")
    if(selectedSampleRate is 0):
        selectedSampleRate = 1
    print(f"""Finished reading {filename}
    Input audio sample rate: {fileSampleRate}Hz. File duration: {DURATION}s
    Need to encode {len(secretMessage):,} characters.
    Selected encoding sample rate is {selectedSampleRate}Hz""")

    PERIOD = int(fileSampleRate/selectedSampleRate)
    for i in range(len(secretMessage)):
        # print(i)
        wavData[(i+1)*PERIOD] = secretMessage[i]

    wavfile.write(outputFilename+'.wav', fileSampleRate, wavData)

    # Graph the signals
    t1 = 0
    t2 = 0.5
    start = int(t1 * 44100)
    end = int(t2 * 44100)
    rng = slice(start, end)
    s1 = origWavData[rng]
    s2 = wavData[rng]
    plot2signals(s1, s2, t1, t2)


def read(filename,  sampleRate=-1, msgLen=-1, output=None):
    """
    Search a file for hidden text messages
    """

    fileSampleRate, wavData = wavfile.read(filename)
    DURATION = int(len(wavData)/fileSampleRate)  # [sec]

    decodedStr = ''
    if (sampleRate and msgLen):
        MAX_LEN = int(DURATION * (sampleRate+1))
        MIN_SR = int(msgLen/DURATION)+1  # minimum sample rate in Hz
        PERIOD = int(fileSampleRate/sampleRate)
        if(MIN_SR is 0):
            MIN_SR = 1
        if (msgLen > MAX_LEN or sampleRate < MIN_SR):
            print("ERROR: Either the specified length of the message is too long, or the specified sample rate is too low for this operation.")
            return

        for i in range(msgLen):
            char = wavData[(i+1)*PERIOD]
            try:
                decodedStr += chr(char)
            except ValueError as ve:
                pass
                #print("ERROR: ", ve)

    elif (not msgLen and sampleRate):
        MAX_LEN = int(DURATION * (sampleRate+1))
        PERIOD = int(fileSampleRate/sampleRate)
        print(
            f"Reading the entire file using a sample rate of {sampleRate}Hz until an invalid character is found.")
        for i in range(MAX_LEN):
            char = wavData[(i+1)*PERIOD]
            try:
                decodedStr += chr(char)
            except ValueError as ve:
                print(
                    f"Done, found character {char}.\nDecoded string length: {len(decodedStr)}")
                break

    elif (msgLen and not sampleRate):
        MIN_SR = int(msgLen/DURATION)+1  # maximum sample rate in Hz
        if(MIN_SR is 0):
            MIN_SR = 1
        PERIOD = int(fileSampleRate/MIN_SR)
        print(
            f"Reading the first {msgLen} samples using a sample rate of {MIN_SR}Hz")
        for i in range(msgLen):
            char = wavData[(i+1)*PERIOD]
            try:
                decodedStr += chr(char)
            except ValueError as ve:
                pass
                #print("ERROR: ", ve)

    if (output is None):
        if len(decodedStr) > 100:
            if ask_user(
                    "The decoded string is quite large, do you want to output it here??"):
                printDecodedMessage(decodedStr)
            else:
                writeToFile("decoded_message.txt", decodedStr)
        else:
            printDecodedMessage(decodedStr)
    else:
        writeToFile(output, decodedStr)


def printDecodedMessage(decodedStr):
    print(
        f"""\n
Decoded message:
-----------------------------BEGIN-----------------------------
{decodedStr}
------------------------------END------------------------------
""")


def writeToFile(output, decodedStr):
    print("Writing output to a file...")
    with open(output, mode="w", encoding="utf8") as outFile:
        outFile.write(decodedStr)
        outFile.close()
    print("\nDone")


def ask_user(question):
    check = str(input(f"{question} (Y/N): ")).lower().strip()
    try:
        if check[:1] == 'y':
            return True
        elif check[:1] == 'n':
            return False
        else:
            print('Invalid Input')
            return ask_user(question)
    except Exception as error:
        print("Please enter Y or N")
        print(error)
        return ask_user(question)
