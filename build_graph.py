import json

fp = open('test.upv')
j = json.load(fp)
fp.close()

nodes = {}

# build up nodes
for ci in j["component_instances"]:
  # common node info
  id = ci["instance_id"]
  nodes[id] = {}
  nodes[id]["id"] = id
  nodes[id]["name"] = ci["attributes"]["refdes"]
  nodes[id]["pins"] = {}

  # resistor
  if j["components"][ci["library_id"]]["attributes"]["_type"] == "resistor":
    nodes[id]["type"] = "passive"
    nodes[id]["type-passive"] = "resistor"
    nodes[id]["resistance"] = j["components"][ci["library_id"]]["attributes"]["_resistance"]

  # TODO LRC


# build up nets
for n in j["nets"]:
  # assume net_id's and component id's don't overlap
  id = n["net_id"]
  nodes[id] = {}
  nodes[id]["id"] = id
  nodes[id]["pins"] = {}
  nodes[id]["type"] = "net"

  pin_i = 1
  for p in n["points"]:
    for cc in p["connected_components"]:
      nodes[id]["pins"][str(pin_i)] = {}
      nodes[id]["pins"][str(pin_i)]["node"] = cc["instance_id"]
      nodes[id]["pins"][str(pin_i)]["pin"] = cc["pin_number"]
      nodes[cc["instance_id"]][cc["pin_number"]] = {}
      nodes[cc["instance_id"]][cc["pin_number"]]["node"] = id
      nodes[cc["instance_id"]][cc["pin_number"]]["pin"] = str(pin_i)
