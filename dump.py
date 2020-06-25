    def findNearestLeafNode(self,key):
        nearest_node = None
        nearest_node_dist = inf
        for nbr in self.leafUSet + self.leafLSet:
            distance = node_abs_id_distance(nbr.id,key.id)
            if nearest_node_dist > distance:
                nearest_node_dist = distance
                nearest_node = nbr
        return nearest_node
    
    def find_closest_node_in_routing_table(self,key):   ## This is tough
        shl = comman_prefix_length(self.id,key.id)
        node = self.routingTable[shl][int(key.id[shl],16)]
        if node is not None:
            return node
        else:
            for node in self.leafUSet + self.leafLSet:
                shl_node = comman_prefix_length(node.id,key.id)
                if node_abs_id_distance(node.id,key.id) < node_abs_id_distance(node.id,self.id) and shl_node >= shl:
                    return node
            for row in self.routingTable:
                for node in row:
                    if node is not None:
                        shl_node = comman_prefix_length(node.id,key.id)
                        if node_id_distance(node.id,key.id) < node_id_distance(node.id,self.id) and shl_node >= shl:
                            return node
            
            return None

    def find_key(self,key) :  
        if key.name in self.keys:
            return (self.keys[key.name],0)    ### return value and number of further hops which is 0 in this case
        else:
            if len(self.leafLSet+ self.leafUSet) == 0:
                return (None,0)
            if compare_two_nodes(key.id, self.lowest_leaf_node_id,'ge') and compare_two_nodes(key.id,self.hightest_leaf_node_id,'le'):
                leaf_node = self.find_closest_leaf_node(key)
                val,hops = leaf_node.find_key(key)
                return (val,hops+1)
            else:
                routing_node = self.find_closest_node_in_routing_table(key)
                if routing_node is not None:
                    val,hops = routing_node.find_key(key)
                    return (val,hops+1)
                else:
                    return (None,0)
       
    def find_closest_node(self,node) :  
        if len(self.leafLSet+ self.leafUSet) == 0:
            return (self,[self.id])
        if node.id >= self.lowest_leaf_node_id and node.id <= self.hightest_leaf_node_id:
            leaf_node = self.findNearestLeafNode(node)
            closest_node,route = leaf_node.find_closest_node(node)
            return (closest_node,[self.id]+route)

        else:
            routing_node = self.find_closest_node_in_routing_table(node)
            if routing_node is not None:
                closest_node,route = routing_node.find_closest_node(node)
                return (closest_node,[self.id]+route)
            else:
                return (self,[self.id])
                

                
                
                

                
        

            
    def updateLocalNode(self,node):
        nearest_node = None
        nearest_node_dist = 1000000
        for nbr in self.nodes:
            distance = euclidean_distance(nbr.location,node.location)
            if nearest_node_dist > distance:
                nearest_node_dist = distance
                nearest_node = nbr
        return nearest_node
    def findNearestLocalNode(self,node):
        nearest_node = None
        nearest_node_dist = 1000000
        for nbr in self.nodes:
            distance = euclidean_distance(nbr.location,node.location)
            if nearest_node_dist > distance:
                nearest_node_dist = distance
                nearest_node = nbr
        return nearest_node
    
    def findNearestNumericalNode(self,node):
        nearest_node = None
        nearest_node_dist = inf
        for nbr in self.nodes:
            distance = node_id_distance(nbr.id,node.id)
            if nearest_node_dist > distance:
                nearest_node_dist = distance
                nearest_node = nbr
        return nearest_node
    
    
    def addNode(self,node):
        self.nodes.append(node)
        self.node_id_to_object[node.id] = node
        if len(self.nodes) == 1:
            return
        
        nearest_node_local = self.findNearestLocalNode(node)   ### Routes new nodes to its closest numerical closest node
        nearest_numerical_node,route = nearest_node_local.find_closest_node(node)
        ##### update its data
        print(nearest_node_local)
        print(nearest_numerical_node,route)
        
    def deleteNode(self,node):
        return
    
    def addNodes(self,num_of_nodes):
        ### Create first node
        node = Node(1)  ### Nothing needs to be done as this is the only node in system
        self.addNode(node)
        
        node = Node(2)   ####Do something about it now
        self.addNode(node)
        print(node.name)
        #self.nodes.append(node)
        
    #def print_routing_table(self):
        for i in range(0,len(self.routingTable)):
            for j in range(0,len(self.routingTable[0])):
                print( self.routingTable[i][j],end = " | ")
            print("")