import os

import folium
import geopandas as gpd
import requests

c= folium.Map(location=[44.837789, -0.57918],zoom_start=13)




url1="https://opendata.bordeaux-metropole.fr/api/records/1.0/search/?rows=40&sort=-nbplaces&refine.commune=Bordeaux&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImNpX3ZjdWJfcCIsIm9wdGlvbnMiOnsic29ydCI6Ii1uYnBsYWNlcyIsInJlZmluZS5jb21tdW5lIjoiQm9yZGVhdXgiLCJiYXNlbWFwIjoiamF3Zy5zdHJlZXRzIiwibG9jYXRpb24iOiIxNCw0NC44NDE5OSwtMC41Nzc5In19LCJjaGFydHMiOlt7ImFsaWduTW9udGgiOnRydWUsInR5cGUiOiJsaW5lIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoiZ2lkIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2YzJhNSJ9XSwieEF4aXMiOiJtZGF0ZSIsIm1heHBvaW50cyI6bnVsbCwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&location=14,44.84199,-0.5779&basemap=jawg.streets&start=0&dataset=ci_vcub_p&timezone=Europe/Berlin&lang=fr"

url2="https://opendata.bordeaux-metropole.fr/api/records/1.0/search/?rows=40&sort=-nbplaces&refine.commune=Bordeaux&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImNpX3ZjdWJfcCIsIm9wdGlvbnMiOnsic29ydCI6Ii1uYnBsYWNlcyIsInJlZmluZS5jb21tdW5lIjoiQm9yZGVhdXgiLCJiYXNlbWFwIjoiamF3Zy5zdHJlZXRzIiwibG9jYXRpb24iOiIxNCw0NC44NDE5OSwtMC41Nzc5In19LCJjaGFydHMiOlt7ImFsaWduTW9udGgiOnRydWUsInR5cGUiOiJsaW5lIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoiZ2lkIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2YzJhNSJ9XSwieEF4aXMiOiJtZGF0ZSIsIm1heHBvaW50cyI6bnVsbCwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&location=14,44.84199,-0.5779&basemap=jawg.streets&start=40&dataset=ci_vcub_p&timezone=Europe/Berlin&lang=fr"

url3="https://opendata.bordeaux-metropole.fr/api/records/1.0/search/?rows=40&sort=-nbplaces&refine.commune=Bordeaux&dataChart=eyJxdWVyaWVzIjpbeyJjb25maWciOnsiZGF0YXNldCI6ImNpX3ZjdWJfcCIsIm9wdGlvbnMiOnsic29ydCI6Ii1uYnBsYWNlcyIsInJlZmluZS5jb21tdW5lIjoiQm9yZGVhdXgiLCJiYXNlbWFwIjoiamF3Zy5zdHJlZXRzIiwibG9jYXRpb24iOiIxNCw0NC44NDE5OSwtMC41Nzc5In19LCJjaGFydHMiOlt7ImFsaWduTW9udGgiOnRydWUsInR5cGUiOiJsaW5lIiwiZnVuYyI6IkFWRyIsInlBeGlzIjoiZ2lkIiwic2NpZW50aWZpY0Rpc3BsYXkiOnRydWUsImNvbG9yIjoiIzY2YzJhNSJ9XSwieEF4aXMiOiJtZGF0ZSIsIm1heHBvaW50cyI6bnVsbCwidGltZXNjYWxlIjoieWVhciIsInNvcnQiOiIifV0sImRpc3BsYXlMZWdlbmQiOnRydWUsImFsaWduTW9udGgiOnRydWV9&location=14,44.84199,-0.5779&basemap=jawg.streets&start=80&dataset=ci_vcub_p&timezone=Europe/Berlin&lang=fr"

def requete(url):
        
    req=requests.get(url)
    req=req.text

    req=req.split(', "record_timestamp":')
    for i in range(1,len(req)-1):
        req[i]=req[i].split(', "')
        coords=req[i][4].split('geo_point_2d": ')
        for j in range(len(coords)):
            coords[j]=coords[j].replace("]","")
            coords[j]=coords[j].replace("[","")
        
        coords[1]=coords[1].split(",")
        lat=float(coords[1][0])
        long=float(coords[1][1])

        req[i][5]=req[i][5].split(":")
        velos_dispo=req[i][5][1]
        velos_dispo=velos_dispo.replace('"',"")
        req[i][10]=req[i][10].split(":")
        places_dispo=req[i][10][1]

        req[i][13]=req[i][13].split(":")
        nom=req[i][13][1]

        req[i][15]=req[i][15].split(":")
        velos_elec_dispo=req[i][15][1]
        velos_elec_dispo=velos_elec_dispo.replace('"',"")
        total=int(velos_dispo)+int(velos_elec_dispo)
        message="""<b>Station : </b>{0}<br><b>Vélos dispos ( dont elec) : </b>{1} ({2})<br><b>Places dispos : </b>{3}""".format(nom,total,velos_elec_dispo,places_dispo)
        iframe = folium.IFrame(message)
        popup=folium.Popup(iframe,min_width=300,max_width=300,height=10)
        folium.Marker([lat,long],popup=popup).add_to(c)
    


requete(url1)
requete(url2)
requete(url3)





c.save('vcub-map.html')
