import time
import bci
import stimulations
from threading import Thread

is_stimulating = False

def stimulation_thread():
    stimulations.pre_psychra_stimulate()

def main():
    # initialise BCI parameters
    # bci.init_bci("Synthetic") # Use this for synthetically generated test data
    bci.init_bci("Cyton") # Use this when using the actual bci
    bci.datalogging = True
    stimulations.psychra_pump_init()
    thread_2 = Thread(target= stimulation_thread)
    thread_2.start()
    thread_2.join

    # MAIN LOOP #
    while True:
        time.sleep(5)
        bci.update_data(bci.eeg_channels_psychra) # prompts the BCI to pull any new data from the data buffer

if __name__ == "__main__":
    main()
    
