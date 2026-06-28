from tinytag import TinyTag
from pathlib import Path
from json import dump

def scan_files(path):
    files=Path(path)
    index_place=[]
    file_place=[]
    tage=[[],[],[],[],[]]
    artists={}
    albums={}
    time=[]
    for i in files.rglob("*"):
        if i.suffix in [".mp3",".flac",".wav",".ogg",".m4a"]:
            if i.stat().st_size>100:
                if i.parent not in file_place:
                    file_place.append(i.parent)
                    continue
    return(file_place)

def scan_detail(files):
    for i in files.rglob("*"):
        if i.suffix in [".mp3",".flac",".wav",".ogg",".m4a"]:
            if i.stat().st_size>100:
                time=(i.stat().st_mtime)
                tag=TinyTag.get(i)
                index=(str(i))
                if tag.artist!=None:
                    art=tag.artist.split("/")
                else:
                    art="未知艺术家"
                if tag.title==None:
                    title=(i.stem)
                else:
                    title=(tag.title)
                bit=([tag.samplerate,int(tag.bitrate)])
                moon=(tag.duration)
                yield([index,title,art,tag.album,bit,moon,time])

def scan_all(place):
    index_place=[]
    data_place=[]
    artists={}
    albums={}
    tage=[[],[],[],[],[]]
    time=[]
    index=0
    for i in range(len(place)):
        index_place.append([str(place[i]),index])
        for z in scan_detail(place[i]):
            tage[0].append(z[1])
            tage[1].append(z[2])
            tage[2].append(z[3])
            tage[3].append(z[4])
            tage[4].append(z[5])
            time.append(z[6])
            data_place.append(z[0])
            for y in z[2]:
                if y in artists:                        
                    artists[y].append(index)
                else:
                    artists.update({y:[index]})
                if z[3] not in albums:
                    albums.update({z[3]:[index]})
                else:
                    albums[z[3]].append(index)
            index+=1
        index_place[-1].append(index-1)
    data=[index_place,data_place,tage,artists,albums,time]
    if index_place!=[]:
        return(data)
    else:
        return(None)


#时间转换    
def convert(time):
    mins, secs = divmod(time//1000, 60)
    return("{:02d}:{:02d}".format(mins, secs))

def unconvert(time):
    return(int(time[0:2])*60000+int(time[3:5])*1000+int(time[6:8]))
