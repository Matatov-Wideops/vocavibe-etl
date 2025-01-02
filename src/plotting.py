import os
import numpy as np
import pandas as pd
import yaml
import matplotlib.pyplot as plt
from matplotlib import font_manager
from datetime import datetime, timedelta

from src.settings import Settings
from src.database import Durations, SpecialUsers
from src.utils import check_date_format, hash_phone_number as hashp


class Color:
    VV = np.array([90, 101, 230])/255
    YELLOW = np.array([249, 158, 32])/255
    LIGHT_YELLOW = np.array([253, 179, 48])/255
    GREEN = np.array([43, 143, 143])/255
    LIGHT_GREEN = np.array([177, 244, 108])/255
    DARK_VV = np.array([61, 39, 151])/255
    BLUE = np.array([33, 10, 253])/255

    @classmethod
    def get_unnormalized_rgb(cls, color_name):
        normalized_rgb = getattr(cls, color_name.upper(), None)
        if normalized_rgb is not None:
            return (normalized_rgb * 255).astype(int).tolist()
        return None


def rgb_to_hex(color_array, brightness_factor=0, alpha=1.0):
    adjusted_color = np.clip(color_array * (1 + brightness_factor), 0, 1)
    alpha_int = int(alpha * 255)
    return '{:02x}{:02x}{:02x}{:02x}'.format(alpha_int, int(adjusted_color[0]*255), int(adjusted_color[1]*255), int(adjusted_color[2]*255))









def plot_pies(show_ax=False, exclude_archive=True, only_full=True, counter='time'):
    users = pd.read_csv(Settings.ALL_USERS, dtype=str)
    patients = users[users.entity=='PD']
    healthy = users[users.entity=='HC']
    # if exclude_archive:
    #     healthy = healthy[~healthy.username.isin(IgnoreUsers.archive)]

    npm = len(patients.loc[patients.gender == 'male', 'username'].unique())
    npf = len(patients.loc[patients.gender == 'female', 'username'].unique())
    nhm = len(healthy.loc[healthy.gender == 'male', 'username'].unique())
    nhf = len(healthy.loc[healthy.gender == 'female', 'username'].unique())

    sessions = pd.read_csv(Settings.SESSIONS, dtype=str)
    # sessions = sessions[~sessions.username.isin(Exclude.users)]
    if only_full:
        sessions = sessions[~sessions['paradigm'].str.contains("~")]
    s_pd = len(sessions[(sessions.entity == 'PD')])
    s_hc = len(sessions[(sessions.entity == 'HC')])

    fig, axs = plt.subplots(2, 2, figsize=(12, 14))

    labels = ['PD men', 'PD women', 'HC men', 'HC women']
    sizes = [npm, npf, nhm, nhf]
    colors = [Color.VV, Color.VV, Color.YELLOW, Color.YELLOW]
    explode = [0.03, 0.03, 0.03, 0.03]

    if show_ax:
        ataxia = users[users.entity=='AX']
        na = len(ataxia.username.unique())
        labels.append('Ataxia')
        sizes.append(na)
        colors.append(Color.LIGHT_GREEN)
        explode.append(0.05)

    wedges, texts, autotexts = axs[0, 0].pie(sizes, explode=explode, labels=labels, colors=colors,
                                             autopct=lambda p: f'{round(p * sum(sizes) / 100)}', shadow=True,
                                             startangle=140)
    for autotext in autotexts:
        autotext.set_fontsize(18)
    axs[0, 0].set_title('Participants')



    if counter=='number':
        labels = ['PD', 'HC']
        sizes = [s_pd * 46, s_hc * 23]
        for ii in range(len(labels)):
            labels[ii] = f"{labels[ii]}: {sizes[ii] // 23}"
    elif counter=='time':
        files = pd.read_csv(Settings.ALL_FILES, dtype=str)
        files = files[files['pattern'].isin(['RECORDING','RECORDING1'])]
        files['duration'] = files['exercise'].apply(lambda k: Durations[k])
        labels = ['PD', 'HC']
        sizePD = files.loc[files['entity']=='PD', 'duration'].sum()//60
        sizeHC = files.loc[files['entity']=='HC', 'duration'].sum()//60
        sizes = [sizePD, sizeHC]

    colors = [Color.VV, Color.YELLOW]
    explode = (0.03, 0.03)

    wedges, texts, autotexts = axs[0, 1].pie(sizes, explode=explode, labels=labels, colors=colors,
                                             autopct=lambda p: f'{round(p * sum(sizes) / 100)}\nminutes', shadow=True,
                                             startangle=140)
    for autotext in autotexts:
        autotext.set_fontsize(18)
        # autotext.set_color('white')
    axs[0, 1].set_title('Recordings')



    n_sheba = len(patients.loc[patients.medical_center == 'Sheba', 'username'].unique())
    n_ichilov = len(patients.loc[patients.medical_center == 'Ichilov', 'username'].unique())

    labels = ['Sheba', 'Ichilov']
    sizes = [n_sheba, n_ichilov]
    colors = [Color.DARK_VV, Color.GREEN]
    explode = (0.03, 0.03)

    wedges, texts, autotexts = axs[1, 0].pie(sizes, explode=explode, labels=labels, colors=colors,
                                             autopct=lambda p: f'{round(p * sum(sizes) / 100)}', shadow=True,
                                             startangle=140)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(18)
    axs[1, 0].set_title('Medical Centers')

    n_no = len(patients.loc[patients.genetic == 'NO', 'username'].unique())
    n_yes = len(patients.loc[patients.genetic == 'YES', 'username'].unique())
    n_gba = len(patients.loc[patients.genetic == 'GBA', 'username'].unique())
    n_lrrk2 = len(patients.loc[patients.genetic == 'LRRK2', 'username'].unique())

    labels = ['No', 'Yes', 'GBA', 'LRRK2']
    sizes = [n_no, n_yes, n_gba, n_lrrk2]
    colors = [Color.VV, Color.LIGHT_GREEN, Color.YELLOW, Color.GREEN]
    explode = (0.03, 0.03, 0.03, 0.03)

    wedges, texts, autotexts = axs[1, 1].pie(sizes, explode=explode, labels=labels, colors=colors,
                                             autopct=lambda p: f'{round(p * sum(sizes) / 100)}', shadow=True,
                                             startangle=140)
    for autotext in autotexts:
        autotext.set_fontsize(18)
    axs[1, 1].set_title('Genetic predisposition')

    return fig, axs



def plot_users_over_time(interval=None, exclude_archive=True, dropout=False, annotation_percentage=20):
    users = pd.read_csv(Settings.ALL_USERS, dtype=str)
    patients = users[users.entity == 'PD']
    healthy = users[users.entity == 'HC']
    
    # if exclude_archive:
    #     healthy = healthy[~healthy.username.isin(IgnoreUsers.archive)]

    patients['date'] = pd.to_datetime(patients['date'])
    healthy['date'] = pd.to_datetime(healthy['date'])

    if dropout:
        dropout_df = pd.read_csv(Settings.DROPOUT, dtype=str)
        dropout_df['drop_out'] = pd.to_datetime(dropout_df['drop_out'], format=Settings.DATE_FORMAT)

    patients_counts = patients.groupby(patients['date'].dt.date).size().cumsum()
    healthy_counts = healthy.groupby(healthy['date'].dt.date).size().cumsum()

    combined_counts_patients = pd.DataFrame({'Patients': patients_counts})
    combined_counts_healthy = pd.DataFrame({'Healthy': healthy_counts})

    if dropout:
        # Convert all relevant dates to the same type (Timestamp)
        all_dates = pd.date_range(start=min(combined_counts_patients.index.min(), dropout_df['drop_out'].min().date()), 
                                  end=max(combined_counts_patients.index.max(), dropout_df['drop_out'].max().date()))
        combined_counts_patients = combined_counts_patients.reindex(all_dates, method='ffill').fillna(0)
        combined_counts_healthy = combined_counts_healthy.reindex(all_dates, method='ffill').fillna(0)

        for _, row in dropout_df.iterrows():
            username = hashp(row['user_phone'])
            if username in patients.username.values:
                drop_date = row['drop_out'].date()
                combined_counts_patients.loc[drop_date:] -= 1
            elif username in healthy.username.values:
                drop_date = row['drop_out'].date()
                combined_counts_healthy.loc[drop_date:] -= 1

    if interval:
        start_date, end_date = pd.to_datetime(interval).date
        combined_counts_patients = combined_counts_patients[(combined_counts_patients.index >= start_date) & (combined_counts_patients.index <= end_date)]
        combined_counts_healthy = combined_counts_healthy[(combined_counts_healthy.index >= start_date) & (combined_counts_healthy.index <= end_date)]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(combined_counts_patients.index, combined_counts_patients['Patients'], color=Color.VV, label='Patients', marker='o', alpha=0.7)
    ax.plot(combined_counts_healthy.index, combined_counts_healthy['Healthy'], color=Color.YELLOW, label='Healthy', marker='o', alpha=0.7)

    fig.autofmt_xdate()

    step_patients = max(1, len(combined_counts_patients) * annotation_percentage // 100)
    step_healthy = max(1, len(combined_counts_healthy) * annotation_percentage // 100)

    for i, (date, row) in enumerate(combined_counts_patients.iterrows()):
        if i % step_patients == 0:
            ax.annotate(f'{row["Patients"]:.0f}', (date, row['Patients']), textcoords="offset points", xytext=(0, 10), ha='center', color=Color.VV)

    for i, (date, row) in enumerate(combined_counts_healthy.iterrows()):
        if i % step_healthy == 0:
            ax.annotate(f'{row["Healthy"]:.0f}', (date, row['Healthy']), textcoords="offset points", xytext=(0, 10), ha='center', color=Color.YELLOW)

    upper_limit = 1.2 * max(combined_counts_healthy.max().max(), combined_counts_patients.max().max())
    ax.set_ylim([0, upper_limit])
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Number of Users')
    ax.set_title('Number of Users Joined Over Time')
    ax.legend(loc='lower right')
    ax.grid(True)
    return fig, ax







def users_per_sampler(exclude_archive=True, show=None, ignore=[]):
    import pandas as pd
    import matplotlib.pyplot as plt

    users = pd.read_csv(Settings.ALL_USERS, dtype=str)
    users['date'] = pd.to_datetime(users['date'])
    users['month'] = users['date'].dt.to_period('M')
    patients = users[users.entity == 'PD']
    healthy = users[users.entity == 'HC']
    if exclude_archive:
        healthy = healthy[~healthy.username.isin(SpecialUsers.values())]

    samplers = pd.read_csv(Settings.SAMPLERS_CSV, dtype=str)
    if show:
        samplers = samplers.loc[samplers.group == show, 'sampler_username']
        patients = patients[patients['sampler_username'].isin(samplers)]
        healthy = healthy[healthy['sampler_username'].isin(samplers)]

    if ignore:
        patients = patients[~patients['sampler_username'].isin(ignore)]
        healthy = healthy[~healthy['sampler_username'].isin(ignore)]
    
    patient_counts = patients.groupby(['Hebrew', 'month'])['username'].nunique().unstack(fill_value=0)
    healthy_counts = healthy.groupby(['Hebrew', 'month'])['username'].nunique().unstack(fill_value=0)
    patient_cumulative = patient_counts.cumsum(axis=1)
    patient_cumulative = patient_cumulative.mask(patient_cumulative.diff(axis=1) == 0)

    combined_counts = pd.DataFrame({
        'Patients': patient_counts.sum(axis=1),
        'Healthy': healthy_counts.sum(axis=1)
    }).fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    width = 0.4

    combined_counts['Patients'].plot(kind='bar', color=Color.VV, width=width, position=1, label='Patients', ax=ax)
    combined_counts['Healthy'].plot(kind='bar', color=Color.YELLOW, width=width, position=0, label='Healthy', ax=ax)

    # Add white horizontal lines for monthly registrations in the PD bars, and month codes below them
    for i, (sampler, row) in enumerate(patient_cumulative.iterrows()):
        for month in range(1, len(row)):
            y_position = row.iloc[month-1]
            # Draw the white line if it's not at the top or bottom
            if y_position > 0: # and y_position < row.iloc[-1]:
                # Draw the white line only on the PD bar
                ax.plot([i - width, i], [y_position]*2, color='white', linewidth=1.5)
                # Add the month code below the white line
                month_code = row.index[month-1].strftime('%b')
                ax.text(i - width/2, y_position - 0.3, month_code, ha='center', color='white', va='top', fontsize=8)

    ax.set_xlabel('Sampler')
    ax.set_ylabel('Number of Users')
    if show:
        ax.set_title(f'Number of Users per Sampler - {show}')
    else:
        ax.set_title('Number of Users per Sampler')
    ax.set_xticklabels([label.get_text()[::-1] for label in ax.get_xticklabels()], rotation=45)

    for i, (patients, healthy) in enumerate(zip(combined_counts['Patients'], combined_counts['Healthy'])):
        ax.text(i - width/2, patients + 1.0, f'{patients:.0f}', ha='center', color='black', va='bottom', fontsize=12)
        ax.text(i + width/2, healthy + 1.0, f'{healthy:.0f}', ha='center', color='black', va='bottom', fontsize=12)

    ax.legend()
    ax.grid(axis='y')
    ax.set_xlim([-1, len(combined_counts)])
    ax.set_ylim([0, 1.2 * combined_counts.max().max()])

    return fig, ax



def plot_sessions_count(n, show_all=True, exclude_archive=True):
    sessions = pd.read_csv(Settings.SESSIONS, dtype=str)
    if exclude_archive:
        sessions = sessions[~sessions.username.isin(SpecialUsers.values())]
    sessions = sessions[(sessions['entity'] != 'AX')]

    all_table = pd.DataFrame(index=range(1, n+1), columns=sessions['entity'].unique())
    for i in all_table.index:
        for entity in all_table.columns:
            count = sessions[(sessions['entity'] == entity) & (sessions['session_number'].astype(int) >= i)]['username'].nunique()
            all_table.at[i, entity] = count

    full_sessions = sessions[(~sessions.paradigm.str.contains("~"))]
    full_table = pd.DataFrame(index=range(1, n+1), columns=full_sessions['entity'].unique())
    for i in full_table.index:
        for entity in full_table.columns:
            count = full_sessions[(full_sessions['entity'] == entity) & (full_sessions['session_number'].astype(int) >= i)]['username'].nunique()
            full_table.at[i, entity] = count

    # Load dropout data
    dropout = pd.read_csv(Settings.DROPOUT, dtype=str)
    first_bar_value = all_table['PD'].iloc[0]
    active_users = first_bar_value - len(dropout)

    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.35
    indices = range(len(all_table.index))

    if show_all:
        ax.bar([i - bar_width/2 for i in indices], all_table['PD'], bar_width, label='All PD', color=Color.VV, alpha=0.5)
        ax.bar([i + bar_width/2 for i in indices], all_table['HC'], bar_width, label='All HC', color=Color.YELLOW, alpha=0.5)

    ax.bar([i - bar_width/2 for i in indices], full_table['PD'], bar_width, label='Full PD', color=Color.VV)
    ax.bar([i + bar_width/2 for i in indices], full_table['HC'], bar_width, label='Full HC', color=Color.YELLOW)

    if show_all:
        for i, v in enumerate(all_table['PD']):
            if v == 0:
                continue
            ax.text(i - bar_width/2, v + 4, str(v), ha='center', va='top', color='black', fontsize=12)
        for i, v in enumerate(all_table['HC']):
            if v == 0:
                continue
            ax.text(i + bar_width/2, v + 4, str(v), ha='center', va='top', color='black', fontsize=12)

    for i, v in enumerate(full_table['PD']):
        if v == 0:
            continue
        ax.text(i - bar_width/2, v - 4, str(v), ha='center', va='bottom', color='white', fontsize=12)
    for i, v in enumerate(full_table['HC']):
        if v == 0:
            continue
        ax.text(i + bar_width/2, v - 4, str(v), ha='center', va='bottom', color='white', fontsize=12)

    ax.axhline(y=active_users, color=Color.GREEN, linewidth=1, linestyle='--')
    ax.set_yticks([active_users])
    # ax.set_yticklabels([f'Active Users: {active_users}'], fontsize=12, color='pink')

    ax.set_xlabel('Number of Sessions')
    ax.set_ylabel('Number of Users')
    ax.set_title(f'Number of Users with up to {n} Sessions')
    ax.legend(title='Entity')
    ax.grid(axis='y')
    ax.set_xticks(indices)
    ax.set_xticklabels(all_table.index, rotation=0)
    
    return fig, ax





def plot_dataframe_table(source_file, X=28, fontsize=11, scale=1.3, figsize=(20, 24)):
    
    def send_recording_update_to(source_file=source_file, X=X):
        with open(Settings.CONFIG, 'r') as file:
            cfg = yaml.safe_load(file)

        # Load session and dropout data
        sessions_df = pd.read_csv(Settings.SESSIONS, dtype=str)
        dropout = pd.read_csv(Settings.DROPOUT, dtype=str)
        dropout['username'] = dropout['user_phone'].apply(hashp)
        dropout = dropout['username'].tolist()
        sessions_df = sessions_df[~sessions_df['username'].isin(dropout)].reset_index(drop=True)

        # Filter by 'entity' == 'PD'
        sessions_df = sessions_df[sessions_df['entity'] == 'PD']

        # Convert 'date' to datetime for sorting and calculation purposes
        sessions_df['date'] = pd.to_datetime(sessions_df['date'])

        # Keep only the last session for each user
        sessions_df = sessions_df.sort_values(by=['username', 'date'], ascending=[True, False])
        sessions_df = sessions_df.drop_duplicates(subset='username', keep='first').reset_index(drop=True)
        
        # Rename 'date' to 'last session' and calculate 'days'
        sessions_df['last session'] = sessions_df['date']
        sessions_df['days'] = sessions_df['last session'].apply(lambda x: (datetime.now() - x).days)
        
        # Sort by 'days'
        sessions_df = sessions_df.sort_values(by='days', ascending=False, ignore_index=True)
        
        # Add 'send?' column based on the X value
        sessions_df['SMS'] = sessions_df['days'].apply(lambda x: 1 if x >= X else 0)
        sessions_df = sessions_df[sessions_df['days'] >= X-3]
        
        # Check if the source file exists
        if os.path.exists(source_file):
            # Add columns for 'called', 'answered', and 'quit' from source_file
            source_df = pd.read_csv(source_file, dtype=str)
            
            # Check if 'called', 'answered', and 'quit' exist in the source file, if not, set NaN
            for col in cfg['gal_columns']:
                if col not in source_df.columns:
                    source_df[col] = np.nan
            
            # Merge source_df with sessions_df on 'username'
            sessions_df = pd.merge(sessions_df, source_df[['username'] + cfg['gal_columns']], on='username', how='left')
        else:
            # If the source file doesn't exist, add NaN for 'called', 'answered', and 'quit'
            sessions_df['called'] = np.nan
            sessions_df['answered'] = np.nan
            sessions_df['quit'] = np.nan
        
        # Reorder columns to include new ones
        sessions_df = sessions_df[['username', 'user_phone', 'password', 'last session', 'days', 'session_number', 'SMS']+cfg['gal_columns']]
        
        return sessions_df


    df = send_recording_update_to(source_file)  
    # Replace 'NaN' with an empty string
    df = df.fillna('')

    # Adjust 'last session' to show only the date
    if 'last session' in df.columns:
        df['last session'] = pd.to_datetime(df['last session']).dt.date

    # Export the DataFrame to an Excel file
    df.to_csv(Settings.SEND_PASSWORDS, index=False)

    df['comments'] = df['comments'].apply(lambda x: x[::-1] if isinstance(x, str) else x)
    df.rename(columns={'session_number': 'number',
                       'user_phone': 'phone'}, inplace=True)

    fig, ax = plt.subplots(figsize=figsize)  # Increase figure size for better fitting
    ax.axis('tight')
    ax.axis('off')

    # Escape special characters in column headers and data
    df.columns = [str(col).replace('$', r'\$') for col in df.columns]
    df = df.apply(lambda x: x.map(lambda y: str(y).replace('$', r'\$')))
    df['phone'] = df['phone'].apply(lambda x: x[4:])
    # Create the table with some formatting
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(scale, scale+0.5)  # Adjust scale to make sure columns are wide enough

    # Format the 'username' column to be bold
    cell_dict = table.get_celld()
    for i in range(len(df)):
        cell_dict[(i + 1, 0)].set_text_props(weight='bold')

    # Adjust column widths
    for j in range(len(df.columns)):
        max_len = max([len(str(s)) for s in df.iloc[:, j]] + [len(df.columns[j])])
        table.auto_set_column_width(j)
        if max_len > 10:
            table.auto_set_column_width(j)
            for i in range(len(df) + 1):
                cell_dict[(i, j)].set_width(0.15)

    # Add colors to the table
    for i in range(len(df) + 1):
        for j in range(len(df.columns)):
            cell_dict[(i, j)].set_edgecolor('black')
            cell_dict[(i, j)].set_linewidth(1)
            if i == 0:
                cell_dict[(i, j)].set_facecolor('#40466e')
                cell_dict[(i, j)].set_text_props(weight='bold', color='white')
            else:
                cell_dict[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else '#e0e0e0')

    return fig, ax



def broken_sessions(timeframe=60, only_sampler=False, ignore_sessions=True, fontsize=12, scale=(1.5, 3.1), figsize=(20, 10)):
    df = pd.read_csv(Settings.SESSIONS, dtype=str)
    if ignore_sessions:        
        resolved = pd.read_csv(Settings.RESOLVED_SESSIONS, dtype=str)
        filtered_sessions_df = df.merge(
        resolved[['username', 'session']],
        on=['username', 'session'],
        how='left',
        indicator=True
        )
        filtered_sessions_df = filtered_sessions_df[filtered_sessions_df['_merge'] == 'left_only']
        df = filtered_sessions_df.drop(columns=['_merge'])
        
        dropout = pd.read_csv(Settings.DROPOUT, dtype=str)
        dropout['username'] = dropout['user_phone'].apply(hashp)
        dropout = dropout['username'].tolist()
        df = df[~df['username'].isin(dropout)].reset_index(drop=True)

    samplers = pd.read_csv(Settings.SAMPLERS_CSV, dtype=str, usecols=['sampler_username', 'Hebrew'])

    # Merge samplers dataframe with sessions dataframe
    df = df.merge(samplers, on='sampler_username', how='left')
    df.rename(columns={'Hebrew': 'sampler'}, inplace=True)
    # df.rename(columns={'sampler_username': 'sampler'}, inplace=True)
    df['sampler'] = df['sampler'].fillna(df['session_number'])

    broken_sessions = df.loc[df['paradigm'].str.contains("~"), ['date', 'username', 'session', 'user_phone', 'start', 'end', 'sampler', 'paradigm']]
    broken_sessions.to_csv(Settings.BROKEN_SESSIONS, index=False)
    
    # Show only last 30 days
    broken_sessions['date'] = pd.to_datetime(broken_sessions['date'], format=Settings.DATE_FORMAT)
    days_ago = datetime.now() - timedelta(days=timeframe)
    broken_sessions = broken_sessions.loc[broken_sessions['date'] >= days_ago]
    broken_sessions['date'] = broken_sessions['date'].dt.strftime(Settings.DATE_FORMAT)
    
    # Ensure columns are strings before checking for "~"
    broken_sessions['paradigm'] = broken_sessions['paradigm'].astype(str).str.replace("'","")

    # broken_sessions = df.loc[df['paradigm'].str.contains("~"), ['date', 'username', 'session', 'user_phone', 'start', 'end', 'sampler', 'paradigm']]
    # broken_sessions.to_csv(Settings.BROKEN_SESSIONS, index=False)

    broken_sessions = broken_sessions[['date', 'user_phone', 'start', 'end', 'sampler', 'paradigm']]
    broken_sessions['user_phone'] = broken_sessions['user_phone'].apply(lambda x: x[4:])
    if only_sampler:
        broken_sessions = broken_sessions[~broken_sessions['sampler'].str.isdigit()]

    fig, ax = plt.subplots(figsize=figsize)  # Increase figure size for better fitting
    ax.axis('tight')
    ax.axis('off')

    # Escape special characters in column headers and data, and replace 'nan' with empty strings
    broken_sessions.columns = [str(col).replace('$', r'\$') for col in broken_sessions.columns]
    broken_sessions = broken_sessions.fillna('')  # Replace NaN with empty strings
    broken_sessions = broken_sessions.apply(lambda x: x.map(lambda y: str(y).replace('$', r'\$')))
    broken_sessions = broken_sessions.astype(str).map(lambda x: '' if x == 'nan' else x.replace('$', r'\$'))

    column_widths = {
        'date': 0.085,
        'user_phone': 0.09,
        'start': 0.08,
        'end': 0.08,
        'sampler': 0.1,
        'paradigm': 0.38,
    }

    # Create the table with some formatting
    table = ax.table(cellText=broken_sessions.values, colLabels=broken_sessions.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(fontsize)
    table.scale(*scale)  # Adjust scale to make sure columns are wide enough

    cell_dict = table.get_celld()
    # Adjust column widths based on the provided dictionary
    for j, col in enumerate(broken_sessions.columns):
        col_width = column_widths.get(col, 0.1)  # Default width if not specified in the dictionary
        for i in range(len(broken_sessions) + 1):
            cell_dict[(i, j)].set_width(col_width)

    # Add colors to the table and handle special cases
    for i in range(len(broken_sessions) + 1):
        for j in range(len(broken_sessions.columns)):
            cell_dict[(i, j)].set_edgecolor('black')
            cell_dict[(i, j)].set_linewidth(1)
            if i == 0:
                cell_dict[(i, j)].set_facecolor('#40466e')
                cell_dict[(i, j)].set_text_props(weight='bold', color='white')
            else:
                if '~' in cell_dict[(i, j)].get_text().get_text():
                    cell_dict[(i, j)].set_facecolor('#bebfd4')  # Very light purple
                else:
                    cell_dict[(i, j)].set_facecolor('#f0f0f0' if i % 2 == 0 else '#e0e0e0')


    # Here's where we apply the row border coloring
    sampler_col_index = broken_sessions.columns.get_loc('sampler')
    user_paradigm_col_index = broken_sessions.columns.get_loc('paradigm')
    duplicate_phones = broken_sessions['user_phone'].duplicated(keep=False)

    color_map = {
                2: '#ff0000',     # Red
                3: '#90ee90',     # Light green
                4: '#ff00ff',     # Magenta
                5: '#ffff00',     # Yellow
                6: '#006400',     # Dark green
                7: '#000000',     # Black
                8: '#a52a2a',     # Brown
                9: '#0000ff',     # Blue
                10: '#ffa500'     # Orange
            }
    
    for i in range(1, len(broken_sessions) + 1):
        if broken_sessions.iloc[i - 1]['sampler'].isdigit():
            sampler_value = int(broken_sessions.iloc[i - 1]['sampler'])
            color = color_map.get(sampler_value, '#ffffff')  # Default to white if not in map

            # Apply the color with half transparency
            cell_dict[(i, sampler_col_index)].set_facecolor(color)
            cell_dict[(i, sampler_col_index)].set_alpha(0.5)
            # Color borders for 'sampler' column
            # cell_dict[(i, sampler_col_index)].set_edgecolor('#3232ff')
            # cell_dict[(i, sampler_col_index)].set_linewidth(4)
            # Color borders for 'user_paradigm' column
            # cell_dict[(i, user_paradigm_col_index)].set_edgecolor('#3232ff')
            # cell_dict[(i, user_paradigm_col_index)].set_linewidth(4)

        if duplicate_phones.iloc[i - 1]:
        # Get the corresponding sampler value
            sampler_value = broken_sessions.iloc[i - 1]['sampler']
            if sampler_value.isdigit():
                sampler_value = int(sampler_value)
                color = color_map.get(sampler_value, '#ffffff')  # Default to white if not in map

                # Apply the color with half transparency to the 'user_phone' cell
                cell_dict[(i, broken_sessions.columns.get_loc('user_phone'))].set_facecolor(color)
                cell_dict[(i, broken_sessions.columns.get_loc('user_phone'))].set_alpha(0.5)


    # Ensure 'sampler' text is right-to-left
    for i in range(1, len(broken_sessions) + 1):
        for j in range(len(broken_sessions.columns)):
            if broken_sessions.columns[j] == 'sampler':
                cell_dict[(i, j)].get_text().set_text(' ' + cell_dict[(i, j)].get_text().get_text()[::-1])  # Reverse text for RTL effect

    # Ensure 'user_paradigm' text is aligned to the left and uses a monospaced font
    for i in range(1, len(broken_sessions) + 1):
        for j in range(len(broken_sessions.columns)):
            if broken_sessions.columns[j] in ['paradigm']:
                cell_dict[(i, j)].get_text().set_ha('center')
                cell_dict[(i, j)].get_text().set_fontproperties(font_manager.FontProperties(family='monospace', size=fontsize))
    
    return fig, ax




def plot_histograms(bins=16):
    # Load the data
    data = pd.read_csv(Settings.ALL_FILES, dtype=str)
    exercises_order = ['updrs3', 'updrs124', 'moca', 'fog', 'sdq', 'woq', 'pdq8']
    
    # Create subplots
    fig, axes = plt.subplots(3, 3, figsize=(18, 18))
    axes = axes.flatten()
    
    # Hide all axes initially
    for ax in axes:
        ax.axis('off')
    
    for idx, exercise in enumerate(exercises_order):
        exercise_data = data[data['exercise'] == exercise]
        
        if exercise == 'updrs3':
            pre_scores = exercise_data[exercise_data['timing'] == 'pre']['updrs3_pre'].dropna().astype(float)
            post_scores = exercise_data[exercise_data['timing'] == 'post']['updrs3_post'].dropna().astype(float)
            
            axes[idx].hist(pre_scores, bins=np.linspace(0,132,bins[idx]) if isinstance(bins, list) else bins, alpha=0.5, label='Pre', color=Color.VV)
            axes[idx].hist(post_scores, bins=np.linspace(0,132,bins[idx]) if isinstance(bins, list) else bins, alpha=0.5, label='Post', color=Color.YELLOW)
            axes[idx].set_xlabel('Score')
            axes[idx].set_ylabel('Frequency')
            axes[idx].set_title('UPDRS3 Scores')
            axes[idx].legend(loc='upper right')
        
        elif exercise == 'updrs124':
            scores = exercise_data[['updrs1', 'updrs2', 'updrs4']].dropna().astype(float)
            summed_scores = scores.apply(sum,1)
            
            axes[idx].hist(summed_scores, bins=bins[idx] if isinstance(bins, list) else bins, color=Color.GREEN)
            axes[idx].set_xlabel('Summed Score')
            axes[idx].set_ylabel('Frequency')
            axes[idx].set_title('UPDRS124 Summed Scores')
        
        elif exercise == 'woq':
            pre_scores = exercise_data['woq_pre'].dropna().astype(float)
            post_scores = exercise_data['woq_post'].dropna().astype(float)
                        
            axes[idx].hist(pre_scores, bins=bins[idx] if isinstance(bins, list) else bins, alpha=0.5, label='Pre', color=Color.VV)
            axes[idx].hist(post_scores, bins=bins[idx] if isinstance(bins, list) else bins, alpha=0.5, label='Post', color=Color.YELLOW)
            axes[idx].set_xlabel('Score')
            axes[idx].set_ylabel('Frequency')
            axes[idx].set_title('WOQ Scores')
            axes[idx].legend(loc='upper right')
        
        else:
            scores = exercise_data[exercise].dropna().apply(pd.to_numeric, errors='coerce').dropna()
            
            axes[idx].hist(scores, bins=bins[idx] if isinstance(bins, list) else bins, color=Color.GREEN)
            axes[idx].set_xlabel('Score')
            axes[idx].set_ylabel('Frequency')
            axes[idx].set_title(f'{exercise.upper()} Scores')
        
        axes[idx].axis('on')
    
    fig.tight_layout()
    return fig, axes