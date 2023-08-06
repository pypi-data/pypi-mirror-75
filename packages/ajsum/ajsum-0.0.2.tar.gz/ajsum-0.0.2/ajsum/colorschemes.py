
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
    'misc1': ['#DC8665', '#138086', '#534666', '#CD7672', '#EEB462'],
    'misc2': ['#E8A49C', '#3C4CAD', '#240E8B', '#F04393', '#F9C449'],
    'misc3': ['#7BD5F5', '#787FF6', '#4ADEDE', '#1CA7EC', '#1F2F98'],
    'misc4': ['#0B0742', '#120C6E', '#5E72EB', '#FF9190', '#FDC094'],
    'misc5': ['#205072', '#329D9C', '#56C596', '#7BE495', '#CFF4D2'],
    'misc6': ['#FBEEE6', '#FFE5D8', '#FFCAD4', '#F3ABB6', '#9F8189'],
    'misc7': ['#031B88', '#6096FD', '#AAB6FB', '#FB7B8E', '#FAA7B8'],
    'misc8': ['#2C6975', '#68B2A0', '#CDE0C9', '#E0ECDE', '#FFFFFF'],
    'misc9': ['#6AAB9C', '#FA9284', '#E06C78', '#5874DC', '#384E78'],
    'misc10': ['#4A707A', '#7697A0', '#94B0B7', '#C2C8C5', '#DDDDDA'],
    'misc11': ['#35BBCA', '#0191B4', '#F8D90F', '#D3DD18', '#FE7A15'],
    'misc12': ['#041B2D', '#004E9A', '#428CD4', '#FF9CDA', '#EA4492'],
    'misc13': ['#47CACC', '#63BCC9', '#CDB3D4', '#E7B7C8', '#FFBE88'],
    'misc14': ['#FF7B89', '#8A5082', '#6F5F90', '#758EB7', '#A5CAD2'],
    'misc15': ['#33539E', '#7FACD6', '#BFB8DA', '#E8B7D4', '#A5678E'],
    'misc16': ['#DF825F', '#F8956F', '#DFB15B', '#4D446F', '#706695'],
    'misc17': ['#85CBCC', '#A8DEE0', '#F9E2AE', '#FBC78D', '#A7D676'],
    'misc18': ['#5AA7A7', '#96D7C6', '#BAC94A', '#E2D36B', '#6C8CBF'],
    'misc19': ['#FF7B89', '#8A5082', '#6F5F90', '#758EB7', '#A5CAD2'],
    'misc20': ['#015C92', '#2D82B5', '#FB6602', '#88CDF6', '#BCE6FF'],
    'misc21': ['#522157', '#8B4C70', '#C2649A', '#E4C7B7', '#E4DFD9'],
    'misc22': ['#264D59', '#43978D', '#F9E07F', '#F9AD6A', '#D46C4E'],
    'misc23': ['#C73866', '#FE676E', '#FD8F52', '#FF8D71', '#FFDCA2'],
    'misc24': ['#3B5284', '#5BA8A0', '#CBE54E', '#94B447', '#5D6E1E'],
    'misc25': ['#C6A477', '#ECD59F', '#D3E7EE', '#ABD1DC', '#7097A8'],
    'misc26': ['#7E9680', '#79616F', '#AE6378', '#D87F81', '#EAB595'],
    'misc27': ['#455054', '#308695', '#D45769', '#E69D45', '#D4CFC9'],
    'misc28': ['#478BA2', '#DE5B6D', '#E9765B', '#F2A490', '#B9D4DB'],
    'misc29': ['#FFFFFF', '#E7E7E7', '#D1D1D1', '#B6B6B6', '#9B9B9B'],
    'misc30': ['#AAC9CE', '#B6B4C2', '#C9BBC8', '#E5C1CD', '#F3DBCF'],
    'misc31': ['#F5CEC7', '#E79796', '#FFC98B', '#FFB284', '#C6C09C'],
    'misc32': ['#86E3CE', '#D0E6A5', '#FFDD94', '#FA897B', '#CCABD8'],
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

