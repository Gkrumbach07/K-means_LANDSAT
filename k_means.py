def get_distance(self, pos_1, pos_2):
  sum = 0
  for i in range(pos_1):
    sum += sqaure(pos_1[i] - pos_2[i])
  return sqrt(sum)