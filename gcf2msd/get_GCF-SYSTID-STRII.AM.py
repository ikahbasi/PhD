from obspy import read
import os


lst = []

path = '/media/ekarkooti/ext4/Kahbasi-PhD/Kaki/raw-gcf-data'
for root, dirs, files in os.walk(path):
    for fname in files:
        if fname.endswith('.gcf'):
            try:
                st = read(f'{root}/{fname}')
                for tr in st:
                    gcf = tr.stats.gcf
                    el = (gcf['system_id'], gcf['stream_id'])
                    lst.append(el)
                break
            except:
                pass
