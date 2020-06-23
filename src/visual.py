from networkx.classes import neighbors
import networkx as nx
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


App = dash.Dash(__name__)
    
"""
Attribue à chque noeud une couleur selon son état.
"""
def colored(burned_nodes,nb_nodes,hearth) :
    res = []
    for node in range(0,nb_nodes) :
        if node == hearth :
            text = 'rgb(0,255,0)'
        else :    
            if node in burned_nodes :
                text = 'rgb(255,0,0)'
            else :
                text = 'rgb(255,255,255)'
        res.append(text)
    return res

"""
Modifie la variable Burned_nodes qui contient tous les noeuds brulés.
A partir du foyer mis en paramètre.
"""   
def update_fire(Graph,hearth) :
    Burned_nodes.add(hearth)
    new_burned_nodes = set()
    for burned_node in Burned_nodes :
        for neighbor in neighbors(Graph,burned_node) :
                new_burned_nodes.add(neighbor)
    Burned_nodes.update(new_burned_nodes)
                
"""
Initialise le graphique, les variables globales et lance l'app.
"""                
def draw(graph,burning_sequence) :
    print("Computing display...")
    #Global Variables
    global App 
    
    global Graph
    Graph = graph.copy()
    
    #Associate Node with coordinate
    global Pos
    Pos = nx.layout.spring_layout(graph) 
    
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
     
    #Draw the trace of edges
    edge_trace_x = [0]*(3*len(Graph.edges()))
    edge_trace_y = [0]*(3*len(Graph.edges()))
    index = 0 
    for edge in Graph.edges():
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
    color_seq = [0]*Graph.number_of_nodes()
    color_seq = colored(Burned_nodes,Graph.number_of_nodes(),Burning_sequence[Index])
    
    #Draw the trace of node
    node_trace_x = []
    node_trace_y = []
    node_trace_text = []
    for node in graph.nodes():
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
        html.H1("Graphe de "+str(Graph.number_of_nodes())+" Noeuds"),
        html.Div(dcc.Graph(id='Graph',figure=Fig)),
        html.Div(html.P('En vert le prochain foyer * ',className='anotation')),
        html.Div(id='resultat'),
        html.Button('Brûlons!',id='button'),
        html.Div(id='output')                
       ]) 
    App.run_server()  
    
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
            color_seq = colored(Burned_nodes,Graph.number_of_nodes(),Burning_sequence[Index])
            Fig.update_traces(
                marker=dict(
                    color=color_seq,
                    size=30, 
                    line=dict(width=2)))
    #Trigger on last Turn, Erase the hearth point color
    if Index == len(Burning_sequence) :
        color_seq = colored(Burned_nodes,Graph.number_of_nodes(),-1)
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
    if Index == len(Burning_sequence):
        burning_number = 'Burning Number : ' + str(len(Burning_sequence))
        return [html.P(burning_number,className='burning')]
    else :
        return [html.P("")]