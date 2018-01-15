import config_def as DEF

''' Config File '''

application_window = (15, 10)

output_datetime_format = '%Y-%m-%d %H:%M:%S'
stream_datetime_format = '%d %b %Y %H:%M:%S'

stream_point_attributes = ['sta_name', 'MJD_sys', 'MJD_ini', 'MJD_obs', 'lat', 'lon', 'hgt', 'dN', 'dE', 'dh',
                           'sN', 'sE', 'sh',
                           'cNE', 'cNh', 'cEh', 'sig0', 'pdop', 'cor_age', 'dt_ms', 'pmin', 'pmax',
                           'ar_dt_ms', 'nmsg_obs', 'nmsg_eph', 'nmsg_cor', 'nmsg_ion', 'nsat_trk',
                           'nsat_eph', 'nsat_cor', 'nsat_ion', 'nsat_use', 'nrej_trk', 'nrej_eph',
                           'nrej_cor', 'nrej_ion', 'nrej_elv', 'namb_jmp', 'nrng_rej', 'nphs_rej',
                           'status', 'ffix_amb', 'pfix_amb', 'prov_id', 'soln_id', 'msgc_id']

plot_01 = DEF.PanningGraph_Config(221, ['dN', 'dE', 'dh'], ['blue', 'green', 'brown'], (-0.07, 0.05), None, None, None, 'MJD_sys', 15, (1, 's'), '%Y-%m-%d %H:%M:%S')
plot_02 = DEF.PanningGraph_Config(222, ['sN', 'sE', 'sh'], ['red', 'orange', 'black'], (0.00, 0.02), None, None, None, 'MJD_sys', 15, (1, 's'), '%Y-%m-%d %H:%M:%S')
plot_03 = None
plot_04 = None