import os
import json
import shutil
import elist.elist as elel
import chardet
import zipfile


def fmt_path(path):
    return(os.path.abspath(path))

def get_parent_of_path(path):
    path = fmt_path(path)
    return(os.path.dirname(path))

def get_ance_of_path(which,path):
    path = fmt_path(path)
    c = 0
    ance = path
    while(c<which):
        ance = get_parent_of_path(ance)
        c = c + 1
    return(ance)


def get_all_ances_of_path(path,includng_self=False):
    path = fmt_path(path)
    ances = []
    if(includng_self):
        ances.append(path)
    else:
        pass
    p = os.path.dirname(path)
    while(p!=os.path.sep):
        ances.append(p)
        p = os.path.dirname(p)
    ances.append(os.path.sep)
    ances.reverse()
    return(ances)


def get_top_path(path):
    ances = get_all_ances_of_path(path)
    return(ances[1])

def is_sib_path_of(path0,path1):
    p0 = get_parent_of_path(path0)
    p1 = get_parent_of_path(path1)
    return(p0 == p1)


def get_path_head(path):
    pl = path2pl(path)    
    return(pl[0])

def get_path_tail(path):
    pl = path2pl(path)
    return(elel.join(pl[1:],os.path.sep))

def get_path_init(path):
    pl = path2pl(path)
    return(elel.join(pl[:-1],os.path.sep))

def get_path_last(path):
    pl = path2pl(path)
    return(pl[-1])

def get_running_cwd():
    return(os.getcwd())

def get_file_cwd():
    return(os.path.abspath(__file__))


def pl2path(pl):
    pl = elel.mapv(pl,str)
    return(os.path.join(*pl))

def path2pl(path):
    path = fmt_path(path)
    pl = []
    parent,ele = os.path.split(path)
    pl = elel.unshift(pl,ele)
    while((parent != "")and(parent != os.path.sep)):
        parent,ele = os.path.split(parent)
        pl = elel.unshift(pl,ele)
    return(pl)



def is_descedant_pl_of(des_pl,ances_pl):
    '''
        from xdict.utils import *
        is_descedant_pl_of(['a','b'],['a','b'])
        is_descedant_pl_of(['a','b',''],['a','b'])
        is_descedant_pl_of(['a','b','c'],['a','b'])
        is_descedant_pl_of(['a','b','c','d'],['a','b'])
        is_descedant_pl_of(['a','b','c','d',''],['a','b'])
    '''
    dl_len = des_pl.__len__()
    al_len = ances_pl.__len__()
    if(dl_len > al_len):
        for i in range(0,al_len):
            if(ances_pl[i] == des_pl[i]):
                pass
            else:
                return(False)
        return(True)
    else:
        return(False)


def is_ancestor_pl_of(ances_pl,des_pl):
    '''
        from xdict.utils import *
        is_ancestor_pl_of(['a','b'],['a','b'])
        is_ancestor_pl_of(['a','b'],['a','b',''])
        is_ancestor_pl_of(['a','b'],['a','b','c'])
        is_ancestor_pl_of(['a','b'],['a','b','c','d'])
        is_ancestor_pl_of(['a','b'],['a','b','c','d',''])
    '''
    dl_len = des_pl.__len__()
    al_len = ances_pl.__len__()
    if(dl_len > al_len):
        for i in range(0,al_len):
            if(ances_pl[i] == des_pl[i]):
                pass
            else:
                return(False)
        return(True)
    else:
        return(False)




#####################

def rbfile(fn):
    fd = open(fn,'rb+')
    rslt = fd.read()
    fd.close()
    return(rslt)

def rfile(fn,codec='utf-8'):
    rslt = rbfile(fn)
    rslt = rslt.decode(codec)
    return(rslt)

def wbfile(fn,content):
    fd = open(fn,'wb+')
    fd.write(content)
    fd.close()

def wfile(fn,content,codec='utf-8'):
    content = content.encode(codec)
    wbfile(fn,content)

def abfile(fn,content):
    fd = open(fn,'ab+')
    fd.write(content)
    fd.close()

def afile(fn,content,codec='utf-8'):
    content = content.encode(codec)
    abfile(fn,content)

def pfile(fn1,content,codec='utf-8',**kwargs):
    if('fsp' in kwargs):
        fsp = kwargs['fsp']
    else:
        fsp = "\n"
    if(isinstance(content,bytes)):
        content2 = content
    else:
        content2 = content.decode(codec)
    content1 = rfile(fn1,codec)
    content = content2+fsp+content1
    wfile(fn1,content,codec)


def fpfile(fn1,fn2,codec1='utf-8',codec2='utf-8',**kwargs):
    if('fsp' in kwargs):
        fsp = kwargs['fsp']
    else:
        fsp = "\n"
    content1 = rfile(fn1,codec1)
    content2 = rfile(fn2,codec2)
    content = content2+fsp+content1
    wfile(fn1,content,codec)

####


def rjson(fn,codec='utf-8'):
    s = rfile(fn,codec)
    d = json.loads(s)
    return(d)

def wjson(fn,js,codec='utf-8'):
    s = json.dumps(js)
    wfile(fn,s,codec)

def touch(fn):
    fd = open(fn,"w+")
    fd.write("")
    fd.close()

def filexist(path):
    return(os.path.exists(path) & os.path.isfile(path))

def direxist(path):
    return(os.path.exists(path) & os.path.isdir(path))

def mkdir(path,**kwargs):
    if('force' in kwargs):
        force = kwargs['force']
    else:
        force = False
    try:
        os.mkdir(path)
    except Exception as e:
        if(force):
            if(e.errno == 17):
                try:
                    #print("Try rmdir "+path)
                    os.rmdir(path)
                except Exception as e:
                    if(e.errno == 41):
                        #print("rmtree descendants dirs of "+path)
                        shutil.rmtree(path)
                    else:
                        #print(e)
                        pass
                else:
                    pass
                os.mkdir(path)
            else:
                pass
        else:
            #print(e)
            pass
    else:
        pass

def mkdirs(path,**kwargs):
    if('force' in kwargs):
        force = kwargs['force']
    else:
        force = False
    try:
        os.makedirs(path)
    except Exception as e:
        if(force):
            if(e.errno == 17):
                try:
                    #print("Try removedirs "+path)
                    os.removedirs(path)
                except Exception as e:
                    if(e.errno == 41):
                        #print("rmtree descendants dirs of "+path)
                        shutil.rmtree(path)
                    else:
                        #print(e)
                        pass
                else:
                    pass
                os.makedirs(path)
            else:
                pass
        else:
            #print(e)
            pass
    else:
        pass

####

def rmdir(path,**kwargs):
    if('force' in kwargs):
        force = kwargs['force']
    else:
        force = False
    #############################
    try:
        os.rmdir(path)
    except Exception as e:
        if(force):
            shutil.rmtree(path)
        else:
            #print(e)
            pass
    else:
        pass



####

def walkf(dirpath=os.getcwd()):
    fps = []
    for (root,subdirs,files) in os.walk(dirpath):
        for fn in files:
            path = os.path.join(root,fn)
            fps.append(path)
    return(fps)

def walkd(dirpath=os.getcwd()):
    fps = []
    for (root,subdirs,files) in os.walk(dirpath):
        for subd in subdirs:
            path = os.path.join(root,subd)
            fps.append(path)
    return(fps)

def walk(dirpath=os.getcwd()):
    fps = []
    for (root,subdirs,files) in os.walk(dirpath):
        for fn in files:
            path = os.path.join(root,fn)
            fps.append(path)
        for subd in subdirs:
            path = os.path.join(root,subd)
            fps.append(path)
    return(fps)

####
def detect_file(fn):
    fd = open(fn,'rb+')
    byts = fd.read()
    fd.close()
    encd = chardet.detect(byts)['encoding']
    return(encd)


####

def repl_suffix(src,suffix):
    '''
        src = "./application.scv"
        suffix = ".json"
        repl_suffix(src,suffix)
        >>> os.getcwd()
        '/opt/JS/NV5_MIMEJS/CONSTS'
        >>> repl_suffix(src,suffix)
        '/opt/JS/NV5_MIMEJS/CONSTS/application.json'
        >>>
    '''
    src_abs_path = os.path.abspath(src)
    prefix,orig_suffix = os.path.splitext(src_abs_path)
    if(suffix[0]=="."):
        pass
    else:
        suffix = "." + suffix
    dst_abs_path = prefix+suffix
    return(dst_abs_path)

####

####zip

def zip_dir(src_dir,dst):
    f = zipfile.ZipFile(dst,'w',zipfile.ZIP_DEFLATED)
    fl = walkf(src_dir)
    for file in fl:
        f.write(file)
    f.close()


def unzip(src,dst_dir="./"):
    f = zipfile.ZipFile(src)  
    for file in f.namelist():
        f.extract(file,dst_dir)    
    f.close()


####csv


