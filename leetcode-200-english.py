#  COUNT ISLANDS (LeetCode 200 - Number of Islands)
#  Row-by-row scanning algorithm (Python version)
#
# PROBLEM
#   quan_dao (the "archipelago") is a grid of 1s (land) and 0s (water).
#   An island is a group of land cells connected in 4 directions:
#   up, down, left and right (diagonal neighbours are NOT connected).
#   Count how many islands there are.
#
# NAMES USED IN THE CODE
#   The identifiers are abbreviations of Vietnamese words. This is what they mean:
#
#   vgd  (vung gap dat = "land-meeting zone")
#        A land segment: a run of consecutive land cells in ONE row, written [a, b],
#        meaning every cell from column a to column b is land.
#        A single land cell is the special case a = b.
#   thdd (to hop dai dat = "land-strip combination")
#        An island group: a set of segments that are connected to each other
#        (they may span several rows). Each group is one island being built.
#   nhan
#        The label (name) of a group. Segments with the same nhan belong to
#        the same group.
#   so_dao
#        The number of islands counted so far.
#   "overlap"
#        Two segments in two consecutive rows overlap when they share AT LEAST
#        ONE column (a single shared column is enough).
#
#   quan_dao       the grid          hang        a row
#   la_dat         "is land?"        co          the current column index (cot = column)
#   tim_vgd        "find segments"   dem_so_dao  "count islands"
#   thdd_truoc     segments (with labels) of the previous row
#   thdd_nay       segments (with labels) of the current row
#   nhan_moi       counter used to give a new group a new label
#   nhan_trung     set of the different labels that a segment overlaps
#   nhan_chung     the common label chosen when groups are merged
#   k              how many different groups a segment overlaps
#
# ALGORITHM
#   Step 0. Start with so_dao = 0 and an empty list of segments for the
#           "previous row" (as if there were a row 0 made only of water,
#           so the first row needs no special treatment).
#
#   Step 1. For each row, from top to bottom, find all land segments of that row.
#           A row with no land has no segments.
#
#   Step 2. For EACH segment of the current row, find which DIFFERENT groups of
#           the previous row it overlaps. Let k be the number of those groups:
#             - k = 0  : it overlaps no group -> it starts a new group, so_dao += 1
#             - k = 1  : it joins that group   -> so_dao does not change
#             - k >= 2 : it connects k groups, so they are merged into one group
#                                              -> so_dao -= (k - 1)
#           Note: if a segment overlaps two segments of the previous row, but
#           those two already belong to the same group, then k is still 1 and
#           nothing is subtracted.
#
#   Step 3. When the whole row is done, update: the "previous row" becomes the
#           segments of the row we just processed (with their labels). The old
#           segments have done their job and are dropped.
#           A group that has no segment in the new row is a finished island;
#           it stays counted in so_dao.
#
#   Step 4. At the end of the grid, so_dao is the number of islands.
#
# EXAMPLE (U shape)
#       1 0 1
#       1 1 1
#   Row 1: two segments, [0,0] and [2,2], both with k = 0, so so_dao = 2.
#   Row 2: one segment, [0,2], overlapping 2 different groups (k = 2)
#          -> merged, so_dao = 2 - (2 - 1) = 1. Correct: a U shape is 1 island.

quan_dao = [
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 0],
    [1, 0, 1, 0, 1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [1, 0, 1, 1, 0, 0, 0, 0, 0, 0]
]  # 7 islands


# Helper 1: check whether a cell is land
def la_dat(o):
    # A cell is land if it is the number 1 or the character "1"
    # (the original LeetCode problem uses the characters "1" and "0")
    return o == 1 or o == "1"


# Helper 2 (Step 1): find all land segments (vgd) of ONE row
# Result: a list of segments. Each segment is a dictionary with 3 parts:
#   "a"    : the column where the segment starts
#   "b"    : the column where the segment ends
#   "nhan" : the label of the group the segment belongs to
#            (None = no label yet, because the segment has just been found)
def tim_vgd(hang):
    cac_vgd = []          # the segments of this row, empty at first
    so_cot = len(hang)    # the number of columns in this row
    co = 0                # co is the current column, moving from left to right

    while co < so_cot:
        # Water: skip it and move to the next column
        if not la_dat(hang[co]):
            co += 1
            continue

        # Land: this column is the start of a segment
        a = co

        # Keep moving right as long as the cells are still land
        while co < so_cot and la_dat(hang[co]):
            co += 1

        # The loop above stops at water or at the end of the row,
        # so the last land cell of the segment is column co - 1
        b = co - 1

        cac_vgd.append({"a": a, "b": b, "nhan": None})

    return cac_vgd


# Main function: count the islands
def dem_so_dao(quan_dao):
    # Step 0: initialisation
    so_dao = 0            # no island counted yet
    thdd_truoc = []       # segments (with labels) of the previous row, empty at first
    nhan_moi = 0          # counter for naming new groups (0, 1, 2, ...)

    # Process the grid row by row, from top to bottom
    for hang in quan_dao:

        thdd_nay = []     # segments (with labels) of the current row, empty at first

        # Step 1: find the segments of the current row
        for vgd in tim_vgd(hang):

            # Step 2.1: find the DIFFERENT groups of the previous row that
            # this segment overlaps (a set keeps each label only once)
            nhan_trung = set()
            for v in thdd_truoc:
                # Two segments share at least 1 column when:
                #   the previous segment starts no later than the last column of this one
                #   and the previous segment ends no earlier than the first column of this one
                if v["a"] <= vgd["b"] and v["b"] >= vgd["a"]:
                    nhan_trung.add(v["nhan"])

            k = len(nhan_trung)   # how many different groups this segment overlaps

            # Step 2.2: decide what to do according to k
            if k == 0:
                # It overlaps no group: create a new group, which is a new island
                vgd["nhan"] = nhan_moi
                nhan_moi += 1
                so_dao += 1
            else:
                # k = 1 or more: the segment belongs to one common group.
                # Use the smallest label among the overlapped groups as the common label.
                nhan_chung = min(nhan_trung)

                # Merge: every segment (from the previous row and from the current row)
                # that carries one of the overlapped labels is renamed to the common label.
                # This way the next rows see them as one single group.
                # (v is one segment taken from the list.)
                for v in thdd_truoc + thdd_nay:
                    if v["nhan"] in nhan_trung:
                        v["nhan"] = nhan_chung

                vgd["nhan"] = nhan_chung

                # Merging k groups into 1 loses (k - 1) islands.
                # With k = 1 this is 0, so so_dao does not change.
                so_dao -= (k - 1)

            # Add this segment to the list of the current row
            thdd_nay.append(vgd)

        # Step 3: the row is finished; it becomes the "previous row" for the next loop
        thdd_truoc = thdd_nay

    # Step 4: end of the grid, so_dao is the number of islands
    return so_dao


print("Number of islands is:", dem_so_dao(quan_dao))