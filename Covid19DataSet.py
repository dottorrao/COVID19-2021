class Covid19DataSet:
    
    def __init__(self, data, ric_sintomi, ti, tot_osp, tot_pos, var_tot_pos, nuovi_pos, dimessi, deceduti, tot_casi, tamponi ):
        self.data = data
        self.ric_sintomi = ric_sintomi
        self.ti = ti
        self.tot_osp = tot_osp
        self.tot_pos = tot_pos
        self.var_tot_pos = var_tot_pos
        self.nuovi_pos = nuovi_pos
        self.dimessi = dimessi
        self.deceduti = deceduti
        self.tot_casi = tot_casi
        self.tamponi = tamponi