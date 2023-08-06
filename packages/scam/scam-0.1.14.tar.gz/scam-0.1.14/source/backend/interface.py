from source.backend.fingerprint import Fingerprint
from source.backend.winnowing import *
from source.backend.analyzer import *

# Compares two text files to each other and returns the percent similarity
def compare_files_txt(std1_filename, std2_filename, k, w, boilerplate_filenames):
    # Open the first file and get fingerprints
    std1_file = open(std1_filename, "r")
    std1_txt = std1_file.read()
    std1_fingerprints = text_winnow_setup(std1_txt, k, w)
    # Open the second file and get fingerprints
    std2_file = open(std2_filename, "r")
    std2_txt = std2_file.read()
    std2_fingerprints = text_winnow_setup(std2_txt, k, w)
    # Open boilerplate file(s) to get boilerplate fingerprints
    bp_fingerprints = {}
    for bpfile in boilerplate_filenames:
        bp = open(bpfile, "r")
        bptxt = bp.read()
        if len(bp_fingerprints) == 0:
            bp_fingerprints = text_winnow_setup(bptxt, k, w)
        else:
            bp_fingerprints.update(text_winnow_setup(bptxt, k, w))
    return get_percent_similarity(std1_fingerprints, std2_fingerprints, bp_fingerprints)


# get the common fingerprints between two text files
# if there are more fingerprints than the ignore count then we adjust the window size to gather all of the substrings
def get_fps_txt(std1_filename, std2_filename, k, boilerplate_filenames):
    return get_winnow_fps_txt(std1_filename, std2_filename, k, 2, boilerplate_filenames)


# get the common fingerprints between two text files using the winnowing algorithm
def get_winnow_fps_txt(std1_filename, std2_filename, k, w, boilerplate_filenames):
    # open the files and get the fingerprints
    student_file = open(std1_filename, "r")
    student_txt = student_file.read()

    base_file = open(std2_filename, "r")
    base_txt = base_file.read()

    boilerplate_txts = []
    for bp_filename in boilerplate_filenames:
        boilerplate_file = open(bp_filename, "r")
        boilerplate_txt = boilerplate_file.read()
        boilerplate_txt = re.sub(r'\s+', '', boilerplate_txt.lower())
        boilerplate_txts.append(boilerplate_txt)

    return get_common_fps_txt(student_txt, base_txt, k, w, boilerplate_txts)


# Compares two python files to each other and returns the percent similarity
def compare_files_py(std1_filename, std2_filename, k, w, boilerplate_filenames):
    # Open the first file and get fingerprints
    with open(std1_filename, "r") as student_source:
        vs1 = PyAnalyzer(student_source)
    std1_fingerprints = winnow(vs1.parsed_code, k, w)

    # Open the second file and get fingerprints
    with open(std2_filename, "r") as base_source:
        vs2 = PyAnalyzer(base_source)
    std2_fingerprints = winnow(vs2.parsed_code, k, w)

    # Open boilerplate file(s) and get fingerprints
    bp_fingerprints = {}
    for bpfile in boilerplate_filenames:
        with open(bpfile, "r") as bp_source:
            bp = PyAnalyzer(bp_source)
        if len(bp_fingerprints) == 0:
            bp_fingerprints = winnow(bp.parsed_code, k, w)
        else:
            bp_fingerprints.update(winnow(bp.parsed_code, k, w))
    return get_percent_similarity(std1_fingerprints, std2_fingerprints, bp_fingerprints)


# get the common fingerprints between two python files
# if there are more fingerprints than the ignore count then we adjust the window size to gather all of the substrings
def get_fps_py(std1_filename, std2_filename, k, boilerplate_filenames):
    return get_winnow_fps_py(std1_filename, std2_filename, k, 2, boilerplate_filenames)


# get the common fingerprints between two python files using the winnowing algorithm
def get_winnow_fps_py(std1_filename, std2_filename, k, w, boilerplate_filenames):
    with open(std1_filename, "r") as student_source:
        vs1 = PyAnalyzer(student_source)

    with open(std2_filename, "r") as base_source:
        vs2 = PyAnalyzer(base_source)

    bps = []
    for bpfile in boilerplate_filenames:
        with open(bpfile, "r") as bp_source:
            bp = PyAnalyzer(bp_source)
            bps.append(bp)

    return get_common_fps(vs1, vs2, k, w, bps)


# Compares two java files to each other and returns the percent similarity
def compare_files_java(std1_filename, std2_filename, k, w, boilerplate_filenames):
    # Open the first file and get fingerprints
    with open(std1_filename, "r") as student_source1:
        vs1 = JavaAnalyzer(student_source1)
    std1_fingerprints = winnow(vs1.parsed_code, k, w)
    # Open the second file and get fingerprints
    with open(std2_filename, "r") as student_source2:
        vs2 = JavaAnalyzer(student_source2)
    std2_fingerprints = winnow(vs2.parsed_code, k, w)
    # Open boilerplate files and get fingerprints
    bpfingerprints = {}
    for bpfile in boilerplate_filenames:
        with open(bpfile, "r") as bp_source:
            bp = JavaAnalyzer(bp_source)
        if len(bpfingerprints) == 0:
            bpfingerprints = winnow(bp.parsed_code, k, w)
        else:
            bpfingerprints.update(winnow(bp.parsed_code, k, w))
    return get_percent_similarity(std1_fingerprints, std2_fingerprints, bpfingerprints)


# get the common fingerprints between two java files
# if there are more fingerprints than the ignore count then we adjust the window size to gather all of the substrings
def get_fps_java(std1_filename, std2_filename, k, boilerplate_filenames):
    return get_winnow_fps_java(std1_filename, std2_filename, k, 2, boilerplate_filenames)


# get the common fingerprints between two java files using the winnowing algorithm
def get_winnow_fps_java(std1_filename, std2_filename, k, w, boilerplate_filenames):
    with open(std1_filename, "r") as std1_source:
        vs1 = JavaAnalyzer(std1_source)

    with open(std2_filename, "r") as std2_source:
        vs2 = JavaAnalyzer(std2_source)

    bps = []
    for bpfile in boilerplate_filenames:
        with open(bpfile, "r") as bp_source:
            bp = JavaAnalyzer(bp_source)
            bps.append(bp)

    return get_common_fps(vs1, vs2, k, w, bps)


def get_percent_similarity(std1_fingerprints, std2_fingerprints, bpfingerprints):
    # Get the number of the first student fingerprints
    num_std_fps = 0
    for val in std1_fingerprints.values():
        for _ in val:
            num_std_fps += 1
    # Get the number of times that the common fingerprints were used in the first file (but not boilerplate)
    num_common_fps = 0
    for fp in list(std1_fingerprints.keys()):
        if fp in list(std2_fingerprints.keys()) and fp not in bpfingerprints:
            for _ in std1_fingerprints[fp]:
                num_common_fps += 1
    # return previously calculated number divided by the total number of fingerprints
    similarity = num_common_fps / num_std_fps
    res = similarity * 100
    return res, num_common_fps


def get_common_fps_txt(std1_txt, std2_txt, k, w, boilerplate_txts):
    student_fingerprints = text_winnow_setup(std1_txt, k, w)
    base_fingerprints = text_winnow_setup(std2_txt, k, w)
    boilerplate_fingerprints = {}
    for bp_txt in boilerplate_txts:
        if len(boilerplate_fingerprints) == 0:
            boilerplate_fingerprints = text_winnow_setup(bp_txt, k, w)
        else:
            boilerplate_fingerprints.update(text_winnow_setup(bp_txt, k, w))
    # get the common fingerprints from both files and store them as a list of tuples
    # of the list of fingerprints from both respective files, unless in boilerplate
    common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()) and fp not in boilerplate_fingerprints:
            # for each position add an object
            fingerprints1 = []
            fingerprints2 = []
            for pos in student_fingerprints[fp]:
                substr = get_text_substring(pos, k, std1_txt)
                sfp = Fingerprint(fp, pos, substr)
                fingerprints1.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = get_text_substring(pos, k, std2_txt)
                bfp = Fingerprint(fp, pos, substr)
                fingerprints2.append(bfp)
            common.append((fingerprints1, fingerprints2))
    # return common as a list of tuples of lists
    return common


def get_common_fps(vs1, vs2, k, w, bps):
    student_fingerprints = winnow(vs1.parsed_code, k, w)
    base_fingerprints = winnow(vs2.parsed_code, k, w)
    boilerplate_fingerprints = {}
    for bp in bps:
        if len(boilerplate_fingerprints) == 0:
            boilerplate_fingerprints = winnow(bp.parsed_code, k, w)
        else:
            boilerplate_fingerprints.update(winnow(bp.parsed_code, k, w))
    # get the common fingerprints from both files and store them as a list of tuples
    # of the list of fingerprints from both respective files, unless boilerplate
    common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()) and fp not in boilerplate_fingerprints:
            # for each position add an object
            fingerprints1 = []
            fingerprints2 = []
            for pos in student_fingerprints[fp]:
                substr = vs1.get_code_from_parsed(k, pos)
                sfp = Fingerprint(fp, pos, substr)
                fingerprints1.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                substr = vs2.get_code_from_parsed(k, pos)
                bfp = Fingerprint(fp, pos, substr)
                fingerprints2.append(bfp)
            common.append((fingerprints1, fingerprints2))
    # return common as a list of tuples of lists
    return common


# Takes in a list of multiple filenames, performs the comparison function and
# returns an array of filetofingerprint objects
# the boilerplate argument takes in a list of boilerplate
# ignorecount determines how many fingerprints there must be for a file to be considered similar at all
def compare_multiple_files_txt(filenames, k, w, boilerplate, ignorecount):
    files = wrap_filenames(filenames)
    allfingerprints = collections.defaultdict(dict)
    bpfingerprints = {}

    #get boilerplate hashes/fingerprints
    for bpfile in boilerplate:
        bp = open(bpfile, "r")
        bptxt = bp.read()
        if len(bpfingerprints) == 0:
            bpfingerprints = text_winnow_setup(bptxt, k, w)
        else:
            bpfingerprints.update(text_winnow_setup(bptxt, k, w))

    #put all fingerprints into large fp dictionary
    if len(boilerplate) == 0: #this is to skip the if statement checking boilerplate if there was never any boilerplate
        for file in files:
            f = open(file.filename, "r")
            txt = f.read()
            file.base = txt
            file.fingerprintssetup = text_winnow_setup(txt, k, w)
            for fp in list(file.fingerprintssetup.keys()):
                allfingerprints[fp][file] = []
                for pos in file.fingerprintssetup[fp]:
                    substr = get_text_substring(pos, k, txt)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)
    else:
        for file in files:
            f = open(file.filename, "r")
            txt = f.read()
            file.base = txt
            file.fingerprintssetup = text_winnow_setup(txt, k, w)
            for fp in list(file.fingerprintssetup.keys()): #boilerplate fingerprints aren't considered for comparison
                if fp in bpfingerprints:
                    continue
                allfingerprints[fp][file] = []
                for pos in file.fingerprintssetup[fp]:
                    substr = get_text_substring(pos, k, txt)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)


    #fill the file's similarto dictionary with the necessary fingerprints
    for file in files:
        for fp in list(file.fingerprintssetup.keys()):
            commonfiles = allfingerprints.get(fp)
            if (commonfiles == None):
                continue
            elif len(commonfiles) > 1:
                for commonfile in commonfiles:
                    if file != commonfile: #put it into similarto if it's a different file
                        if commonfile in file.similarto:
                            file.similarto[commonfile].append((allfingerprints[fp][file], allfingerprints[fp][commonfile]))
                        else:
                            file.similarto[commonfile] = [(allfingerprints[fp][file], allfingerprints[fp][commonfile])]
        #clear similarto element if less than ignorecount
        for comfile in list(file.similarto.keys()):
            count = 0
            for uniquefp in file.similarto[comfile]:
                for pos in uniquefp[0]:
                    count +=1
            if count <= ignorecount:
                file.similarto.pop(comfile)


    #this is no longer used (and and I don't think I could get it to work)  but the idea was to use the more in depth algorithm if the similar fingerints was > ignorecount
    """for file in files:
        newsimilarto = file.similarto.copy()
        for simfile in list(file.similarto.keys()):
            fpscount = 0
            for simfp in file.similarto[simfile]:
                for fp in simfp[0]:
                    fpscount += 1
            if fpscount > ignorecount:
                newf1common = []
                #newf2common = [()]
                f1 = open(file.filename, "r")
                txt1 = f1.read()
                file.fingerprintssetup = text_compute_all_setup(txt, k)
                f2 = open(simfile.filename, "r")
                txt2 = f2.read()
                simfilefingerprintssetup = text_compute_all_setup(txt, k)
                f2prints = list(simfilefingerprintssetup.keys())
                count = 0
                for fp in list(file.fingerprintssetup.keys()):
                    if fp in bpfingerprints:
                        continue
                    if fp in f2prints:
                        fps1 = []
                        fps2 = []
                        for pos in file.fingerprintssetup[fp]:
                            substr = get_text_substring(pos, k, txt1)
                            newfp = Fingerprint(fp, pos, substr)
                            fps1.append(newfp)
                        for pos in simfilefingerprintssetup[fp]:
                            substr = get_text_substring(pos, k, txt2)
                            newfp = Fingerprint(fp, pos, substr)
                            fps2.append(newfp)
                        newf1common.append((fps1, fps2))
                newsimilarto.pop(simfile, None)
                #print(len(newf1common), "newf1common length")
                newsimilarto[simfile] = newf1common
        file.similarto.clear()
        for v in newsimilarto:
            for ff1 in newsimilarto[v][0]:
                for f1 in ff1:
                    print(f1.global_pos, f1.substring, end = "")
            print("")
            for ff2 in newsimilarto[v][1]:
                for f2 in ff2:
                    print(f2.global_pos, f2.substring, end = "")
        file.similarto = newsimilarto"""
    return files

#python version
def compare_multiple_files_py(filenames, k, w, boilerplate, ignorecount):
    files = wrap_filenames(filenames)
    allfingerprints = collections.defaultdict(dict)
    bpfingerprints = {}

    #get boilerplate hashes/fingerprints
    for bpfile in boilerplate:
        with open(bpfile, "r") as student_source:
            bp = PyAnalyzer(student_source)
        if len(bpfingerprints) == 0:
            bpfingerprints = winnow(bp.parsed_code, k, w)
        else:
            bpfingerprints.update(winnow(bp.parsed_code, k, w))

    #put all fingerprints into large fp dictionary
    if len(boilerplate) == 0: #this is to skip the if statement checking boilerplate if there was never any boilerplate
        for file in files:
            with open(file.filename, "r") as student_source:
                vs = PyAnalyzer(student_source)
            file.base = vs
            file.fingerprintssetup = winnow(vs.parsed_code, k, w)
            for fp in list(file.fingerprintssetup.keys()):
                allfingerprints[fp][file] = []
                for pos in file.fingerprintssetup[fp]:
                    substr = vs.get_code_from_parsed(pos, k)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)
    else:
        for file in files:
            with open(file.filename, "r") as student_source:
                vs = PyAnalyzer(student_source)
            file.base = vs
            file.fingerprintssetup = winnow(vs.parsed_code, k, w)
            for fp in list(file.fingerprintssetup.keys()): #skip boilerplate hashes
                if fp in bpfingerprints:
                    continue
                allfingerprints[fp][file] = []
                for pos in file.fingerprintssetup[fp]:
                    substr = vs.get_code_from_parsed(pos, k)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)


    #fill the file's similarto dictionary with the necessary fingerprints
    for file in files:
        for fp in list(file.fingerprintssetup.keys()):
            commonfiles = allfingerprints.get(fp)
            if (commonfiles == None):
                continue
            elif len(commonfiles) > 1:
                for commonfile in commonfiles:
                    if file != commonfile: #put it into similarto if it's a different file
                        if commonfile in file.similarto:
                            file.similarto[commonfile].append((allfingerprints[fp][file], allfingerprints[fp][commonfile]))
                        else:
                            file.similarto[commonfile] = [(allfingerprints[fp][file], allfingerprints[fp][commonfile])]
        # clear similarto element if less than ignorecount
        for comfile in list(file.similarto.keys()):
            print("File", file.filename, "similarto:", len(file.similarto[comfile]))
            count = 0
            for uniquefp in file.similarto[comfile]:
                for pos in uniquefp[0]:
                    count += 1
            if count <= ignorecount:
                file.similarto.pop(comfile)

        # this is no longer used (and and I don't think I could get it to work)  but the idea was to use the more in depth algorithm if the similar fingerints was > ignorecount
        """for file in files:
            newsimilarto = file.similarto.copy()
            for simfile in list(file.similarto.keys()):
                simfps = 0
                for simfp in file.similarto[simfile]:
                    for fp in simfp[0]:
                        simfps += 1
                if simfps > ignorecount:
                    newf1common = []
                    with open(file.filename, "r") as student_source:
                        vs = PyAnalyzer(student_source)
                    file.fingerprintssetup = compute_all(vs.parsed_code, k, w)
                    with open(file.filename, "r") as student_source:
                        vb = PyAnalyzer(student_source)
                    simfilefingerprintssetup = compute_all(vb.parsed_code, k, w)
                    f2prints = list(simfilefingerprintssetup.keys())
                    for fp in list(file.fingerprintssetup.keys()):
                        if fp in bpfingerprints:
                            continue
                        if fp in f2prints:
                            fps1 = []
                            fps2 = []
                            for pos in file.fingerprintssetup[fp]:
                                vs.get_code_from_parsed(k, pos)
                                newfp = Fingerprint(fp, pos, substr)
                                fps1.append(newfp)
                            for pos in simfilefingerprintssetup[fp]:
                                vb.get_code_from_parsed(k, pos)
                                newfp = Fingerprint(fp, pos, substr)
                                fps2.append(newfp)
                            newf1common.append((fps1, fps2))
                    newsimilarto[simfile] = newf1common
            file.similarto = newsimilarto"""
    return files

#java version
def compare_multiple_files_java(filenames, k, w, boilerplate, ignorecount):
    files = wrap_filenames(filenames)
    allfingerprints = collections.defaultdict(dict)
    bpfingerprints = {}

    #get the boilerplate hashes/fingerprints
    for bpfile in boilerplate:
        with open(bpfile, "r") as student_source:
            bp = JavaAnalyzer(student_source)
        if len(bpfingerprints) == 0:
            bpfingerprints = winnow(bp.parsed_code, k, w)
        else:
            bpfingerprints.update(winnow(bp.parsed_code, k, w))

    #put all fingerprints into large fp dictionary
    if len(boilerplate) == 0: #this is to skip the if statement checking boilerplate hashes if there never was any boilerplate
        for file in files:
            with open(file.filename, "r") as student_source:
                vs = JavaAnalyzer(student_source)
            file.base = vs
            file.fingerprintssetup = winnow(vs.parsed_code, k, w)
            for fp in list(file.fingerprintssetup.keys()):
                allfingerprints[fp][file] = []
                for pos in file.fingerprintssetup[fp]:
                    substr = vs.get_code_from_parsed(pos, k)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)
    else:
        for file in files:
            with open(file.filename, "r") as student_source:
                vs = JavaAnalyzer(student_source)
            file.base = vs
            file.fingerprintssetup = winnow(vs.parsed_code, k, w)
            for fp in list(file.fingerprintssetup.keys()):
                if fp in bpfingerprints: #don't consider boilerplate hashes/fingerprints
                    continue
                allfingerprints[fp][file] = []
                for pos in file.fingerprintssetup[fp]:
                    substr = vs.get_code_from_parsed(pos, k)
                    newfp = Fingerprint(fp, pos, substr)
                    allfingerprints[fp][file].append(newfp)

    #fill the file's similarto dictionary with the necessary fingerprints
    for file in files:
        for fp in list(file.fingerprintssetup.keys()):
            commonfiles = allfingerprints.get(fp)
            if (commonfiles == None):
                continue
            elif len(commonfiles) > 1:
                for commonfile in commonfiles:
                    if file != commonfile: #put it into similarto if it's a different file
                        if commonfile in file.similarto: #fp blocks may be able to be determined here to be faster
                            file.similarto[commonfile].append((allfingerprints[fp][file], allfingerprints[fp][commonfile]))
                        else:
                            file.similarto[commonfile] = [(allfingerprints[fp][file], allfingerprints[fp][commonfile])]
        # clear similarto element if less than ignorecount
        for comfile in list(file.similarto.keys()):
            count = 0
            for uniquefp in file.similarto[comfile]:
                for pos in uniquefp[0]:
                    count += 1
            if count <= ignorecount:
                file.similarto.pop(comfile)
        # this is no longer used (and and I don't think I could get it to work)  but the idea was to use the more in depth algorithm if the similar fingerints was > ignorecount
        """for file in files:
            newsimilarto = file.similarto.copy()
            for simfile in list(file.similarto.keys()):
                simfps = 0
                for simfp in file.similarto[simfile]:
                    for fp in simfp[0]:
                        simfps += 1
                if simfps > ignorecount:
                    newf1common = []
                    with open(file.filename, "r") as student_source:
                        vs = PyAnalyzer(student_source)
                    file.fingerprintssetup = compute_all(vs.parsed_code, k, w)
                    with open(file.filename, "r") as student_source:
                        vb = PyAnalyzer(student_source)
                    simfilefingerprintssetup = compute_all(vb.parsed_code, k, w)
                    f2prints = list(simfilefingerprintssetup.keys())
                    for fp in list(file.fingerprintssetup.keys()):
                        if fp in bpfingerprints:
                            continue
                        if fp in f2prints:
                            fps1 = []
                            fps2 = []
                            for pos in file.fingerprintssetup[fp]:
                                vs.get_code_from_parsed(k, pos)
                                newfp = Fingerprint(fp, pos, substr)
                                fps1.append(newfp)
                            for pos in simfilefingerprintssetup[fp]:
                                vb.get_code_from_parsed(k, pos)
                                newfp = Fingerprint(fp, pos, substr)
                                fps2.append(newfp)
                            newf1common.append((fps1, fps2))
                    newsimilarto[simfile] = newf1common
            file.similarto = newsimilarto"""
    return files

# for the future
"""def compare_files_cpp(student_filename1, student_filename2, k, w):
    with open(student_filename1, "r") as student_source1:
        vs1 = CppAnalyzer(student_source1)
    with open(student_filename2, "r") as student_source2:
        vs2 = CppAnalyzer(student_source2)
    print("CPP PARSE CODE1: ",vs1.parsed_code)
    print("CPP PARSED CODE2: ",vs2.parsed_code)
    student_fingerprints1 = winnow(vs1.parsed_code, k, w)
    student_fingerprints2 = winnow(vs2.parsed_code, k, w)
    num_std_fps = 0
    for val in student_fingerprints1.values():
        for _ in val:
            num_std_fps += 1
    num_common_fps = 0
    for fp in list(student_fingerprints1.keys()):
        if fp in list(student_fingerprints2.keys()):
            for _ in student_fingerprints1[fp]:
                num_common_fps += 1
    similarity = num_common_fps / num_std_fps
    print(res := similarity * 100)
    return res, num_common_fps"""


# gets the most important matches of filetofingerprintobjects f1 to f2, as determined by the blocks of consecutive fingerprints, puts the
# results into f1's mostimportantmatches property as large substrings for the frontend's purposes
# changing blocksize determines how many consecutive fingerprints there have to be before being considered
# a block, changing offset determines the distance that's allowed between each print for it to be considered within the same block
# the files need to have their similarto attribute filled up through compare_multiple_files first for this to work
# this ended up being pretty complicated so I wouldn't recommend trying to add to it but you can try if you want
# if you undo those comments (not the debug printing) you should get back a fingerprint range rather than a substring block actually
def get_most_important_matches_txt(f1, f2, k, blocksize, offset):
    if f1.similarto.get(f2) == None:
        f1.similarto = []
        return
    f1_fingerprints = []
    f2_fingerprints = {}
    for fptuple in f1.similarto[f2]: #order the fingerprint's individually by location
        f2_fingerprints[fptuple[1][0].fp_hash] = fptuple[1]
        for f1_fp in fptuple[0]:
            f1_fingerprints.append(f1_fp)
    f1_fingerprints.sort(key = lambda fps: fps.global_pos)
    blockcounter = 0
    most_important_match_locations = []
    fp2lastpos = []
    for fp in range(len(f1_fingerprints) - 1): #find if consecutive
        okay = False
        if blockcounter == 0: #start of a new block
            start = f1_fingerprints[fp]
            f2start = f2_fingerprints[f1_fingerprints[fp].fp_hash].copy()
            fp2lastpos = f2start.copy()
        blockcounter +=1
        if ((f1_fingerprints[fp].global_pos + k + offset) >= f1_fingerprints[fp + 1].global_pos): #f1 fingerprint is consecutive
            i = 0
            for f2matchpos in fp2lastpos: #check all potential positions, making chains of potential blocks in f2
                if f2matchpos.global_pos == -1: #skip invalid chains from the given error code
                    i += 1
                    continue
                for fp2 in f2_fingerprints[f1_fingerprints[fp].fp_hash]: #check if consecutive in f2, 1st position
                    if fp2.global_pos == f2matchpos.global_pos:
                        for fp2prime in f2_fingerprints[f1_fingerprints[fp + 1].fp_hash]: #check if consecutive in f2, second position
                            if fp2prime.global_pos < f2matchpos.global_pos: #only check locations which can be consecutive
                                if (blockcounter < blocksize):
                                    fp2lastpos[i] = Fingerprint(-1, -1, "")  # error code
                                continue
                            elif (f2matchpos.global_pos + k + offset) >= fp2prime.global_pos: #get last consecutive occurence
                                okay = True
                                fp2lastpos[i] = fp2prime
                            elif (blockcounter < blocksize) and (okay == False): #the chain is not possibly valid, give an error code to make sure it's not appended, append subloc here maybe
                                fp2lastpos[i] = Fingerprint(-1, -1, "") #error code
                i += 1
        if okay == False:   #end of block
            if blockcounter >= blocksize:
                end = f1_fingerprints[fp]
                templist = []
                blockstring = ""
                for pos in range(len(fp2lastpos)):
                    if fp2lastpos[pos].global_pos == -1:
                        continue
                    distance = fp2lastpos[pos].global_pos - f2start[pos].global_pos
                    templist.append(get_text_substring(f2start[pos].global_pos, distance + k, f2.base))
                    #templist.append((f2start[pos], fp2lastpos[pos]))
                #most_important_match_locations.append(((start, end), templist))
                distance = end.global_pos - start.global_pos
                most_important_match_locations.append((get_text_substring(start.global_pos, distance + k, f1.base), templist))
            blockcounter = 0
    if blockcounter >= blocksize: #1 more block check to see if the last one was end of a block
        end = f1_fingerprints[len(f1_fingerprints) - 1]
        templist = []
        for pos in range(len(fp2lastpos)):
            if fp2lastpos[pos].global_pos == -1:
                continue
            distance = fp2lastpos[pos].global_pos - f2start[pos].global_pos
            templist.append(get_text_substring(f2start[pos].global_pos, distance + k, f2.base))
            #templist.append((f2start[pos], fp2lastpos[pos]))
        #most_important_match_locations.append(((start, end), templist))
        distance = end.global_pos - start.global_pos
        most_important_match_locations.append((get_text_substring(start.global_pos, distance + k, f1.base), templist))
    if len(most_important_match_locations) != 0:
        f1.mostimportantmatches[f2] = most_important_match_locations
    else:
        f1.mostimportantmatches[f2] = []

    #debug printing
    """for mostimportant in most_important_match_locations:
        print("F1: ")
        print(mostimportant[0][0].substring + "(" + str(mostimportant[0][0].global_pos) + ") - " + mostimportant[0][1].substring + "(" + str(mostimportant[0][1].global_pos) + ")")
        print("F2: ")
        i = 1
        for f2matchblock in mostimportant[1]:
            if len(mostimportant[1]) == 0:
                print(f2matchblock[0].substring + "("+ str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ")
            elif i < len(mostimportant[1]):
                print(f2matchblock[0].substring + "(" + str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ", end="+ ")
            else:
                print(f2matchblock[0].substring + "(" + str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ")
            i += 1
        print("")"""

# the version for java + python, check the txt version of this above for more info, undoing those comments should also return a range
def get_most_important_matches_javpy(f1, f2, k, blocksize, offset):
    if f1.similarto.get(f2) == None:
        f1.mostimportantmatches[f2] = []
        return
    f1_fingerprints = []
    f2_fingerprints = {}
    for fptuple in f1.similarto[f2]: #order the fingerprint's individually by location
        f2_fingerprints[fptuple[1][0].fp_hash] = fptuple[1]
        for f1_fp in fptuple[0]:
            f1_fingerprints.append(f1_fp)
    f1_fingerprints.sort(key = lambda fps: fps.global_pos)
    blockcounter = 0
    most_important_match_locations = []
    fp2lastpos = []
    for fp in range(len(f1_fingerprints) - 1): #find if consecutive
        okay = False
        if blockcounter == 0: #start of a new block
            start = f1_fingerprints[fp]
            f2start = f2_fingerprints[f1_fingerprints[fp].fp_hash].copy()
            fp2lastpos = f2start.copy()
        blockcounter +=1
        if ((f1_fingerprints[fp].global_pos + k + offset) >= f1_fingerprints[fp + 1].global_pos): #f1 fingerprint is consecutive
            i = 0
            for f2matchpos in fp2lastpos: #check all potential positions, making chains of potential blocks in f2
                if f2matchpos.global_pos == -1:
                    i += 1
                    continue
                for fp2 in f2_fingerprints[f1_fingerprints[fp].fp_hash]: #check if consecutive in f2, 1st position
                    if fp2.global_pos == f2matchpos.global_pos:
                        for fp2prime in f2_fingerprints[f1_fingerprints[fp + 1].fp_hash]: #check if consecutive in f2, second position
                            if fp2prime.global_pos < f2matchpos.global_pos: #only check locations which can be consecutive
                                if (blockcounter < blocksize):
                                    fp2lastpos[i] = Fingerprint(-1, -1, "")  # error code
                                continue
                            elif (f2matchpos.global_pos + k + offset) >= fp2prime.global_pos: #get last consecutive occurence
                                okay = True
                                fp2lastpos[i] = fp2prime
                            elif (blockcounter < blocksize) and (okay == False): #the chain is not possibly valid, give an error code to make sure it's not appended, append subloc here maybe
                                fp2lastpos[i] = Fingerprint(-1, -1, "") #error code
                i += 1
        if okay == False:   #end of block
            if blockcounter >= blocksize:
                end = f1_fingerprints[fp]
                templist = []
                for pos in range(len(fp2lastpos)):
                    if fp2lastpos[pos].global_pos == -1:
                        continue
                    #templist.append((f2start[pos], fp2lastpos[pos]))
                    distance = fp2lastpos[pos].global_pos - f2start[pos].global_pos
                    templist.append(f2.base.get_code_from_parsed(f2start[pos].global_pos, distance + k))
                #most_important_match_locations.append(((start, end), templist))
                distance = end.global_pos - start.global_pos
                most_important_match_locations.append((f1.base.get_code_from_parsed(start.global_pos, distance + k), templist))
            blockcounter = 0
    if blockcounter >= blocksize: #1 more block check to see if the last one was end of a block
        end = f1_fingerprints[len(f1_fingerprints) - 1]
        templist = []
        for pos in range(len(fp2lastpos)):
            if fp2lastpos[pos].global_pos == -1:
                continue
            #templist.append((f2start[pos], fp2lastpos[pos]))
            distance = fp2lastpos[pos].global_pos - f2start[pos].global_pos
            templist.append(f2.base.get_code_from_parsed(f2start[pos].global_pos, distance + k))
        #most_important_match_locations.append(((start, end), templist))
        distance = end.global_pos - start.global_pos
        most_important_match_locations.append((f1.base.get_code_from_parsed(start.global_pos, distance + k), templist))
    if len(most_important_match_locations) != 0:
        f1.mostimportantmatches[f2] = most_important_match_locations
    else:
        f1.mostimportantmatches[f2] = []

    #debug printing
    """for mostimportant in most_important_match_locations:
        print("F1: ")
        print(mostimportant[0][0].substring + "(" + str(mostimportant[0][0].global_pos) + ") - " + mostimportant[0][1].substring + "(" + str(mostimportant[0][1].global_pos) + ")")
        print("F2: ")
        i = 1
        for f2matchblock in mostimportant[1]:
            if len(mostimportant[1]) == 0:
                print(f2matchblock[0].substring + "("+ str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ")
            elif i < len(mostimportant[1]):
                print(f2matchblock[0].substring + "(" + str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ", end="+ ")
            else:
                print(f2matchblock[0].substring + "(" + str(f2matchblock[0].global_pos) + ") - " + f2matchblock[1].substring + " (" + str(f2matchblock[1].global_pos) + ") ")
            i += 1
        print("")"""


# the version for multiple files (I don't think it gets used)
def get_most_important_matches_multiple_files_txt(files, k , blocksize, offset):
    for f1 in files:
        for f2 in files:
            get_most_important_matches_txt(f1, f2, k, blocksize, offset)


def get_most_important_matches_multiple_files_javpy(files, k, blocksize, offset):
    for f1 in files:
        for f2 in files:
            get_most_important_matches_javpy(f1, f2, k, blocksize, offset)


# gets % similarity between 2 different filetofingerprintobjects that were initialized through compare_multiple_documents
def get_similarity(f1, f2):
    print(f1.filename, f2.filename)
    if f1.similarto.get(f2) == None:
        return 0.0
    else:
        simcount = 0
        totalfps = 0
        for simfp in f1.similarto[f2]:
            for loc in simfp[0]:
                simcount += 1
        for fp in f1.fingerprintssetup.values():
            for loc in fp:
                totalfps += 1
        return simcount / totalfps


# Printings debug results for development/testing, accepts filetofingerprint object
def print_prototype_test(files, boilerplate):
    print("Testing files ", end="")
    for i in range(len(files)):
        if i != (len(files) - 1):
            print(files[i].filename + ", ", end="")
        else:
            print(files[i].filename + ".")
    print("")
    if len(boilerplate) == 0:
        print("No boilerplate.", end = "")
    else:
        print("The boilerplate is: ", end = "")
        for i in range(len(boilerplate)):
            if i != (len(boilerplate) - 1):
                print(boilerplate[i] + ", ", end="")
            else:
                print(boilerplate[i] + ".", end = "")
    print("")
    print("")
    for file in files:
        if (len(file.similarto) == 0):
            print("File " + str(file.fileid) + ", " + file.filename + ", is similar to nothing.")
            continue
        print("File " + str(file.fileid) + ", " + file.filename + ", is similar to ", end="")
        for sim in file.similarto:
            print(sim.filename)
            print("They're similar at (loc(position), loc(position) for each of the 2 documents):")
            l = 0  # this l will probably get taken out, it's only to keep too many results from printing
            fpcount = 0
            for simfps in file.similarto[sim]:
                if (l == 9):
                    print("etc....")
                    #break
                for fps in simfps[0]:
                    substr = fps.substring.split('\n')
                    substr = "\\n".join(substr)
                    print(str(fps.global_pos) + "(" + substr + ")", end = " ")
                print(", ", end = "")
                for fps in simfps[1]:
                    substr = fps.substring.split('\n')
                    substr = "\\n".join(substr)
                    print(str(fps.global_pos) + "(" + substr + ")", end = " ")
                print("")
                l += 1
            print(sim.filename, "by {:.2%}".format(get_similarity(file, sim)))
            print("")

#you can set the script path here if you want to test stuff
def main():
    boilerplatejava = []
    # res, num_common = compare_files_txt("test_files/test.txt", "test_files/test2.txt", 10, 5)
    # get_winnow_fps_txt("test_files/songtest1.txt", "test_files/songtest2.txt", 5, 4)
    # get_fps_txt("test_files/test.txt", "test_files/test2.txt", 10, 5, num_common, 5)
    #compare_files_py("test_files/test2innocent.py", "test_files/test2.py", 50, 50, boilerplatejava)
    #common = get_winnow_fps_py("test_files/test2innocent.py", "test_files/test2.py", 50, 50, boilerplatejava)
    """for c in common:
        print("FP1:\n" + c[0][0].substring)
        print("FP2:\n" + c[1][0].substring)"""
    # boilerplatejava = ["test_files/test2.java"]
    boilerplatejava = []
    compare_files_java('test_files/test1.java', 'test_files/test1same.java', 10, 5, boilerplatejava)
    common = get_winnow_fps_java('test_files/test1.java', 'test_files/test1same.java', 10, 5, boilerplatejava)
    """for c in common:
        print("FP1:\n" + c[0][0].substring)
        print("FP2:\n" + c[1][0].substring)"""
    """print("Multi-document tests: ")
    # multidocumenttest = ["songtest1.txt", "songtest2.txt", "javatest1.java", "c++test1.cpp", "texttest2.txt"]
    multidocumenttesttxt = ["test_files/songtest1.txt", "test_files/songtest2.txt", "test_files/javatest1.java", "test_files/lorem.txt", "test_files/ipsum.txt"]
    #filetofingerprintobjects = compare_multiple_files_txt(multidocumenttesttxt, 10, 5, [], 0)
    #print_prototype_test(filetofingerprintobjects, [])
    multidocumenttestpy = ["test_files/test1.py", "test_files/test1copier.py"]
    filetofingerprintobjects = compare_multiple_files_py(multidocumenttestpy, 5, 10, [], 0)
    get_most_important_matches_javpy(filetofingerprintobjects[0], filetofingerprintobjects[1], 5, 2, 20)
    #print_prototype_test(filetofingerprintobjects, [])
    mixtest = ["test_files/test1.py", "test_files/test1copier.py", "test_files/test1innocent.py", "test_files/test1same.py"]
    filetofingerprintobjects = compare_multiple_files_txt(mixtest, 10, 5, [], 0)
    #print_prototype_test(filetofingerprintobjects, [])
    print("")

    print("Boilerplate tests: ")
    boilerplatepy = ["test_files/test1.py", "test_files/test2same.py", "test_files/test.txt", "test_files/test2.txt"]
    boilerplatetestpy = ["test_files/test1same.py", "test_files/test1copier.py"]
    #filetofingerprintobjects = compare_multiple_files_py(boilerplatetestpy, 5, 4, boilerplatepy, 0)
    #print_prototype_test(filetofingerprintobjects, boilerplatepy)

    boilerplatetxt = ["test_files/ipsum.txt"]
    boilerplatetesttxt = ["test_files/songtest1.txt", "test_files/songtest2.txt", "test_files/lorem.txt", "test_files/test.txt", "test_files/test2.txt"]
    filetofingerprintobjects = compare_multiple_files_txt(boilerplatetesttxt, 10, 5, boilerplatetxt, 0)
   # print_prototype_test(filetofingerprintobjects, boilerplatetxt)

    print("Most important matches:")
    get_most_important_matches_multiple_files_txt(filetofingerprintobjects, 10, 3, 20)
    for importanttest in filetofingerprintobjects:
        print(importanttest.filename + " important matches: ")
        for matchingfile in list(importanttest.mostimportantmatches.keys()):
            print(matchingfile.filename + " important")
            for match in importanttest.mostimportantmatches[matchingfile]:
                print("F1: " + importanttest.filename)
                print(match[0])
                print("F2: " + matchingfile.filename)
                print(match[1])
        print("-------------------------------")"""


if __name__ == "__main__":
    main()