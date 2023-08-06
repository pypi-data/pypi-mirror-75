# A filetofingerprint object has a filename, a base which for Python/Java is a class object from analyzer.py and for text is simply the file text,
# a unique fileid, an originality percentage (not implemented but possible in the future), a fingerprintssetup as [hash:locationinfile],
# a similarto dictionary as {(similarfileobject) :[([originalfingerprintobjects],[similarfingerprintobjects])]}, and a mostimportantmatches
# dictionary as {mostimportantfileobjectmatch : [(originalfilemostimportantstring, [similarfilemostimportantstrings])]
class filetofingerprint():
    def __init__(self, filename, fileid, base, originality, fingerprintssetup, similarto, mostimportantmatches):
        self.filename = filename
        self.fileid = fileid
        self.base = base
        self.originality = originality
        self.fingerprintssetup = fingerprintssetup
        self.similarto = similarto
        self.mostimportantmatches = mostimportantmatches
