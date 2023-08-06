import sys
sys.path.append('../')
import os
import time
import glob
import tkinter as tk
from tkinter import filedialog as fd
#from PIL import Image, ImageTk
from source.backend.interface import *
from source.backend.analyzer import remove_comments


class SourceAnalyzer:
    '''
    A class used as the main structure for the Tkinter based GUI.

    Methods:
    ----------

        File Selection:
        ----------------
            open_file1:
                    Responsible for student file addition
            clear_file1:
                    Responsible for clearing student files
            open_file2:
                    Responsible for boilerplate file addition
            clear_file2:
                    Responsible for clearing boilerplate files
        
        Backend Interface:
        ----------------
            export_files:
                    Sends student/boilerplate files to and nitializes filetofingerprint objects from the backend, 
                    ensures more than one student file is sent, and that boilerplate files can't be identical to student files.
            get_output:
                    Responsible for printing at-a-glance results between two files, and issues warnings if incorrect analyzer is used.
            gather_reg_fingerprints:
                    With two provided filetofingerprint objects (based on tracking indexes in a class variable), and other user input data
                    (k, window size, ignore count), an in-depth comparison of the two files with eachother is done on the backend via
                    compare_files and get_fps functions. The documents are output to the GUI's side-by-side textboxes, and that output
                    is invisibly tagged with the locations of every found fingerprint (done searching for provided substrings). The tags
                    follow the format 'match#' with # being a number from 0 to (max fingerprints). This function also establishes the
                    number of fingerprints in a given comparison, as well as initializes the current fingerprint to 1.
            gather_most_fingerprints:
                    Very similar to gather_reg_fingerprints, only using backend functions pertaining specifically to most_important_fingerprints.
                    These matches are tagged using 'most#', and differs slightly in how the returned list/tuple structure is parsed.

        File Navigation:
        ----------------
            next_file1:
                    Responsible for increasing the value self.curr_index1, which keeps track of which file is currently being compared on the left.
            next_file2:
                    Responsible for increasing the value self.curr_index2, which keeps track of which file is being compared to on the right.
            prev_file1:
                    Responsible for decreasing self.curr_index1
            prev_file2:
                    Responsible for decreasing self.curr_index2

        Fingerprint Display:
        ----------------
            show_fp:
                    Called when 'View All' is toggled in order to update which fingerprints are being shown. Decides which version of show_fp to
                    run based on what type of fingerprint is being displayed.
            show_reg_fp:
                    Depending on whether 'View All' is selected, either highlights every tagged fingerprint, or highlights the first fingerprint and
                    initializes a class variable to track the current fingerprint. Note that the textbox is changed to 'normal' at the beginning and 'disabled' at the
                    end of the function, to ensure users can't edit information inside the textboxes.
            show_most_fp:
                    Very similar to show_reg_fp, only instead of highlighting the 'match#' tags, it highlights the 'most#' tags.
        
        Fingerprint Navigation:
        ----------------
            next_fp:
                    Responsible for incrementing to and highlighting the next fingerprint. Due to issues with overlapping fingerprints, the current tag must be
                    raised in rank to ensure it shows up in full, hence this function must lower the previous tag, raise this new one, and highlight it yellow. This
                    function contains the code for both the most_important and regular fingerprints, the only difference being the name of the tags.
            last_fp:
                    Very similar to next_fp, only responsible for going to the previous fingerprint.

        Other Functions:
        ----------------
            clear_output:
                    Runs when the Clear Output button is pressed, but also immediately once the Compare button is pressed. Resets all class variables and
                    clears text output on screen.
            mult_yview:
                    Allows the scroll bars on the side-by-side text boxes to move in sync (when clicked and dragged)
            report:
                    Responsible for generating the output report full of at-a-glance results.
            open_help:
                    Responsible for the help menu in the toolbar.
            
        Main Class:
        ----------------
            __init__:
                    Initializes class and runs create_widgets, which builds the GUI itself.
            create_widgets:
                    Responsible for creating and laying all the actual GUI elements: Frames, Buttons, Text-Boxes, etc. Also creates class variables.

    '''

#File Selection

    def open_file1(self):
        '''
        File selection for student files.
        '''
        if self.language_var.get() == "Python":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Python Files", "*.py"),("Text Files", "*.txt"),("Java Files", "*.java")))
        elif self.language_var.get() == "Java":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Java Files", "*.java"),("Python Files", "*.py"),("Text Files", "*.txt")))
        else:
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("Python Files", "*.py"),("Java Files", "*.java")))
        # print(files)
        self.files1 = files
        for file in files:
            self.file_name1.insert(tk.END, file)

    def clear_file1(self):
        '''
        Clears student files.
        '''
        self.file1 = []
        self.file_name1.delete(0, tk.END)

    def open_file2(self):
        '''
        File selection for boilerplate files.
        '''
        if self.language_var.get() == "Python":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Python Files", "*.py"),("Text Files", "*.txt"),("Java Files", "*.java")))
        elif self.language_var.get() == "Java":
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Java Files", "*.java"),("Python Files", "*.py"),("Text Files", "*.txt")))
        else:
            files = fd.askopenfilenames(initialdir=os.getcwd(), title="Open File", filetypes=(("Text Files", "*.txt"),("Python Files", "*.py"),("Java Files", "*.java")))
        # print(files)
        self.files2 = files
        for file in files:
            self.file_name2.insert(tk.END, file)

    def clear_file2(self):
        '''
        Clears boilerplate files.
        '''
        self.file2 = []
        self.file_name2.delete(0, tk.END)

#Backend Interface

    def export_files(self):
        '''
        Interfaces with backend based on user inputs (student files, parameters, etc.)

        Gathers list of files, and from that gathers a list of filetofingerprint objects, based on user parameters.
        Also ensures user input is valid (to an extent).

        '''

        #Clear current output before new comparison
        self.clear_output()

        file1 = self.file_name1.get(0, tk.END) #student
        file2 = self.file_name2.get(0, tk.END) #boilerplate

        #k and w from user inputs
        k = int(self.k_input.get())
        w = int(self.windowSizeInput.get())

        #Default displayed file indexes are 0 and 1 (first and second files of list)
        index1 = 0
        index2 = 1

        if (not (len(file1)<=1)): #Runs if there are at least 2 student files

            diff = True
            for x in file1:
                for y in file2:
                    if x == y:
                        diff = False
            if diff: #Runs if all student files are different from boilerplate files

                #File Output
                self.file1out = open(file1[index1], 'r').read()
                self.file2out = open(file1[index2], 'r').read()

                #Ignore count from user input
                ignorecount = int(self.ignore_input.get())

                #Python
                if self.language_var.get() == "Python":
                    file2fp_objs = compare_multiple_files_py(file1, k, w, file2, ignorecount)
                #Java
                elif self.language_var.get() == "Java":
                    file2fp_objs = compare_multiple_files_java(file1, k, w, file2, ignorecount)
                #Text
                else:
                    file2fp_objs = compare_multiple_files_txt(file1, k, w, file2, ignorecount)

                #Set class variables
                self.f2fp = file2fp_objs
                self.curr_index1 = index1
                self.curr_index2 = index2

                #Print at-a-glance output
                self.get_output()
                
            else:
                print("there exists a same file between boilerplate and student files")
                self.out_result.configure(state='normal')
                self.out_result.delete('1.0', tk.END)
                self.out_result.insert(tk.END, "There exists a same file between boilerplate and student files!")
                self.out_result.configure(state='disabled')

        else:
            self.out_result.configure(state='normal')
            self.out_result.delete('1.0', tk.END)
            self.out_result.insert(tk.END, "Please include more student files to compare!")
            self.out_result.configure(state='disabled')

    def get_output(self):
        '''
        Responsible for printing at-a-glance results between two files, and issues warnings if incorrect analyzer is used.
        '''

        self.out_result.configure(state='normal')

        self.out_result.delete('1.0', tk.END)

        #Python analyzer warning
        if self.language_var.get() == "Python":
            if self.f2fp[self.curr_index1].filename[(len(self.f2fp[self.curr_index1].filename) - 3):] != '.py' or self.f2fp[self.curr_index2].filename[(len(self.f2fp[self.curr_index2].filename) - 3):] != '.py':
                self.out_result.insert(tk.END, "WARNING: Used improper analyzer for file type. Results will be inaccurate!\n")

        #Java analyzer warning
        if self.language_var.get() == "Java":
            if self.f2fp[self.curr_index1].filename[(len(self.f2fp[self.curr_index1].filename) - 5):] != '.java' or self.f2fp[self.curr_index2].filename[(len(self.f2fp[self.curr_index2].filename) - 5):] != '.java':
                self.out_result.insert(tk.END, "WARNING: Used improper analyzer for file type. Results will be inaccurate!\n")

        #If files have enough fingerprints in common (determined on backend using ignore count), display output for them
        if self.f2fp[self.curr_index2] in self.f2fp[self.curr_index1].similarto:
            percentage = "{:.2%}".format(get_similarity(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2]))
            f2fpstring = str("Files Compared: " + self.f2fp[self.curr_index1].filename + " and " + self.f2fp[self.curr_index2].filename + "\nPercentage Similarity: " + str(percentage) + "\nCommon Fingerprints: " + str(len(self.f2fp[self.curr_index1].similarto[self.f2fp[self.curr_index2]])))
        
        #Otherwise, state the similarity is negligible
        else:
            f2fpstring = str("Files Compared: " + self.f2fp[self.curr_index1].filename + " and " + self.f2fp[self.curr_index2].filename + "\nSimilarity between files deemed negligible via ignore count.")

        #Output to text box
        self.out_result.insert(tk.END, f2fpstring)

        self.out_result.configure(state='disabled')

        #Depending on what fingerprints are requested, run specified function
        if self.fp_type.get() == 0:
            self.gather_reg_fingerprints()
        else:
            self.gather_most_fingerprints()

    def gather_reg_fingerprints(self):
        '''
        Responsible for gathering regular fingerprints from backend, used for side-by-side comparison.
        '''

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        #k and w from user input
        k = int(self.k_input.get())
        w = int(self.windowSizeInput.get())

        #Two files being compared side-by-side
        file1 = self.f2fp[self.curr_index1].filename
        file2 = self.f2fp[self.curr_index2].filename

        #Output of those files
        file1out = open(file1, 'r').read()
        file2out = open(file2, 'r').read()

        #If the analyzer is set to Java, remove comments from files
        if self.language_var.get() == "Java":
            file1out = remove_comments(file1out)
            file2out = remove_comments(file2out)

        if self.f2fp[self.curr_index2] in self.f2fp[self.curr_index1].similarto:

            #Python
            if self.language_var.get() == "Python":
                res, num_common_fps = compare_files_py(file1, file2, k, w, self.file_name2.get(0, tk.END))
                fp = get_fps_py(file1, file2, k, self.file_name2.get(0, tk.END))

            #Java
            elif self.language_var.get() == "Java":
                res, num_common_fps = compare_files_java(file1, file2, k, w, self.file_name2.get(0, tk.END))
                fp = get_fps_java(file1, file2, k, self.file_name2.get(0, tk.END))

            #Text
            else:
                res, num_common_fps = compare_files_txt(file1, file2, k, w, self.file_name2.get(0, tk.END))
                fp = get_fps_txt(file1, file2, k, self.file_name2.get(0, tk.END))
            
        else:
            fp = []


        #fp = self.f2fp[self.curr_index1].similarto[self.f2fp[self.curr_index2]]

        #Initialize tags
        for i in range(len(fp)):
            self.out_text1.tag_config("match" + str(i), background='white')
            self.out_text2.tag_config("match" + str(i), background='white')

        #Clear text boxes, and add file outputs
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)
        self.out_text1.insert(tk.END, file1out)
        self.out_text2.insert(tk.END, file2out)

        #Used to progress the search through the file, so multiple instances of the same substring aren't caught.
        index_track1 = '1.0'
        fp_track = 0
        remove_fps = []

        #For each fingerprint
        for fingerprint in fp:

            index_track2 = '1.0'
            increment_fp = True

            new_tag1 = ''
            new_tag2 = ''

            #Parse through all substrings in File 1 for a given fingerprint, tagging them for this fingerprint
            for i in range(len(fingerprint[0])):
                new_tag1 = self.out_text1.search(fingerprint[0][i].substring, index_track1, tk.END, exact=False)
                
                if new_tag1 != '':
                    '''print("1 - " + str(fp_track + 1) + ": " + fingerprint[0][i].substring)'''
                    self.out_text1.tag_add("match" + str(fp_track), new_tag1, str(new_tag1) + "+" + str(len(fingerprint[0][i].substring)) + "c")
                else:
                    increment_fp = False
                    '''print("1 - " + str(fp_track + 1) + ": " + fingerprint[0][i].substring)'''
                    '''print("COULD NOT FIND")'''

            #Parse through all substrings in File 2 for a given fingerprint, tagging them for this fingerprint
            for i in range(len(fingerprint[1])):
                new_tag2 = self.out_text2.search(fingerprint[1][i].substring, '1.0', tk.END, exact=False)
                
                if new_tag2 != '':
                    '''print("2 - " + str(fp_track + 1) + ": " + fingerprint[1][i].substring)'''
                    self.out_text2.tag_add("match" + str(fp_track), new_tag2, str(new_tag2) + "+" + str(len(fingerprint[1][i].substring)) + "c")
                    index_track2 = new_tag2
                else:
                    increment_fp = False
                    '''print("2 - " + str(fp_track + 1) + ": " + fingerprint[1][i].substring)'''
                    '''print("COULD NOT FIND")'''

            if increment_fp:
                fp_track += 1
            else:
                self.out_text1.tag_delete("match" + str(fp_track))
                self.out_text2.tag_delete("match" + str(fp_track))
                remove_fps.append(fingerprint)

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        for rfp in remove_fps:
            fp.remove(rfp)

        self.fp = fp

        self.max_fp = len(self.fp)
        self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        #Show fingerprints
        self.show_reg_fp()

    def gather_most_fingerprints(self):
        '''
        Responsible for gathering most important fingerprints from backend, used for side-by-side comparison.
        '''

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        #k and w from user input
        k = int(self.k_input.get())
        w = int(self.windowSizeInput.get())

        #Two files being compared side-by-side
        file1 = self.f2fp[self.curr_index1].filename
        file2 = self.f2fp[self.curr_index2].filename

        #Output of those files
        file1out = open(file1, 'r').read()
        file2out = open(file2, 'r').read()

        #If the analyzer is set to Java, remove comments from files
        if self.language_var.get() == "Java":
            file1out = remove_comments(file1out)
            file2out = remove_comments(file2out)

        #Python
        if self.language_var.get() == "Python":
            get_most_important_matches_javpy(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2], k, int(self.fp_count_in.get()), int(self.offset_in.get()))

        #Java
        elif self.language_var.get() == "Java":
            get_most_important_matches_javpy(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2], k, int(self.fp_count_in.get()), int(self.offset_in.get()))

        #Text
        else:
            get_most_important_matches_txt(self.f2fp[self.curr_index1], self.f2fp[self.curr_index2], k, 3, 6)

        #If there exist most important matches, use them
        if self.f2fp[self.curr_index2] in self.f2fp[self.curr_index1].mostimportantmatches:
            fp = self.f2fp[self.curr_index1].mostimportantmatches[self.f2fp[self.curr_index2]]
        else:
            fp = []

        #Initialize tags
        for i in range(len(fp)):
            self.out_text1.tag_config("match" + str(i), background='white')
            self.out_text2.tag_config("match" + str(i), background='white')

        #Clear text boxes, and add file outputs
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)
        self.out_text1.insert(tk.END, file1out)
        self.out_text2.insert(tk.END, file2out)

        #Used to progress the search through the file, so multiple instances of the same substring aren't caught.
        index_track1 = '1.0'
        fp_track = 0
        remove_fps = []

        #For each fingerprint
        for fingerprint in fp:

            index_track2 = '1.0'
            increment_fp = True

            new_tag1 = ''
            new_tag2 = ''

            #Parse through all substrings in File 1 for a given fingerprint, tagging them for this fingerprint
            for i in range(len(fingerprint[0])):
                new_tag1 = self.out_text1.search(fingerprint[0], '1.0', tk.END)
                '''print("1 - " + str(fp_track + 1) + ": " + fingerprint[0])'''
                if new_tag1 != '':
                    self.out_text1.tag_add("most" + str(fp_track), new_tag1, str(new_tag1) + "+" + str(len(fingerprint[0])) + "c")
                else:
                    increment_fp = False
                    '''print("COULD NOT FIND")'''

            #Parse through all substrings in File 2 for a given fingerprint, tagging them for this fingerprint
            for i in range(len(fingerprint[1])):
                new_tag2 = self.out_text2.search(fingerprint[1][i], '1.0', tk.END)
                '''print("2 - " + str(fp_track + 1) + ": " + fingerprint[1][i])'''
                if new_tag2 != '':
                    self.out_text2.tag_add("most" + str(fp_track), new_tag2, str(new_tag2) + "+" + str(len(fingerprint[1][i])) + "c")
                    index_track2 = new_tag2
                else:
                    increment_fp = False
                    '''print("COULD NOT FIND")'''    

            #If fingerprints found, progress the search
            if len(self.out_text1.tag_ranges("most" + str(fp_track))) > 0:
                index_track1 = new_tag1

            if increment_fp:
                fp_track += 1
            else:
                self.out_text1.tag_delete("most" + str(fp_track))
                self.out_text2.tag_delete("most" + str(fp_track))
                remove_fps.append(fingerprint)

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        for rfp in remove_fps:
            fp.remove(rfp)

        self.most_fp = fp

        self.max_fp = len(self.most_fp)
        self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

        #Show fingerprints
        self.show_most_fp()

#File Navigation

    def next_file1(self):
        '''
        Responsible for changing to the next file currently being analyzed on the left of the side-by-side
        '''
        self.out_result.configure(state='normal')
        #print("REACHED next_file1. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))

        #Makes sure file isn't identical to the other side, and that index loops around when necessary
        if (self.curr_index1+1) == self.curr_index2:
            self.curr_index1 = self.curr_index1 + 2
        else:
            self.curr_index1 = self.curr_index1 + 1

        if self.curr_index1 >= len(self.f2fp):
            if self.curr_index2 != 0:
                self.curr_index1 = 0
            else:
                self.curr_index1 = 1

        self.out_result.configure(state='disabled')
        self.get_output()

    def next_file2(self):
        '''
        Responsible for changing to the next file currently being analyzed on the right of the side-by-side
        '''
        self.out_result.configure(state='normal')
        #print("REACHED next_file2. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))

        #Makes sure file isn't identical to the other side, and that index loops around when necessary
        if (self.curr_index2+1) == self.curr_index1:
            self.curr_index2 = self.curr_index2 + 2
        else:
            self.curr_index2 = self.curr_index2 + 1

        if self.curr_index2 >= len(self.f2fp):
            if self.curr_index1 != 0:
                self.curr_index2 = 0
            else:
                self.curr_index2 = 1

        self.out_result.configure(state='disabled')
        self.get_output()

    def prev_file1(self):
        '''
        Responsible for changing to the previous file currently being analyzed on the left of the side-by-side
        '''
        self.out_result.configure(state='normal')
        #print("REACHED prev_file1. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))

        #Makes sure file isn't identical to the other side, and that index loops around when necessary
        if (self.curr_index1-1) == self.curr_index2:
            self.curr_index1 = self.curr_index1 - 2
        else:
            self.curr_index1 = self.curr_index1 - 1

        if self.curr_index1 < 0:
            if self.curr_index2 != len(self.f2fp) - 1:
                self.curr_index1 = len(self.f2fp) - 1
            else:
                self.curr_index1 = len(self.f2fp) - 2

        self.out_result.configure(state='disabled')
        self.get_output()

    def prev_file2(self):
        '''
        Responsible for changing to the previous file currently being analyzed on the right of the side-by-side
        '''
        self.out_result.configure(state='normal')
        #print("REACHED prev_file2. curr_index1=" + str(self.curr_index1) + ". curr_index2=" + str(self.curr_index2))

        #Makes sure file isn't identical to the other side, and that index loops around when necessary
        if (self.curr_index2-1) == self.curr_index1:
            self.curr_index2 = self.curr_index2 - 2
        else:
            self.curr_index2 = self.curr_index2 - 1

        if self.curr_index2 < 0:
            if self.curr_index1 != len(self.f2fp) - 1:
                self.curr_index2 = len(self.f2fp) - 1
            else:
                self.curr_index2 = len(self.f2fp) - 2

        self.out_result.configure(state='disabled')
        self.get_output()

#Fingerprint Display

    def show_fp(self):
        '''
        Responsible for calling the correct show function depending on fingerprint mode.
        '''
        if self.fp_type.get() == 0:
            self.show_reg_fp()
        else:
            self.show_most_fp()

    def show_reg_fp(self):
        '''
        Responsible for showing regular fingerprints on screen, whether highlighting all of them, or just the first one.
        '''

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        #View all
        if self.view_var.get() == 1:
            if self.max_fp > 0:
                self.cur_fp = 1
            else:
                self.cur_fp = 0
            for i in range(len(self.fp)):
                self.out_text1.tag_config("match" + str(i), background='yellow')
                self.out_text2.tag_config("match" + str(i), background='yellow')

        #Highlight first one and initialize class variables
        else:
            if self.max_fp > 0:
                self.cur_fp = 1
                
                #Set all others to white background
                for i in range(len(self.fp)):
                    self.out_text1.tag_config("match" + str(i), background='white')
                    self.out_text2.tag_config("match" + str(i), background='white')

                #Raise priority of and highlight first fingerprint
                self.out_text1.tag_config("match0", background='yellow')
                self.out_text2.tag_config("match0", background='yellow')

                self.out_text1.tag_raise("match0")
                self.out_text2.tag_raise("match0")

                #Automatically scroll to it
                if len(self.out_text1.tag_ranges("match0")) > 0:
                    self.out_text1.see(self.out_text1.tag_ranges("match0")[0])
                if len(self.out_text2.tag_ranges("match0")) > 0:
                    self.out_text2.see(self.out_text2.tag_ranges("match0")[0])
                
            else:
                self.cur_fp = 0
            self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(len(self.fp))

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

    def show_most_fp(self):
        '''
        Responsible for showing most important fingerprints on screen, whether highlighting all of them, or just the first one.
        '''

        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        #View all
        if self.view_var.get() == 1:
            if len(self.most_fp) > 0:
                self.cur_fp = 1
            else:
                self.cur_fp = 0
            for i in range(len(self.most_fp)):
                self.out_text1.tag_config("most" + str(i), background='green')
                self.out_text2.tag_config("most" + str(i), background='green')

        #Highlight first one and initialize class variables
        else:
            if len(self.most_fp) > 0:
                self.cur_fp = 1
                
                #Set others to white background
                for i in range(len(self.most_fp)):
                    self.out_text1.tag_config("most" + str(i), background='white')
                    self.out_text2.tag_config("most" + str(i), background='white')

                #Raise priority of and highlight first fingerprint
                self.out_text1.tag_config("most0", background='green')
                self.out_text2.tag_config("most0", background='green')

                self.out_text1.tag_raise("most0")
                self.out_text2.tag_raise("most0")

                #Automatically scroll to it
                self.out_text1.see(self.out_text1.tag_ranges("most0")[0])
                self.out_text2.see(self.out_text2.tag_ranges("most0")[0])
                
            else:
                self.cur_fp = 0
            self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(len(self.most_fp))

        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

#Fingerprint Navigation

    def next_fp(self):
        '''
        Responsible for incrementing to the next fingerprint.
        '''

        #Checks whether working with most important or regular fingerprints
        if self.fp_type.get() == 0:

            #Checks to ensure view all isn't active
            if self.view_var.get() == 0:

                #Checks to ensure there are fingerprints remaining
                if self.cur_fp < self.max_fp:

                    #Set others to white background
                    for i in range(self.max_fp):
                        self.out_text1.tag_config("match" + str(i), background='white')
                        self.out_text2.tag_config("match" + str(i), background='white')

                    #Lower priority of prior fingerprint
                    self.out_text1.tag_lower("match" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("match" + str(self.cur_fp - 1))

                    #Raise priority of and highlight new fingerprint
                    self.out_text1.tag_config("match" + str(self.cur_fp), background='yellow')
                    self.out_text2.tag_config("match" + str(self.cur_fp), background='yellow')

                    self.out_text1.tag_raise("match" + str(self.cur_fp))
                    self.out_text2.tag_raise("match" + str(self.cur_fp))

                    #Autoscrolling
                    self.out_text1.see(self.out_text1.tag_ranges("match" + str(self.cur_fp))[1])
                    self.out_text2.see(self.out_text2.tag_ranges("match" + str(self.cur_fp))[1])

                    #Increment current fingerprint
                    self.cur_fp = self.cur_fp + 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)
        else:

            #Checks to ensure view all isn't active
            if self.view_var.get() == 0:

                #Checks to ensure there are fingerprints remaining
                if self.cur_fp < self.max_fp:

                    #Set others to white background
                    for i in range(self.max_fp):
                        self.out_text1.tag_config("most" + str(i), background='white')
                        self.out_text2.tag_config("most" + str(i), background='white')

                    #Lower priority of prior fingerprint
                    self.out_text1.tag_lower("most" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("most" + str(self.cur_fp - 1))

                    #Raise priority of and highlight new fingerprint
                    self.out_text1.tag_config("most" + str(self.cur_fp), background='green')
                    self.out_text2.tag_config("most" + str(self.cur_fp), background='green')

                    self.out_text1.tag_raise("most" + str(self.cur_fp))
                    self.out_text2.tag_raise("most" + str(self.cur_fp))

                    #Autoscrolling
                    self.out_text1.see(self.out_text1.tag_ranges("most" + str(self.cur_fp))[1])
                    self.out_text2.see(self.out_text2.tag_ranges("most" + str(self.cur_fp))[1])

                    #Increment current fingerprint
                    self.cur_fp = self.cur_fp + 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

    def last_fp(self):
        '''
        Responsible for decrementing to the previous fingerprint.
        '''

        #Checks whether working with most important or regular fingerprints
        if self.fp_type.get() == 0:

            #Checks to ensure view all isn't active
            if self.view_var.get() == 0:

                #Checks to ensure there are fingerprints remaining
                if self.cur_fp > 1:

                    #Set others to white background
                    for i in range(self.max_fp):
                        self.out_text1.tag_config("match" + str(i), background='white')
                        self.out_text2.tag_config("match" + str(i), background='white')

                    #Lower priority of prior fingerprint
                    self.out_text1.tag_lower("match" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("match" + str(self.cur_fp - 1))

                    #Raise priority of and highlight new fingerprint
                    self.out_text1.tag_config("match" + str(self.cur_fp - 2), background='yellow')
                    self.out_text2.tag_config("match" + str(self.cur_fp - 2), background='yellow')

                    self.out_text1.tag_raise("match" + str(self.cur_fp - 2))
                    self.out_text2.tag_raise("match" + str(self.cur_fp - 2))

                    #Autoscrolling
                    self.out_text1.see(self.out_text1.tag_ranges("match" + str(self.cur_fp - 2))[0])
                    self.out_text2.see(self.out_text2.tag_ranges("match" + str(self.cur_fp - 2))[0])
                    
                    #Decrement current fingerprint
                    self.cur_fp = self.cur_fp - 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)
        else:

            #Checks to ensure view all isn't active
            if self.view_var.get() == 0:

                #Checks to ensure there are fingerprints remaining
                if self.cur_fp > 1:

                    #Set others to white background
                    for i in range(self.max_fp):
                        self.out_text1.tag_config("most" + str(i), background='white')
                        self.out_text2.tag_config("most" + str(i), background='white')

                    #Lower priority of prior fingerprint
                    self.out_text1.tag_lower("most" + str(self.cur_fp - 1))
                    self.out_text2.tag_lower("most" + str(self.cur_fp - 1))

                    #Raise priority of and highlight new fingerprint
                    self.out_text1.tag_config("most" + str(self.cur_fp - 2), background='green')
                    self.out_text2.tag_config("most" + str(self.cur_fp - 2), background='green')

                    self.out_text1.tag_raise("most" + str(self.cur_fp - 2))
                    self.out_text2.tag_raise("most" + str(self.cur_fp - 2))

                    #Autoscrolling
                    self.out_text1.see(self.out_text1.tag_ranges("most" + str(self.cur_fp - 2))[0])
                    self.out_text2.see(self.out_text2.tag_ranges("most" + str(self.cur_fp - 2))[0])
                    
                    #Decrement current fingerprint
                    self.cur_fp = self.cur_fp - 1
                    self.current_fp['text'] = "Current: " + str(self.cur_fp) + "/" + str(self.max_fp)

#Misc

    def clear_output(self):
        '''
        Responsible for clearing the output boxes on the GUI, as well as resetting class variables to default/empty states.
        '''

        self.out_result.configure(state='normal')
        self.out_text1.configure(state='normal')
        self.out_text2.configure(state='normal')

        self.out_result.delete('1.0', tk.END)
        self.out_text1.delete('1.0', tk.END)
        self.out_text2.delete('1.0', tk.END)

        for i in range(len(self.fp)):
            self.out_text1.tag_delete('match' + str(i))
            self.out_text2.tag_delete('match' + str(i))

        for i in range(len(self.most_fp)):
            self.out_text1.tag_delete('most' + str(i))
            self.out_text2.tag_delete('most' + str(i))

        self.out_result.configure(state='disabled')
        self.out_text1.configure(state='disabled')
        self.out_text2.configure(state='disabled')

        self.fp = []
        self.f2fp = []
        self.most_fp = []
        self.curr_index1 = 0
        self.curr_index2 = 1
        self.cur_fp = 0
        self.max_fp = 0

    def mult_yview(self, *args):
        '''
        Allows both scroll bars in the side-by-side output to move at the same time.
        '''
        self.out_text1.yview(*args)
        self.out_text2.yview(*args)

    def report(self):
        '''
        Responsible for generating the output report full of at-a-glance results.
        '''

        self.out_result.configure(state='normal')

        total = len(self.f2fp)
        if total != 0:

            self.report_index1 = self.curr_index1 % total
            self.report_index2 = self.curr_index2 % total

            current_time = time.strftime("%Y-%m-%d_%H-%M-%S")

            localreport = fd.asksaveasfile(mode='w', initialdir=os.getcwd(), initialfile='SCAM-report_' + current_time + '.txt', title="Save SCAM report file", filetypes=(("text files", "*.txt"), ("all files", "*.*")))

            for x in self.f2fp:
                for y in self.f2fp:
                    if self.report_index1 == self.report_index2:
                        self.report_index2 = (self.report_index2 + 1) % total
                        continue
                    else:
                        if self.f2fp[self.report_index2] in self.f2fp[self.report_index1].similarto:
                            percentage = "{:.2%}".format(get_similarity(self.f2fp[self.report_index1], self.f2fp[self.report_index2]))
                            localreport.write(str("Files Compared: " + str(self.f2fp[self.report_index1].filename) + " and " + str(self.f2fp[self.report_index2].filename)))
                            localreport.write(str("\nPercentage Similarity: " + str(percentage)))
                            localreport.write(str("\nCommon Fingerprints: " + str(len(self.f2fp[self.report_index1].similarto[self.f2fp[self.report_index2]])) + "\n\n"))
                        self.report_index2 = (self.report_index2 + 1 ) % total

                self.report_index1 = (self.report_index1 + 1) % total

            localreport.close()

            """                
            report.reportname.insert(tk.END, )            
            def clear_file1(self):
                self.file1 = []
                self.file_name1.delete(0, tk.END)
            """
            #localreport.close()


            self.out_result.delete('1.0', tk.END)
            self.out_result.insert(tk.END, "Full Report Generated!\n")

            print(localreport)


        else:
            self.out_result.delete('1.0', tk.END)
            self.out_result.insert(tk.END, "Must Compare files before generating report!")

        self.out_result.configure(state='disabled')

    def openHelp(self):
        
        self.helpSect = tk.Toplevel()#height=800, width=600)
        self.helpSect.title("SCAM Help Manual")
        self.helpSect.geometry("800x600")

        self.hm_lbl = tk.Label(self.helpSect, text="Welcome to the SCAM help manual!", )
        self.hm_lbl.pack(pady = 15)

        self.hm_main = tk.Text(self.helpSect, height='30', width='80', wrap='word')
        self.hm_main.pack()
        self.hm_main.configure(state='normal')

        self.hm_scroll= tk.Scrollbar(self.helpSect, command=self.hm_main.yview)
        self.hm_main['yscrollcommand'] = self.hm_scroll.set

        self.hm_main.insert(tk.INSERT,
"""\n\tOur tool, the Source Code Analyzing Machine, is used to analyze similarity in source code for the purpose of plagiarism detection. It supports the lang- uages of Python and Java, but it can also analyze raw text which can be used for (although may not be as robust) other currently unsupported languages. 
   
                             
Here is some general information to start off...
                                     
    -Ignore Count determines fingerprint threshold for commonality.
    -K-grams (noise threshold) impacts sensitivity. 
    -Window Size is the winnow size used by the algorithm." 
    -Fingerprints size < k will be ignored.
    -Block Size is the number of fingerprints required be to be considered 
        a most important match block
    -Offset is the allowable distance between them for most important matches
    -Number of fingerprints shown at the bottom does not reflect the results 
        of the user's search. This number is calculated via a separate in-depth
        search specifically for the side-by-side comparison, and is also limited 
        by what fingerprints are viewable. It can be larger or smaller than the 
        reported number.


This program was originally built for python software, thus \"*.py\" files are the most likely to produce the best results. 
\n\n\t\t\t***SCROLL DOWN FOR FUTHER INFO***\n\n
""")
        
        #manual        
        for dirpath, dirs, files in os.walk('./'):  
            for filename366 in files: 
                self.ffpath = os.path.join(dirpath,filename366)
                #print("fpath:"+self.ffpath) 
                if self.ffpath.endswith('manual.txt'):     
                    self.manpath = self.ffpath
                    #print("manpath:" + self.manpath)
                    break
        
        self.hm_file = open(self.manpath, 'r', encoding="utf-8").read()

        self.hm_main.insert(tk.INSERT, self.hm_file)
        self.hm_main.configure(state='disable')

        self.donebtn = tk.Button(self.helpSect, text="DONE", command=self.helpSect.destroy).pack()

        self.helpSect.mainloop()


#Main Class

    def __init__(self, master):
        self.master = master
        self.create_widgets()

    def create_widgets(self):

    #Class Variables

        #Store Filenames
        self.files1 = []
        self.files2 = []

        #Tracking Fingerprints
        self.cur_fp = 0
        self.max_fp = 0
        self.fp = []
        self.most_fp = []

        #Tracking Multiple Files
        self.curr_index1 = 0
        self.curr_index2 = 1
        self.f2fp = []

    #Frames/Layout

        self.menubar = tk.Menu(self.master)
        self.menubar.config(font=(None, 9))
        
        self.upper = tk.Frame(self.master)
        self.upper.pack(side = "top", fill='both', pady=5, padx=5)

        self.top_frame = tk.Frame(self.upper)
        self.top_frame.pack(expand=True, side = "left", fill='both', pady=5)

        self.button_panel = tk.Frame(self.upper)
        self.button_panel.pack(side="right", fill='x', padx=10, pady=5)

        self.output_frame = tk.Frame(self.master)
        self.output_frame.pack(expand=True, fill='both', pady=5, side='bottom')

        self.bottom_frame = tk.Frame(self.output_frame)
        self.bottom_frame.pack(expand=True, fill='both', pady=5)

        self.index_btns = tk.Frame(self.bottom_frame)
        self.index_btns.pack(expand=False, fill='x', pady=5, side='bottom')

        self.index_btns1 = tk.Frame(self.index_btns)
        self.index_btns1.pack(expand=True, fill='x', side='left')

        self.index_btns2 = tk.Frame(self.index_btns)
        self.index_btns2.pack(expand=True, fill='x', side='right')

        self.very_bottom = tk.Frame(self.output_frame, width=0, height=5)
        self.very_bottom.pack(expand=False, fill='none', pady=5, side="bottom")

    #Tools Menu

        self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        self.toolsmenu.add_command(label="Generate Report", command=self.report)
        #self.toolsmenu.add_command(label="Check Matches", command=self.donothing)
        #self.toolsmenu.add_command(label="Fingerprint Offest", command=self.donothing)
        self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="Manual", command= self.openHelp)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        #self.toolsmenu = tk.Menu(self.menubar, tearoff=0)
        #self.toolsmenu.add_command(label="Check Matches", command=self.donothing)
        #self.toolsmenu.add_command(label="Fingerprint Offest", command=self.donothing)
        #self.menubar.add_cascade(label="Tools", menu=self.toolsmenu)

        #self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        #self.helpmenu.add_command(label="Manual", command= self.openHelp)
        #self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.master.config(menu=self.menubar)
        
    #Filename Display

        self.file1_frame = tk.Frame(self.top_frame)
        self.file1_frame.pack(side='top', expand=True, fill='both')

        self.file2_frame = tk.Frame(self.top_frame)
        self.file2_frame.pack(side='bottom', expand=True, fill='both')

        #ADDED for bp
        self.bpfile_frame = tk.Frame(self.top_frame)
        self.bpfile_frame.pack(side='bottom', expand=True, fill='both')

        #Filebox 1

        self.cur_file_label1 = tk.Label(self.file1_frame, text = "Student Files: ")
        self.cur_file_label1.pack(anchor='w')
        self.cur_file_label1.config(font=(None, 9))

        self.file_name1 = tk.Listbox(self.file1_frame, height=5, exportselection=False)

        self.file_scroll1 = tk.Scrollbar(self.file1_frame, command=self.file_name1.yview)
        self.file_name1['yscrollcommand'] = self.file_scroll1.set
        self.file_scroll1.pack(expand=False, fill="y", side='right')

        self.file_name1.pack(expand=True, pady=(0, 10), fill='both')

        #Filebox 2

        self.cur_file_label2 = tk.Label(self.file2_frame, text = "Boilerplate Files: ")
        self.cur_file_label2.pack(anchor='w')
        self.cur_file_label2.config(font=(None, 9))

        self.file_name2 = tk.Listbox(self.file2_frame, height=5, exportselection=False)

        self.file_scroll2 = tk.Scrollbar(self.file2_frame, command=self.file_name2.yview)
        self.file_name2['yscrollcommand'] = self.file_scroll2.set
        self.file_scroll2.pack(expand=False, fill="y", side='right')

        self.file_name2.pack(expand=True, fill='both')

    #Button Panel

        #Logo        

        for dirpath, dirs, files in os.walk('./'):  
            for filename365 in files: 
                self.fpath = os.path.join(dirpath,filename365)
                #print("fpath:"+self.fpath) 
                if self.fpath.endswith('SCAM.png'):     
                    self.scampath = self.fpath
                    #print("scampath:" + self.scampath)
                    break
                
        
        logo = tk.PhotoImage(file=self.scampath)
        smallerlogo = logo.subsample(6,6)
        imglabel = tk.Label(self.button_panel, image=smallerlogo)
        imglabel.image = smallerlogo
        imglabel.grid(row=0, column=0, columnspan=4, padx=100)
        
        """
        logo = Image.open("./SCAM.png")
        smallerlogo = logo.resize((round(logo.size[0] * .1), round(logo.size[1] * .1)));
        render = ImageTk.PhotoImage(smallerlogo)
        img = tk.Label(self.button_panel, image=render)
        img.image = render
        img.grid(row=0, column=0, columnspan=4)
        """

        #self.k_desc_label = tk.Label(self.button_panel, text = "K (noise threshold) impacts sensitivity. Fingerprints size < k will be ignored.\nWindow Size is the winnow size used by the algorithm.\nIgnore Count determines fingerprint threshold for commonality.\nPython files should be able to be compiled for the best results.")
        #self.k_desc_label.grid(row=1, column=0, columnspan=4)
        #self.k_desc_label.config(font=(None, 8))

        self.w_desc_label = tk.Label(self.button_panel, text = "Default values set for optimal machine output. \n View Help Manual for more information.")
        self.w_desc_label.grid(row=1, column=0, columnspan=4)
        self.w_desc_label.config(font=(None, 8))

        #self.ignore_label = tk.Label(self.button_panel, text = "Ignore Files: ")
        #self.ignore_label.grid(row=1, column=0)
        #self.ignore_label.config(font=(None, 9))

        #self.file_ignore = tk.Text(self.button_panel, height=1, width=30, state='disabled')
        #self.file_ignore.grid(row=1, column=1, columnspan=4)

        #Add Files

        self.button1 = tk.Button(self.button_panel, text="Add Student Files", command=self.open_file1, bg="gray75", width=20)
        self.button1.grid(row = 2, column = 0, padx = 1, pady = 2, columnspan=2)
        self.button1.config(font=(None, 9))

        self.button1a = tk.Button(self.button_panel, text="Clear Student File(s)", command=self.clear_file1, bg="gray80", width=20)
        self.button1a.grid(row = 2, column = 2, padx = 1, pady = 2, columnspan=2)
        self.button1a.config(font=(None, 9))

        self.button2 = tk.Button(self.button_panel, text="Add Boilerplate Files", command=self.open_file2, bg="gray75", width=20)
        self.button2.grid(row = 3, column = 0, padx =1, pady = 2, columnspan=2)
        self.button2.config(font=(None, 9))

        self.button2a = tk.Button(self.button_panel, text="Clear Boilerplate File(s)", command=self.clear_file2, bg="gray80", width=20)
        self.button2a.grid(row = 3, column = 2, padx = 1, pady = 2, columnspan=2)
        self.button2a.config(font=(None, 9))

        #Language Select/Ignore Count

        self.lang_label = tk.Label(self.button_panel, text = "Language: ")
        self.lang_label.grid(row = 5, column = 0, pady = 10)
        self.lang_label.config(font=(None, 9))

        self.language_var = tk.StringVar(self.button_panel)
        self.language_var.set("Python")
        self.languageMenu = tk.OptionMenu(self.button_panel, self.language_var, "Text", "Python", "Java")
        self.languageMenu.grid(row=5, column=1, pady=10, sticky='w', columnspan=1)
        self.languageMenu.config(font=(None, 9))

        self.ignore_count_label = tk.Label(self.button_panel, text = "Ignore Count: ")
        self.ignore_count_label.grid(row = 5, column = 2, pady = 10)
        self.ignore_count_label.config(font=(None, 9))

        self.ignore_input = tk.Spinbox(self.button_panel, from_=0, to=255, width=5)
        self.ignore_input.grid(row=5, column=3, pady=10)
        self.ignore_input.delete(0, tk.END)
        self.ignore_input.insert(0, '5')
        self.ignore_input.config(font=(None, 9))

        #Advanced

        self.k_label = tk.Label(self.button_panel, text = "K-grams: ")
        self.k_label.grid(row = 7, column = 0, padx = 1, pady = (10,0))
        self.k_label.config(font=(None, 9))

        self.k_input = tk.Spinbox(self.button_panel, from_=1, to=999, width=5)
        self.k_input.grid(row=7, column=1, padx=5, pady = (10,0))

        self.k_input.delete(0, tk.END)
        self.k_input.insert(0, '15')
        self.k_input.config(font=(None, 9))

        self.w_label = tk.Label(self.button_panel, text = "Window Size: ")
        self.w_label.grid(row = 7, column = 2, padx = 1, pady = (10,0))
        self.w_label.config(font=(None, 9))

        self.windowSizeInput = tk.Spinbox(self.button_panel, from_=1, to=999, width=5)
        self.windowSizeInput.grid(row=7, column=3, padx=5, pady = (10,0))
        self.windowSizeInput.config(font=(None, 9))

        self.windowSizeInput.delete(0, tk.END)
        self.windowSizeInput.insert(0, '30')

        self.fp_count_lbl = tk.Label(self.button_panel, text = "Block Size: ")
        self.fp_count_lbl.grid(row = 8, column = 0, padx = 5, pady = 5)
        self.fp_count_lbl.config(font=(None, 9))

        self.fp_count_in = tk.Spinbox(self.button_panel, from_=1, to=999, width=5)
        self.fp_count_in.grid(row=8, column=1, padx=5, pady = 5)
        self.fp_count_in.delete(0, tk.END)
        self.fp_count_in.insert(0, '3')
        self.fp_count_in.config(font=(None, 9))

        self.offset_lbl = tk.Label(self.button_panel, text = "Offset: ")
        self.offset_lbl.grid(row = 8, column = 2, padx = 1, pady = 5, columnspan=1)
        self.offset_lbl.config(font=(None, 9))

        self.offset_in = tk.Spinbox(self.button_panel, from_=1, to=999, width=5)
        self.offset_in.grid(row=8, column=3, padx=0, pady = 5, columnspan=2)
        self.offset_in.delete(0, tk.END)
        self.offset_in.insert(0, '6')
        self.offset_in.config(font=(None, 9))

        self.fp_type = tk.IntVar(self.button_panel)
        self.fp_type.set(0)
        self.fp_menu1 = tk.Radiobutton(self.button_panel, text="All Fingerprints", variable=self.fp_type, value=0)
        self.fp_menu1.grid(row=9, column=0, padx=5, pady=(10,5), columnspan=2)
        self.fp_menu1.config(font=(None, 9))
        self.fp_menu2 = tk.Radiobutton(self.button_panel, text="Important Blocks", variable=self.fp_type, value=1)
        self.fp_menu2.grid(row=9, column=2, padx=(0,10), pady=(10,5), columnspan=2)
        self.fp_menu2.config(font=(None, 9))

        #Compare

        self.run_label = tk.Button(self.button_panel, text="Compare", height = 1, width = 40, command=self.export_files, bg="gray75", bd=3)
        self.run_label.grid(row=11, column=0, pady=(5, 0), columnspan=4)
        self.run_label.config(font=(None, 9))

        self.clear_label = tk.Button(self.button_panel, text="Clear Output", height = 1, width = 40, command=self.clear_output, bg="gray80", bd=3)
        self.clear_label.grid(row=12, column=0, pady=2.5, columnspan=4)
        self.clear_label.config(font=(None, 9))

        #self.report_label = tk.Button(self.button_panel, text="Full Report", height=1, width=40, command=self.report_output, bg="gray80", bd=3)
        #self.report_label.grid(row=11, column=0, pady=2.5, columnspan=4)

    #Output Display

        self.output_frame = tk.Frame(self.bottom_frame)
        self.output_frame.pack(expand=False, fill='x', side='top', padx=10, pady=5)

        self.output_lbl = tk.Label(self.output_frame, text = "Output")
        self.output_lbl.pack()

        self.out_result = tk.Text(self.output_frame, width=1, height=3)
        self.out_result.pack(expand=True, fill="both", side='left', padx=0)
        self.res_scroll = tk.Scrollbar(self.output_frame, command=self.out_result.yview)
        self.out_result['yscrollcommand'] = self.res_scroll.set
        self.res_scroll.pack(expand=False, fill="y", side='left')
        self.out_result.configure(state='disabled')

        self.out_text1 = tk.Text(self.bottom_frame, width=1, height=1)
        self.out_text1.configure(state='disabled')

        self.txt_scroll1 = tk.Scrollbar(self.bottom_frame, command=self.mult_yview)
        self.out_text1['yscrollcommand'] = self.txt_scroll1.set

        self.out_text1.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
        self.txt_scroll1.pack(side='left', padx=(0,10), fill='y', pady=10)

        self.out_text2 = tk.Text(self.bottom_frame, width=1, height=1, )
        self.out_text2.configure(state='disabled')

        self.txt_scroll2 = tk.Scrollbar(self.bottom_frame, command=self.mult_yview)
        self.out_text2['yscrollcommand'] = self.txt_scroll2.set

        self.out_text2.pack(expand=True, fill="both", padx=(10,0),pady=10, side='left')
        self.txt_scroll2.pack(side='left', padx=(0,10), fill='y', pady=10)

    #Next File Buttons

        self.next_filebtn1 = tk.Button(self.index_btns1, text="Compare Next File", command=self.next_file1, bg="gray75", width=15)
        self.next_filebtn1.pack(expand=True, side='right', padx=(5,25), fill='x')

        self.prev_filebtn1 = tk.Button(self.index_btns1, text="Compare Previous File", command=self.prev_file1, bg="gray80", width=15)
        self.prev_filebtn1.pack(expand=True, side='left', padx=(25,5), fill='x')

        self.next_filebtn2 = tk.Button(self.index_btns2, text="Compare Next File", command=self.next_file2, bg="gray75", width=15)
        self.next_filebtn2.pack(expand=True, side='right', padx=(5,25), fill='x')

        self.prev_filebtn2 = tk.Button(self.index_btns2, text="Compare Previous File", command=self.prev_file2, bg="gray80", width=15)
        self.prev_filebtn2.pack(expand=True, side='left', padx=(25,5), fill='x')

    #Very Bottom
        
        self.view_label = tk.Label(self.very_bottom, text="View All?")
        self.view_label.grid(row=0, column=3, padx=(10,0), pady=5)

        self.view_var = tk.IntVar()

        self.view_all = tk.Checkbutton(self.very_bottom, command=self.show_fp, variable=self.view_var)
        self.view_all.grid(row=0, column=4, padx=5, pady=5)

        self.last_fp = tk.Button(self.very_bottom, text="Last Fingerprint", command=self.last_fp)
        self.last_fp.grid(row=0, column=5, padx=5, pady=5)

        self.current_fp = tk.Label(self.very_bottom, text="Current: " + str(self.cur_fp) + "/" + str(self.max_fp))
        self.current_fp.grid(row=0, column=6, padx=5, pady=5)

        self.next_fp = tk.Button(self.very_bottom, text="Next Fingerprint", command=self.next_fp)
        self.next_fp.grid(row=0, column=7, padx=(5, 100), pady=5)

        #self.warning_lbl2 = tk.Label(self.very_bottom, text="")
        #self.warning_lbl2.grid(row=2, column=0, padx=(10,0), pady=5, columnspan=30)
        #self.warning_lbl2.config(font=(None, 8))


def main():
    root = tk.Tk()
    root.geometry("1080x740")
    root.title("Source Code Analyzing Machine")
    gui = SourceAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

