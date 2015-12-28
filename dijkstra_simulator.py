#importing the required libraries 
#Tkinter is standard GUI package
#matplotlib provides object oriented API for embedding plots in GUI
#pylab interface used for interactive calculations and plotting

import Tkinter as tk
import ttk
import tkMessageBox
import tkFileDialog
import copy
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pylab


#different types of fonts used

LARGE_FONT= ("Verdana", 20)
MEDIUM_FONT= ("Verdana",16)
SMALL_FONT= ("Verdana",12)


#User defined custom exception, used for catching incorrect node values

class IncorrectNodeException(Exception):
    pass

#main class for UI
class SeaofBTCapp(tk.Tk):
    
    #def __init__ is the function that is called automatically upon an object's construction
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Computer Networks Project")
        
        #container for all the frames
        
        self.container = tk.Frame(self)
        
        #self is used to reference the object itself
        
        self.container.pack(side="top", fill="both", expand = True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
                
        self.frames = {}
        # this is a dictionary of frames
        
        #all static windows are contained in this frame
        for F in (StartPage, enter_source_node,selection_page,add_node_page,add_edge_page):

            frame = F(self.container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        
    #used to display a frame
    
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        #tkraise shows one window at a time by bringing a window in front of the other
        
    #method for formation of connection table    
    def connection_table(self,pre, source, g):
       
        nodes = len(g[0])
        a = copy.copy(pre)
        c = {}
        c[source] = '-'
        for i in range(nodes):

            l = []

            if i == source:
                continue
            j = i
            l = [i]
            while j != source:
                l.append(a[j][0])
                j =a[j][0]
            l = l[::-1]

            c[i] = l[1]
        return c
        #returns a dictionary of values in the connection table

        
    def dijkstra_algo(self,g, source):
        
        #implementation of dijkstra algorithm
        
        nodes = len(g[0])
        pre = {}
        dist = {}
        q = []
        for i in range(nodes):
            dist[i] = 999
            pre[i] = [-1]
            q.append(i)
        dist[source] = 0

        while len(q) != 0:
            n_dist = {}
            for i in q:
                n_dist[i] = dist[i]
            u = min(n_dist.items(), key=lambda x: x[1])
            u = u[0]
            q.remove(u)
            for i in range(nodes):
                if g[u][i] not in [0,-1]:
                    alt = dist[u] + g[u][i]
                    if alt < dist[i]:
                        dist[i] = alt
                        pre[i] = [u]
                    elif alt == dist[i]:
                        pre[i].append(u)

        return pre
    

    
    def get_the_network(self):
        
            #reading the matrix file that is taken as an input from the user
        try:
            file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
            data=file.read()
            g  = []
            data = data.split('\n')
            for i in data:
                g.append(map(int,i.split()))
            self.data = g
            
           
            
            self.show_frame(enter_source_node)
            
        #Exception for invalid entry like special characters or any other combinations.
        except ValueError:
            tkMessageBox.showerror(
            "Input File Error",
            "Oops! That was not a valid input file. Please Try again with a valid '.txt' file..."
        )
    
    #method to get the source node entry from the user
    def get_source(self, source):
        
        try:
            self.source = int(source.get())
            
            #Checking if source entered not a valid node from topology, then an exception will be raised
            
            if self.source > (len(self.data)-1):
                raise IncorrectNodeException
        
            self.show_frame(selection_page)
        
        #Exception for invalid entry like special characters or any other combinations.
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a valid Source Node..."
        )
        
        #Custom exception for incorrect node or any other integer other than node entered
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "Oops! That was not a valid node for the topology selected. Please Try again with a valid Source Node..."
        )
        return
    
    #method to display the network    
    def display_network(self):
        
        frame = display_network_page(self.container, self)

        self.frames[display_network_page] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(display_network_page)
    
    #method to create an object for destination page and raising it above other windows
    def enter_destination(self):
        
        try:
            self.pre = self.dijkstra_algo(self.data,self.source)
        
            self.connection = self.connection_table(self.pre,self.source,self.data)
        
            frame = enter_destination_page(self.container, self)

            self.frames[enter_destination_page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
            self.show_frame(enter_destination_page)
        
        except IndexError:
            tkMessageBox.showerror(
            "Memory Error",
            "Oops! There are too many destinations entered earlier. Please use Back to Home button to start again from fresh..."
        )
        return
    
    #method to get the destination node from the user
    def network_to_destination(self,entry):
        
        try:
        
            self.destination = int(entry.get())
            
            #Checking if destination entered not a valid node from topology, then an exception will be raised
            
            if self.destination > (len(self.data)-1):
                raise IncorrectNodeException
        
            frame = network_to_destination_page(self.container, self)

            self.frames[network_to_destination_page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
            self.show_frame(network_to_destination_page)
        
        
        #Exception for invalid entry like special characters or any other combinations.
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a valid Destination Node..."
        )
        
        #Custom exception for incorrect node or any other integer other than destination node entered
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "Oops! That was not a valid node for the topology selected. Please Try again with a valid Destination Node..."
        )
        return
        
    #method to create an object of connection table frame and raising it above other windows   
    def display_connection_table(self):
        
        try:
        
            self.pre = self.dijkstra_algo(self.data,self.source)
        
            self.connection = self.connection_table(self.pre,self.source,self.data)
        
            frame = display_connection_table_page(self.container, self)

            self.frames[display_connection_table_page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
        

            self.show_frame(display_connection_table_page)
        
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a valid weights..."
        )
        except IndexError:
            tkMessageBox.showerror(
            "Memory Error",
            "Oops! There are too many connection tables opened earlier. Please use Back to Home button to start again from fresh..."
        )
        return
    
    #method to create an object of display shortest path frame and raising it above other windows
    def display_shortest_path(self):
        
        try:
        
            self.pre = self.dijkstra_algo(self.data,self.source)
        
            self.connection = self.connection_table(self.pre,self.source,self.data)
        
                
            frame = display_shortest_path_page(self.container, self)

            self.frames[display_shortest_path_page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
            self.show_frame(display_shortest_path_page)
        
        except IndexError:
            tkMessageBox.showerror(
            "Memory Error",
            "Oops! There are too many shortest paths displayed earlier. Please use Back to Home button to start again from fresh..."
        )
        return
    
    #method to add a node    
    def add_node(self,new_node):
        
        try:
        
            
            self.new_node = new_node.get().split()
            self.new_node = map(int,self.new_node)
            
            if len(self.new_node) != len(self.data):
                raise IncorrectNodeException
        
            self.new_node.append(0)
            
            
                
            for i in range(len(self.data)):
                self.data[i].append(self.new_node[i])
            
            

            self.data.append(self.new_node)
        
        
            self.show_frame(selection_page)

        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a valid weights..."
        )
        except IndexError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a space between values..."
        )
            
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "Oops! That was not a valid number of node. Please Try with %s nodes..." % len(self.data)
        )
        return
         
    
    #method to add an edge
    def add_edge(self,new_edge,new_weight):
        
        try:
            
            self.new_edge = new_edge.get().split()
            self.new_edge = map(int,self.new_edge)
            
            #Checking if entered edge, whose weight needs to be modified contains two valid nodes from topology, 
            #if not raise an exception
            
            for i in self.new_edge:
                if i not in range(0, len(self.data)):
                    raise IncorrectNodeException
        
            self.new_weight = new_weight.get()
            self.new_weight = int(self.new_weight)
        
    
            self.data[self.new_edge[0]][self.new_edge[1]] = self.new_weight
            self.data[self.new_edge[1]][self.new_edge[0]] = self.new_weight
        
        
            self.show_frame(selection_page)
        
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a valid weight..."
        )
        except IndexError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a space between values..."
        )
            
        #Custom exception for incorrect node or any other integer other than destination node entered
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "Oops! That was not a valid node for the topology selected. Please Try again with a valid Node for Edge..."
        )
        return
              
class StartPage(tk.Frame):
    
    #StartPage is inheriting from TK FRAME
    
    #here controller represents the container
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        #creating a label
        
        label = ttk.Label(self, text="Implementation Of Dijkstra Algorithm", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #creating a button 
        button = ttk.Button(self, text="Enter the network matrix",
                            command=lambda: controller.get_the_network())
        button.pack()

        
class enter_source_node(tk.Frame):
    
    #enter_source_node is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        label = ttk.Label(self, text="Please Enter the source node", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        entry = ttk.Entry(self, width=10)
        entry.pack(pady=10,padx=10)
        
        #creating a button
        
        button = ttk.Button(self, text="Enter!!",
                            command=lambda: controller.get_source(entry))
        button.pack(pady=10,padx=10)
        
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)
        
class selection_page(tk.Frame):
     
    #selection_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        label = ttk.Label(self, text="Select from the following options", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        #creating buttons
        
        #click button to display the network frame
        
        button1 = ttk.Button(self, text="Display the Network",
                            command=lambda: controller.display_network())
        button1.pack(pady=10,padx=10)
        
        #click button to display the connection table frame
        
        button2 = ttk.Button(self, text="Display the connection table",
                            command=lambda: controller.display_connection_table())
        button2.pack(pady=10,padx=10)
        
        #click button to display the shortest path to all nodes frame
        
        button3 = ttk.Button(self, text="Display the shortest path to all nodes",
                            command=lambda: controller.display_shortest_path())
        button3.pack(pady=10,padx=10)
        
        #click button to display path to a destination frame
        
        button6 = ttk.Button(self, text="Display path to a destination",
                            command=lambda: controller.enter_destination())
        button6.pack(pady=10,padx=10)
        
        #click button to add an extra node frame
        
        button4 = ttk.Button(self, text="Add an extra node",
                            command=lambda: controller.show_frame(add_node_page))
        button4.pack(pady=10,padx=10)
        
        #click button to add or modify the edge weight frame

        button5 = ttk.Button(self, text="Add or modify edge weight",
                            command=lambda: controller.show_frame(add_edge_page))
        button5.pack(pady=10,padx=10)
        
        #click button to take us back to the home page frame

        button6 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button6.pack(pady=10,padx=10)
        
        #click button to take us back to the selection page frame
        
        button7 = ttk.Button(self, text="Back to Source Node Selection Page",
                            command=lambda: controller.show_frame(enter_source_node))
        button7.pack(pady=10,padx=10)

    
        
class display_connection_table_page(tk.Frame):
    
    #display_connection_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a scrollbar to scroll through the connection table frame
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = tk.RIGHT, fill= tk.Y)
       
        #creating a list box to populate the connection table 
    
        mylist = tk.Listbox(self, yscrollcommand = scrollbar.set ) 
        mylist.insert(tk.END, "\nRouter %s Connection Table \n" % controller.source)
        
        mylist.insert(tk.END, "{:<8} {:<15}".format('Destination ',' Interface'))
                       
        for k, v in controller.connection.iteritems():
            mylist.insert(tk.END,"\t {:<8} \t {:<15}".format(k, v))
            mylist.insert(tk.END,"\n")
            
        mylist.pack(fill = "both",expand=True)   
        
        #creating a button and click the button to get back to selection page
        
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        
        button1.pack()
        
class display_shortest_path_page(tk.Frame):
    
    #display_shortest_path_page is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        main_graph = nx.Graph()
        i=0
        for row in controller.data:
            j=0
            for col in row:
                if col not in [0,-1]:
                    main_graph.add_edge(i,j, weight = int(controller.data[i][j]) )

                j = j+1
            i = i+1
            
        
        #creating scrollbar to scroll through the shortest path frame
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = tk.RIGHT, fill= tk.Y)
        
        mylist = tk.Listbox(self, yscrollcommand = scrollbar.set )
        self.a = copy.copy(controller.pre)
        for i in range(len(controller.data)):
            

            if i == controller.source:
                continue
            
            mylist.insert(tk.END,"smallest path from node %s to node %s" % (controller.source,i))
            
               
            paths = nx.all_shortest_paths(main_graph,source=controller.source,target= i, weight = 'weight')
            
            for path in paths:
                
                mylist.insert(tk.END,"path = %s" % path)
            
                self.cost = self.calculating_total_cost(path,controller.data)
            
                mylist.insert(tk.END,"Cost = %s " % self.cost)
                mylist.insert(tk.END,"\n")
        
        
        scrollbar.config( command = mylist.yview )
        mylist.pack(fill = "both",expand=True)
            
            
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
               
        button1.pack()
        
        
    #method for calculating total cost                    
    def calculating_total_cost(self,l,g):
        sum1 = 0
        i = 0
        j = 1
        for r in range(len(l)-1):
            sum1 = sum1 + g[l[i]][l[j]]
            i += 1 
            j += 1
            
        return sum1   

        
        
class add_node_page(tk.Frame):
    
    #add_node_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        label = ttk.Label(self, text="Enter the edge weights from new node to other nodes", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        entry = ttk.Entry(self, width=10)
        entry.pack(pady=10,padx=10)
        
        #creating buttons
        
        #click the button to add the node taken as input from user to the network
        
        button = ttk.Button(self, text="Add Node",
                            command=lambda: controller.add_node(entry))
        button.pack(pady=10,padx=10)
        
        #click button to go back to selection page frame
        
        button2 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        button2.pack()
        
        #click button to go back to home page frame
        
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)

        
class add_edge_page(tk.Frame):
    
    #add_edge_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating labels
        
        label = ttk.Label(self, text="Enter the edge to change the weight(For ex:4 5)", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        entry_edge = ttk.Entry(self, width=10)
        entry_edge.pack(pady=10,padx=10)
        
        label = ttk.Label(self, text="Enter the new weight", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        entry_weight = ttk.Entry(self, width=10)
        entry_weight.pack(pady=10,padx=10)
        
        #creating buttons
        
        #click button to make the changes to the network
        
        button = ttk.Button(self, text="Change Edge Weight",
                            command=lambda: controller.add_edge(entry_edge, entry_weight))
        #calling the function add_edge to make changes in the network
        
        button.pack(pady=10,padx=10)
        
        #click button to go to the Selection page frame
        button2 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        button2.pack()
        
        #click button to go to back to home page frame
        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack(pady=10,padx=10)
        

class display_network_page(tk.Frame):
    
    #display_network_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        graph = nx.Graph()
        i = 0
        edge_labels = {}
        for row in controller.data:
            j=0
            for col in row:
                if col not in [0,-1]:
                    graph.add_edge(i,j)
                    edge_labels[(i,j)] = int(controller.data[i][j])
                j = j+1
            i = i+1
        
        f = plt.figure(figsize=(5,4))
        
        plt.axis('off')
        pos = nx.circular_layout(graph)
        
        nx.draw(graph,pos,with_labels = True)
        nx.draw_networkx_edge_labels(graph,pos,edge_labels = edge_labels)
        
        
        #creating a canvas to draw the network
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        
        #click button to go to back to selection page frame
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        button1.pack()

class enter_destination_page(tk.Frame):
    
    #enter_destination_page is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        label = ttk.Label(self, text="Please Enter the destination node", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        entry = ttk.Entry(self, width=10)
        entry.pack(pady=10,padx=10)
        
        #creating buttons
        button = ttk.Button(self, text="Enter!!",
                            command=lambda: controller.network_to_destination(entry))
        button.pack(pady=10,padx=10)
        
        #click button to go to back to selection page frame
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        button1.pack()

        
        
class network_to_destination_page(tk.Frame):
    
    #network_to_destination_page is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        main_graph = nx.Graph()
        i=0
        for row in controller.data:
            j=0
            for col in row:
                if col not in [0,-1]:
                    main_graph.add_edge(i,j, weight = int(controller.data[i][j]) )

                j = j+1
            i = i+1
            
            
        graph = nx.Graph()
        edge_labels = {}
        for p in nx.all_shortest_paths(main_graph,source=controller.source,target=controller.destination, weight = 'weight'):
            

            edge = []

            for i in range(len(p)-1):
                edge = [p[i],p[i+1]]

                graph.add_edge(edge[0],edge[1])
                edge_labels[(p[i],p[i+1])] = int(controller.data[p[i]][p[i+1]])

        f = plt.figure(figsize=(5,4))
        pos = nx.circular_layout(graph)
        nx.draw(graph,pos,with_labels = True)
        nx.draw_networkx_edge_labels(graph,pos,edge_labels = edge_labels)
       
   
        #creating a canvas to draw the shortest path network     
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        
        #click button to go to back to selection page frame
        
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        button1.pack()
                    

#object of sea class
app = SeaofBTCapp()

#for recursive call
app.mainloop()
