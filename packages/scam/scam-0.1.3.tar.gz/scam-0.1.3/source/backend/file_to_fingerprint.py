# A filetofingerprint object has a filename, a unique fileid, a base which for Python/Java is a class object from analyzer.py and for text is simply the file text,
# an originality percentage (not implemented but possible in the future), a fingerprintssetup as [hash:locationinfile] mostly used for setting things up,
# a similarto dictionary as {(similarfileobject) :[([originalfingerprintobjects],[similarfingerprintobjects])]}, and a mostimportantmatches
# dictionary as {mostimportantfileobjectmatch : [(originalfilemostimportantstring, [similarfilemostimportantstrings])]
class filetofingerprint():
    def __init__(self, filename, fileid, base, originality, fingerprintssetup, similarto, mostimportantmatches):
        self.filename = filename
        self.fileid = fileid
        self.base = base
        self.originality = originality #originality isn't added right now
        self.fingerprintssetup = fingerprintssetup
        self.similarto = similarto
        self.mostimportantmatches = mostimportantmatches
