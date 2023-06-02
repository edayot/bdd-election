import folium
import json
import numpy as np
import matplotlib.pyplot as plt
import os
import pyodbc
import ast
import numpy as np

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    return '#%02x%02x%02x' % rgb_color

def average_color(hex_colors, sizes):
    rgb_colors = [hex_to_rgb(hex_color) for hex_color in hex_colors]
    num_colors = len(rgb_colors)
    
    weighted_sum = [0, 0, 0]
    total_size = sum(sizes)
    
    for i in range(num_colors):
        weight = sizes[i] / total_size
        weighted_rgb = [col * weight for col in rgb_colors[i]]
        weighted_sum = [weighted_sum[j] + weighted_rgb[j] for j in range(3)]
    
    avg_rgb = [int(col) for col in weighted_sum]
    avg_hex = rgb_to_hex(tuple(avg_rgb))
    
    return avg_hex

def style_function(feature):
    return {
        'fillOpacity': 0.5,
        'weight': 0,
        'fillColor': feature["properties"]["color"]
    }
def highlight_function(feature):
    return {
        'fillOpacity': 0.5,
        'weight': 2,
        'fillColor': 'white'
    }

def display_departement(id,id_election):
    path = "C:\\Users\\erwan\\Documents\\Dev\\bdd-election\\_Elections.accdb"
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path + ';')

    cursor = conn.cursor()

    query="""
SELECT Count(*) AS NombreVotes, Candidats.Id_Parti, Bulletin.Id_election, Bulletin.Id_bureaux, CNI.Nom, CNI.Prenom, Type_Elections.Type, Elections.date_premier_tour
FROM Type_Elections INNER JOIN (Elections INNER JOIN (CNI INNER JOIN (Candidats INNER JOIN (Bulletin INNER JOIN Liste_Candidats ON (Bulletin.Id_election = Liste_Candidats.Id_Elections) AND (Bulletin.Id_vote = Liste_Candidats.Id_Candidats)) ON Candidats.Id_Candidats = Liste_Candidats.Id_Candidats) ON CNI.NuméroCNI = Candidats.Id_CNI) ON Elections.Id = Liste_Candidats.Id_Elections) ON Type_Elections.Id = Elections.type_elections
WHERE Bulletin.Id_election = ?
GROUP BY Candidats.Id_Parti, Bulletin.Id_election, Bulletin.Id_bureaux, CNI.Nom, CNI.Prenom, Type_Elections.Type, Elections.date_premier_tour, Bulletin.Id_vote;


    """
    cursor.execute(query,id_election)
    results=cursor.fetchall()
    print(results)

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

    



    m = folium.Map(location=[48.8, 3.0], zoom_start=5)
    for row in rows:
        global a
        a=row[2]
        
        
        
        # Create a pie chart
        # using the result list find all maching results
        result = [x for x in results if x[3]==row[1]]
        
        # take the r[0] for the number of votes and r[5] + r[4] for the name of the candidate
        labels = [f"{r[5]} {r[4]}" for r in result]

        colors=[]
        for r in result:
            cursor = conn.cursor()
            # Select the color of the party in "Parti Politique" table
            queryy=f"""
            SELECT Parti_Politique.Couleur FROM Parti_Politique
WHERE Parti_Politique.ID_Parti = ?
            """

            cursor.execute(queryy,r[1])
            colors.append("#"+cursor.fetchall()[0][0])

        # take the r[0] for the number of votes
        sizes = [r[0] for r in result]

        # Select the color with the most votes
        max_color = "#FFFFFF"
        max_color = average_color(colors, (np.array(sizes))**2)

        print(max_color, row[1])
        
        feature={
            "type":row[0],
            "geometry":ast.literal_eval(row[2]),
            "properties":{
                "ID":row[1],
                "color":max_color
            }
        }
        circ=folium.GeoJson(feature,highlight_function=highlight_function,style_function=style_function)
        name=f"{dpt_name} {row[1]}"
        circ.add_child(folium.Tooltip(name))


        #print(colors)
            

        
        # Create the pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90,colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(name)
        #


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
    conn.close()


def display_all(id_election):
    path = "C:\\Users\\erwan\\Documents\\Dev\\bdd-election\\_Elections.accdb"
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + path + ';')
    
    cursor = conn.cursor()

    query="""
SELECT Count(*) AS NombreVotes, Candidats.Id_Parti, Bulletin.Id_election, Bulletin.Id_bureaux, CNI.Nom, CNI.Prenom, Type_Elections.Type, Elections.date_premier_tour
FROM Type_Elections INNER JOIN (Elections INNER JOIN (CNI INNER JOIN (Candidats INNER JOIN (Bulletin INNER JOIN Liste_Candidats ON (Bulletin.Id_election = Liste_Candidats.Id_Elections) AND (Bulletin.Id_vote = Liste_Candidats.Id_Candidats)) ON Candidats.Id_Candidats = Liste_Candidats.Id_Candidats) ON CNI.NuméroCNI = Candidats.Id_CNI) ON Elections.Id = Liste_Candidats.Id_Elections) ON Type_Elections.Id = Elections.type_elections
WHERE Bulletin.Id_election = ?
GROUP BY Candidats.Id_Parti, Bulletin.Id_election, Bulletin.Id_bureaux, CNI.Nom, CNI.Prenom, Type_Elections.Type, Elections.date_premier_tour, Bulletin.Id_vote;


    """
    cursor.execute(query,id_election)
    results=cursor.fetchall()

    

    cursor = conn.cursor()
    query=f"""
    SELECT Toxicode.type, Toxicode.ID, Toxicode.geometry, Toxicode.code_dpt FROM Toxicode
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    



    m = folium.Map(location=[48.8, 3.0], zoom_start=5)
    for row in rows:
        global a
        a=row[2]
        
        
        
        # Create a pie chart
        # using the result list find all maching results
        result = [x for x in results if x[3]==row[1]]
        
        # take the r[0] for the number of votes and r[5] + r[4] for the name of the candidate
        labels = [f"{r[5]} {r[4]}" for r in result]

        colors=[]
        for r in result:
            cursor = conn.cursor()
            # Select the color of the party in "Parti Politique" table
            queryy=f"""
            SELECT Parti_Politique.Couleur FROM Parti_Politique
WHERE Parti_Politique.ID_Parti = ?
            """

            cursor.execute(queryy,r[1])
            colors.append("#"+cursor.fetchall()[0][0])

        # take the r[0] for the number of votes
        sizes = [r[0] for r in result]

        # Select the color with the most votes
        max_color = "#FFFFFF"
        max_color = average_color(colors, np.exp((np.array(sizes))))

        #print(max_color, row[1])
        
        feature={
            "type":row[0],
            "geometry":ast.literal_eval(row[2]),
            "properties":{
                "ID":row[1],
                "color":max_color
            }
        }
        circ=folium.GeoJson(feature,highlight_function=highlight_function,style_function=style_function)

        cursor = conn.cursor()
        query=f"""
        SELECT Departement.nom_departement FROM Departement
        WHERE Departement.code_departement = ? 
        """
        id=row[3]
        if id[0]=="0":
            cursor.execute(query,id[1:])
        else:
            cursor.execute(query,id[:])
        #print(id)
        try:
            dpt_name=cursor.fetchall()[0][0]
        except:
            dpt_name="Non trouvé"

        name=f"{dpt_name} {row[1]}"
        circ.add_child(folium.Tooltip(name))


        #print(colors)
            

        
        # Create the pie chart
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90,colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.set_title(name)
        #


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
    

    # Ajout des résultats nationaux

    query="""
SELECT DISTINCTROW CNI.Nom, CNI.Prenom, Elections.Id, Elections.date_premier_tour, Type_Elections.Type, Count(*) AS [Compte De Bulletin]
FROM Type_Elections INNER JOIN (Elections INNER JOIN (CNI INNER JOIN (Candidats INNER JOIN (Bulletin INNER JOIN Liste_Candidats ON (Bulletin.Id_vote = Liste_Candidats.Id_Candidats) AND (Bulletin.Id_election = Liste_Candidats.Id_Elections)) ON Candidats.Id_Candidats = Liste_Candidats.Id_Candidats) ON CNI.NuméroCNI = Candidats.Id_CNI) ON Elections.Id = Liste_Candidats.Id_Elections) ON Type_Elections.Id = Elections.type_elections
WHERE Bulletin.Id_election = ?
GROUP BY CNI.Nom, CNI.Prenom, Elections.Id, Elections.date_premier_tour, Type_Elections.Type, Bulletin.Id_vote, Bulletin.Id_election;
    """
    cursor.execute(query,id_election)

    results=cursor.fetchall()
    # Create a pie chart
    # using the result list find all maching results

    sizes = [r[5] for r in results]
    labels = [f"{r[1]} {r[0]}" for r in results]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title("Résultats nationaux")
    
    plt.savefig(f"graph/pie_national.png")
    
      

    conn.close()













    
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
