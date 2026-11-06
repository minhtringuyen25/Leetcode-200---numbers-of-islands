# Nhiệm vụ
#   quan_dao là ma trận gồm số 1 (đất) và số 0 (nước).
#   Một đảo là các ô đất nối nhau theo 4 hướng: trên, dưới, trái, phải
#   (hai ô chéo nhau không tính là nối). Đếm xem có bao nhiêu đảo.
#
# viết tắt
#   vgd  (vùng gặp đất)   : một đoạn đất liên tiếp trên MỘT hàng, viết là [a, b],
#                           nghĩa là các ô từ cột a đến cột b đều là đất.
#                           Ô đất đứng một mình là trường hợp a = b.
#   thdd (tổ hợp dải đất) : nhóm các vgd nối với nhau (có thể nằm trên nhiều
#                           hàng). Mỗi thdd là một đảo đang được xét.
#-nhan : tên của thdd. Các vgd có cùng nhan là cùng một thdd.
#-so_dao : số đảo đếm được tính đến thời điểm hiện tại.
#-"trùng": hai vgd ở hai hàng liên tiếp gọi là trùng nhau khi
#                           có ít nhất cột chung (tối thiểu 1 chỗ trùng là đủ).
#
# thuật toán
#  Bắt đầu: so_dao = 0 và thdd của "hàng trước" là rỗng
#       (coi như có một hàng 0 toàn nước, nên hàng đầu tiên không cần xử lý riêng).
#
#   bước1/ Với mỗi hàng, đi từ trên xuống dưới: tìm tất cả vgd của hàng đó.
#       Hàng không có đất thì không có vgd nào.
#
#   bước2: Với MỖI vgd của hàng đang xét, xem nó trùng với những thdd KHÁC NHAU
#       nào ở hàng trước. Gọi k là số thdd khác nhau đó:
#      k = 0  : không trùng thdd nào -> vgd tạo thành thdd mới, so_dao += 1
#      k = 1: vgd gia nhập thdd đó      -> so_dao không đổi
#      k >= 2 : vgd nối k thdd lại, gom chúng thành 1 thdd
#                    -> so_dao -= (k - 1)
#  Chú ý này: nếu vgd trùng 2 đoạn của hàng trước nhưng 2 đoạn đó đã thuộc
# cùng 1 thdd thì vẫn tính k = 1, không trừ gì hết.
#
#   bước3: Xét xong cả hàng thì cập nhật: thdd của "hàng trước" := các vgd của
#       hàng vừa xét (kèm nhan của chúng). Các vgd của hàng cũ hết nhiệm vụ nên bỏ.
#       thdd nào không còn vgd nào ở hàng mới là đảo đã hoàn thành,
#       nó vẫn được giữ trong so_dao.
#
#   bước4. Hết ma trận quần đảo thì so_dao chính là số đảo
quan_dao = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
] # 7 đảo
#so_dao là số đảo
# Hàm phụ 1: kiểm tra một ô có phải là đất hay không
def la_dat(o):
    # Ô là đất khi bằng số 1 hoặc ký tự "1"
    return o == 1 or o == "1"

#Hàm phụ 2 (bước 1): tìm tất cả vgd của MỘT hàng
# Kết quả: danh sách các vgd, mỗi vgd là một tập hợp giá trị kích gốc có 3 phần:
#a: cột bắt đầu của đoạn đất
#b: cột kết thúc của đoạn đất
# "nhan": nhãn tên thdd mà vgd thuộc về (lúc mới tìm ra thì chưa có, để None-trống)
def tim_vgd(hang):
    cac_vgd = []          # danh sách vgd(vùng gặp đất) của hàng này, ban đầu rỗng
    so_cot = len(hang)    # số cột của hàng này
    co = 0                # co là cột đang xét, đi từ trái sang phải
 
    while co < so_cot:
        # Gặp nước thì bỏ qua, sang cột kế tiếp
        if not la_dat(hang[co]):
            co  += 1
            continue
 
        # Gặp đất:cột này là điểm bắt đầu của một vgd
        a = co
 
        # Đi tiếp sang phải đến khi nào còn là đất
        while co < so_cot and la_dat(hang[co]):
            co += 1
        b = co - 1
 
        cac_vgd.append({"a": a, "b": b, "nhan": None})
 
    return cac_vgd
 
#Hàm đếm số đảo
def dem_so_dao(quan_dao):
    # bước khởi tạo
    so_dao = 0            # chưa có đảo nào
    thdd_truoc = []       # các vgd (kèm nhan) của hàng trước, ban đầu rỗng
    nhan_moi = 0          # bộ đếm để đặt nhãn tên cho thdd mới (0, 1, 2, ..., 36)
 
    # Xét từng hàng của ma trận quần đảo, từ trên xuống dưới
    for hang in quan_dao:
 
        thdd_nay = []     # các vgd (kèm nhan) của hàng đang xét, ban đầu rỗng
 
        # Bước 1: tìm các vgd của hàng đang xét
        for vgd in tim_vgd(hang):
 
            # B2.a: tìm các thdd KHÁC NHAU ở hàng trước mà vgd này trùng
            # (dùng set để mỗi tên thdd chỉ được tính một lần)
            nhan_trung = set()#nhãn trùng
            for v in thdd_truoc:
                # Hai đoạn có chung ít nhất 1 cột khi:
                #   đoạn trước bắt đầu không quá cột cuối của vgd này
                #   và đoạn trước kết thúc không trước cột đầu của vgd này
                if v["a"] <= vgd["b"] and v["b"] >= vgd["a"]:
                    nhan_trung.add(v["nhan"])
 
            k = len(nhan_trung)   # số thdd khác nhau mà vgd này trùng
            # k là số thdd khác nhau ở hàng trước mà vgd đang xét trùng cột
            # k == 0 không trung thdd-tổ hợp dải đất nào ,tức sẽ tạo tổ hợp mới
            # k == 1 , thdd mới thay cho tổ hợp trước bị trùng
            # k == n ,tức n thdd hợp lại thành 1 thdd mới ví dụ: 36,18,9
            # B2.b: xử lý theo k
            if k == 0:
                # Không trùng thdd nào: tạo thdd mới, đó là một đảo mới
                vgd["nhan"] = nhan_moi
                nhan_moi += 1
                so_dao += 1
            else:
                # k = 1 hoặc nhiều hơn: vgd thuộc về một thdd chung.
                # Chọn tên nhỏ nhất trong các thdd bị trùng làm tên chung.
                nhan_chung = min(nhan_trung)
 
                # Gom mọi vgd (của hàng trước và của hàng đang xét) đang mang
                # tên một trong các thdd bị trùng thì đổi sang tên chung.
                # Nhờ vậy các hàng sau nhìn thấy chúng là cùng một thdd.
                for v in thdd_truoc + thdd_nay:
                    if v["nhan"] in nhan_trung:
                        v["nhan"] = nhan_chung
#v là 1 vùng gặp đất-vgd được lấy từ thdd-tổ hợp dải đất
                vgd["nhan"] = nhan_chung
 
                # Gom k thdd thành 1 thì mất đi (k - 1) đảo.
                # Với k = 1 thì k - 1 = 0, so_dao không đổi.
                so_dao -= (k - 1)
 
            # Xếp vgd này vào danh sách của hàng đang xét
            thdd_nay.append(vgd)
 
        # B3: xét xong cả hàng, cập nhật "hàng trước" cho vòng lặp kế tiếp
        thdd_truoc = thdd_nay
 
    # B4: hết ma trận, so_dao là số đảo
    return so_dao
print("Số đảo:", dem_so_dao(quan_dao))