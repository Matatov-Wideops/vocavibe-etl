class Settings():
    BASE_PATH = '/home/alon/dev/bucket/'
    BUCKET_NAME = 'vocabucket'

    RESOURCE_BUCKET_NAME = 'vocavibe-source'
    # Resources

    SAMPLERS_CSV = 'resources/samplers.csv'
    USERS_YAHAV_CSV = 'resources/users_yahav.csv'
    USERSPD = 'resources/userspd.csv'
    USERSHC = 'resources/usershc.csv'
    HC_PHONES_CSV = 'resources/healthy_phone_numbers.csv'
    SHEBA_DATABASE  = 'resources/sheba.csv'
    ICHILOV_DATABASE = 'resources/ichilov.csv'

    # log
    USERS_EC2_CSV = 'log/users_ec2.csv'
    HC_EC2_CSV = 'log/hc_ec2.csv'
    REPLACEMENTS = 'log/replace_attributes.csv'
    BLACKLIST = 'log/blacklist.csv'
    UPDATE_SESSIONS = 'log/update_session.csv'
    DROPOUT = 'log/dropout.csv'
    RESOLVED_SESSIONS = 'log/resolved_sessions.csv'
    SOURCE_CSV = 'log/source/gal/send_passwords 28112024.csv'
    OPENED_HC = 'log/opened_hc.csv'
    DEMO_USERS = 'log/demo_users.csv'
    CHANGED_PASSWORDS = 'log/changed_passwords.csv'
    CONFIG = 'src/config.yaml'
    OPEN_HEALTHY = 'log/open_healthy.csv'
    FORM_CSV = 'log/source/healthy/newhc15122024.csv'

    # Raw data
    BUCKET_CSV = 'results/raw/bucket.csv' 
    RAW_CSV = 'results/raw/raw.csv' 
    UPDRS_CSV = 'results/raw/updrs.csv'
    MOCA_CSV = 'results/raw/moca.csv'
    PDQ8_CSV = 'results/raw/pdq8.csv'
    FOG_CSV = 'results/raw/fog.csv'
    SDQ_CSV = 'results/raw/sdq.csv'
    WOQ_CSV = 'results/raw/woq.csv'
    REGISTRATION_CSV = 'results/raw/registration.csv'
    UPDATE_CSV = 'results/raw/update.csv'
    MEDICATION_CSV = 'results/raw/medication.csv'


    # Resloved and merged data
    ALL_FILES = 'results/csv/all_files.csv'
    SESSIONS = 'results/csv/sessions.csv'
    REAL_SESSIONS = 'results/csv/real_sessions.csv'
    ALL_USERS = 'results/csv/all_users.csv'
    COLORED_SESSIONS = 'results/csv/colored_sessions.xlsx'
    SEND_PASSWORDS = 'results/csv/send_passwords.csv'
    QUERY = 'results/queries/plots_{}.pdf'
    BROKEN_SESSIONS = 'results/csv/broken_sessions.csv'
    RECORDINGS = 'results/csv/recordings.csv'
    QNNRS = 'results/csv/questionnaires.csv'
    REQUEST4DETAILS = 'resources/details_request_healthy.csv'
    FEATURES = 'results/csv/features.csv'

    TIME_FORMAT = '%H:%M:%S'
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME = '%Y-%m-%d_%H:%M:%S'
    FORM_DATETIME = '%d/%m/%Y %H:%M:%S'
    



