import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def display_picked_positions_by_year_and_month(dataframe):
    picked_positions_by_year_and_month = dataframe.groupby(['Year', 'Month'])['PicklistenPositionenID'].count().reset_index()
    picked_positions_by_year_and_month = picked_positions_by_year_and_month.rename(columns={'PicklistenPositionenID': 'PickedPositions'})
    picked_positions_by_year_and_month['YearAndMonth'] = picked_positions_by_year_and_month['Year'].astype(str) + '-' + picked_positions_by_year_and_month['Month'].astype(str)

    x = picked_positions_by_year_and_month['YearAndMonth'].to_list()
    y = picked_positions_by_year_and_month['PickedPositions'].to_list()

    plt.bar(x, y)
    plt.xlabel("Monat und Jahr")
    plt.ylabel("Gepickte Positionen")
    plt.title("Gepickte Positionen pro Monat und Jahr")
    plt.show()


def display_picked_positions_by_year_and_month_and_cluster(dataframe):
    picked_positions_by_year_and_month_and_cluster = dataframe.groupby(['Year', 'Month', 'Cluster'])['PicklistenPositionenID'].count().reset_index()
    picked_positions_by_year_and_month_and_cluster = picked_positions_by_year_and_month_and_cluster.rename(columns={'PicklistenPositionenID': 'PickedPositions'})
    picked_positions_by_year_and_month_and_cluster['YearAndMonth'] = picked_positions_by_year_and_month_and_cluster['Year'].astype(str) + '-' + picked_positions_by_year_and_month_and_cluster['Month'].astype(str)

    months = picked_positions_by_year_and_month_and_cluster['YearAndMonth'].unique().tolist()

    cluster_counts = {}
    c1_values_dataframe = picked_positions_by_year_and_month_and_cluster[picked_positions_by_year_and_month_and_cluster['Cluster'] == 'C1']
    cluster_counts['C1'] = np.array(c1_values_dataframe['PickedPositions'])

    c1_values_dataframe = picked_positions_by_year_and_month_and_cluster[picked_positions_by_year_and_month_and_cluster['Cluster'] == 'C2']
    cluster_counts['C2'] = np.array(c1_values_dataframe['PickedPositions'])

    c1_values_dataframe = picked_positions_by_year_and_month_and_cluster[picked_positions_by_year_and_month_and_cluster['Cluster'] == 'C3']
    cluster_counts['C3'] = np.array(c1_values_dataframe['PickedPositions'])

    c1_values_dataframe = picked_positions_by_year_and_month_and_cluster[picked_positions_by_year_and_month_and_cluster['Cluster'] == 'OOR']
    cluster_counts['OOR'] = np.array(c1_values_dataframe['PickedPositions'])

    width = 0.6

    fig, ax = plt.subplots()
    bottom = np.zeros(len(months))

    for cluster, cluster_count in cluster_counts.items():
        p = ax.bar(months, cluster_count, width, label=cluster, bottom=bottom)
        bottom += cluster_count
        ax.bar_label(p, label_type='center')

    ax.set_title("Number of Picked Positions by Year, Month and Cluster")
    ax.legend(loc="upper center")

    plt.show()


dataframe_picklisten_raw = pd.read_csv('Picklisten.csv')
dataframe_picklisten_positionen_raw = pd.read_csv('PicklistenPositionen.csv')

# nur Großkugel betrachten, da letztes verbelibendes Lager
dataframe_picklisten_raw = dataframe_picklisten_raw[dataframe_picklisten_raw['Standort'] == 'GRO']

dataframe_picklisten = dataframe_picklisten_raw[['PicklistenID', 'Picker', 'Erstellungsdatum', 'Cluster', 'Standort', 'FinishedTime', 'inProcessTime', 'PufferschieneTime']]
dataframe_picklisten_positionen = dataframe_picklisten_positionen_raw[['PicklistenPositionenID', 'PicklistenID', 'Menge', 'Picker', 'Pickzeit', 'Packer', 'Packzeit']]

# Erstellungsdatum: createPicklist, getdate() wenn Eintrag erzeugt wird
# FinishedTime: finish-picklist/{PicklistenID}, beenden der Pickliste
# inProcessTime: setPickingListPositionDetail, jedes mal wenn ein Artikel gepickt wird (ergo Zeit wenn letzter Artikel gepickt wurde)
# PufferschieneTime: packagepicklist-to-pufferschiene/{PicklistenID}, wenn Pickliste auf Pufferscheine gebucht wird

# NUR datensätze betrachten, welche ALLE Zeiten enthalten
dataframe_picklisten = dataframe_picklisten.dropna(subset=['Erstellungsdatum', 'FinishedTime', 'inProcessTime', 'PufferschieneTime'])
dataframe_picklisten_positionen = dataframe_picklisten_positionen.dropna(subset=['Pickzeit', 'Packzeit'])

joined_dataframe = pd.merge(dataframe_picklisten, dataframe_picklisten_positionen, on=['PicklistenID']).sort_values(by='PicklistenPositionenID')

joined_dataframe['Year'] = pd.DatetimeIndex(joined_dataframe['Erstellungsdatum']).year
joined_dataframe['Month'] = pd.DatetimeIndex(joined_dataframe['Erstellungsdatum']).month
joined_dataframe['Day'] = pd.DatetimeIndex(joined_dataframe['Erstellungsdatum']).day

# display_picked_positions_by_year_and_month(joined_dataframe)
display_picked_positions_by_year_and_month_and_cluster(joined_dataframe)
