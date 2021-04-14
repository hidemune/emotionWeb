# coding: utf_8
from flask import Flask, render_template, request
from collections import defaultdict
import math

app = Flask(__name__)

class Anchor():
    def __init__(self, eng, jp, x, z, y):
        self.eng = eng
        self.jp = jp
        self.x = float(x);
        self.z = float(z);
        self.y = float(y);
        self.deniCnt = 0;
        self.no = False;
        self.bunbo = 1;
        self.len = 0;
        self.emotion = "";

anchors = []
anchorObj = Anchor("love", "愛", 1, 0, 0);
anchors.append(anchorObj)
anchorObj = Anchor("optimism", "楽観", 1, 1, 0);
anchors.append(anchorObj)
anchorObj = Anchor("joy", "喜び", 1, 1, 1);
anchors.append(anchorObj)
anchorObj = Anchor("anticipation", "関心", 1, 1, -1);
anchors.append(anchorObj)
anchorObj = Anchor("submission", "素直", 1, -1, 0);
anchors.append(anchorObj)
anchorObj = Anchor("trust", "信頼", 1, -1, 1);
anchors.append(anchorObj)
anchorObj = Anchor("fear", "心配", 1, -1, -1);
anchors.append(anchorObj)
anchorObj = Anchor("remorse", "自責", -1, 0, 0);
anchors.append(anchorObj)
anchorObj = Anchor("contempt", "軽蔑", -1, 1, 0);
anchors.append(anchorObj)
anchorObj = Anchor("disgust", "嫌悪", -1, 1, 1);
anchors.append(anchorObj)
anchorObj = Anchor("anger", "怒り", -1, 1, -1);
anchors.append(anchorObj)
anchorObj = Anchor("disapproval", "失望", -1, -1, 0);
anchors.append(anchorObj)
anchorObj = Anchor("sadness", "悲しみ", -1, -1, 1);
anchors.append(anchorObj)
anchorObj = Anchor("surprise", "驚き", -1, -1, -1);
anchors.append(anchorObj)
anchorObj = Anchor("aggressiveness", "攻撃", 0, 1, 0);
anchors.append(anchorObj)
anchorObj = Anchor("awe", "畏れ", 0, -1, 0);
anchors.append(anchorObj)

d = defaultdict(lambda: Anchor("", "", 0,0,0))

# coding: UTF-8
f = open('emotion.csv')
data1 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
lines1 = data1.split('\n')
for line in lines1:
    kwd = line.split('\t')
    if len(kwd[0].strip()) > 0:
      anc = Anchor("", kwd[0].strip(), float(kwd[1]), float(kwd[2]), float(kwd[3]));
      anc.deniCnt = int(kwd[5])
      #d[kwd[0]].append( anc )
      d.setdefault(kwd[0], anc)

class Member():
    def __init__(self):
        self.emotion = ""
        self.text = ""
        self.detail = [];

def get_emotion(txt):
    ret = "無関心"
    #ret = anchors[3].jp
    #文章全体の印象
    bkKey = []
    bkKey2 = Anchor(txt, txt, 0, 0, 0)
    line2 = []
    
    xx = 0
    yy = 0
    zz = 0
    #print(d)
    txt1 = txt.strip();
    emotionFlg = False;
    # 分割処理
    begin = 0;
    end = len(txt1);
    while (begin < end) :
        longest_length = 1;
        #for (int i = begin+1; i <= end; i++) {
        #print(begin, end)
        for i in range(begin+1, end+1):
            wk =  d.get(txt1[begin:i]);
            if (wk != None) :
                longest_length = i-begin;
                #print(txt1[begin : begin + longest_length])
        if (longest_length == 0) :
            longest_length = 1;
        line2.append(txt1[begin : begin + longest_length]);
        begin = begin + longest_length;
    
    print("Bunkatu:")
    print(line2)
    cnt = 0;
    no = False;
    #for (int k = line2.size()-1 ; k >= 0 ; k--) {
    for k in range(len(line2)-1, -1,-1):
        keyword = line2[k];
        #print("KEY:" + keyword)
        if (d.get(keyword) != None) :
            #print("JP:" + d.get(keyword).jp)
            if (d.get(keyword).deniCnt < 0) :
                no = True;
                cnt = - d[keyword].deniCnt;
        bkKey.insert(0, Anchor("", keyword, 0, 0, 0));
        bkKey[0].no = no;
        if (no) :
            cnt += -1
            if (cnt < 0) :
                no = False;
        flgCm = False;
        
        if (flgCm == False) :
            flgOk = True;
            
            if (flgOk) :
                # emotion Search
                wkKey = d[keyword];
                # distance
                if (wkKey != None) :
                    bkKey[0].jp = keyword;
                    if (bkKey[0].no) :
                        bkKey[0].x = - wkKey.x;
                    else :
                        bkKey[0].x = wkKey.x;
                    
                    bkKey[0].y = wkKey.y;
                    bkKey[0].z = wkKey.z;
                    bkKey[0].bunbo = wkKey.bunbo;
                    bkKey[0].deniCnt = wkKey.deniCnt;
    no = False;
    #for (int k = 0 ; k < bkKey.size() ; k++) {
    for k in range(0, len(bkKey)):
        if (bkKey[k].deniCnt > 0) :
            no = True;
            cnt = bkKey[k].deniCnt;
        if (no) :
            bkKey[k].no = not bkKey[k].no;
            bkKey[k].x = - bkKey[k].x;
            cnt += -1;
            if (cnt < 0) :
                no = False;
        #for (int l = 0 ; l < bkKey.size(); l++) {
        for l in range(0, len(bkKey)):
            lenT = math.sqrt((bkKey[l].x ** 2) + (bkKey[l].y ** 2) + (bkKey[l].z ** 2) );
            if (lenT > 0) :
                # Norm
                xx = 0;
                yy = 0;
                zz = 0;
                if (lenT > 0) :
                    xx = bkKey[l].x / lenT;
                    yy = bkKey[l].y / lenT;
                    zz = bkKey[l].z / lenT;
            dist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
            idx = 100;
            mini=99999;
            #for (int i = 1; i < anchors.size(); i++) {
            for i in range(0, len(anchors)):
                # 距離
                #print(i)
                dist[i] = ((anchors[i].x - xx ) ** 2) + ((anchors[i].y - yy ) ** 2) + ((anchors[i].z - zz ) ** 2);
            #for (int i = 1; i < anchors.size(); i++) {
            for i in range(0, len(anchors)):
                if (dist[i] < mini) :
                    idx = i;
                    mini = dist[i];
            if (idx < 100) :
                bkKey2.x = bkKey2.x + bkKey[l].x
                bkKey2.y = bkKey2.y + bkKey[l].y
                bkKey2.z = bkKey2.z + bkKey[l].z
                bkKey2.bunbo = bkKey2.bunbo + 1
                # 各要素の分類とスコアを保存
                bkKey[l].len = lenT;
                bkKey[l].emotion = anchors[idx].jp;
                
                
        # 全体の印象
        bkKey2.jp = "";
        bkKey2.eng = "";
        
        
        
        
        
        lenT = math.sqrt((bkKey2.x ** 2) + (bkKey2.y ** 2) + (bkKey2.z ** 2));
        if (lenT > 0) :
            # Norm
            xx = bkKey2.x / lenT;
            yy = bkKey2.y / lenT;
            zz = bkKey2.z / lenT;
            
            dist = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
            idx = 100;
            mini=99999;
            #for (int i = 1; i < anchorObj.size(); i++) {
            for i in range(0, len(anchors)):
                # 距離
                dist[i] = ((anchors[i].x - xx ) ** 2) + ((anchors[i].y - yy ) ** 2) + ((anchors[i].z - zz ) ** 2);
            #for (int i = 1; i < anchorObj.size(); i++) {
            for i in range(0, len(anchors)):
                if (dist[i] < mini) :
                    idx = i;
                    mini = dist[i];
            if (idx < 100) :
                bkKey2.jp = anchors[idx].jp;
                bkKey2.eng = anchors[idx].eng;
    print(bkKey2.jp)
    print(bkKey2.eng)
    return bkKey2.jp, bkKey

@app.route('/')
def defpage():
    name = ""
    #return name
    return render_template('emotionWeb.html', title='emotion web', txt=name)

@app.route('/', methods=['POST']) #Methodを明示する必要あり
def hello():
  members = []
  if request.method == 'POST':
    text = request.form['text']
  arr = text.split("\n")
  for item in arr:
    if item.strip() != "":
      member = Member()
      member.text = item
      member.emotion, member.detail = get_emotion(item)
      members.append(member)
  return render_template('emotionWeb.html', title='emotion web', members=members, txt=text)

## おまじない
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

