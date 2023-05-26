import folium
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pyodbc
import ast

def style_function(feature):
    # Random color
    color = "#"+''.join([np.random.choice(list('0123456789ABCDEF')) for j in range(6)])
    return {
        'fillOpacity': 0.5,
        'weight': 0,
        'fillColor': color
    }
def highlight_function(feature):
    return {
        'fillOpacity': 0.5,
        'weight': 2,
        'fillColor': 'white'
    }

def display_departement(id):
    path = "C:\\Users\\erwan\\Documents\\Dev\\bdd-election\\_Elections.accdb"
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path + ';')

    cursor = conn.cursor()
    query=f"""
    SELECT Departement.nom_departement FROM Departement
    WHERE Departement.code_departement = ? 
    """
    if id[0]=="0":
        cursor.execute(query,id[1:])
    else:
        cursor.execute(query,id[:])

    dpt_name=cursor.fetchall()[0][0]
    print(dpt_name)

    cursor = conn.cursor()
    query=f"""
    SELECT Toxicode.type, Toxicode.ID, Toxicode.geometry FROM Toxicode
    WHERE Toxicode.code_dpt = ? 
    """
    cursor.execute(query,id)
    rows = cursor.fetchall()

    conn.close()



    m = folium.Map(location=[48.8, 3.0], zoom_start=5)
    for row in rows:
        global a
        a=row[2]
        feature={
            "type":row[0],
            "geometry":ast.literal_eval(row[2]),
            "properties":{
                "ID":row[1]
            }
        }
        
        circ=folium.GeoJson(feature,highlight_function=highlight_function,style_function=style_function)
        name=f"{dpt_name} {row[1]}"
        circ.add_child(folium.Tooltip(name))
        # Create a pie chart
        fig, ax = plt.subplots()
        labels = ['Mélenchon', 'Le Pen', 'Macron', 'Fillon', 'Hamon', 'Dupont-Aignan', 'Poutou', 'Asselineau', 'Arthaud', 'Cheminade']
        sizes = np.random.randint(1, 100, len(labels))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(name)
        # Save the file with random name
        try:
            os.mkdir("graph")
        except:
            pass
        plt.savefig(f"graph/pie_{row[1]}.png")
        plt.close(fig)


        # Add the pie chart to the map
        graph_html = '<img src="{}">'.format(f"graph/pie_{row[1]}.png")
        popup = folium.Popup(graph_html, max_width=2650)
        popup.add_to(circ)
        circ.add_to(m)
    m.save('map.html')

    
        





"""

m = folium.Map(location=[48.8, 3.0], zoom_start=5)


# Open france-circonscriptions-legislatives-2012.json and draw the geojson

json_file = open('france-circonscriptions-legislatives-2012.json', 'r')
json_data = json.load(json_file)



for i,feature in enumerate(json_data["features"][:]):
    name=f"{feature['properties']['nom_dpt']} {feature['properties']['num_circ']}"

    circ=folium.GeoJson(feature,style_function=style_function,highlight_function=highlight_function)
    circ.add_child(folium.Tooltip(name))

    # Create a pie chart
    fig, ax = plt.subplots()
    labels = ['Mélenchon', 'Le Pen', 'Macron', 'Fillon', 'Hamon', 'Dupont-Aignan', 'Poutou', 'Asselineau', 'Arthaud', 'Cheminade']
    sizes = np.random.randint(1, 100, len(labels))
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title(name)
    # Save the file with random name
    try:
        os.mkdir("graph")
    except:
        pass
    plt.savefig(f"graph/pie_{i}.png")
    plt.close(fig)


    # Add the pie chart to the map
    graph_html = '<img src="{}">'.format(f"graph/pie_{i}.png")
    popup = folium.Popup(graph_html, max_width=2650)
    popup.add_to(circ)


    




    circ.add_to(m)

m.save('map.html')

    
"""
