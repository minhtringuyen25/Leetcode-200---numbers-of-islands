
//  ĐẾM SỐ ĐẢO (LeetCode 200) - THEO THUẬT TOÁN CỦA TÔI  (bản Java)
//
// ĐỀ BÀI
//   quan_dao là ma trận gồm số 1 (đất) và số 0 (nước).
//   Một đảo là các ô đất nối nhau theo 4 hướng: trên, dưới, trái, phải
//   (hai ô chéo nhau KHÔNG tính là nối). Đếm xem có bao nhiêu đảo.
//
// Thuật ngữ viết tắt
//   vgd  (vùng gặp đất)   : một đoạn đất liên tiếp trên MỘT hàng, viết là [a, b],
//                           nghĩa là các ô từ cột a đến cột b đều là đất.
//                           Ô đất đứng một mình là trường hợp a = b.
//   thdd (tổ hợp dải đất) : nhóm các vgd nối với nhau (có thể nằm trên nhiều
//                           hàng). Mỗi thdd là một đảo đang được xét.
//   nhan                  : tên của thdd. Các vgd có cùng nhan là cùng một thdd.
//   so_dao                : số đảo đếm được tính đến thời điểm hiện tại.
//   "trùng"               : hai vgd ở hai hàng liên tiếp gọi là trùng nhau khi
//                           có ÍT NHẤT MỘT cột chung (tối thiểu 1 chỗ trùng là đủ).
//
// THUẬT TOÁN
//   Chuẩn bị: so_dao = 0 và thdd của "hàng trước" là rỗng
//       (coi như có một hàng 0 toàn nước, nên hàng đầu tiên không cần xử lý riêng ).
//
//   Bước 1: Với mỗi hàng, đi từ trên xuống dưới: tìm tất cả vgd của hàng đó.
//       Hàng không có đất thì không có vgd nào.
//
//   Bước 2: Với MỖI vgd của hàng đang xét, xem nó trùng với những thdd KHÁC NHAU
//       nào ở hàng trước. Gọi k là số thdd khác nhau đó:
//         - k = 0  : không trùng thdd nào -> vgd tạo thành thdd mới, so_dao += 1
//         - k = 1  : vgd gia nhập thdd đó                -> so_dao không đổi
//         - k >= 2 : vgd nối k thdd lại, gom chúng thành 1 thdd
//                                                        -> so_dao -= (k - 1)
//       Chú ý: nếu vgd trùng 2 đoạn của hàng trước nhưng 2 đoạn đó đã thuộc
//       cùng 1 thdd thì vẫn tính k = 1, không trừ gì cả.
//
//   Bước 3: Xét xong cả hàng thì cập nhật: thdd của "hàng trước" := các vgd của
//       hàng vừa xét (kèm nhan của chúng). Các vgd của hàng cũ hết nhiệm vụ nên bỏ.
//       thdd nào không còn vgd nào ở hàng mới là đảo đã hoàn thành,
//       nó vẫn được giữ trong so_dao.
//
//   Bước 4: Hết ma trận thì so_dao chính là số đảo.
//


import java.util.ArrayList;   // ArrayList: danh sách có thể dài ra, ngắn lại
import java.util.List;        // List: kiểu danh sách chung, dùng để khai báo biến
import java.util.TreeSet;     // TreeSet: tập hợp, mỗi giá trị chỉ xuất hiện một lần và luôn xếp từ nhỏ đến lớn

// Trong Java, mọi thứ nằm trong một class, và tên class phải trùng với tên file (LeetCode200.java)
public class LeetCode200viejava {

    // Kiểu dữ liệu cho một vgd (bản Python dùng dictionary, C++ dùng struct, Java dùng class)
    //   a    : cột bắt đầu của đoạn đất
    //   b    : cột kết thúc của đoạn đất
    //   nhan : tên thdd mà vgd thuộc về (lúc mới tìm ra thì chưa có, để -1)
    static class Vgd {
        int a;
        int b;
        int nhan;

        // Hàm tạo: dùng để tạo một vgd mới với 3 giá trị cho trước
        Vgd(int a, int b, int nhan) {
            this.a = a;
            this.b = b;
            this.nhan = nhan;
        }
    }


    // Hàm phụ 1: kiểm tra một ô có phải là đất hay không
    // Trả về true (đúng) nếu là đất, false (sai) nếu là nước
    // (static nghĩa là gọi hàm trực tiếp, không cần tạo đối tượng LeetCode200)
    static boolean la_dat(int o) {
        // Ô là đất khi bằng số 1
        return o == 1;
    }


    // Hàm phụ 2 (bước B1): tìm tất cả vgd của MỘT hàng
    // Kết quả: danh sách các vgd của hàng đó
    // (int[] hang là một hàng của ma trận, int[][] là cả ma trận)
    static List<Vgd> tim_vgd(int[] hang) {
        List<Vgd> cac_vgd = new ArrayList<>();  // danh sách vgd của hàng này, ban đầu rỗng
        int so_cot = hang.length;               // số cột của hàng này
        int x = 0;                              // x là cột đang xét, đi từ trái sang phải

        while (x < so_cot) {
            // Gặp nước thì bỏ qua, sang cột kế tiếp
            if (!la_dat(hang[x])) {
                x++;
                continue;
            }

            // Gặp đất: cột này là điểm bắt đầu của một vgd
            int a = x;

            // Đi tiếp sang phải chừng nào còn là đất
            while (x < so_cot && la_dat(hang[x])) {
                x++;
            }

            // Vòng lặp trên dừng khi gặp nước hoặc hết hàng,
            // nên ô đất cuối cùng của đoạn là cột x - 1
            int b = x - 1;

            // Tạo vgd mới (chưa có tên nên nhan = -1) và xếp vào danh sách
            cac_vgd.add(new Vgd(a, b, -1));
        }

        return cac_vgd;
    }


    // Hàm chính: đếm số đảo
    static int dem_so_dao(int[][] quan_dao) {
        // B0: khởi tạo
        int so_dao = 0;                            // chưa có đảo nào
        List<Vgd> thdd_truoc = new ArrayList<>();  // các vgd (kèm nhan) của hàng trước, ban đầu rỗng
        int nhan_moi = 0;                          // bộ đếm để đặt tên cho thdd mới (0, 1, 2, ...)

        // Xét từng hàng của ma trận, từ trên xuống dưới
        for (int[] hang : quan_dao) {

            List<Vgd> thdd_nay = new ArrayList<>();  // các vgd (kèm nhan) của hàng đang xét, ban đầu rỗng

            // B1: tìm các vgd của hàng đang xét
            List<Vgd> cac_vgd = tim_vgd(hang);

            for (Vgd vgd : cac_vgd) {

                // B2.1: tìm các thdd KHÁC NHAU ở hàng trước mà vgd này trùng
                // (dùng TreeSet để mỗi tên thdd chỉ được tính một lần)
                TreeSet<Integer> nhan_trung = new TreeSet<>();
                for (Vgd v : thdd_truoc) {
                    // Hai đoạn có chung ít nhất 1 cột khi:
                    //   đoạn trước bắt đầu không quá cột cuối của vgd này
                    //   và đoạn trước kết thúc không trước cột đầu của vgd này
                    if (v.a <= vgd.b && v.b >= vgd.a) {
                        nhan_trung.add(v.nhan);
                    }
                }

                int k = nhan_trung.size();  // số thdd khác nhau mà vgd này trùng

                // B2.2: xử lý theo k
                if (k == 0) {
                    // Không trùng thdd nào: tạo thdd mới, đó là một đảo mới
                    vgd.nhan = nhan_moi;
                    nhan_moi++;
                    so_dao++;
                } else {
                    // k = 1 hoặc nhiều hơn: vgd thuộc về một thdd chung.
                    // TreeSet luôn xếp các giá trị từ nhỏ đến lớn,
                    // nên first() là tên nhỏ nhất. Lấy nó làm tên chung.
                    int nhan_chung = nhan_trung.first();

                    // Gom: mọi vgd (của hàng trước và của hàng đang xét) đang mang
                    // tên một trong các thdd bị trùng thì đổi sang tên chung.
                    // Nhờ vậy các hàng sau nhìn thấy chúng là cùng một thdd.
                    for (Vgd v : thdd_truoc) {
                        if (nhan_trung.contains(v.nhan)) {
                            v.nhan = nhan_chung;
                        }
                    }
                    for (Vgd v : thdd_nay) {
                        if (nhan_trung.contains(v.nhan)) {
                            v.nhan = nhan_chung;
                        }
                    }

                    vgd.nhan = nhan_chung;

                    // Gom k thdd thành 1 thì mất đi (k - 1) đảo.
                    // Với k = 1 thì k - 1 = 0, so_dao không đổi.
                    so_dao -= (k - 1);
                }

                // Xếp vgd này vào danh sách của hàng đang xét
                thdd_nay.add(vgd);
            }

            // B3: xét xong cả hàng, cập nhật "hàng trước" cho vòng lặp kế tiếp
            thdd_truoc = thdd_nay;
        }

        // B4: hết ma trận, so_dao là số đảo
        return so_dao;
    }


    // Hàm main: nơi chương trình Java bắt đầu chạy. Chạy thử với ma trận mẫu (kết quả đúng là 7 đảo)
    public static void main(String[] args) {
        int[][] quan_dao = {
            {1, 1, 1, 1, 1, 0, 0, 0, 0, 0},
            {1, 0, 0, 0, 1, 0, 1, 1, 1, 0},
            {1, 0, 1, 0, 1, 0, 0, 1, 1, 0},
            {1, 0, 0, 0, 1, 0, 0, 0, 0, 0},
            {1, 1, 1, 1, 1, 0, 0, 0, 1, 0},
            {0, 0, 0, 0, 0, 1, 0, 0, 1, 0},
            {1, 0, 1, 1, 0, 0, 0, 1, 1, 0},
            {1, 0, 1, 1, 0, 0, 0, 0, 0, 0}
        };  // 7 đảo

        System.out.println("Số đảo: " + dem_so_dao(quan_dao));
    }
}