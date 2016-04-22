import scipy.io.wavfile
import numpy as np
import math
import sys

class PCP:
    
    def __init__(self):
        self.note_references = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
        self.results = [[]]
        
    
    def create_fft(self, filename):
        self.rate, self.data = scipy.io.wavfile.read('horn_sample.wav')
        
        self.frames = self.data.size
        print "Number of Frames: ", self.frames
        
        print "Rate: ", self.rate
        
        self.samples = self.frames/self.rate
        print "Number of samples: ", self.samples
        
        self.fft_results = np.fft.rfft(self.data) ##fft computing and normalization
        #raw_input()
    
    
    # The work of the following classes was almost entirely based on a
    # thread in DSP.  Here is the link to the particular article
    # http://dsp.stackexchange.com/questions/13722/pitch-class-profiling
    # This function returns the values of the notes given the spectrograph
    def m_func(self, l, p):
        #M(l) = round(12 * log_2( (f_s*l)/(N*f_ref) ) ) % 12
        #print "L: ", l
        l = l.real
        #print "Real L: ", l
        #print "Note: ", p
        a = self.rate * l
        b = self.frames * self.note_references[p]
        c = 12 * np.log2(a/b)
        #print "What note, times 12, log2: ", c
        d = -1 * np.round(c)
        #print "After rounding, ", d
        e = d % 12
        #print "Mod by 12!: ", e
        #raw_input()
        return e


    def pcp(self, p, j): 
        r = 0
        starting = j * self.rate
        #print "Starting set: ", starting
        ending = starting + self.rate
        if(ending > self.frames): ending = self.frames
        #print "Ending set: ", ending
        #raw_input()
        for l in self.fft_results[ starting : ending ]:
            result = self.m_func(l[0], p)
            #print "actual returned result", result
            if result == p:
                r+=1
                #print "There was a match!  Add it!"
        return r

    
    def calculate_PCP(self):
        for j in range(0,self.samples):
            self.results.append([])
            for p in range(0,11): #for all 12 notes
                self.results[j].append(self.pcp(p,j))


    def print_results(self):
        for i in range(0,self.samples):
            print "Second: ", i, " : ", self.results[i]


def main():
    m = PCP()
    m.create_fft("fmin.wav")
    m.calculate_PCP()
    m.print_results()


if __name__ == '__main__':
    main()
