import pandas as pd
from typing import List, Tuple, Literal, Union

from src.settings import Settings
from src.database import Bucket, Registration, Update, Qnnrs, Entity




def remove_usernames(raw: pd.DataFrame) -> pd.DataFrame:
    bl = pd.read_csv(Settings.BLACKLIST, dtype=str)
    users = bl.loc[bl['category']=='user','entry'].tolist()
    rows = raw[raw.username.isin(users)]
    if not rows.index.empty:
        raw = raw.drop(rows.index)
        raw = raw.reset_index(drop=True)
    return raw
    


def remove_sessions(raw: pd.DataFrame) -> pd.DataFrame:
    bl = pd.read_csv(Settings.BLACKLIST, dtype=str)
    users = bl.loc[bl['category']=='session', 'username'].tolist()
    sessions = bl.loc[bl['category']=='session', 'entry'].tolist()
    for user,session in zip(users,sessions):
        rows = raw[(raw['username']==user) & (raw['session']==session)]
        if not rows.index.empty:
            raw = raw.drop(rows.index)
            raw = raw.reset_index(drop=True)
    return raw



def remove_files(raw: pd.DataFrame) -> pd.DataFrame:
    bl = pd.read_csv(Settings.BLACKLIST, dtype=str)
    files = bl.loc[bl['category']=='file','entry'].tolist()
    rows = raw[raw.filekey.isin(files)]
    if not rows.index.empty:
        raw = raw.drop(rows.index)
        raw = raw.reset_index(drop=True)
    return raw



def remove_multiple_sending_in_session(raw: pd.DataFrame) -> pd.DataFrame:
    grouped = raw.groupby(['username', 'session', 'exercise', 'timing'])
    for group_name, group in grouped:
        session_value = group_name[1]
        if pd.notna(session_value) and session_value != '':
            if len(group) > 1:
                sorted_group = group.sort_values('datetime')
                duplicates = sorted_group.iloc[1:]
                raw = raw.drop(duplicates.index)
    raw = raw.reset_index(drop=True)
    return raw



def resolve_updrs_filenames(raw: pd.DataFrame) -> pd.DataFrame:
    # First, replace the EXERCISE name "updrs" with updrs3/updrs124:
    def process_updrs_group(group):
        if len(group) == 3:
            timings = group['timing'].value_counts()
            
            # Scenario 1: one 'pre' and two 'post'
            if timings.get('pre', 0) == 1 and timings.get('post', 0) == 2:
                # Identify the earlier 'post' file and change its 'timing' to 'unknown'
                post_files = group[group['timing'] == 'post']
                earlier_post_index = post_files['time'].idxmin()
                group.loc[earlier_post_index, 'timing'] = 'unknown'
                
                # Change 'exercise' according to 'timing'
                group['exercise'] = group['timing'].apply(lambda x: 'updrs3' if x in ['pre', 'post'] else 'updrs124')
            
            # Scenario 2: one 'pre', one 'unknown', one 'post'
            elif timings.get('pre', 0) == 1 and timings.get('unknown', 0) == 1 and timings.get('post', 0) == 1:
                # Change 'exercise' according to 'timing'
                group['exercise'] = group['timing'].apply(lambda x: 'updrs3' if x in ['pre', 'post'] else 'updrs124')
        # else:
        #     print(f"UPDRS session that could not convert into UPDRS3 or UPDRS124: {group['username'].unique().item()}")    
        return group
    
    updrs_df = raw[raw['exercise'] == 'updrs']
    updrs_df = updrs_df.groupby(['username', 'date']).apply(process_updrs_group)
    updrs_df = updrs_df.reset_index(drop=True)

    # apply changes
    for index, row in updrs_df.iterrows():
        original_index = raw[(raw['username'] == row['username']) & 
                            (raw['date'] == row['date']) & 
                            (raw['time'] == row['time'])].index
        if not original_index.empty:
            original_index = original_index[0]
            raw.at[original_index, 'timing'] = row['timing']
            raw.at[original_index, 'exercise'] = row['exercise']
    
    return raw



def change_columns(raw: pd.DataFrame):
    replacements = pd.read_csv(Settings.REPLACEMENTS, dtype=str)
    for _, row in replacements.iterrows():
        filekey = row['filekey']
        column = row['column']
        new_value = row['value']
        raw.loc[raw['filekey']==filekey, column] = new_value
    return raw
 



#################### FILES ########################
def match_sessions(changes: List[Tuple[str]]) -> None:
    df = pd.read_csv(Settings.ALL_FILES, dtype=str)
    for change in changes:
        df.loc[df['filekey']==change[0], 'session'] = change[1]
    df.to_csv(Settings.ALL_FILES, index=False)


    

def merge_sessions_into_early(username, early_session, late_session, how='early'):
    df = pd.read_csv(Settings.ALL_FILES, dtype=str)
    late_session_df = df[(df['username'] == username) & (df['session'] == late_session)].copy() # & (df['pattern'] == 'RECORDING')]
    
    if not late_session_df.empty:
        # Update 'session' and 'timing' for the late session's RECORDING files
        late_session_df['session'] = early_session
        late_session_df.loc[late_session_df['pattern']=='RECORDING', 'timing'] = 'post'
        
        # Update the original DataFrame
        for index, row in late_session_df.iterrows():
            df.loc[index, 'session'] = row['session']
            df.loc[index, 'timing'] = row['timing']
        
        # Save the updated DataFrame to a new CSV file
        df.to_csv('../'+Settings.ALL_FILES, index=False)


def replace_session_number(username: str, current_number: str, new_number: str) -> None:
    df = pd.read_csv(Settings.ALL_FILES, dtype=str)
    session_df = df[(df['username'] == username) & (df['session'] == current_number)]
    df.loc[session_df.index, 'session'] = new_number
    df.to_csv(Settings.ALL_FILES, index=False)


def change_user_property_in_all_files(username: str, column: str, new_value: str) -> None:
    df = pd.read_csv(Settings.ALL_FILES, dtype=str)
    user_df = df[df['username'] == username]
    df.loc[user_df.index, column] = new_value
    df.to_csv(Settings.ALL_FILES, index=False)


######################################################################################################################






def resolve_files():
    
    change_user_property_in_all_files(username='hc_383265f69a80046268da6a5c93d5c21964798c5a', column='entity', new_value='AX')

    match_sessions([
        ('hc_63fb9e5416fe7b05cb5f2564fca55ae226712f54/user_register_2024-07-11_18:40:31.csv', 'b10a810f-7688-4a61-946c-564d1b2d102e'),
        ('6adb9ad6636a73b9501599b2e53b7649654268a7/6adb9ad6636a73b9501599b2e53b7649654268a7_he_post_2024-05-18_20:29:46_updrs.csv', '8d022900-b8b3-4948-a15c-208989936e6c'),
    ])



def remove_samplers(df: pd.DataFrame) -> pd.DataFrame:
    samplers = df.loc[df['entity']=='sampler'].index
    df = df.drop(samplers)
    df = df.reset_index(drop=True)
    return df
  


def resolve(df):
    # Remove
    df = remove_usernames(df)
    df = remove_samplers(df)
    df = remove_sessions(df)
    df = remove_files(df)
    df = remove_multiple_sending_in_session(df)
    df = resolve_updrs_filenames(df)

    df.loc[df[Bucket.EXERCISE] == 'updrs3', ['updrs1','updrs2','updrs4']] = [pd.NaT, pd.NaT, pd.NaT]
    df.loc[df[Bucket.EXERCISE] == 'updrs124', 'updrs3'] = pd.NaT
    usernames_to_update = df.loc[df[Registration.HEALTHY].str.lower().str.contains('ataxia|אטקסיה', case=False, na=False), 'username']
    df.loc[df['username'].isin(usernames_to_update), Bucket.ENTITY] = Entity.AX
    df['dbs'] = df['dbs'].replace('1970-01-01', pd.NaT)
    
    return df 



def update_session_and_timing(df: pd.DataFrame, username: str, session: str, new_session: str, new_timing: str = None) -> pd.DataFrame:
    if new_timing:
        df.loc[(df['username']==username) & (df['session']==session) & (df['pattern']=="RECORDING"), 'timing'] = new_timing
    df.loc[(df['username']==username) & (df['session']==session), 'session'] = new_session
    
    return df


def resolve_sessions(df):
    sessions2update = pd.read_csv(Settings.UPDATE_SESSIONS, dtype=str)
    for _,row in sessions2update.iterrows():
        timing = None if pd.isna(row['new_timing']) else row['new_timing']
        df = update_session_and_timing(df, username=row['username'],
                                            session=row['session'],
                                            new_session=row['new_session'],
                                            new_timing=timing,)
    return df
        
