from networkx.classes import neighbors
import networkx as nx
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


App = dash.Dash(__name__)
    
"""
Retourne le noeud qui correspond au coordonnées passé en
paramètre dans la séquence. (On utilisera Pos)
"""
def searchByPos(x,y,seq) :
    for elt in seq.keys() :
        if seq[elt][0] == x and seq[elt][1] == y :
            return elt
    return None

"""
Attribue à chque communauté une couleur selon son état.
"""
def colored(seq,nb_nodes,hearth) :
    res = []
    for com in range(0,nb_nodes) :
        if com == hearth :
            text = 'rgb(0,255,0)'
        else :    
            if seq[com]!=0 :
                text = 'rgb('+str(255*(1-seq[com]))+',0,0)'
            else :
                text = 'rgb(255,255,255)'
        res.append(text)
    return res
 
"""
Modifie la variable Burned_nodes qui contient tous les noeuds brulés.
A partir du foyer mis en paramètre.
Met à jour le tableau Com_percent_size.
"""   
def update_fire(Graph,hearth) :    
    Burned_nodes.add(hearth)
    new_burned_nodes = set()
    for burned_node in Burned_nodes :
        for neighbor in neighbors(Graph,burned_node) :
            if neighbor not in Burned_nodes :
                new_burned_nodes.add(neighbor)
    Burned_nodes.update(new_burned_nodes)     
    #Update number of burned nodes by community
    Com_size_fire[Com_vector[hearth]] += 1
    for burned_node in new_burned_nodes :
        if burned_node not in Burning_sequence :
            Com_size_fire[Com_vector[burned_node]] +=1
    #Update percent of burned nodes by community        
    for com in MetaGraph :
        Com_percent_fire[com] = Com_size_fire[com] / Com_size[com]   
               

"""
Initialise le graphique, les variables globales et lance l'app.
"""                
def draw(graph,burning_sequence,com_vector,metagraph=None) :
    print("Computing display...")
    #Global Variables
    global App     

    global Graph
    Graph = graph.copy()
    
    global Com_vector
    Com_vector = com_vector
    
    #Metagraph setting is optionnal, will be initialize is not given
    global MetaGraph
    if metagraph is not None :
        MetaGraph = metagraph
    else:
        MetaGraph = nx.Graph()
        for edge in graph.edges() :
            com_1 = Com_vector[edge[0]]
            com_2 = Com_vector[edge[1]]
            if com_1 not in MetaGraph.nodes() :
                MetaGraph.add_node(com_1)
            if com_2 not in MetaGraph.nodes() :
                MetaGraph.add_node(com_2)
            if com_1 != com_2 :
                if not MetaGraph.has_edge(com_1,com_2) :
                    MetaGraph.add_edge(com_1,com_2)
                    
    #Associate Node to a coordinate
    global Pos
    Pos = nx.layout.spring_layout(MetaGraph)
    
    global Burning_sequence
    i = 0
    Burning_sequence = [0]*len(burning_sequence)
    for elt in burning_sequence :
        Burning_sequence[i] = elt
        i = i +1 
    
    global Burned_nodes
    Burned_nodes = set()
    
    global Index
    Index = 0
    
    #Associate community with its size
    global Com_size
    Com_size = [0]*MetaGraph.number_of_nodes()    
    for i in range(0,Graph.number_of_nodes()) :
        Com_size[Com_vector[i]] += 1 
    
    #Associate community wiith its number of burned nodes
    global Com_size_fire
    Com_size_fire = [0]*MetaGraph.number_of_nodes()  
    
    #Associate community with its percentage of burned nodes
    global Com_percent_fire
    Com_percent_fire = [0]*MetaGraph.number_of_nodes()
    
    #Draw the trace of edges
    edge_trace_x = [0]*(3*len(MetaGraph.edges()))
    edge_trace_y = [0]*(3*len(MetaGraph.edges()))
    index = 0
    for edge in MetaGraph.edges():
        x0 = Pos[edge[0]][0]
        y0 = Pos[edge[0]][1]
        x1 = Pos[edge[1]][0]
        y1 = Pos[edge[1]][1]
        edge_trace_x[index] = x0
        edge_trace_y[index] = y0
        index+=1
        edge_trace_x[index] = x1
        edge_trace_y[index] = y1
        index+=1
        edge_trace_x[index] = None
        edge_trace_y[index] = None
        index+=1        
    edge_trace = go.Scatter(
        x=edge_trace_x,
        y=edge_trace_y,                            
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',                       
        mode="lines")
    
    #Create the sequence which contains the color of nodes
    color_seq = [0]*MetaGraph.number_of_nodes()
    color_seq = colored(Com_percent_fire,MetaGraph.number_of_nodes(),Com_vector[Burning_sequence[Index]])
    
    #Draw the trace of node
    node_trace_x = []
    node_trace_y = []
    node_trace_text = []    
    for node in MetaGraph.nodes():
        x = Pos[node][0]
        y = Pos[node][1]
        node_trace_x.append(x)
        node_trace_y.append(y)
        node_trace_text.append(node)        
    node_trace = go.Scatter(
        x=node_trace_x,
        y=node_trace_y,
        text=node_trace_text,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            color=color_seq,
            size=30, 
            line=dict(width=2)))
   
    #Draw the figure which contains edge_trace and node_trace 
    global Fig
    Fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))
    Fig.update_layout(plot_bgcolor='rgb(72,70,92)',paper_bgcolor = 'rgb(72,70,92)')
    
    #Create the html page which will be use by Dash
    App.layout = html.Div([
        html.H1("MétaGraphe de "+str(MetaGraph.number_of_nodes())+" communautés"),
        html.Div(dcc.Graph(id='Graph',figure=Fig)),
        html.Div(html.P('En vert la communauté du prochain foyer * ',className='anotation')),
        html.Div(id='resultat'),
        html.Button('Brûlons!',id='button'),
        html.Div(id='output')                
       ]) 
    App.run_server()   

"""
Affiche les données de la communauté sur laquelle l'on passe sa souris.
"""
@App.callback(
        Output('output','children'),
        [Input('Graph','hoverData')])
def display_selected_data(hoverData):
    if hoverData is not None :
        x = hoverData['points'][0]['x']
        y = hoverData['points'][0]['y']
        com = searchByPos(x, y, Pos)
        text_com = 'Communauté : '+ str(com)
        text_size = ' Taille : ' + str(Com_size[com])
        text_size_fire = ' Taille du Feu : ' + str(Com_size_fire[com])
        text_percent_fire = ' Pourcentage de Brûlure : ' + str(round(Com_percent_fire[com]*100,2)) + '%'
        return [html.P(text_com),html.P(text_size),html.P(text_size_fire),html.P(text_percent_fire)]
    else :
        return [html.P("")]    
"""    
Répends le feu à travers le graphe et met à jour la couleur des noeuds. 
"""
@App.callback( 
    Output('Graph','figure'),
    [Input('button','n_clicks')])
def update_graph(n_clicks):
    #specify with use global Index
    global Index    
    if Index != len(Burning_sequence):
        #At the load of the page n_clicks = None
        if n_clicks is not None :
            update_fire(Graph,Burning_sequence[Index])
            Index += 1
        if Index != len(Burning_sequence) :   
            color_seq = colored(Com_percent_fire,MetaGraph.number_of_nodes(),Com_vector[Burning_sequence[Index]])
            Fig.update_traces(
                marker=dict(
                    color=color_seq,
                    size=30, 
                    line=dict(width=2)))
    #Trigger on last Turn, Erase the hearth point color
    if Index == len(Burning_sequence) :
        color_seq = colored(Com_percent_fire,MetaGraph.number_of_nodes(),-1)
        Fig.update_traces(
            marker=dict(
                color=color_seq,
                size=30, 
                line=dict(width=2)))  
    return Fig
    
"""    
Affiche le Burning number quand le feu s'est entièrement répandu
"""
@App.callback(
    Output('resultat','children'),
    [Input('button','n_clicks')])
def display_results(n_clicks) :
    if Index == len(Burning_sequence) :
        burning_number = 'Burning Number : ' + str(len(Burning_sequence))
        return [html.P(burning_number,className='burning')]
    else :
        return [html.P("")]