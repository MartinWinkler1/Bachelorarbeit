import pandas as pd

dataframe_picklisten_raw = pd.read_csv('Picklisten.csv')
dataframe_picklisten_positionen_raw = pd.read_csv('PicklistenPositionen.csv')

dataframe_picklisten = dataframe_picklisten_raw[["PicklistenID", "Picker", "Erstellungsdatum", "Cluster", "Standort", "FinishedTime", "inProcessTime", "PufferschieneTime"]]
dataframe_picklisten_positionen = dataframe_picklisten_positionen_raw[["PicklistenPositionenID", "PicklistenID", "Menge", "Picker", "Pickzeit", "Packer", "Packzeit"]]

# Erstellungsdatum: createPicklist, getdate() wenn Eintrag erzeugt wird
# FinishedTime: finish-picklist/{PicklistenID}, beenden der Pickliste
# inProcessTime: setPickingListPositionDetail, jedes mal wenn ein Artikel gepickt wird (ergo Zeit wenn letzter Artikel gepickt wurde)
# PufferschieneTime: packagepicklist-to-pufferschiene/{PicklistenID}, wenn Pickliste auf Pufferscheine gebucht wird

# NUR datensätze betrachten, welche ALLE Zeiten enthalten
dataframe_picklisten = dataframe_picklisten.dropna(subset=['Erstellungsdatum', 'FinishedTime', 'inProcessTime', 'PufferschieneTime'])
dataframe_picklisten_positionen = dataframe_picklisten_positionen.dropna(subset=['Pickzeit', 'Packzeit'])

print(dataframe_picklisten.info())
print(dataframe_picklisten_positionen.info())

joined_dataframe = pd.merge(dataframe_picklisten, dataframe_picklisten_positionen, on=["PicklistenID"])
print(joined_dataframe.info())
