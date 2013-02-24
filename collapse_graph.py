def collapse_graph(nodes):
  for id in nodes:
    node = nodes[id]
    if node["type"] == "passive" and node["type-passive"] == "resistor":
      if nodes[node["pins"]["1"]["node"]]["type"] == "net":
        R1_p1 = "2"
        R1_p2 = "1"
      elif nodes[node["pins"]["2"]["node"]]["type"] == "net":
        R1_p1 = "1"
        R1_p2 = "2"
      else:
        # boo no net connected to this resistor
        continue

      R1_id = id
      R1 = node
      N_id = R1["pins"][R1_p2]["node"]
      N_p1 = R1["pins"][R1_p2]["pin"]

      for i, p in nodes[N_id]["pins"].items():
        if p["node"] != id and nodes[p["node"]]["type"] == "passive" and nodes[p["node"]]["type-passive"] == "resistor":
          R2_id = p["node"]
          R2 = nodes[p["node"]]
          N_p2 = i
          R2_p1 = p["pin"]
          if R2_p1 == "1":
            R2_p2 = "2"
          elif R2_p1 == "2":
            R2_p2 = "1"
          else:
            # this shouldn't happen...?
            return

          resistor_with_resistor(nodes, R1_id, R1_p1, R1_p2, N_id, N_p1, N_p2, R2_id, R2_p1, R2_p2)
          print "combined a resistor?"
          return


def resistor_with_resistor(nodes, R1_id, R1_p1, R1_p2, N_id, N_p1, N_p2, R2_id, R2_p1, R2_p2):
  R1 = nodes[R1_id]
  R2 = nodes[R2_id]
  N = nodes[N_id]

  S_id = new_id_spice()

  nodes[S_id] = {}
  S = nodes[S_id]

  S["id"] = S_id
  S["pins"] = {}
  S["type"] = "spice"


  S["pins"]["1"] = {}
  S["pins"]["1"]["node"] = R1["pins"][R1_p1]["node"]
  S["pins"]["1"]["pin"] = R1["pins"][R1_p1]["pin"]

  node_left = nodes[S["pins"]["1"]["node"]]
  node_left_pin = S["pins"]["1"]["pin"]
  node_left["pins"][node_left_pin]["node"] = S_id
  node_left["pins"][node_left_pin]["pin"] = "1"


  S["pins"]["2"] = {}
  S["pins"]["2"]["node"] = R2["pins"][R2_p2]["node"]
  S["pins"]["2"]["pin"] = R2["pins"][R2_p2]["pin"]

  node_right = nodes[S["pins"]["2"]["node"]]
  node_right_pin = S["pins"]["2"]["pin"]
  node_right["pins"][node_right_pin]["node"] = S_id
  node_right["pins"][node_right_pin]["pin"] = "2"


  S["pins"]["3"] = {}
  S["pins"]["3"]["node"] = N_id
  S["pins"]["3"]["pin"] = N_p1

  del N["pins"][N_p2]

  N["pins"][N_p1]["node"] = S_id
  N["pins"][N_p1]["pin"] = "3"


  S["spice-circuit"] = "%s 1 3 %s\n%s 3 2 %s\n" % (R1["name"], R1["resistance"], R2["name"], R2["resistance"])


  del nodes[R1_id]
  del nodes[R2_id]
  if len(N["pins"]) == 1:
    del nodes[N_id]



def new_id_spice():
  if not hasattr(new_id_spice, "counter"):
    new_id_spice.counter = 0
  new_id = "spice" + str(new_id_spice.counter)
  new_id_spice.counter += 1
  return new_id
