import pandas as pd
import matplotlib.pyplot as plt

dataframe_picklisten_raw = pd.read_csv('Picklisten.csv')
dataframe_picklisten_positionen_raw = pd.read_csv('PicklistenPositionen.csv')

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

picked_positions_by_year_and_month = joined_dataframe.groupby(['Year', 'Month'])['PicklistenPositionenID'].count().reset_index()
picked_positions_by_year_and_month = picked_positions_by_year_and_month.rename(columns={'PicklistenPositionenID': 'PickedPositions'})
picked_positions_by_year_and_month['YearAndMonth'] = picked_positions_by_year_and_month['Year'].astype(str) + '-' + picked_positions_by_year_and_month['Month'].astype(str)

x = picked_positions_by_year_and_month['YearAndMonth'].to_list()
y = picked_positions_by_year_and_month['PickedPositions'].to_list()

plt.bar(x, y)
plt.xlabel("Monat und Jahr")
plt.ylabel("Gepickte Positionen")
plt.title("Gepickte Positionen pro Monat und Jahr")
plt.show()
