import time
import pickle
import bci
import stimulations

def main():

    valance_class = pickle.load(open('valance_class.sav', 'rb'))
    # initialise BCI parameters
    bci.init_bci("Synthetic") # Use this for synthetically generated test data
    # bci.init_bci("Cyton") # Use this when using the actual bci
    bci.datalogging = True
    stimulations.psychra_pump_init()

    # MAIN LOOP #
    while True:
        
        time.sleep(5) 
        bci.update_data(bci.eeg_channels_psychra) # prompts the BCI to pull any new data from the data buffer
        bands = bci.get_bands(bci.data, bci.eeg_channels_psychra)
        concentration = bci.get_concentration(bands)
        valance = bci.get_valance_bands(bci.data, valance_class)
        emotion = bci.get_emotion(valance, concentration)

        print("concentration: ", concentration)
        print("valance: ", valance)
        print("emotion: ", emotion)

        if emotion == "Stressed":
            stimulations.psychra_stimulate()

if __name__ == "__main__":
    main()


# for each 5 second epoch : raw -> z score normalise -> chip between -3 and 3 -> get (alpha/rest of the spectrum) / (theta/rest of the spectrum). 