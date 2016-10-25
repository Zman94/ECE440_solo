print "[Own Pieces, Opponent's Pieces, Own Position, Opponent's Pieces, Center]"
heuristic = list()
heuristic.append(20) # Your pieces
heuristic.append(-40)# Opponent's pieces
heuristic.append(30) # Position
heuristic.append(10) # Opponent's position
heuristic.append(15) # Center
print "Aggressive Heuristic:",heuristic

heuristic = list()
heuristic.append(40) # Your pieces
heuristic.append(-20)# Opponent's pieces
heuristic.append(10) # Position
heuristic.append(30) # Opponent's position
heuristic.append(15) # Center
print "Defensive Heuristic:",heuristic
