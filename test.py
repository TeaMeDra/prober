from build_graph import *
from collapse_graph import *


def main():
  if len(sys.argv) < 2:
    print "you didn't specify a filename"
    return

  fp = open(sys.argv[1])
  j = json.load(fp)
  fp.close()

  nodes = build_graph(j)
  # print_graph(nodes)

  running = True
  while running:
    if not collapse_graph(nodes):
      running = False

  print_graph(nodes)


if __name__ == "__main__":
  main()
