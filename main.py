import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def display_picked_deliveries_by_year_and_month(dataframe):
    picked_positions_by_year_and_month = dataframe.groupby(['Year', 'Month'])['PaketNr'].nunique().reset_index()
    picked_positions_by_year_and_month = picked_positions_by_year_and_month.rename(columns={'PaketNr': 'PickedDeliveries'})
    picked_positions_by_year_and_month['YearAndMonth'] = picked_positions_by_year_and_month['Year'].astype(str) + '-' + picked_positions_by_year_and_month['Month'].astype(str)

    x = picked_positions_by_year_and_month['YearAndMonth'].to_list()
    y = picked_positions_by_year_and_month['PickedDeliveries'].to_list()

    plt.bar(x, y)
    plt.xlabel("Monat und Jahr")
    plt.ylabel("Gepickte Lieferungen")
    plt.title("Gepickte Lieferungen pro Monat und Jahr")
    plt.show()


def display_picked_deliveries_by_year_and_month_and_cluster(dataframe):
    picked_deliveries_by_year_and_month_and_cluster = dataframe.groupby(['Year', 'Month', 'Cluster'])['PaketNr'].nunique().reset_index()
    picked_deliveries_by_year_and_month_and_cluster = picked_deliveries_by_year_and_month_and_cluster.rename(columns={'PaketNr': 'PickedDeliveries'})
    picked_deliveries_by_year_and_month_and_cluster['YearAndMonth'] = picked_deliveries_by_year_and_month_and_cluster['Year'].astype(str) + '-' + picked_deliveries_by_year_and_month_and_cluster['Month'].astype(str)

    months = picked_deliveries_by_year_and_month_and_cluster['YearAndMonth'].unique().tolist()

    cluster_counts = {}
    c1_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'C1']
    cluster_counts['C1'] = np.array(c1_values_dataframe['PickedDeliveries'])

    c2_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'C2']
    cluster_counts['C2'] = np.array(c2_values_dataframe['PickedDeliveries'])

    c3_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'C3']
    cluster_counts['C3'] = np.array(c3_values_dataframe['PickedDeliveries'])

    oor_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'OOR']
    cluster_counts['OOR'] = np.array(oor_values_dataframe['PickedDeliveries'])

    width = 0.6

    fig, ax = plt.subplots()
    bottom = np.zeros(len(months))

    for cluster, cluster_count in cluster_counts.items():
        p = ax.bar(months, cluster_count, width, label=cluster, bottom=bottom)
        bottom += cluster_count
        ax.bar_label(p, label_type='center')

    ax.set_ylabel('Gepickte Lieferungen')
    ax.set_xlabel('Jahr und Monat')
    ax.set_title('Anzahl der gepickten Lieferungen pro Jahr und Monat')
    ax.legend(loc="upper center")

    plt.show()


def display_picked_articles_by_year_and_month_and_cluster(dataframe):
    picked_deliveries_by_year_and_month_and_cluster = dataframe.groupby(['Year', 'Month', 'Cluster'])['Menge'].sum().reset_index()
    picked_deliveries_by_year_and_month_and_cluster = picked_deliveries_by_year_and_month_and_cluster.rename(columns={'Menge': 'PickedArticles'})
    picked_deliveries_by_year_and_month_and_cluster['YearAndMonth'] = picked_deliveries_by_year_and_month_and_cluster['Year'].astype(str) + '-' + picked_deliveries_by_year_and_month_and_cluster['Month'].astype(str)

    months = picked_deliveries_by_year_and_month_and_cluster['YearAndMonth'].unique().tolist()

    cluster_counts = {}
    c1_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'C1']
    cluster_counts['C1'] = np.array(c1_values_dataframe['PickedArticles'])

    c2_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'C2']
    cluster_counts['C2'] = np.array(c2_values_dataframe['PickedArticles'])

    c3_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'C3']
    cluster_counts['C3'] = np.array(c3_values_dataframe['PickedArticles'])

    oor_values_dataframe = picked_deliveries_by_year_and_month_and_cluster[picked_deliveries_by_year_and_month_and_cluster['Cluster'] == 'OOR']
    cluster_counts['OOR'] = np.array(oor_values_dataframe['PickedArticles'])

    width = 0.6

    fig, ax = plt.subplots()
    bottom = np.zeros(len(months))

    for cluster, cluster_count in cluster_counts.items():
        p = ax.bar(months, cluster_count, width, label=cluster, bottom=bottom)
        bottom += cluster_count
        ax.bar_label(p, label_type='center')

    ax.set_ylabel('Gepickte Artikel')
    ax.set_xlabel('Jahr und Monat')
    ax.set_title('Anzahl der gepickten Artikel pro Jahr und Monat')
    ax.legend(loc="upper center")

    plt.show()


def display_picklist_duration_per_cluster(dataframe):
    picklist_duration_by_cluster = dataframe.groupby('Cluster').agg({'Picklistendauer': 'mean',
                                                                     'Packdauer': 'mean'}).reset_index()

    cluster = picklist_duration_by_cluster['Cluster'].to_list()
    pick_durations = picklist_duration_by_cluster['Picklistendauer'].tolist()
    pick_durations = [(p.seconds//60) for p in pick_durations]
    pack_durations = picklist_duration_by_cluster['Packdauer'].tolist()
    pack_durations = [(p.seconds//60) for p in pack_durations]
    durations = {
        'Pickdauer': pick_durations,
        'Packdauer': pack_durations
    }

    width = 0.25
    multiplier = 0
    x = np.arange(len(cluster))
    fig, ax = plt.subplots(layout='constrained')

    for type_of_duration, durations in durations.items():
        offset = width * multiplier + width/2
        rects = ax.bar(x + offset, durations, width, label=type_of_duration)
        ax.bar_label(rects)
        multiplier += 1

    ax.set_ylabel('Dauer in Minuten')
    ax.set_xlabel('Cluster')
    ax.set_title(f'Pick- und Packdauer pro Pickliste im Durchschnitt aus {len(dataframe)} Picklisten')
    ax.set_xticks(x + width, cluster)
    ax.legend(loc='upper left')
    plt.show()


def display_duration_per_picked_delivery_per_cluster(dataframe):
    dataframe = dataframe.groupby(['PicklistenID', 'Cluster', 'Picklistendauer', 'Packdauer'])['PaketNr'].nunique().reset_index()
    dataframe = dataframe.rename(columns={'PaketNr': 'PickedDeliveries'})
    dataframe = dataframe.groupby('Cluster').agg({'PickedDeliveries': 'mean',
                                                  'Picklistendauer': 'mean',
                                                  'Packdauer': 'mean'})

    dataframe['DauerProGepickteDelivery'] = dataframe['Picklistendauer'] / dataframe['PickedDeliveries']
    dataframe['DauerProGepackteDelivery'] = dataframe['Packdauer'] / dataframe['PickedDeliveries']
    test = 0


dataframe_picklisten_raw = pd.read_csv('Picklisten.csv')
dataframe_picklisten_positionen_raw = pd.read_csv('PicklistenPositionen.csv')

# nur Großkugel betrachten, da letztes verbelibendes Lager
dataframe_picklisten_raw = dataframe_picklisten_raw[dataframe_picklisten_raw['Standort'] == 'GRO']

# Picklistenpositionen mit Status 10 rausrechnen, da sie noch mal gepickt werden
dataframe_picklisten_positionen_raw = dataframe_picklisten_positionen_raw[dataframe_picklisten_positionen_raw['Status'] != 10]

dataframe_picklisten = dataframe_picklisten_raw[['PicklistenID', 'Picker', 'Erstellungsdatum', 'Cluster', 'Standort', 'FinishedTime', 'inProcessTime', 'PufferschieneTime']]
dataframe_picklisten.loc[:, 'Erstellungsdatum'] = pd.to_datetime(dataframe_picklisten['Erstellungsdatum'], format="%Y-%m-%d %H:%M:%S")
dataframe_picklisten.loc[:, 'FinishedTime'] = pd.to_datetime(dataframe_picklisten['FinishedTime'], format="%Y-%m-%d %H:%M:%S")
dataframe_picklisten.loc[:, 'inProcessTime'] = pd.to_datetime(dataframe_picklisten['inProcessTime'], format="%Y-%m-%d %H:%M:%S")
dataframe_picklisten.loc[:, 'PufferschieneTime'] = pd.to_datetime(dataframe_picklisten['PufferschieneTime'], format="%Y-%m-%d %H:%M:%S")

dataframe_picklisten_positionen = dataframe_picklisten_positionen_raw[['PicklistenPositionenID', 'PicklistenID', 'Menge', 'Picker', 'Pickzeit', 'Packer', 'Packzeit', 'PaketNr']]
dataframe_picklisten_positionen.loc[:, 'Pickzeit'] = pd.to_datetime(dataframe_picklisten_positionen['Pickzeit'], format="%Y-%m-%d %H:%M:%S")
dataframe_picklisten_positionen.loc[:, 'Packzeit'] = pd.to_datetime(dataframe_picklisten_positionen['Packzeit'], format="%Y-%m-%d %H:%M:%S")

# Erstellungsdatum: createPicklist, getdate() wenn Eintrag erzeugt wird
# FinishedTime: finish-picklist/{PicklistenID}, beenden der Pickliste
# inProcessTime: setPickingListPositionDetail, sobald der erste Artikel gepickt wurde
# PufferschieneTime: packagepicklist-to-pufferschiene/{PicklistenID}, wenn Pickliste auf Pufferscheine gebucht wird

# NUR datensätze betrachten, welche ALLE Zeiten enthalten
dataframe_picklisten_positionen = dataframe_picklisten_positionen.dropna(subset=['Pickzeit', 'Packzeit'])

dataframe_picklisten = dataframe_picklisten.dropna(subset=['Erstellungsdatum', 'FinishedTime', 'inProcessTime', 'PufferschieneTime'])
dataframe_picklisten['Picklistendauer'] = dataframe_picklisten['PufferschieneTime'] - dataframe_picklisten['Erstellungsdatum']

packdauer = dataframe_picklisten_positionen.groupby('PicklistenID')['Packzeit'].apply(lambda x: x.max() - x.min())
dataframe_picklisten['Packdauer'] = dataframe_picklisten['PicklistenID'].map(packdauer)

joined_dataframe = pd.merge(dataframe_picklisten, dataframe_picklisten_positionen, on=['PicklistenID']).sort_values(by='PicklistenPositionenID')

joined_dataframe['Year'] = pd.DatetimeIndex(joined_dataframe['Erstellungsdatum']).year
joined_dataframe['Month'] = pd.DatetimeIndex(joined_dataframe['Erstellungsdatum']).month
joined_dataframe['Day'] = pd.DatetimeIndex(joined_dataframe['Erstellungsdatum']).day

# Wie viele Lieferungen werden pro Monat gepickt
# display_picked_deliveries_by_year_and_month(joined_dataframe)

# Wie viele Lieferungen werden pro Monat und pro Cluster gepickt
display_picked_deliveries_by_year_and_month_and_cluster(joined_dataframe)

# Wie viele Artikel sind in diesen Lieferungen
display_picked_articles_by_year_and_month_and_cluster(joined_dataframe)

# Wie lange dauert im Durchschnitt eine Pickliste pro Cluster
# display_picklist_duration_per_cluster(dataframe_picklisten)

# Wie lange braucht ein Picker pro Lieferung in einem Cluster --> Dauer der Picklisten teilen durch Anzahl Lieferungen in Pickliste pro Cluster
# Wie viele Lieferungen enthält eine Pickliste pro Cluster
# display_duration_per_picked_delivery_per_cluster(joined_dataframe)


# Vision: Wie teile ich die Mitarbeiter ein um für den restlichen Tag am meisten Lieferungen rauszukriegen?
# Vision: Wie viele Leute brauche ich um den Rest der Lieferungen noch rauszukriegen?

# Vision/Ausblick: In welchem Cluster performt Mitarbeiter X am besten?
