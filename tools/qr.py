#!/usr/bin/env python3
# Minimal QR code generator (no dependencies except Pillow). Usage: python3 tools/qr.py "https://mycraftgames.com/" assets/qr-site.png
# Minimal QR encoder (byte mode, ECC M, versions 1-6), Nayuki-style.
import sys
from PIL import Image
ECC_M_CW={1:(10,1),2:(16,1),3:(26,1),4:(18,2),5:(24,2),6:(16,4)}  # ecc codewords per block, num blocks
TOTAL={1:26,2:44,3:70,4:100,5:134,6:172}
ALIGN={1:[],2:[6,18],3:[6,22],4:[6,26],5:[6,30],6:[6,34]}
def gf_tables():
    exp=[0]*512;log=[0]*256;x=1
    for i in range(255):
        exp[i]=x;log[x]=i;x<<=1
        if x&0x100:x^=0x11d
    for i in range(255,512):exp[i]=exp[i-255]
    return exp,log
EXP,LOG=gf_tables()
def gmul(a,b):return 0 if a==0 or b==0 else EXP[LOG[a]+LOG[b]]
def rs_gen(n):
    g=[1]
    for i in range(n):
        ng=[0]*(len(g)+1)
        for j,c in enumerate(g):
            ng[j]^=c;ng[j+1]^=gmul(c,EXP[i])
        g=ng
    return g
def rs_ecc(data,n):
    g=rs_gen(n);r=list(data)+[0]*n
    for i in range(len(data)):
        c=r[i]
        if c:
            for j in range(len(g)):r[i+j]^=gmul(g[j],c)
    return r[len(data):]
def encode(text):
    data=text.encode()
    for ver in range(1,7):
        ecn,nb=ECC_M_CW[ver];cap=TOTAL[ver]-ecn*nb
        cc_bits=8 if ver<10 else 16
        if 4+cc_bits+8*len(data)<=cap*8:break
    else:raise SystemExit('too long')
    bits=[]
    def put(v,n):
        for i in range(n-1,-1,-1):bits.append((v>>i)&1)
    put(4,4);put(len(data),cc_bits)
    for b in data:put(b,8)
    put(0,min(4,cap*8-len(bits)))
    while len(bits)%8:bits.append(0)
    cw=[int(''.join(map(str,bits[i:i+8])),2) for i in range(0,len(bits),8)]
    pad=[0xEC,0x11];k=0
    while len(cw)<cap:cw.append(pad[k%2]);k+=1
    # split blocks (all equal for these versions with M)
    bl=cap//nb;blocks=[cw[i*bl:(i+1)*bl] for i in range(nb)];eccs=[rs_ecc(b,ecn) for b in blocks]
    final=[b[i] for i in range(bl) for b in blocks]+[e[i] for i in range(ecn) for e in eccs]
    return ver,final
def build(text):
    ver,cw=encode(text);n=17+4*ver
    M=[[None]*n for _ in range(n)];F=[[False]*n for _ in range(n)]
    def setf(x,y,v):M[y][x]=v;F[y][x]=True
    for i in range(n):setf(6,i,i%2==0);setf(i,6,i%2==0)
    def finder(cx,cy):
        for dy in range(-4,5):
            for dx in range(-4,5):
                x,y=cx+dx,cy+dy
                if 0<=x<n and 0<=y<n:
                    d=max(abs(dx),abs(dy));setf(x,y,d!=2 and d!=4)
    finder(3,3);finder(n-4,3);finder(3,n-4)
    al=ALIGN[ver]
    for i in al:
        for j in al:
            if (i==6 and j==6) or (i==6 and j==al[-1]) or (i==al[-1] and j==6):continue
            for dy in range(-2,3):
                for dx in range(-2,3):setf(i+dx,j+dy,max(abs(dx),abs(dy))!=1)
    # reserve format areas
    for i in range(9):
        if not F[8][i]:setf(i,8,False)
        if not F[i][8]:setf(8,i,False)
    for i in range(8):setf(n-1-i,8,False);setf(8,n-1-i,False)
    setf(8,n-8,True)  # dark module
    # place data
    bits=[(b>>(7-i))&1 for b in cw for i in range(8)];k=0
    x=n-1;up=True
    while x>0:
        if x==6:x-=1
        for vert in range(n):
            y=n-1-vert if up else vert
            for dx in (0,1):
                xx=x-dx
                if not F[y][xx]:
                    M[y][xx]=bool(bits[k]) if k<len(bits) else False;k+=1
        up=not up;x-=2
    def masked(m):
        fn=[lambda x,y:(x+y)%2==0,lambda x,y:y%2==0,lambda x,y:x%3==0,lambda x,y:(x+y)%3==0,
            lambda x,y:(x//3+y//2)%2==0,lambda x,y:(x*y)%2+(x*y)%3==0,lambda x,y:((x*y)%2+(x*y)%3)%2==0,lambda x,y:((x+y)%2+(x*y)%3)%2==0][m]
        R=[[M[y][x]^(not F[y][x] and fn(x,y)) for x in range(n)] for y in range(n)]
        # format bits: ECC M = 00
        data=(0<<3)|m;rem=data
        for _ in range(10):rem=(rem<<1)^((rem>>9)*0x537)
        fb=((data<<10)|rem)^0x5412
        b=lambda i:bool((fb>>i)&1)
        for i in range(6):R[i][8]=b(i)
        R[7][8]=b(6);R[8][8]=b(7);R[8][7]=b(8)
        for i in range(9,15):R[8][14-i]=b(i)
        for i in range(8):R[8][n-1-i]=b(i)
        for i in range(8,15):R[n-15+i][8]=b(i)
        R[n-8][8]=True
        return R
    def penalty(R):
        p=0
        for rows in (R,[list(c) for c in zip(*R)]):
            for r in rows:
                run=1
                for i in range(1,n):
                    if r[i]==r[i-1]:run+=1
                    else:
                        if run>=5:p+=run-2
                        run=1
                if run>=5:p+=run-2
                s=''.join('1' if v else '0' for v in r)
                p+=40*(s.count('10111010000')+s.count('00001011101'))
        for y in range(n-1):
            for x in range(n-1):
                if R[y][x]==R[y][x+1]==R[y+1][x]==R[y+1][x+1]:p+=3
        dark=sum(map(sum,R));p+=abs(dark*20-n*n*10)//(n*n)*10
        return p
    best=min(range(8),key=lambda m:penalty(masked(m)))
    return masked(best)
def save(text,path,size=330,border=2):
    R=build(text);n=len(R);tot=n+2*border;sc=size//tot
    img=Image.new('RGB',(tot*sc,tot*sc),'white');px=img.load()
    for y in range(n):
        for x in range(n):
            if R[y][x]:
                for a in range(sc):
                    for b in range(sc):px[(x+border)*sc+a,(y+border)*sc+b]=(17,17,17)
    img.save(path)
if __name__=='__main__':save(sys.argv[1],sys.argv[2])
