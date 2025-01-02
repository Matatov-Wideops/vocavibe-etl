import os
from os.path import join, exists
import re
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm
import parselmouth
from parselmouth.praat import call
from scipy.io import wavfile

from src.settings import Settings

# import sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


# from src.utils.logger import get_logger, FileException
# from src.utils.helper import *
# from src.settings.settings import Settings
# from src.datasets.filenamePatterns import Patterns, extract_from_filename
# from src.datasets.database import Users, DbColumns, DemoUsernames
# from src.datasets.resolve.resolve import *
# from src.users.utils import patients_phone_numbers_from_xls


'''
For each user listed, extract the demographic data, and for each recording extract the features
'''



                    

def standardize_ataxia(term):
    match = re.search(r'ataxia\s*(\d+)', term, re.IGNORECASE)
    if match:
        number = match.group(1)
        return f'Ataxia {number}'
    else:
        return term


def get_demographic_data(session: pd.Series) -> pd.DataFrame:
    '''I need to add here - 
    Age, sex, smoke...

    '''
    return session



def trim_sound(
    sound: parselmouth.Sound, threshold: int = 25, min_pitch: int = 50
) -> parselmouth.Sound:
    """
    Trim silent segments from the beginning and end of a sound signal.

    Parameters:
    - sound: Parselmouth Sound object.
    - threshold: intensity threshold below which the sound is considered silent.

    Returns:
    - trimmed_sound: Parselmouth Sound object after trimming.
    """

    intensity = sound.to_intensity(min_pitch)

    # Use numpy's pitchay functionality to find where the intensity goes above the threshold
    times = intensity.xs()
    intensity_values = intensity.values[0, :]

    # Find the start and end times above threshold
    start_time = times[intensity_values > threshold][0]
    end_time = times[intensity_values > threshold][-1]

    # Trim the sound object
    trimmed_sound = sound.extract_part(from_time=start_time, to_time=end_time)

    return trimmed_sound


def get_pitch(
    sound: parselmouth.Sound,
    time_step: float = 0.01,
    min_pitch: int = 75,
    max_pitch: int = 600,
) -> np.ndarray:
    
    pitch = parselmouth.praat.call(
        sound, "To Pitch", time_step, min_pitch, max_pitch
    )  # Arguments are: time step, minimum pitch, and maximum pitch
    pitch_values = np.array(pitch.selected_array["frequency"])
    return pitch_values


def get_intensity(
    sound: parselmouth.Sound, min_pitch: int = 50, time_step: float = 0.01
) -> np.ndarray:
    intensity = parselmouth.praat.call(sound, "To Intensity", min_pitch, time_step)
    # Convert intensity data to numpy array
    intensity_values = np.array(intensity.values.T)
    return intensity_values


def get_vu_segments(
    sound: parselmouth.Sound,
) -> tuple[list[list[int]], list[list[int]]]:
    pitch = get_pitch(sound, time_step=0.01)
    # Identify the points where the array changes (from zero to non-zero or vice versa)
    change_points = np.where(np.diff(np.sign(pitch)))[0] + 1
    # Start and end indices for each segment
    start_end_pairs: np.ndarray = np.column_stack(
        (
            np.concatenate(([0], change_points)),  # type: ignore
            np.concatenate((change_points, [len(pitch)])),  # type: ignore
        )
    )

    segments = []
    for start, end in start_end_pairs:
        segment = list(range(start, end))
        segments.append(segment)

    U = [seg for seg in segments if pitch[seg[0]] == 0]
    V = [seg for seg in segments if pitch[seg[0]] > 0]
    return V, U



def pitch_to_semitones(pitch: np.ndarray) -> np.ndarray:
    """Return the number of semitones between the reference frequency and the target frequency."""
    A4 = 440.0
    C0 = A4 * 2 ** (-4.75)
    return 12 * np.log2(pitch / C0)



def meanF0(filename: str, trim=False) -> float:
    sound = parselmouth.Sound(filename)
    if trim:
        sound = trim_sound(sound)
    pitch = get_pitch(sound)
    return np.mean(pitch)



def jitter(filename: str, trim=False) -> float:
    sound = parselmouth.Sound(filename)
    if trim:
        sound = trim_sound(sound)
    pitch = get_pitch(sound)
    absolute_diff = np.abs(np.diff(pitch))
    jitter = 100 * np.mean(absolute_diff) / np.mean(pitch)
    return jitter
    


def shimmer(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    intensity = get_intensity(sound)
    intensity = intensity.squeeze()
    diffs = np.abs(np.diff(intensity))
    return 100 * np.mean(diffs) / np.mean(intensity)



def frequencyVariability(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    pitch = get_pitch(sound)
    semi = pitch_to_semitones(pitch[pitch != 0])
    return np.std(semi[semi > 0])



def intensityMean(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    intensity = get_intensity(sound)
    return intensity.mean()



def intensityVariability(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    intensity = get_intensity(sound)
    return intensity.std()



def formantF1(filename: str, size_frame = 0.025, time_shift = 0.01) -> float:
    sound = parselmouth.Sound(filename)
    formant = sound.to_formant_burg(time_step=time_shift, window_length=size_frame)
    F1 = []

    for time in np.arange(0, sound.duration, time_shift):
        f1 = formant.get_value_at_time(1, time)
        if not np.isnan(f1): # Ensure formant values are valid
            F1.append(f1)
    
    # Convert lists to numpy arrays
    F1 = np.asarray(F1)
    
    return F1.mean()



def formantF2(filename: str, size_frame = 0.025, time_shift = 0.01) -> float:
    sound = parselmouth.Sound(filename)
    formant = sound.to_formant_burg(time_step=time_shift, window_length=size_frame)
    F2 = []

    for time in np.arange(0, sound.duration, time_shift):
        f2 = formant.get_value_at_time(2, time)
        if not np.isnan(f2): # Ensure formant values are valid
            F2.append(f2)
    
    # Convert lists to numpy arrays
    F2 = np.asarray(F2)
    
    return F2.mean()



def numV(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    return len(V)


def lenV(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    lens = [len(v) for v in V]
    return np.mean(lens)


def regV(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    lens = [len(v) for v in V]
    return np.std(lens)


def numU(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    return len(U)


def lenU(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    lens = [len(u) for u in U]
    return np.mean(lens)


def regU(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    lens = [len(u) for u in U]
    return np.std(lens)


def percentageU(filename: str) -> float:
    sound = parselmouth.Sound(filename)
    V,U = get_vu_segments(sound)
    lensU = [len(u) for u in U]
    lensV = [len(v) for v in V]
    return sum(lensU) / (sum(lensU) + sum(lensV))


def silence_length(filename):
    try:
        # Read the wav file
        sample_rate, data = wavfile.read(filename)
        
        # Normalize the data (assuming it's stereo or mono audio)
        if len(data.shape) > 1:
            data = data.mean(axis=1)
        
        # Threshold for considering silence (assuming 16-bit PCM)
        silence_threshold = 500
        
        # Find the first point where the sound exceeds the silence threshold
        non_silence_index = np.argmax(np.abs(data) > silence_threshold)
        
        # Calculate the silence length in seconds
        silence_length = non_silence_index / sample_rate
        return silence_length
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None


analysis = {'vowels': [jitter, shimmer, frequencyVariability, intensityMean, intensityVariability, meanF0, formantF1, formantF2 ,lenV, numU, percentageU, silence_length],
            'ddk': [frequencyVariability, intensityMean, intensityVariability, meanF0, numV, lenV, regV, numU, lenU, regU, percentageU, silence_length],
            'talk': [frequencyVariability, intensityMean, intensityVariability, meanF0, numV, lenV, regV, numU, lenU, regU, percentageU, silence_length]}

tasks = {'vowels': ['mpt1', 'mpt2', 'mpt3', 'iii1', 'iii2', 'uuu1', 'uuu2', 'glissandoup', 'glissandodn'],
         'ddk': ['pataka','dana','bama','papa','kala',],
         'talk': ['1210','sen1','sen2','sen3','sen4','reading1','reading2','question','feedback']}


def extract_features():
    # Load the dataframe with file data
    df = pd.read_csv(Settings.ALL_FILES, dtype=str)
    
    # Filter the dataframe for rows where the pattern is 'RECORDING' or 'RECORDING1'
    df = df[df['pattern'].isin(['RECORDING', 'RECORDING1'])]

    # Initialize the feature columns in the dataframe for each analysis function
    for analysis_type in analysis.values():
        for func in analysis_type:
            df[func.__name__] = np.nan  # Initialize the columns for each function

    # Process each file row in the dataframe
    for idx, row in tqdm(df.iterrows(), total=len(df)):
        exercise = row['exercise']
        filekey = row['filekey']
        filename = join(Settings.BASE_PATH,filekey)
        if exists(filename):
            # Determine the analysis type (vowels, ddk, or talk) based on the exercise name
            for task_type, exercises in tasks.items():
                if exercise in exercises:
                    # Get the corresponding analysis functions for this task type
                    analysis_functions = analysis[task_type]

                    # Extract features by applying each function in the analysis list
                    for func in analysis_functions:
                        
                        try:
                            # Assume each function takes a filekey as input and returns a result
                            feature_value = func(filename)
                            
                            # Store the feature value in the corresponding column
                            df.at[idx, func.__name__] = feature_value
                            # print(f"Successful processing {filekey} with function {func.__name__}")
                        except Exception as e:
                            # print(filename)
                            print(f"Error processing {filekey} with function {func.__name__}: {e}")
    df.to_csv(Settings.FEATURES, index=False)







if __name__ == "__main__":
#    extract_features()
    pass