from PCP import PCP

def main():
    m = PCP()
    m.create_fft("fmin.wav")
    m.calculate_PCP()
    m.print_results()
    
if __name__ == '__main__':
    main()