import os
import subprocess
import sys

def get_dir(path):
    return os.path.dirname(path) if os.path.dirname(path) else '/'

def ui_print(message):
    print(message)

def abort(message):
    print(message)
    sys.exit(1)

def run_command(command, check=True):
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if check and result.returncode != 0:
        abort(f"! Command failed: {command}\n{result.stderr}")
    return result.stdout

def main():
    bootmode = os.getenv('BOOTMODE', 'false') == 'true'  # 示例初始化

    if len(sys.argv) != 2:
        abort("Usage: python boot_patch.py <bootimage>")
    
    bootimage = sys.argv[1]
    if not os.path.exists(bootimage):
        abort(f"{bootimage} does not exist!")

    if os.path.isfile(bootimage):  # 检查是否为文件
        run_command(f'nanddump -f boot.img {bootimage}')
        bootnand = bootimage
        bootimage = 'boot.img'

    keepverity = os.getenv('KEEPVERITY', 'false')
    keepforcencrypt = os.getenv('KEEPFORCEENCRYPT', 'false')
    patchvbmetaflag = os.getenv('PATCHVBMETAFLAG', 'false')
    recoverymode = os.getenv('RECOVERYMODE', 'false')
    legacysar = os.getenv('LEGACYSAR', 'false')

    ui_print("- Unpacking boot image")
    result = run_command(f'./magiskboot unpack "{bootimage}"', check=False)
    if result:
        if "ChromeOS boot image detected" in result:
            chromos = True
            ui_print("- ChromeOS boot image detected")
        else:
            abort("! Unsupported/Unknown image format")

    ui_print("- Checking ramdisk status")
    if os.path.exists('ramdisk.cpio'):
        run_command('./magiskboot cpio ramdisk.cpio test')
        status = 0
        skip_backup = ""
    else:
        status = 0
        skip_backup = "#"

    if status & 3 == 0:
        ui_print("- Stock boot image detected")
        sha1 = run_command(f'./magiskboot sha1 "{bootimage}"')
        run_command(f'cp {bootimage} stock_boot.img')
        run_command('cp -af ramdisk.cpio ramdisk.cpio.orig')
    elif status & 3 == 1:
        ui_print("- Magisk patched boot image detected")
        run_command('./magiskboot cpio ramdisk.cpio "extract .backup/.magisk config.orig" "restore"')
        run_command('cp -af ramdisk.cpio ramdisk.cpio.orig')
        run_command('rm -f stock_boot.img')
    elif status & 3 == 2:
        abort("! Boot image patched by unsupported programs")

    init = 'init.real' if status & 4 != 0 else 'init'
    preinitdevice = ''
    if os.path.exists('config.orig'):
        with open('config.orig', 'r') as file:
            config_lines = file.readlines()
        for line in config_lines:
            if line.startswith('SHA1'):
                sha1 = line.split('=')[1].strip()
            if not bootmode:
                if line.startswith('PREINITDEVICE'):
                    preinitdevice = line.split('=')[1].strip()
        os.remove('config.orig')

    ui_print("- Patching ramdisk")
    skip32 = "#"
    skip64 = "#"
    if os.path.exists('magisk64'):
        if bootmode and not preinitdevice:
            preinitdevice = run_command('./magisk64 --preinit-device').strip()
        run_command('./magiskboot compress=xz magisk64 magisk64.xz')
        skip64 = ""
    if os.path.exists('magisk32'):
        if bootmode and not preinitdevice:
            preinitdevice = run_command('./magisk32 --preinit-device').strip()
        run_command('./magiskboot compress=xz magisk32 magisk32.xz')
        skip32 = ""
    run_command('./magiskboot compress=xz stub.apk stub.xz')

    with open('config', 'w') as file:
        file.write(f"KEEPVERITY={keepverity}\n")
        file.write(f"KEEPFORCEENCRYPT={keepforcencrypt}\n")
        file.write(f"RECOVERYMODE={recoverymode}\n")
        if preinitdevice:
            ui_print(f"- Pre-init storage partition: {preinitdevice}")
            file.write(f"PREINITDEVICE={preinitdevice}\n")
        if sha1:
            file.write(f"SHA1={sha1}\n")

    run_command(f'./magiskboot cpio ramdisk.cpio '
                f'"add 0750 {init} magiskinit" '
                f'"mkdir 0750 overlay.d" '
                f'"mkdir 0750 overlay.d/sbin" '
                f'{skip32}add 0644 overlay.d/sbin/magisk32.xz magisk32.xz '
                f'{skip64}add 0644 overlay.d/sbin/magisk64.xz magisk64.xz '
                f'"add 0644 overlay.d/sbin/stub.xz stub.xz" '
                f'"patch" '
                f'{skip_backup}backup ramdisk.cpio.orig '
                f'"mkdir 000 .backup" '
                f'"add 000 .backup/.magisk config"')

    run_command('rm -f ramdisk.cpio.orig config magisk*.xz stub.xz')

    for dt in ['dtb', 'kernel_dtb', 'extra']:
        if os.path.exists(dt):
            run_command(f'./magiskboot dtb {dt} test')
            run_command(f'./magiskboot dtb {dt} patch')

    if os.path.exists('kernel'):
        patched_kernel = False
        run_command('''./magiskboot hexpatch kernel \
            49010054011440B93FA00F71E9000054010840B93FA00F7189000054001840B91FA00F7188010054 \
            A1020054011440B93FA00F7140020054010840B93FA00F71E0010054001840B91FA00F7181010054''')
        patched_kernel = True

        run_command('''./magiskboot hexpatch kernel 821B8012 E2FF8F12''')
        patched_kernel = True

        if legacysar:
            run_command('''./magiskboot hexpatch kernel \
                736B69705F696E697472616D667300 \
                77616E745F696E697472616D667300''')
            patched_kernel = True

        if not patched_kernel:
            os.remove('kernel')

    ui_print("- Repacking boot image")
    run_command(f'./magiskboot repack "{bootimage}"')

    if chromos:
        run_command('sign_chromeos')

    if os.path.exists(bootnand):
        bootimage = bootnand

if __name__ == "__main__":
    main()
