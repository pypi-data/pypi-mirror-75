'''
# CLI Frontend for NCMFunctions

Which sets an example to use this module.have fun ;)
'''
splash = '''\033[31m       
             p0000,      
       _p00 ]0#^~M!      
      p00M~  00          ______         _______ ______ _______  
     j0@^  pg0000g_     |   __ \___ ___|    |  |      |   |   |
    ]00   #00M0#M00g    |    __/|  |  ||       |   ----       |
    00'  j0F  00 ^Q0g   |___|   |___  ||__|____|______|__|_|__|
    00   00   #0f  00           |_____|                        
    00   #0&__#0f  #0c  ———————————————————————————————————————
    #0t   M0000F   00                 by greats3an @ mos9527.tooo.top 
     00,          j0#   SYANTAX HELP:
     ~00g        p00        --help,-h show manual
      `000pg,ppg00@         --help,-h 显示帮助文本
        ~M000000M^

    e.g. pyncm  --clear-temp song 1334780738\033[0m
'''
import argparse
import sys
import shutil
import colorama,coloredlogs,logging
import os
import json

from . import ncm

# All imports are good?Print the splash text
colorama.init()
print(splash)
logging.getLogger("urllib3").setLevel(logging.WARNING)
# Set logging level for `urllib3`
parser = argparse.ArgumentParser(
    description='NCM All-in-One Downloader for python', formatter_class=argparse.RawTextHelpFormatter)
# Parser begin----------------------------------------------------------------------------
parser.add_argument('operation', metavar='OPERATION',
                    help='''What to do:
[song_audio]   download audio file only to temporay folder
[song_lyric]   download lyrics and coverts them into lrc to temporay folder
[song_meta]    download metadata only to temporay folder
[song_down]    download all above,but not perfoming migration
[song]         download all above,and perform migration
[playlist]     parse playlist,then download every song
[album]        download every song in album with such id''')
parser.add_argument('id', metavar='ID', help='''ID of the song / playlist / album''')
parser.add_argument('--quality', type=str, default='lossless',
                    help='''Audio quality
    Specifiy download quality,e.g.[lossless] will download the song in Lossless quality
    (if exsists and user's account level statisfies requirement)
    [standard, higher, lossless] are possible''')
parser.add_argument('--temp', type=str, default='temp',
                    help='''Folder to store downloads''')
parser.add_argument('--output', type=str, default='output',
                    help='''Folder to store all your output''')
parser.add_argument('--phone', type=str,
                    help='''Phone number of your account''', default='')
parser.add_argument('--password', type=str,
                    help='''Password of your account''', default='')
parser.add_argument('--merge-only', action='store_true',
                    help='''Only merge the downloaded stuff''')
parser.add_argument('--clear-temp', action='store_true',
                    help='''Clears the temp folder afterwards''')
parser.add_argument('--pool-size', type=int, default=4,
                    help='''Download pool size''')
parser.add_argument('--buffer-size', type=int, default=256,
                    help='''Download buffer size (KB)''')
parser.add_argument('--random-keys', action='store_true',
                    help='''Use random AES key for encryption''')
parser.add_argument('--logging-level', type=int, default=logging.DEBUG,
                    help='''Logging Level,see the following list for help
50 FATAL
40 ERROR
30 WARN
20 INFO
10 DEBUG (default)
''')                    
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(2)
args = parser.parse_args()
args = args.__dict__

operation, id, quality,  temp, output, phone, password, merge_only, clear_temp,  pool_size, buffer_size, random_keys,logging_level = args.values()
# Parser end----------------------------------------------------------------------------
print('''Initalized with the following settings:
    ID                  :       {}
    Operation           :       {}
    Option              :       {}
    Password Hash       :       {}
    Phone               :       {}
    Do clear temp       :       {}
    Do merge only       :       {}
    Temporay folder     :       {}
    Output folder       :       {}
    Poolsize            :       {} Workers
    Buffer Size         :       {} KB
    Use random encSecKey:       {}
    Logging Level       :       {}'''.format(
id,operation, quality, ncm.ncm_core.NeteaseCloudMusicKeygen.generate_hash('', password) if password else '',
phone, clear_temp, merge_only, temp, output,pool_size, buffer_size, 
random_keys,logging_level))
coloredlogs.install(level=logging_level)
ncmfunc = ncm.ncm_func.NCMFunctions(temp, output, merge_only, pool_size,buffer_size, random_keys)
if os.path.exists('.cookies'):
    # If cookies are stored,load them in
    try:
        cookies = open('.cookies',encoding='utf-8').read()
        cookies = json.loads(cookies)
        ncm.session.cookies.update(cookies)
        logging.info('Loaded stored cookies,continue...')
    except Exception as e:
        logging.error('Failed to load stored cookies:%s' % e)

if phone and password:
    # Provided,logging in with them
    ncmfunc.Login(phone, password)
    # ...and save the cookies afterwards
    open('.cookies','w+',encoding='utf-8').write(json.dumps(ncm.session.cookies.get_dict()))
    logging.info('Saved cookies to `.cookies`')
'''
    Reflect the operations to certain functions
'''
def NoExecWrapper(func, *args, **kwargs):
    '''
        Wrapper that treats functions like a variable then returns them
    '''
    def wrapper():
        func(*args, **kwargs)
    return wrapper

reflection = {
    'song_audio': NoExecWrapper(ncmfunc.DownloadSongAudio, id=id, quality=quality),
    'song_lyric':   NoExecWrapper(ncmfunc.DownloadAndFormatLyrics, id=id),
    'song_meta': NoExecWrapper(ncmfunc.DownloadSongInfo, id=id),
    'song_down': NoExecWrapper(ncmfunc.DownloadAll, id=id, quality=quality),
    'song':  NoExecWrapper(ncmfunc.DownloadAllAndMerge, id=id, quality=quality),
    'playlist': NoExecWrapper(ncmfunc.DownloadAllSongsInPlaylistAndMerge, id=id, quality=quality, merge_only=merge_only),
    'album': NoExecWrapper(ncmfunc.DownloadAllSongsInAlbumAndMerge, id=id, quality=quality, merge_only=merge_only)
}

if not operation in reflection.keys():
    logging.error('Invalid operation:%s' % operation)
else:
    func = reflection[operation]()

if clear_temp:
    # Clears temporay folder
    logging.info('Clearing temp folder:%s' % temp)
    shutil.rmtree(temp)
