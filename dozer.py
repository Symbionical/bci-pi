import time
import pickle
import bci
import stimulations

def main():

    threshold_summation = 0
    cooldown = 0
    sleepy_class = pickle.load(open('sleepy_class.sav', 'rb'))
    # initialise BCI parameters
    # bci.init_bci("Synthetic") # Use this for synthetically generated test data
    bci.init_bci("Cyton") # Use this when using the actual bci
    bci.datalogging = True

    # MAIN LOOP #
    while True:
        
        time.sleep(10) 
        bci.update_data(bci.eeg_channels_dozer) # prompts the BCI to pull any new data from the data buffer
        # sleepiness = bci.get_sleepieness(sleepy_class)
        alpha_theta = bci.get_alpha_theta_ratio(bci.data, bci.eeg_channels_dozer)
        mean_alpha_theta = alpha_theta.mean(axis=1)

        print('Cooldown: %s' % str(cooldown))

        # update cooldown
        if cooldown > 0:
            cooldown -= 5

        print(mean_alpha_theta)

        if mean_alpha_theta < 1.0:
            threshold_summation += 1
        else:
            threshold_summation = 0

        # if sleepiness == 0:
        #     print("not sleepy")

        # if sleepiness == 1:
        #     print("sleepy")

        # if user is sleepy and cooldown is not active, begin stimulation and activate cooldown
        if threshold_summation == 3 and cooldown == 0:
            stimulations.stimulate_all()
            cooldown = 28800 #28800 seconds = 480 minutes = 8 hours. Lets the user sleep

if __name__ == "__main__":
    main()


# for each 5 second epoch : raw -> z score normalise -> chip between -3 and 3 -> get (alpha/rest of the spectrum) / (theta/rest of the spectrum). 