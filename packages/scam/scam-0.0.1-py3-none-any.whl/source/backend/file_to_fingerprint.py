# A filetofingerprint object has a filename, a unique fileid, an originality percentage (not implemented right now), a fingerprintssetup as [hash:locationinfile],
# a similarto dictionary as {(similarfileobject) :[([originalfingerprintobjects],[similarfingerprintobjects])]}, and a mostimportantmatches
# list dictionary as {mostimportantfilematch:[((originalfilestartfingerprint, originalfileendfingerprint), [(simfilestartfingerprint, simfileendfingerprint)])]}
class filetofingerprint():
    def __init__(self, filename, fileid, originality, fingerprintssetup, similarto, mostimportantmatches):
        self.filename = filename
        self.fileid = fileid
        self.originality = originality
        self.fingerprintssetup = fingerprintssetup
        self.similarto = similarto
        self.mostimportantmatches = mostimportantmatches
