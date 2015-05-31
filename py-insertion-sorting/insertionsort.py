# -*- coding: utf-8 -*-

def insertionsort(aList, element):
  k = len(aList)
  # check if the list is empty
  if k == 0:
    aList.append(element)
  else:
    # insert the element in correct sequence
    while k > 0 and element < aList[k - 1]:
      k -= 1
    aList.insert(k, element)

if __name__ == "__main__":
  print "Just keep input a integer and press enter. Stop anytime by pressing Ctrl-C. \nEnjoy ^_^"
  maxLength = 5
  a = []
  try:
    while(1):
      try:
        read_buffer = [int(x) for x in raw_input().split()]
      except ValueError: # typically input is not int
        print "Don't feed me with shit, please!"
        continue
      # got correct input, process them
      for item in read_buffer:
        insertionsort(a, item)
        a = a[-maxLength:]

      print "Current list =", a
  except KeyboardInterrupt: # Ctrl-C pressed
    print "Sum =", sum(a)
