from enum import Enum
from typing import Dict


class Bucket(str, Enum):
    FILEKEY = 'filekey'
    USERNAME = 'username'
    HEALTHY = 'healthy_name'
    ENTITY = 'entity'
    SESSION = 'session'
    SAMPLER = 'sampler_phone'
    PATTERN = 'pattern'
    EXERCISE = 'exercise'
    TIMING = 'timing'
    ONMED = 'onmed'
    ONOFF = 'onoff'
    LANG = 'language'
    DATE = 'date'
    TIME = 'time'
    DATETIME = 'datetime'
    FILESIZE = 'filesize'

    @classmethod
    def values(cls):
        return [member.value for member in cls]
    


class Qnnrs(str, Enum):
    UPDRS1 = 'updrs1'
    UPDRS2 = 'updrs2'
    UPDRS3 = 'updrs3'
    UPDRS4 = 'updrs4'
    HY = 'H&Y'
    MOCA = 'moca'
    PDQ8 = 'pdq8'
    FOG = 'fog'
    SDQ = 'sdq'
    WOQ_PRE = 'woq_pre'
    WOQ_POST = 'woq_post'

    @classmethod
    def values(cls):
        return [member.value for member in cls]



class Registration(str, Enum):
    SAMPLER = 'sampler_phone'
    HEALTHY = 'healthy_name'
    BIRTHDATE = 'birth_date'
    GENDER = 'gender'
    MOTHER_TONGUE = 'mother_tongue'
    YEAR = 'year_of_diagnosis'
    RESP = 'respiratory_disorders'
    SMOKING = 'smoking_routine'
    DBS = 'dbs'
    CENTER = 'medical_center'
    SLEEP_TALK = 'sleep_talk'
    CONSTIPATION = 'constipation'
    FALLING = 'falling'
    SMELL = 'smell'
    GENETIC = 'genetic'

    @classmethod
    def values(cls):
        return [member.value for member in cls]
    


class ExtraCols(str, Enum):
    SAMPLER_USERNAME = 'sampler_username'
    USER_PHONE = 'user_phone'
    HEBREW = 'Hebrew'
    PASSWORD = 'password'
    CAREGIVER_PHONE = 'caregiver_phone'
    SESSION_NUMBER = 'session_number'

    @classmethod
    def values(cls):
        return [member.value for member in cls]
    


class Update(str, Enum):
    IS_DBS = 'is_dbs'
    IS_SMOKING = 'is_change_in_smoking_routine'
    SMOKING = 'smoking_routine'
    IS_PAROXYSMAL = 'is_paroxysmal'
    VOCAL_CORDS = 'is_vocal_cords_damage'
    CHANGE_VOICE = 'is_change_in_voice'
    TREATED = 'is_treated'
    PRACTICING = 'is_practicing'
    SATISFIED = 'is_satisfied'
    CHANGE_MEDICATION = 'is_change_in_medication'

    @classmethod
    def values(cls):
        return [member.value for member in cls]
    



class Timing(str, Enum):
    POST = "post"
    PRE = "pre"
    UNKNOWN = "unknown"
    HEALTHY = "healthy"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class Language(str, Enum):
    HEBREW = "he"
    ENGLISH = "en"
    ARABIC = "ar"
    RUSSIAN = "ru"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class AllRecordType(str, Enum):
    MPT1 = "mpt1"
    MPT2 = "mpt2"
    MPT3 = "mpt3"

    AAA1 = "aaa1"
    AAA2 = "aaa2"
    AAA3 = "aaa3"

    EEE1 = "eee1"
    EEE2 = "eee2"
    EEE3 = "eee3"

    III1 = "iii1"
    III2 = "iii2"
    III3 = "iii3"

    OOO1 = "ooo1"
    OOO2 = "ooo2"
    OOO3 = "ooo3"

    UUU1 = "uuu1"
    UUU2 = "uuu2"
    UUU3 = "uuu3"

    ONE_TO_TEN = "1210"

    PATAKA = "pataka"
    BAMA = "bama"
    DANA = "dana"
    KALA = "kala"
    PAPA = "papa"
    SEN1 = "sen1"
    SEN2 = "sen2"
    SEN3 = "sen3"
    SEN4 = "sen4"

    GLISSANDO_UP = "glissandoup"
    GLISSANDO_DN = "glissandodn"

    READING1 = "reading1"
    READING2 = "reading2"
    READING3 = "reading3"
    READING4 = "reading4"
    READING5 = "reading5"

    QUESTION = "question"
    FEEDBACK = "feedback"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class Exercise(str, Enum):
    MPT1 = "mpt1"
    MPT2 = "mpt2"
    MPT3 = "mpt3"
    III1 = "iii1"
    III2 = "iii2"
    UUU1 = "uuu1"
    UUU2 = "uuu2"
    ONE_TO_TEN = "1210"
    PATAKA = "pataka"
    BAMA = "bama"
    DANA = "dana"
    KALA = "kala"
    PAPA = "papa"
    SEN1 = "sen1"
    SEN2 = "sen2"
    SEN3 = "sen3"
    SEN4 = "sen4"
    GLISSANDO_UP = "glissandoup"
    GLISSANDO_DN = "glissandodn"
    READING1 = "reading1"
    READING2 = "reading2"
    QUESTION = "question"
    FEEDBACK = "feedback"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class FeelOnOff(str, Enum):
    ON = "ON"
    OFF = "OFF"
    UNKNOWN = "unknown"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class SurveyType(str, Enum):
    PDQ8 = "PDQ8"
    UPDRS = "UPDRS"
    MOCA = "MOCA"
    FOG = "FOG"
    SDQ = "SDQ"
    WOQ = "WOQ"
    MEDICATIONS = "MEDICATIONS"

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class OnMed(str, Enum):
    ONMED = "onMed"
    NOTONMED = "notOnMed"
    UNKNOWN = "unknown"

    @classmethod
    def values(cls):
        return [member.value for member in cls]



class SamplerQnnrs(Dict, Enum):
    UPDRS3_PRE = {'exercise': 'updrs3', 'timing': Timing.PRE, 'marker': 'UPDRS3'}
    UPDRS124 = {'exercise': 'updrs124', 'timing': Timing.UNKNOWN, 'marker': 'UPDRS124'}
    MOCA = {'exercise': 'moca', 'timing': '', 'marker': 'MoCA'}
    PDQ8 = {'exercise': 'pdq8', 'timing': '', 'marker': 'PDQ8'}
    MEDICATIONS = {'exercise': 'medications', 'timing': '', 'marker': 'Meds'}
    UPDRS3_POST = {'exercise': 'updrs3', 'timing': Timing.POST, 'marker': 'UPDRS3'}    

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class PatientQnnrs(str, Enum):
    FOG = 'fog'
    SDQ = 'sdq'
    WOQ = 'woq'
    UPDATE = 'update'

    @classmethod
    def values(cls):
        return [member.value for member in cls]


class UPDRS(Enum):
    updrs1 = [
        'cognitive_impairment',
        'hallucinations_and_delusions',
        'depressed_mood',
        'anxious_mood',
        'apathy',
        'dopamine_dysregulation_syndrome',
        'sleep_problems',
        'daytime_sleepiness',
        'pain_and_other_sensations',
        'urinary_problems',
        'constipation_problems',
        'light_headedness_on_standing',
        'fatigue',
    ]

    updrs2 = [
        'speech_daily',
        'saliva',
        'chewing_and_swallowing',
        'eating_tasks',
        'dressing',
        'hygiene',
        'handwriting',
        'hobbies',
        'turning_in_bed',
        'tremor',
        'getting_out_of_bed',
        'walking_and_balance',
        'freezing',
    ]

    updrs3 = [
        'speech',
        'facial_expression',
        'rigidity_neck',
        'rigidity_rue',
        'rigidity_lue',
        'rigidity_rle',
        'rigidity_lle',
        'finger_tapping_right',
        'finger_tapping_left',
        'hand_movements_right',
        'hand_movements_left',
        'pronation_supination_right',
        'pronation_supination_left',
        'toe_tapping_right',
        'toe_tapping_left',
        'leg_agility_right',
        'leg_agility_left',
        'arising_from_chair',
        'gait',
        'freezing_of_gait',
        'postural_stability',
        'posture',
        'global_spontaneity_of_movement',
        'postural_tremor_right',
        'postural_tremor_left',
        'kinetic_tremor_right',
        'kinetic_tremor_left',
        'rest_tremor_amplitude_rul',
        'rest_tremor_amplitude_lul',
        'rest_tremor_amplitude_rll',
        'rest_tremor_amplitude_lll',
        'rest_tremor_amplitude_lip',
        'rest_tremor_amplitude_jaw',
        'consistency_of_rest_tremor',
        'hoehn_and_yahr'
    ]

    updrs4 = [
        'time_spent_with_dyskinesia',
        'functional_impact_of_dyskinesias',
        'motor_fluctuations',
        'functional_impact_of_fluctuations',
        'complexity_of_motor_fluctuations',
        'off_dystonia',
    ]

    hy = 'hoehn_and_yahr'



class MoCA(list, Enum):
    moca = [
        'line_connection',
        'square_drawing',
        'clock_circumference',
        'clock_numbers',
        'clock_hands',
        'lion',
        'rhinoceros',
        'camel',
        'repeat_the_numbers_21854',
        'repeat_the_numbers_742',
        'tap_their_hand_every_time_the_letter_a',
        'serial_subtraction_from_100',
        'john_sentence',
        'cats_and_dogs_sentence',
        'words_with_the_letter_f',
        'train_and_bicycle',
        'watch_and_ruler',
        'delayed_face',
        'delayed_velvet',
        'delayed_church',
        'delayed_dasy',
        'delayed_red',
        'day_month',
        'month',
        'year',
        'day_week',
        'place',
        'city',
        'is_12_years_or_less',
    ]



class PDQ8(list, Enum):
    pdq8 = [
        'difficulty_getting_around_in_public',
        'dressing_yourself',
        'felt_depressed',
        'problems_with_personal_relationships',
        'unable_to_communicate',
        'problems_concentration',
        'muscle_cramps',
        'embarrassed_in_public',
    ]

    

class FOG(list, Enum):
    fog = [
        'do_you_walk',
        'gait_difficulties_affecting_daily_activities',
        'feet_glued_to_the_floor',
        'longest_freezing_episode',
        'typical_start_hesitation_episode',
        'typical_turning_hesitation',
    ]


    
class SDQ(list, Enum):
    sdq = [
        'difficulty_chewing',
        'food_residues',
        'out_from_nose',
        'dribbling',
        'drooling',
        'swallow_several_times',
        'difficulty_swallowing_solids',
        'difficulty_swallowing_puree',
        'lump_in_throat',
        'cough_while_swallowing_liquids',
        'cough_while_swallowing_solids',
        'change_in_voice_after_eating',
        'coughing_as_a_result_of_saliva',
        'difficulty_breathing_during_meals',
        'respiratory_infection',
    ]



    
class WOQ(list, Enum):
    pre = [
        'reduced_dexterity_pre',
        'muscle_cramping_pre',
        'cloudy_mind_or_slowness_of_thinking_pre',
        'difficulty_in_speech_pre',
        'pain_pre',
        'tremor_pre',
        'slowness_of_movement_pre',
        'stiffness_pre',
        'anxiety_or_panic_pre',
        'mood_changes_pre',
        'difficulty_in_swallowing_pre',
    ]

    post = [
        'reduced_dexterity_post',
        'muscle_cramping_post',
        'cloudy_mind_or_slowness_of_thinking_post',
        'difficulty_in_speech_post',
        'pain_post',
        'tremor_post',
        'slowness_of_movement_post',
        'stiffness_post',
        'anxiety_or_panic_post',
        'mood_changes_post',
        'difficulty_in_swallowing_post',
    ]




patient = ['username',
            'sampler_phone',
            'birth_date',
            'language',
            'gender',
            'mother_tongue',
            'diagnosed_condition',
            'year_of_diagnosis',
            'respiratory_disorders',
            'is_change_in_smoking_routine',
            'smoking_routine',
            'dbs',
            'medical_center',
            'genetic',
            'is_dbs',
            'is_paroxysmal',
            'is_vocal_cords_damage',
            'is_change_in_voice',
            'is_treated',
            'is_practicing',
            'is_satisfied',
            'session',
            'is_change_in_medication',
            ]

healthy = ['username',
            'healthy_name',
            'sampler_phone',
            'birth_date',
            'language',
            'gender',
            'mother_tongue',
            'smoking_routine',
            'sleep_talk',
            'constipation',
            'falling',
            'smell',
            'genetic',
]


ataxia = ['username',
            'healthy_name',
            'sampler_phone',
            'birth_date',
            'language',
            'gender',
            'mother_tongue',
            'smoking_routine',
            'genetic',
]



class Entity:
    PD = "PD"
    HC = "HC"
    AX = "AX"
    SA = "sampler"



Durations = {
    'mpt1': 6,
    'mpt2': 6,
    'mpt3': 6,
    'aaa1': 2,
    'aaa2': 2,
    'aaa3': 2,
    'eee1': 2,
    'eee2': 2,
    'eee3': 2,
    'iii1': 2,
    'iii2': 2,
    'iii3': 2,
    'ooo1': 2,
    'ooo2': 2,
    'ooo3': 2,
    'uuu1': 2,
    'uuu2': 2,
    'uuu3': 2,
    '1210': 10,
    'pataka': 5,
    'dana': 5,
    'bama': 5,
    'papa': 5,
    'kala': 5,
    'sen1': 4,
    'sen2': 4,
    'sen3': 4,
    'sen4': 4,
    'glissandoup': 4,
    'glissandodn': 4,
    'reading1': 45,
    'reading2': 45,
    'reading3': 45,
    'reading4': 45,
    'reading5': 45,
    'question': 30,
    'feedback': 30,
}
    

class SpecialUsers(str, Enum):
    archive = '24b3c5819103f797f612714f143eccff34974b0b'
    archive_hc = 'hc_24b3c5819103f797f612714f143eccff34974b0b'
    demo = '0e7fe052a970524bf667d3bae82030a3fec89fe1'
    demo_hc = 'hc_0e7fe052a970524bf667d3bae82030a3fec89fe1'

    @classmethod
    def values(cls):
        return [member.value for member in cls]