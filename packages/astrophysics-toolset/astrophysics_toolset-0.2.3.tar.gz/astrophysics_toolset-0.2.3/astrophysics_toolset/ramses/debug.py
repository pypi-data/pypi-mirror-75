import numpy as np
import yt

dsold = yt.load(
    "/home/ccc/Documents/Postdoc/genetIC-angular-momentum-constrain/simulations/data/DM_256_planck/resim/00140/halo_189/relative_change_lx_0.8/output_00001/info_00001.txt"
)
dsnew = yt.load("output_00080/info_00001.txt")

orderold = np.argsort(dsold.r["io", "particle_identity"])
ordernew = np.argsort(dsnew.r["io", "particle_identity"])

for field in dsnew.field_list:
    print("Testing %s,%s" % field)
    new = dsnew.r[field][ordernew]
    old = dsold.r[field][orderold]

    np.testing.assert_allclose(new, old)
