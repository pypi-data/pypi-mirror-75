
from matplotlib import cycler
import matplotlib.pyplot as plt

schemes = {
    'sunset': ['#F8B195', '#F67280', '#C06C84', '#6C5B7B', '#355C7D'],
    'pastel': ['#99B898', '#FECEA8', '#FF847C', '#E84A5F', '#2A363B'],
    'lightpastel': ['#A8E6CE', '#DCEDC2', '#FFD3B5', '#FFAAA6', '#FF8C94'],
    'blackcherry': ['#A8A7A7', '#CC527A', '#E8175D', '#474747', '#363636'],
    'sherbet': ['#A7226E', '#EC2049', '#F26B38', '#F7DB4F', '#2F9599'],
    'sunrise': ['#E1F5C4', '#EDE574', '#F9D423', '#FC913A', '#FF4E50'],
    'coolbreeze': ['#E5FCC2', '#9DE0AD', '#45ADA8', '#547980', '#594F4F'],
    'kiwistrawberry': ['#FE4365', '#FC9D9A', '#F9CDAD', '#C8C8A9', '#83AF9B'],
}


def formatter(scheme, facecolor='#E6E6E6', linewidth=2):

    cycle = cycler('color', schemes[scheme])
    plt.rc('axes', facecolor=facecolor, edgecolor='none', axisbelow=True,
           grid=True, prop_cycle=cycle)
    plt.rc('grid', color='w', linestyle='solid')
    plt.rc('xtick', direction='out', color='gray')
    plt.rc('ytick', direction='out', color='gray')
    plt.rc('patch', edgecolor='#E6E6E6')
    plt.rc('lines', linewidth=linewidth)

