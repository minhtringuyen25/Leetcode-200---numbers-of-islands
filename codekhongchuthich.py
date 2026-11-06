#
quan_dao = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,1,1,1,1,1,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1],
    [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1],
    [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]# 5
def la_dat(o):
    return o == 1 or o == "1"
def tim_vgd(hang):
    cac_vgd = []
    so_cot = len(hang)
    co = 0
 
    while co < so_cot:
        if not la_dat(hang[co]):
            co += 1
            continue
        a = co
 
        while co < so_cot and la_dat(hang[co]):
            co += 1
        b = co - 1
 
        cac_vgd.append({"a": a, "b": b, "nhan": None})
 
    return cac_vgd
 
def dem_so_dao(quan_dao):
    so_dao = 0
    thdd_truoc = []
    nhan_moi = 0

    for hang in quan_dao:
        thdd_nay = []

        for vgd in tim_vgd(hang):

            nhan_trung = set()
            for v in thdd_truoc:
                if v["a"] <= vgd["b"] and v["b"] >= vgd["a"]:
                    nhan_trung.add(v["nhan"])
 
            k = len(nhan_trung)
 
            if k == 0:
                vgd["nhan"] = nhan_moi
                nhan_moi += 1
                so_dao += 1
            else:
                nhan_chung = min(nhan_trung)
 
                for v in thdd_truoc + thdd_nay:
                    if v["nhan"] in nhan_trung:
                        v["nhan"] = nhan_chung
 
                vgd["nhan"] = nhan_chung
                so_dao -= (k - 1)
            thdd_nay.append(vgd)
        
        thdd_truoc = thdd_nay
    
    return so_dao
print("Số đảo:", dem_so_dao(quan_dao))