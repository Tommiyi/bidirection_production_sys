# 20200320
# 王兴浩
import rule
from stack import Stack
class result:
  animal = -1
  confidence = -1.0
  lossevidence = []
  def __init__(self) :
    super().__init__()
  def make_result(self, a, c, l):
    self.animal = a
    self.confidence = c
    self.lossevidence = l
re = []
evidence = [0] * 24
foevidence = []
baevidence = []
endbaevidence = []
endfoevidence = []
guess = 0
mode = -1
def input_evidence() :
  a = input("请输入观测的证据：")
  b = a.split(" ")
  for i in b :
    evidence[int(i)] = 1
  global foevidence
  foevidence = evidence
def input_guess():
  g = input("请输入猜测可能的目标（没有猜测输入-1）：")
  global guess
  global mode
  guess = int(g)
  if guess == -1:
    mode = 0
  else:
    mode = 1
def forward_production() :
  changed = 0
  for i in rule.r :
    satisfied = 1
    for j in i.evidence:
      if foevidence[j] != 1:
        satisfied = 0
        break
    if satisfied :
      if i.result > 23 :
        tmp = result()
        tmp.make_result(i.result, 1, [])
        re.append(tmp)
        changed = 2
        break
      else :
        if foevidence[i.result] == 0 :
          foevidence[i.result] = 1
          changed = 1
  return changed
def backward_production() :
  for i in range(24, 31) :
    global baevidence
    baevidence = [0] * 24
    st = Stack()
    st.push(i)
    while not st.isEmpty() :
      t = st.pop()
      flag = 0
      if t <= 23 and evidence[t] == 1 :
        baevidence[t] = 1
      else :
        for j in rule.r :
          if j.result == t :
            flag = 1
            for k in j.evidence :
              st.push(k)
      if not flag :
        baevidence[t] = 1
    flag = 1
    count = 0
    summ = 0
    for l in range(0, len(evidence)) :
      if evidence[l] == 1 and baevidence[l] == 0 :
        flag = 0
        break
      elif evidence[l] == 0 and baevidence[l] == 1 :
        count += 1
        summ += 1
      elif evidence[l] == 1 and baevidence[l] == 1 :
        summ += 1
        baevidence[l] = 0
    if flag :
      tmp = result()
      tmp.animal = i
      tmp.confidence = (summ - count) / summ
      tmp.lossevidence = baevidence
      re.append(tmp)
def backward_production_once_with_check_satisfied() :
  # Backward production process
  global baevidence
  global endbaevidence
  global endfoevidence
  changed = 0
  if len(baevidence) == 0 :
    endbaevidence = [0] * 24
    endfoevidence = [0] * 24
    baevidence = [0] * 24
    changed = 1
    for i in rule.r :
      if i.result == guess :
        for j in i.evidence :
          baevidence[j] = 1
  for i in range(0, len(baevidence)) :
    if baevidence[i] == 1 :
      for j in rule.r :
        if j.result == i :
          changed = 1
          for k in j.evidence :
            baevidence[k] = 1
  # Check Process
  for i in range(0, 24) :
    if foevidence[i] == 1 and baevidence[i] == 1 :
      baevidence[i] = 0
      endbaevidence[i] = 1
      endfoevidence[i] = 1
  return changed
def bidirect_production_sys():
  if mode == 0 : 
    # Only Envidence, No Guess
    changed = 1
    # Do Forward First
    while changed == 1 :
      changed = forward_production()
    if changed == 0 : 
      # Not Found, Do backward
      backward_production()
      print("可能的目标和其置信为：")
      for i in re :
        print(rule.feature[i.animal], i.confidence)
    elif changed == 2 : 
      # Found Only result, Print Result
      print("目标为：", rule.feature[re[0].animal])
  if mode == 1 :
    changed = 1
    changed1 = 1
    while changed == 1 and changed1 == 1 :
      # Not Only Evidence, But Guess
      changed = forward_production()
      # Do Once Forward with Check satisfied
      changed1 = backward_production_once_with_check_satisfied() 
    left_forward = 0
    left_backward = 0
    if changed == 2 :
      if re[0].animal == guess :
        print("猜测的对。")
      else :
        print("猜错了，是", rule.feature[re[0].animal])
    else :
      for i in range(0, len(evidence)) :
        if foevidence[i] == 1 and endfoevidence[i] == 0 :
          left_forward = 1
        if baevidence[i] == 1 and endbaevidence[i] == 0 :
          left_backward = 1
      if left_forward == 1 and left_backward == 1 :
        print("猜错了！")
      elif left_forward == 0 and left_backward == 1 :
        print("无法确定，可能需要证实的证据还有：")
        for i in range(len(baevidence)) :
          if baevidence[i] == 1 :
            print(rule.feature[i])
if __name__ == "__main__":
  rule.Show_feature()
  rule.Add_rule()
  input_evidence()
  input_guess()
  bidirect_production_sys()
